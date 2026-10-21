from __future__ import annotations

import argparse
import json
import sys

from cimcime.state_store import (
    GitHubIssuesStore,
    StateStore,
    TopicRecord,
    TopicStatus,
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

    category_status = subparsers.add_parser("category-status")
    category_status.add_argument("category")

    category_rollup = subparsers.add_parser("category-rollup")
    category_rollup.add_argument("category")

    return parser


def _handle_get_topic(store: StateStore, args: argparse.Namespace) -> dict:
    return _topic_to_dict(store.get_topic(args.topic_id))


def _handle_update_status(store: StateStore, args: argparse.Namespace) -> dict:
    return _topic_to_dict(store.update_status(args.topic_id, TopicStatus(args.status)))


def _handle_add_finding(store: StateStore, args: argparse.Namespace) -> dict:
    return _topic_to_dict(store.add_finding(args.topic_id, args.finding))


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


_HANDLERS = {
    "get-topic": _handle_get_topic,
    "update-status": _handle_update_status,
    "add-finding": _handle_add_finding,
    "category-status": _handle_category_status,
    "category-rollup": _handle_category_rollup,
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
    }


def main() -> None:
    store = GitHubIssuesStore(repo=DEFAULT_REPO)
    print(run(sys.argv[1:], store))


if __name__ == "__main__":
    main()
