from __future__ import annotations

import argparse
import json
import sys

from cimcime.state_store import GitHubIssuesStore, StateStore, TopicRecord, TopicStatus

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

    return parser


def _handle_get_topic(store: StateStore, args: argparse.Namespace) -> TopicRecord:
    return store.get_topic(args.topic_id)


def _handle_update_status(store: StateStore, args: argparse.Namespace) -> TopicRecord:
    return store.update_status(args.topic_id, TopicStatus(args.status))


def _handle_add_finding(store: StateStore, args: argparse.Namespace) -> TopicRecord:
    return store.add_finding(args.topic_id, args.finding)


_HANDLERS = {
    "get-topic": _handle_get_topic,
    "update-status": _handle_update_status,
    "add-finding": _handle_add_finding,
}


def run(argv: list[str], store: StateStore) -> str:
    args = build_parser().parse_args(argv)
    record = _HANDLERS[args.command](store, args)
    return json.dumps(_to_dict(record))


def _to_dict(record: TopicRecord) -> dict:
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
