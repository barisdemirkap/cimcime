from __future__ import annotations

import argparse
import json
import sys

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

DEFAULT_REPO = "barisdemirkap/forward-deployed-engineer"


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


def main() -> None:
    store = GitHubIssuesStore(repo=DEFAULT_REPO)
    print(run(sys.argv[1:], store))


if __name__ == "__main__":
    main()
