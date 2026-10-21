from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# Display title (as it appears in the research doc's "## N. Title" headings) -> category slug
# (as used everywhere else: state-store categories, the 9 .claude/agents/*.md files). "Documentation"
# folds into "client-engagement-delivery" - see that agent's framing paragraph for why.
CATEGORY_SLUGS: dict[str, str] = {
    "FDE Role & Career Path": "fde-role-career",
    "Core Software Engineering Foundations": "core-software-engineering",
    "AI & LLM Engineering": "ai-llm-engineering",
    "AI Coding Tools": "ai-coding-tools",
    "Cloud, Infrastructure & DevOps": "platform-infra-devops",
    "Data Engineering": "data-engineering",
    "Integration & Enterprise Systems": "integration-enterprise-systems",
    "Client Engagement & Delivery": "client-engagement-delivery",
    "Business & Strategy": "business-strategy",
    "Documentation": "client-engagement-delivery",
}

DEFAULT_RESEARCH_DOC_PATH = (
    Path(__file__).parent.parent.parent / "docs" / "research" / "forward-deployed-engineer-roadmap.md"
)

_CATEGORY_HEADING_RE = re.compile(r"^## (?:\d+\.\s*)?(.+?)\s*$")
_TOPIC_HEADING_RE = re.compile(r"^### (.+?)\s*$")
_RESOURCE_URL_RE = re.compile(r"\]\((https?://[^)]+)\)")
_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slugify(title: str) -> str:
    return _SLUG_RE.sub("-", title.lower()).strip("-")


@dataclass(frozen=True)
class RoadmapTopic:
    topic_id: str
    category: str
    title: str
    resources: tuple[str, ...]


def topic_entries(research_doc_path: Path) -> list[RoadmapTopic]:
    """Every topic in the research doc, with its real title and resource URLs - the single
    parse both the seeding script and `expected_topics`/`expected_topic_counts` build on, so
    there's one parser rather than two drifting copies of the same heading-walking logic.
    Unrecognized `##` sections (e.g. "Gaps / notes") stop collecting until the next recognized
    one."""
    entries: list[RoadmapTopic] = []
    current_slug: str | None = None
    current_title: str | None = None
    current_resources: list[str] = []

    def emit() -> None:
        if current_slug is not None and current_title is not None:
            entries.append(
                RoadmapTopic(
                    topic_id=_slugify(current_title),
                    category=current_slug,
                    title=current_title,
                    resources=tuple(current_resources),
                )
            )

    for line in research_doc_path.read_text().splitlines():
        category_heading = _CATEGORY_HEADING_RE.match(line)
        if category_heading:
            emit()
            current_title, current_resources = None, []
            current_slug = CATEGORY_SLUGS.get(category_heading.group(1))
            continue

        topic_heading = _TOPIC_HEADING_RE.match(line)
        if current_slug is not None and topic_heading:
            emit()
            current_title, current_resources = topic_heading.group(1), []
            continue

        if current_title is not None:
            url_match = _RESOURCE_URL_RE.search(line)
            if url_match:
                current_resources.append(url_match.group(1))

    emit()
    return entries


def expected_topics(research_doc_path: Path) -> dict[str, set[str]]:
    """The true expected topic roster per category slug. Identity, not just a count, so a
    mislabeled or duplicate topic can't make a category look complete when the real expected
    topics are still untouched."""
    topics: dict[str, set[str]] = {}
    for entry in topic_entries(research_doc_path):
        topics.setdefault(entry.category, set()).add(entry.topic_id)
    return topics


def expected_topic_counts(research_doc_path: Path) -> dict[str, int]:
    """Convenience view of `expected_topics` for callers that only need the tally (e.g. display)."""
    return {category: len(ids) for category, ids in expected_topics(research_doc_path).items()}
