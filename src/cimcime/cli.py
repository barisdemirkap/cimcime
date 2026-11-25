from __future__ import annotations

import argparse
import json
import sys
from datetime import timedelta
from pathlib import Path

from cimcime.approval_gate import ActionType
from cimcime.config import get_repo
from cimcime.delegation import (
    Backend,
    DelegationLog,
    default_log_path,
    delegate_summarize,
    log_external_delegation,
)
from cimcime.decision_log import DecisionLog
from cimcime.message_log import Direction, MessageLog, default_path
from cimcime.roadmap import DEFAULT_RESEARCH_DOC_PATH, expected_topics, topic_entries
from cimcime.state_store import (
    GitHubIssuesStore,
    Phase,
    StateStore,
    TopicRecord,
    TopicStatus,
    category_breakdown,
    summarize_category,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cimcime")
    subparsers = parser.add_subparsers(dest="command", required=True)

    get_topic = subparsers.add_parser("get-topic")
    get_topic.add_argument("topic_id")

    update_status = subparsers.add_parser("update-status")
    update_status.add_argument("topic_id")
    update_status.add_argument("status", choices=[status.value for status in TopicStatus])

    add_finding = subparsers.add_parser("add-finding")
    add_finding.add_argument("topic_id")
    add_finding.add_argument("finding")

    flag_needs_better_sources = subparsers.add_parser("flag-needs-better-sources")
    flag_needs_better_sources.add_argument("topic_id")

    category_status = subparsers.add_parser("category-status")
    category_status.add_argument("category")

    category_rollup = subparsers.add_parser("category-rollup")
    category_rollup.add_argument("category")

    subparsers.add_parser("phase-check")

    subparsers.add_parser("get-phase")

    set_phase = subparsers.add_parser("set-phase")
    set_phase.add_argument("phase", choices=[phase.value for phase in Phase])

    seed_parser = subparsers.add_parser("seed")
    seed_parser.add_argument("--doc", default=None, help="research doc to seed from (default: the original roadmap doc)")
    seed_parser.add_argument("--dry-run", action="store_true", help="report what would be created without creating it")

    log_message = subparsers.add_parser("log-message")
    log_message.add_argument("chat_id")
    log_message.add_argument("direction", choices=[d.value for d in Direction])
    log_message.add_argument("text")
    log_message.add_argument("--message-id")
    log_message.add_argument("--sent-at")

    recent_messages = subparsers.add_parser("recent-messages")
    recent_messages.add_argument("chat_id")
    recent_messages.add_argument("--limit", type=int, default=20)

    log_decision = subparsers.add_parser("log-decision")
    log_decision.add_argument("project")
    log_decision.add_argument("decision")
    log_decision.add_argument("--rationale", default="")
    log_decision.add_argument("--decided-at")

    recent_decisions = subparsers.add_parser("recent-decisions")
    recent_decisions.add_argument("--project")
    recent_decisions.add_argument("--limit", type=int, default=50)

    unanswered_messages = subparsers.add_parser("unanswered-messages")
    unanswered_messages.add_argument("chat_id")
    unanswered_messages.add_argument("--limit", type=int, default=50)

    delegate_summarize_parser = subparsers.add_parser("delegate-summarize")
    delegate_summarize_parser.add_argument("text", help="the tool output to summarize, or '-' to read it from stdin")
    delegate_summarize_parser.add_argument(
        "--action-type", default=ActionType.ROUTINE_WORK.value, choices=[a.value for a in ActionType]
    )
    delegate_summarize_parser.add_argument("--qwen-url")

    log_delegation_parser = subparsers.add_parser("log-delegation")
    log_delegation_parser.add_argument("backend", choices=[b.value for b in Backend])
    log_delegation_parser.add_argument("--outcome", default="ok")
    log_delegation_parser.add_argument("--detail")

    recent_delegations = subparsers.add_parser("recent-delegations")
    recent_delegations.add_argument("--limit", type=int, default=20)

    return parser


def _handle_get_topic(store: StateStore, args: argparse.Namespace) -> dict:
    return _topic_to_dict(store.get_topic(args.topic_id))


def _handle_update_status(store: StateStore, args: argparse.Namespace) -> dict:
    return _topic_to_dict(store.update_status(args.topic_id, TopicStatus(args.status)))


def _handle_add_finding(store: StateStore, args: argparse.Namespace) -> dict:
    return _topic_to_dict(store.add_finding(args.topic_id, args.finding))


def _handle_flag_needs_better_sources(store: StateStore, args: argparse.Namespace) -> dict:
    return _topic_to_dict(store.flag_needs_better_sources(args.topic_id))


def _handle_category_status(store: StateStore, args: argparse.Namespace) -> dict:
    """Read-only: tallies and returns the summary, posts nothing."""
    return _category_tally(store, args.category)


def _handle_category_rollup(store: StateStore, args: argparse.Namespace) -> dict:
    """Posts the tally as a comment on the category's tracking issue. Not read-only -
    call `category-status` instead if you just want to check without writing anywhere."""
    result = _category_tally(store, args.category)
    store.post_category_rollup(args.category, result["summary"])
    return result


def _category_tally(store: StateStore, category: str) -> dict:
    topics = store.query_by_category(category)
    return {
        "category": category,
        "total": len(topics),
        "researched": sum(1 for t in topics if t.status == TopicStatus.RESEARCHED),
        "summary": summarize_category(topics),
    }


def _handle_phase_check(store: StateStore, args: argparse.Namespace) -> dict:
    """Read-only: checks Learning Phase completion against the real roadmap research doc's
    expected topic roster, by identity not just count (ADR-0007: needs-better-sources counts
    as settled). Builds on the same `category_breakdown` `is_learning_phase_complete` uses, so
    the two can't drift."""
    breakdown = category_breakdown(store, expected_topics(DEFAULT_RESEARCH_DOC_PATH))
    complete = all(not category["unsettled_topic_ids"] for category in breakdown.values())
    return {"complete": complete, "breakdown": breakdown}


def _handle_get_phase(store: StateStore, args: argparse.Namespace) -> dict:
    return {"phase": store.get_phase().value}


def _handle_set_phase(store: StateStore, args: argparse.Namespace) -> dict:
    store.set_phase(Phase(args.phase))
    return {"phase": store.get_phase().value}


def _handle_seed(store: StateStore, args: argparse.Namespace) -> dict:
    """Idempotent: a topic already tracked (by topic_id) is skipped, never duplicated."""
    created = skipped = 0
    would_create: list[str] = []
    doc = Path(args.doc) if args.doc else DEFAULT_RESEARCH_DOC_PATH
    for entry in topic_entries(doc):
        try:
            store.get_topic(entry.topic_id)  # ValueError here means "not tracked yet"
            skipped += 1
        except ValueError:
            if args.dry_run:
                would_create.append(entry.topic_id)
            else:
                store.create_topic(entry.topic_id, entry.category, entry.title, entry.resources)
            created += 1
    result = {"created": created, "skipped": skipped}
    if args.dry_run:
        result = {"dry_run": True, "would_create": would_create, "skipped": skipped}
    return result


def _handle_log_message(store: StateStore, args: argparse.Namespace) -> dict:
    """Appends one Telegram message to the local message log (not the GitHub-backed store)."""
    MessageLog(default_path()).log(
        args.chat_id,
        Direction(args.direction),
        args.text,
        message_id=args.message_id,
        sent_at=args.sent_at,
    )
    return {"logged": True}


def _handle_recent_messages(store: StateStore, args: argparse.Namespace) -> dict:
    """Read-only: the last `limit` messages with this chat, oldest first."""
    messages = MessageLog(default_path()).recent(args.chat_id, args.limit)
    return {
        "messages": [
            {
                "direction": m.direction.value,
                "message_id": m.message_id,
                "sent_at": m.sent_at,
                "text": m.text,
            }
            for m in messages
        ]
    }


def _handle_delegate_summarize(store: StateStore, args: argparse.Namespace) -> dict:
    """Delegates a tool-output summary to the local Qwen backend (ADR-0012 - the
    only task type currently in scope). Reads from stdin when text is '-', since a
    real tool output can be far larger than a shell is comfortable passing as an arg."""
    text = sys.stdin.read() if args.text == "-" else args.text
    log = DelegationLog(default_log_path())
    summary = delegate_summarize(text, log=log, action_type=ActionType(args.action_type), base_url=args.qwen_url)
    return {"summary": summary}


def _handle_log_delegation(store: StateStore, args: argparse.Namespace) -> dict:
    """Records a Haiku/Sonnet delegation that already happened through the existing
    Agent tool (ADR-0012) - no inference call here, this is just the log entry."""
    log_external_delegation(DelegationLog(default_log_path()), Backend(args.backend), args.outcome, args.detail)
    return {"logged": True}


def _handle_recent_delegations(store: StateStore, args: argparse.Namespace) -> dict:
    """Read-only: the last `limit` delegation decisions, newest first."""
    return {"delegations": DelegationLog(default_log_path()).recent(args.limit)}


def _handle_unanswered_messages(store: StateStore, args: argparse.Namespace) -> dict:
    """Read-only: inbound messages since the last reply - usage-limit recovery
    check, see MessageLog.unanswered's docstring for why this exists."""
    messages = MessageLog(default_path()).unanswered(args.chat_id, args.limit)
    return {
        "messages": [
            {"direction": m.direction.value, "message_id": m.message_id, "sent_at": m.sent_at, "text": m.text}
            for m in messages
        ]
    }


def _handle_log_decision(store: StateStore, args: argparse.Namespace) -> dict:
    DecisionLog().log(args.project, args.decision, args.rationale, args.decided_at)
    return {"logged": True}


def _handle_recent_decisions(store: StateStore, args: argparse.Namespace) -> dict:
    decisions = DecisionLog().recent(args.project, args.limit)
    return {"decisions": [d.__dict__ for d in decisions]}


_HANDLERS = {
    "get-topic": _handle_get_topic,
    "update-status": _handle_update_status,
    "add-finding": _handle_add_finding,
    "flag-needs-better-sources": _handle_flag_needs_better_sources,
    "category-status": _handle_category_status,
    "category-rollup": _handle_category_rollup,
    "phase-check": _handle_phase_check,
    "get-phase": _handle_get_phase,
    "set-phase": _handle_set_phase,
    "seed": _handle_seed,
    "log-message": _handle_log_message,
    "recent-messages": _handle_recent_messages,
    "log-decision": _handle_log_decision,
    "recent-decisions": _handle_recent_decisions,
    "unanswered-messages": _handle_unanswered_messages,
    "delegate-summarize": _handle_delegate_summarize,
    "log-delegation": _handle_log_delegation,
    "recent-delegations": _handle_recent_delegations,
}


def run(argv: list[str], store: StateStore) -> str:
    args = build_parser().parse_args(argv)
    return json.dumps(_HANDLERS[args.command](store, args))


def _topic_to_dict(record: TopicRecord) -> dict:
    return {
        "topic_id": record.topic_id,
        "category": record.category,
        "title": record.title,
        "status": record.status.value,
        "resources": list(record.resources),
        "findings": list(record.findings),
        "needs_better_sources": record.needs_better_sources,
    }


def _local_command(argv: list[str]) -> int | None:
    """Commands that need no GitHub store (and so no configured repo)."""
    if argv and argv[0] in _MEMORY_COMMANDS:
        return _memory_command(argv)
    if argv and argv[0] == "eval-memory":
        return _eval_memory_command(argv[1:])
    if argv and argv[0] in {"export-data", "delete-data"}:
        return _owner_data_command(argv)
    if not argv or argv[0] not in {"doctor", "init", "service", "watchdog", "status", "voice", "usage-check"}:
        return None
    if argv[0] == "voice":
        return _voice_command(argv[1:])
    if argv[0] == "usage-check":
        from cimcime import usage_guard

        print(json.dumps(usage_guard.check()))
        return 0
    if argv[0] == "status":
        from cimcime.monitor import snapshot

        print(snapshot())
        return 0
    if argv[0] == "watchdog":
        from cimcime.watchdog import run_once

        print(run_once())
        return 0
    if argv[0] == "service":
        from cimcime import service

        sp = argparse.ArgumentParser(prog="cimcime service")
        sp.add_argument("action", choices=["install", "uninstall", "status", "restart"])
        a = sp.parse_args(argv[1:])
        try:
            if a.action == "install":
                for item in service.install():
                    print(f"installed {item}")
            elif a.action == "uninstall":
                service.uninstall()
                print("uninstalled")
            elif a.action == "restart":
                print("restarted" if service.restart() else "restart failed")
            else:
                print("running" if service.is_running() else "not running")
        except service.ServiceError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        return 0
    if argv[0] == "doctor":
        from cimcime.doctor import all_required_ok, format_report, run_checks

        checks = run_checks()
        print(format_report(checks))
        return 0 if all_required_ok(checks) else 1
    from cimcime.init_cmd import write_config

    p = argparse.ArgumentParser(prog="cimcime init")
    p.add_argument("repo", help="GitHub repo owner/name that tracks Cimcime's issues")
    p.add_argument("--local", action="store_true", help="write ./cimcime.toml instead of the user config dir")
    p.add_argument("--force", action="store_true")
    args = p.parse_args(argv[1:])
    try:
        print(f"Wrote {write_config(args.repo, local=args.local, force=args.force)}")
    except (ValueError, FileExistsError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


def _owner_data_command(argv: list[str]) -> int:
    from pathlib import Path

    from cimcime import owner_data

    p = argparse.ArgumentParser(prog="cimcime")
    sub = p.add_subparsers(dest="command", required=True)
    e = sub.add_parser("export-data", help="write messages and decisions to a 0600 JSON file")
    e.add_argument("out")
    d = sub.add_parser("delete-data", help="delete one chat's messages (and optionally all decisions)")
    d.add_argument("--chat-id")
    d.add_argument("--decisions", action="store_true")
    d.add_argument("--yes", action="store_true")
    args = p.parse_args(argv)
    if args.command == "export-data":
        result = owner_data.export_data(Path(args.out))
    else:
        result = owner_data.delete_data(args.chat_id, args.decisions, args.yes)
    print(json.dumps(result))
    return 0


DEFAULT_EVAL_CONFIG = Path(__file__).resolve().parents[2] / "docs" / "memory-eval" / "thresholds.toml"


def _eval_memory_command(argv: list[str]) -> int:
    """Deterministic retrieval-first memory eval (ADR-0017, docs/memory-eval.md). Exit 0 when every
    pre-registered gate passes or is skipped, 1 when one fails, 2 on a bad or tampered fixture."""
    from cimcime import memory_eval

    p = argparse.ArgumentParser(prog="cimcime eval-memory")
    p.add_argument("--fixture", required=True, help="frozen fixture JSON (SHA-256 pinned in the config)")
    p.add_argument("--config", default=str(DEFAULT_EVAL_CONFIG), help="thresholds TOML")
    p.add_argument("--embedder", choices=["none", "hash", "ollama", "unavailable"], default="none",
                   help="none: keyword variants only; hash: stdlib stand-in (plumbing, not quality);"
                        " ollama: local nomic-embed-text; unavailable: simulate an outage")
    p.add_argument("--json", action="store_true", help="print the full JSON report instead of Markdown")
    p.add_argument("--out-dir", default=None, help="also write report.json and report.md here (outside the repo)")
    args = p.parse_args(argv)
    try:
        report = memory_eval.evaluate(Path(args.fixture), Path(args.config), args.embedder)
    except (memory_eval.FixtureError, memory_eval.ManifestError) as exc:
        print(f"cimcime eval-memory: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    text = memory_eval.render_markdown(report)
    if args.out_dir:
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        (out / "report.md").write_text(text, encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False) if args.json else text)
    return 0 if report["ok"] else 1


_MEMORY_COMMANDS = {"memory-index", "memory-search", "memory-snapshot", "memory-brief", "memory-embed", "memory-checkpoint"}

# Claude Code hook event (slice 0 payloads, docs/memory.md) -> snapshot trigger.
_HOOK_TRIGGER = {"Stop": "stop", "PreCompact": "precompact"}


def _memory_command(argv: list[str]) -> int:
    """Context memory (ADR-E, docs/memory.md). Needs no GitHub store. Prints JSON, except in
    --hook mode, where output follows the Claude Code hook contract and errors never fail the
    session (they go to stderr, exit 0)."""
    from cimcime import memory

    p = argparse.ArgumentParser(prog="cimcime")
    sub = p.add_subparsers(dest="command", required=True)
    index = sub.add_parser("memory-index", help="ingest Telegram messages and decisions")
    index.add_argument("--source", default=None, help="message log db (default: the message log path)")
    sub.add_parser("memory-embed", help="embed chunks that have no vector yet (needs local Ollama; optional)")
    search = sub.add_parser("memory-search", help="hybrid (FTS5 + vector) search; keyword-only without embeddings")
    search.add_argument("--no-embed", action="store_true", help="skip the vector side")
    search.add_argument("query")
    search.add_argument("--scope", action="append", help="repeatable; sensitive scopes only when named")
    search.add_argument("--limit", type=int, default=10)
    snap = sub.add_parser("memory-snapshot", help="archive the transcript and store a handoff summary")
    snap.add_argument("--hook", action="store_true", help="read a Stop/PreCompact hook payload from stdin")
    snap.add_argument("--session-id")
    snap.add_argument("--transcript")
    snap.add_argument("--trigger", choices=["manual", "stop", "precompact"], default="manual")
    snap.add_argument("--if-due", action="store_true", help="only when the snapshot interval is reached")
    snap.add_argument("--interval", type=int, default=memory.SNAPSHOT_INTERVAL_TOKENS)
    snap.add_argument("--scope", default=memory.DEFAULT_SCOPE)
    snap.add_argument("--max-age-minutes", type=float, default=None, help="also snapshot when this old (with --if-due)")
    cp = sub.add_parser("memory-checkpoint", help="checkpoint-and-rotate: archive, embed, print the handoff brief")
    cp.add_argument("--session-id", required=True)
    cp.add_argument("--transcript", required=True)
    cp.add_argument("--if-due", action="store_true", help="only past the token interval or --max-age-minutes")
    cp.add_argument("--interval", type=int, default=memory.SNAPSHOT_INTERVAL_TOKENS)
    cp.add_argument("--max-age-minutes", type=float, default=None)
    cp.add_argument("--scope", default=memory.DEFAULT_SCOPE)
    cp.add_argument("--max-tokens", type=int, default=memory.BRIEF_MAX_TOKENS)
    brief = sub.add_parser("memory-brief", help="the handoff brief a new session starts from")
    brief.add_argument("--hook", action="store_true", help="emit SessionStart additionalContext JSON")
    brief.add_argument("--scope", default=memory.DEFAULT_SCOPE)
    brief.add_argument("--max-tokens", type=int, default=memory.BRIEF_MAX_TOKENS)
    args = p.parse_args(argv)

    def _age(a):
        m = getattr(a, "max_age_minutes", None)
        return timedelta(minutes=m) if m is not None else None

    try:
        embedder = None if getattr(args, "no_embed", False) else memory.OllamaEmbedder(timeout=10)
        mem = memory.Memory(memory.default_path(), embedder=embedder)
        if args.command == "memory-index":
            result: dict = mem.index(Path(args.source) if args.source else default_path())
            result["embedding"] = mem.embed_pending()
        elif args.command == "memory-embed":
            result = mem.embed_pending()
        elif args.command == "memory-checkpoint":
            age = timedelta(minutes=args.max_age_minutes) if args.max_age_minutes is not None else None
            result = mem.checkpoint(args.session_id, Path(args.transcript), scope=args.scope,
                                    if_due=args.if_due, interval=args.interval, max_age=age,
                                    max_tokens=args.max_tokens)
        elif args.command == "memory-search":
            found = mem.search(args.query, args.scope, args.limit)
            result = {"mode": found.mode, "note": found.note, "hits": [h.__dict__ for h in found.hits]}
        elif args.command == "memory-snapshot":
            if args.hook:
                payload = json.loads(sys.stdin.read() or "{}")
                trigger = _HOOK_TRIGGER.get(payload.get("hook_event_name"), "manual")
                mem.snapshot(payload["session_id"], Path(payload["transcript_path"]), trigger,
                             scope=args.scope, if_due=trigger == "stop", interval=args.interval, max_age=_age(args))
                return 0
            if not (args.session_id and args.transcript):
                p.error("memory-snapshot needs --session-id and --transcript (or --hook)")
            result = mem.snapshot(args.session_id, Path(args.transcript), args.trigger, scope=args.scope,
                                  if_due=args.if_due, interval=args.interval, max_age=_age(args))
        else:
            text = mem.brief(args.scope, args.max_tokens)
            if args.hook:
                if text:
                    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                                             "additionalContext": text}}))
                return 0
            result = {"brief": text, "tokens": memory.estimate_tokens(text)}
    except Exception as exc:  # noqa: BLE001 - a hook must never take the session down
        print(f"cimcime memory: {type(exc).__name__}: {exc}", file=sys.stderr)
        if getattr(args, "hook", False):
            return 0
        print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"}))
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


def _voice_command(argv: list[str]) -> int:
    """voice transcribe <file> | voice speak <chat_id> <text> | voice doctor. Always prints JSON;
    exit code 1 with {"ok": false, "error": ...} so the caller can answer in text instead."""
    from pathlib import Path

    from cimcime import voice

    p = argparse.ArgumentParser(prog="cimcime voice")
    sub = p.add_subparsers(dest="action", required=True)
    t = sub.add_parser("transcribe")
    t.add_argument("file")
    t.add_argument("--language", default="tr")
    s = sub.add_parser("speak")
    s.add_argument("chat_id")
    s.add_argument("text")
    s.add_argument("--caption", default=None)
    sub.add_parser("doctor")
    args = p.parse_args(argv)
    try:
        if args.action == "doctor":
            checks = voice.doctor()
            print(json.dumps({"ok": all(ok for _, ok, _ in checks), "checks": [
                {"name": n, "ok": ok, "detail": d} for n, ok, d in checks]}))
            return 0 if all(ok for _, ok, _ in checks) else 1
        if args.action == "transcribe":
            print(json.dumps({"ok": True, "transcript": voice.transcribe(Path(args.file), args.language)},
                             ensure_ascii=False))
            return 0
        result = voice.speak(args.chat_id, args.text, caption=args.caption)
        MessageLog(default_path()).log(
            args.chat_id, Direction.OUTBOUND, f"[voice] {args.text}", message_id=result["message_id"]
        )
        print(json.dumps({"ok": True, **result}))
        return 0
    except voice.VoiceError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1


def main() -> None:
    code = _local_command(sys.argv[1:])
    if code is not None:
        sys.exit(code)
    store = GitHubIssuesStore(repo=get_repo())
    print(run(sys.argv[1:], store))


if __name__ == "__main__":
    main()
