from __future__ import annotations

import re
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

_HEADING_RE = re.compile(r"^## (?:\d+\.\s*)?(.+?)\s*$")
_TOPIC_HEADING_RE = re.compile(r"^### (.+?)\s*$")
_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slugify(title: str) -> str:
    return _SLUG_RE.sub("-", title.lower()).strip("-")


def expected_topics(research_doc_path: Path) -> dict[str, set[str]]:
    """The true expected topic roster per category slug - topic_ids slugified from the research
    doc's `### <Topic>` headings, grouped under their `## N. <Category>` section. Identity, not
    just a count, so a mislabeled or duplicate topic can't make a category look complete when
    the real expected topics are still untouched. Unrecognized `##` sections (e.g. "Gaps / notes")
    stop collecting until the next recognized one."""
    topics: dict[str, set[str]] = {}
    current_slug: str | None = None
    for line in research_doc_path.read_text().splitlines():
        heading = _HEADING_RE.match(line)
        if heading:
            current_slug = CATEGORY_SLUGS.get(heading.group(1))
            continue
        topic_heading = _TOPIC_HEADING_RE.match(line)
        if current_slug is not None and topic_heading:
            topics.setdefault(current_slug, set()).add(_slugify(topic_heading.group(1)))
    return topics


def expected_topic_counts(research_doc_path: Path) -> dict[str, int]:
    """Convenience view of `expected_topics` for callers that only need the tally (e.g. display)."""
    return {category: len(ids) for category, ids in expected_topics(research_doc_path).items()}
