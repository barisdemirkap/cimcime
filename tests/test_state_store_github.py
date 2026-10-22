import json
import subprocess
import uuid

import pytest

from cimcime.state_store import GitHubIssuesStore, Phase, TopicStatus

pytestmark = pytest.mark.integration

REPO = "barisdemirkap/forward-deployed-engineer"


def _close_test_issue(store: GitHubIssuesStore, topic_id: str) -> None:
    # Cleanup only, via plain `gh` — not part of the production StateStore interface.
    # Reuses the store's own lookup (exact marker match) instead of re-implementing
    # the list-and-filter dance here too.
    number = store._find_issue_number(topic_id)
    if number is not None:
        subprocess.run(["gh", "issue", "close", str(number), "--repo", REPO], check=True)


@pytest.fixture
def store() -> GitHubIssuesStore:
    return GitHubIssuesStore(repo=REPO)


@pytest.fixture
def topic_id() -> str:
    # unique per run so repeated test runs never collide with a leftover issue
    return f"test-topic-{uuid.uuid4().hex[:8]}"


def test_create_update_and_query_round_trip_against_a_real_issue(
    store: GitHubIssuesStore, topic_id: str
):
    try:
        created = store.create_topic(
            topic_id=topic_id,
            category="test-category",
            title=f"[integration test] {topic_id}",
            resources=["https://example.com/resource-a", "https://example.com/resource-b"],
        )
        assert created.status == TopicStatus.NEEDS_RESEARCH
        assert created.resources == (
            "https://example.com/resource-a",
            "https://example.com/resource-b",
        )

        by_category = {t.topic_id for t in store.query_by_category("test-category")}
        assert topic_id in by_category

        by_needs_research = {t.topic_id for t in store.query_by_status(TopicStatus.NEEDS_RESEARCH)}
        assert topic_id in by_needs_research

        with_finding = store.add_finding(topic_id, "a real finding from the live test")
        assert with_finding.findings == ("a real finding from the live test",)

        researched = store.update_status(topic_id, TopicStatus.RESEARCHED)
        assert researched.status == TopicStatus.RESEARCHED

        by_researched = {t.topic_id for t in store.query_by_status(TopicStatus.RESEARCHED)}
        assert topic_id in by_researched

        by_needs_research_after = {
            t.topic_id for t in store.query_by_status(TopicStatus.NEEDS_RESEARCH)
        }
        assert topic_id not in by_needs_research_after
    finally:
        _close_test_issue(store, topic_id)


def test_topics_in_the_same_category_nest_under_one_shared_category_issue(
    store: GitHubIssuesStore,
):
    # "test-category" is a long-lived fixture category reused across integration-test
    # runs on purpose (create_topic's category issue is find-or-create, so this proves
    # reuse rather than duplication) — its tracking issue is deliberately never closed.
    first_id = f"test-topic-{uuid.uuid4().hex[:8]}"
    second_id = f"test-topic-{uuid.uuid4().hex[:8]}"
    try:
        store.create_topic(
            topic_id=first_id,
            category="test-category",
            title=f"[integration test] {first_id}",
            resources=[],
        )
        store.create_topic(
            topic_id=second_id,
            category="test-category",
            title=f"[integration test] {second_id}",
            resources=[],
        )

        category_issue_number = store._find_or_create_category_issue("test-category")

        # Read each child's own `parent` field rather than the parent's `sub_issues`
        # listing: `gh issue create --parent` sets the relationship atomically with
        # creation, but the parent's own sub_issues listing can lag right after a write
        # (the same general eventual-consistency class documented on `_query` above) —
        # checking from the child's side avoids relying on that lagging derived view.
        for topic_id in (first_id, second_id):
            number = store._require_issue_number(topic_id)
            result = subprocess.run(
                ["gh", "issue", "view", str(number), "--repo", REPO, "--json", "parent"],
                capture_output=True,
                text=True,
                check=True,
            )
            assert json.loads(result.stdout)["parent"]["number"] == category_issue_number
    finally:
        _close_test_issue(store, first_id)
        _close_test_issue(store, second_id)


def test_post_category_rollup_comments_on_the_real_category_issue(store: GitHubIssuesStore):
    summary = f"rollup check {uuid.uuid4().hex[:8]}"

    store.post_category_rollup("test-category", summary)

    category_issue_number = store._find_or_create_category_issue("test-category")
    result = subprocess.run(
        ["gh", "issue", "view", str(category_issue_number), "--repo", REPO, "--json", "comments"],
        capture_output=True,
        text=True,
        check=True,
    )
    comments = [c["body"] for c in json.loads(result.stdout)["comments"]]
    assert summary in comments


def test_phase_round_trips_against_the_real_system_issue(store: GitHubIssuesStore):
    # This is real, global, persistent state for this repo - not a scratch fixture - so leave it
    # exactly as found (this repo is genuinely still in its real Learning Phase) rather than
    # leaking a test-induced phase change into production state.
    original = store.get_phase()
    try:
        store.set_phase(Phase.RUNTIME)
        assert store.get_phase() == Phase.RUNTIME

        store.set_phase(Phase.LEARNING)
        assert store.get_phase() == Phase.LEARNING
    finally:
        store.set_phase(original)


def test_flag_needs_better_sources_sets_the_real_label(
    store: GitHubIssuesStore, topic_id: str
):
    try:
        store.create_topic(
            topic_id=topic_id,
            category="test-category",
            title=f"[integration test] {topic_id}",
            resources=[],
        )

        flagged = store.flag_needs_better_sources(topic_id)

        assert flagged.needs_better_sources is True
        assert flagged.status == TopicStatus.NEEDS_RESEARCH
        reread = store.get_topic(topic_id)
        assert reread.needs_better_sources is True
    finally:
        _close_test_issue(store, topic_id)
