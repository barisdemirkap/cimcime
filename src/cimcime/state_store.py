from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any, Protocol, Sequence


class TopicStatus(str, Enum):
    NEEDS_RESEARCH = "needs_research"
    RESEARCHED = "researched"


@dataclass(frozen=True)
class TopicRecord:
    topic_id: str
    category: str
    title: str
    status: TopicStatus
    resources: tuple[str, ...] = ()
    findings: tuple[str, ...] = ()


class StateStore(Protocol):
    def create_topic(
        self, topic_id: str, category: str, title: str, resources: Sequence[str]
    ) -> TopicRecord: ...

    def get_topic(self, topic_id: str) -> TopicRecord: ...

    def update_status(self, topic_id: str, status: TopicStatus) -> TopicRecord: ...

    def add_finding(self, topic_id: str, finding: str) -> TopicRecord: ...

    def query_by_category(self, category: str) -> list[TopicRecord]: ...

    def query_by_status(self, status: TopicStatus) -> list[TopicRecord]: ...


class InMemoryStore:
    """Fake StateStore for tests: no I/O, same contract as GitHubIssuesStore."""

    def __init__(self) -> None:
        self._topics: dict[str, TopicRecord] = {}

    def create_topic(
        self, topic_id: str, category: str, title: str, resources: Sequence[str]
    ) -> TopicRecord:
        if topic_id in self._topics:
            raise ValueError(f"topic {topic_id!r} already exists")

        record = TopicRecord(
            topic_id=topic_id,
            category=category,
            title=title,
            status=TopicStatus.NEEDS_RESEARCH,
            resources=tuple(resources),
        )
        self._topics[topic_id] = record
        return record

    def get_topic(self, topic_id: str) -> TopicRecord:
        return self._require(topic_id)

    def update_status(self, topic_id: str, status: TopicStatus) -> TopicRecord:
        record = self._require(topic_id)
        updated = replace(record, status=status)
        self._topics[topic_id] = updated
        return updated

    def add_finding(self, topic_id: str, finding: str) -> TopicRecord:
        record = self._require(topic_id)
        updated = replace(record, findings=record.findings + (finding,))
        self._topics[topic_id] = updated
        return updated

    def query_by_category(self, category: str) -> list[TopicRecord]:
        return [t for t in self._topics.values() if t.category == category]

    def query_by_status(self, status: TopicStatus) -> list[TopicRecord]:
        return [t for t in self._topics.values() if t.status == status]

    def _require(self, topic_id: str) -> TopicRecord:
        try:
            return self._topics[topic_id]
        except KeyError:
            raise ValueError(f"topic {topic_id!r} does not exist") from None


_STATUS_LABELS: dict[TopicStatus, str] = {
    TopicStatus.NEEDS_RESEARCH: "fde:needs-research",
    TopicStatus.RESEARCHED: "fde:researched",
}
_CATEGORY_LABEL_PREFIX = "fde:category:"
_CATEGORY_MAP_LABEL = "fde:category-map"
_TOPIC_MARKER_RE = re.compile(r"<!-- cimcime:topic_id=(\S+) -->")
_RESOURCE_LINE_RE = re.compile(r"^- (.+)$", re.MULTILINE)


def _topic_id_marker(topic_id: str) -> str:
    return f"<!-- cimcime:topic_id={topic_id} -->"


def _category_marker(category: str) -> str:
    return f"<!-- cimcime:category={category} -->"


def _render_body(topic_id: str, resources: Sequence[str]) -> str:
    lines = [_topic_id_marker(topic_id), "", "## Resources", ""]
    lines += [f"- {r}" for r in resources]
    return "\n".join(lines)


def _parse_resources(body: str) -> tuple[str, ...]:
    _, _, after = body.partition("## Resources")
    return tuple(_RESOURCE_LINE_RE.findall(after))


def _status_from_labels(labels: Sequence[str]) -> TopicStatus:
    for status, label in _STATUS_LABELS.items():
        if label in labels:
            return status
    raise ValueError(f"issue has no recognized status label: {labels!r}")


def _category_from_labels(labels: Sequence[str]) -> str:
    for label in labels:
        if label.startswith(_CATEGORY_LABEL_PREFIX):
            return label[len(_CATEGORY_LABEL_PREFIX) :]
    raise ValueError(f"issue has no category label: {labels!r}")


class GitHubIssuesStore:
    """StateStore backed by real GitHub Issues - the source of truth, per ADR-0004.

    Topics nest under a per-category tracking issue (the `/wayfinder` map-and-children
    pattern ADR-0004 calls for): the category issue is created lazily, the first time a
    topic in that category is created, and reused for every topic after that.
    """

    _ISSUE_FIELDS = "number,title,body,labels,comments"
    _LOOKUP_FIELDS = "number,body"

    def __init__(self, repo: str) -> None:
        self._repo = repo

    def create_topic(
        self, topic_id: str, category: str, title: str, resources: Sequence[str]
    ) -> TopicRecord:
        if self._find_issue_number(topic_id) is not None:
            raise ValueError(f"topic {topic_id!r} already exists")

        parent_number = self._find_or_create_category_issue(category)

        self._run(
            [
                "issue",
                "create",
                "--title",
                title,
                "--body",
                _render_body(topic_id, resources),
                "--label",
                _STATUS_LABELS[TopicStatus.NEEDS_RESEARCH],
                "--label",
                f"{_CATEGORY_LABEL_PREFIX}{category}",
                "--parent",
                str(parent_number),
            ]
        )
        return self._get(topic_id)

    def get_topic(self, topic_id: str) -> TopicRecord:
        return self._get(topic_id)

    def update_status(self, topic_id: str, status: TopicStatus) -> TopicRecord:
        number = self._require_issue_number(topic_id)
        current = self._get(topic_id)
        self._run(
            [
                "issue",
                "edit",
                str(number),
                "--remove-label",
                _STATUS_LABELS[current.status],
                "--add-label",
                _STATUS_LABELS[status],
            ]
        )
        return self._get(topic_id)

    def add_finding(self, topic_id: str, finding: str) -> TopicRecord:
        number = self._require_issue_number(topic_id)
        self._run(["issue", "comment", str(number), "--body", finding])
        return self._get(topic_id)

    def query_by_category(self, category: str) -> list[TopicRecord]:
        return self._query(label=f"{_CATEGORY_LABEL_PREFIX}{category}")

    def query_by_status(self, status: TopicStatus) -> list[TopicRecord]:
        return self._query(label=_STATUS_LABELS[status])

    # -- internals --

    def _run(self, args: list[str]) -> str:
        result = subprocess.run(
            ["gh", *args, "--repo", self._repo],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout

    def _query(self, label: str) -> list[TopicRecord]:
        # Deliberately not `gh issue list --label` / `--search`: both appear to go
        # through GitHub's search index under the hood, which lags right after a
        # write (eventual consistency) — a just-created/just-labeled issue can be
        # briefly invisible to it. Listing all issues and filtering by the `labels`
        # field client-side is exact and cheap at this issue count.
        #
        # `--state all`, not `--state open`: TopicStatus (needs_research/researched)
        # is the source of truth for a topic's state, not GitHub's open/closed flag.
        # A topic whose issue gets closed (by a human, by cleanup, by anything) must
        # stay visible to queries — it shouldn't silently vanish from category/status
        # rollups just because the issue's open/closed flag changed.
        return [
            self._to_record(issue)
            for issue in self._list_all()
            if label in {label_name["name"] for label_name in issue["labels"]}
        ]

    def _list_all(self) -> list[dict[str, Any]]:
        out = self._run(
            ["issue", "list", "--state", "all", "--limit", "500", "--json", self._ISSUE_FIELDS]
        )
        return json.loads(out)

    def _find_issue_number(self, topic_id: str) -> int | None:
        out = self._run(
            ["issue", "list", "--state", "all", "--limit", "500", "--json", self._LOOKUP_FIELDS]
        )
        for issue in json.loads(out):
            if _topic_id_marker(topic_id) in issue["body"]:
                return issue["number"]
        return None

    def _find_or_create_category_issue(self, category: str) -> int:
        marker = _category_marker(category)
        for issue in self._list_all():
            if marker in issue["body"]:
                return issue["number"]

        url = self._run(
            [
                "issue",
                "create",
                "--title",
                f"[category] {category}",
                "--body",
                f"{marker}\n\nTracks every topic in the '{category}' category.",
                "--label",
                _CATEGORY_MAP_LABEL,
            ]
        )
        return int(url.strip().rsplit("/", 1)[-1])

    def _require_issue_number(self, topic_id: str) -> int:
        number = self._find_issue_number(topic_id)
        if number is None:
            raise ValueError(f"topic {topic_id!r} does not exist")
        return number

    def _get(self, topic_id: str) -> TopicRecord:
        number = self._require_issue_number(topic_id)
        out = self._run(["issue", "view", str(number), "--json", self._ISSUE_FIELDS])
        return self._to_record(json.loads(out))

    def _to_record(self, issue: dict[str, Any]) -> TopicRecord:
        labels = [label["name"] for label in issue["labels"]]
        marker = _TOPIC_MARKER_RE.search(issue["body"])
        if marker is None:
            raise ValueError(f"issue #{issue['number']} has no cimcime topic marker")
        return TopicRecord(
            topic_id=marker.group(1),
            category=_category_from_labels(labels),
            title=issue["title"],
            status=_status_from_labels(labels),
            resources=_parse_resources(issue["body"]),
            findings=tuple(comment["body"] for comment in issue["comments"]),
        )
