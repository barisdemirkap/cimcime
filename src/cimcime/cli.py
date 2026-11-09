from __future__ import annotations

import argparse
import json
import sys

from cimcime.approval_gate import ActionType
from cimcime.config import get_repo
from cimcime.delegation import (
    Backend,
    DelegationLog,
    default_log_path,
    delegate_summarize,
    log_external_delegation,
)
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

    subparsers.add_parser("seed")

    log_message = subparsers.add_parser("log-message")
    log_message.add_argument("chat_id")
    log_message.add_argument("direction", choices=[d.value for d in Direction])
    log_message.add_argument("text")
    log_message.add_argument("--message-id")
    log_message.add_argument("--sent-at")

    recent_messages = subparsers.add_parser("recent-messages")
    recent_messages.add_argument("chat_id")
    recent_messages.add_argument("--limit", type=int, default=20)

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
    for entry in topic_entries(DEFAULT_RESEARCH_DOC_PATH):
        try:
            store.get_topic(entry.topic_id)  # ValueError here means "not tracked yet"
            skipped += 1
        except ValueError:
            store.create_topic(entry.topic_id, entry.category, entry.title, entry.resources)
            created += 1
    return {"created": created, "skipped": skipped}


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
    if not argv or argv[0] not in {"doctor", "init", "service", "watchdog"}:
        return None
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


def main() -> None:
    code = _local_command(sys.argv[1:])
    if code is not None:
        sys.exit(code)
    store = GitHubIssuesStore(repo=get_repo())
    print(run(sys.argv[1:], store))


if __name__ == "__main__":
    main()
