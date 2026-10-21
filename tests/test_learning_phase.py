import pytest

from cimcime.state_store import InMemoryStore, TopicStatus, category_breakdown, is_learning_phase_complete


@pytest.fixture
def store() -> InMemoryStore:
    return InMemoryStore()


def test_complete_when_no_categories_are_expected(store: InMemoryStore):
    assert is_learning_phase_complete(store, expected_topics_by_category={}) is True


def test_incomplete_when_a_category_has_no_tracked_topics_yet(store: InMemoryStore):
    assert (
        is_learning_phase_complete(store, expected_topics_by_category={"x": {"a", "b"}}) is False
    )


def test_researched_topics_count_toward_completion(store: InMemoryStore):
    store.create_topic(topic_id="a", category="x", title="A", resources=[])
    store.create_topic(topic_id="b", category="x", title="B", resources=[])
    store.update_status("a", TopicStatus.RESEARCHED)
    store.update_status("b", TopicStatus.RESEARCHED)

    assert is_learning_phase_complete(store, expected_topics_by_category={"x": {"a", "b"}}) is True


def test_needs_better_sources_topics_also_count_toward_completion(store: InMemoryStore):
    store.create_topic(topic_id="a", category="x", title="A", resources=[])
    store.create_topic(topic_id="b", category="x", title="B", resources=[])
    store.update_status("a", TopicStatus.RESEARCHED)
    store.flag_needs_better_sources("b")

    assert is_learning_phase_complete(store, expected_topics_by_category={"x": {"a", "b"}}) is True


def test_untouched_needs_research_topics_block_completion(store: InMemoryStore):
    store.create_topic(topic_id="a", category="x", title="A", resources=[])
    store.create_topic(topic_id="b", category="x", title="B", resources=[])
    store.update_status("a", TopicStatus.RESEARCHED)
    # b stays plain needs_research - neither researched nor needs-better-sources

    assert is_learning_phase_complete(store, expected_topics_by_category={"x": {"a", "b"}}) is False


def test_every_category_must_be_settled_not_just_one(store: InMemoryStore):
    store.create_topic(topic_id="a", category="x", title="A", resources=[])
    store.update_status("a", TopicStatus.RESEARCHED)
    store.create_topic(topic_id="c", category="y", title="C", resources=[])
    # y's one topic is untouched

    assert (
        is_learning_phase_complete(store, expected_topics_by_category={"x": {"a"}, "y": {"c"}})
        is False
    )


def test_a_mislabeled_topic_cannot_fake_completion_by_count_alone(store: InMemoryStore):
    # The real risk identity-checking guards against: category "x" expects {a, b}. Only "a" is
    # tracked and settled under "x", but some unrelated topic "z" also lives under "x" - so a
    # pure *count* comparison (1 expected missing, but 1 "extra" tracked) could wrongly balance
    # out to "looks done" if it only compared totals. Identity checking must not be fooled by this.
    store.create_topic(topic_id="a", category="x", title="A", resources=[])
    store.create_topic(topic_id="z", category="x", title="Z (not in the real roster)", resources=[])
    store.update_status("a", TopicStatus.RESEARCHED)
    store.update_status("z", TopicStatus.RESEARCHED)

    assert is_learning_phase_complete(store, expected_topics_by_category={"x": {"a", "b"}}) is False


def test_category_breakdown_reports_which_topic_ids_are_still_unsettled(store: InMemoryStore):
    store.create_topic(topic_id="a", category="x", title="A", resources=[])
    store.update_status("a", TopicStatus.RESEARCHED)

    breakdown = category_breakdown(store, expected_topics_by_category={"x": {"a", "b"}})

    assert breakdown["x"]["expected"] == 2
    assert breakdown["x"]["settled"] == 1
    assert breakdown["x"]["unsettled_topic_ids"] == ["b"]
