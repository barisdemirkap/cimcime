import pytest

from cimcime.state_store import InMemoryStore, Phase, TopicStatus


@pytest.fixture
def store() -> InMemoryStore:
    return InMemoryStore()


def test_created_topic_starts_needs_research(store: InMemoryStore):
    store.create_topic(
        topic_id="rag",
        category="ai-llm-engineering",
        title="RAG",
        resources=["https://example.com/rag-article"],
    )

    [topic] = store.query_by_status(TopicStatus.NEEDS_RESEARCH)
    assert topic.topic_id == "rag"
    assert topic.category == "ai-llm-engineering"
    assert topic.title == "RAG"
    assert topic.resources == ("https://example.com/rag-article",)


def test_creating_a_duplicate_topic_id_raises(store: InMemoryStore):
    store.create_topic(topic_id="rag", category="ai-llm-engineering", title="RAG", resources=[])

    with pytest.raises(ValueError):
        store.create_topic(topic_id="rag", category="ai-llm-engineering", title="RAG", resources=[])


def test_get_topic_returns_the_current_record(store: InMemoryStore):
    store.create_topic(topic_id="rag", category="ai-llm-engineering", title="RAG", resources=[])

    topic = store.get_topic("rag")
    assert topic.topic_id == "rag"


def test_get_topic_on_an_unknown_topic_raises(store: InMemoryStore):
    with pytest.raises(ValueError):
        store.get_topic("does-not-exist")


def test_update_status_moves_topic_between_status_queries(store: InMemoryStore):
    store.create_topic(topic_id="rag", category="ai-llm-engineering", title="RAG", resources=[])

    store.update_status("rag", TopicStatus.RESEARCHED)

    assert store.query_by_status(TopicStatus.NEEDS_RESEARCH) == []
    [topic] = store.query_by_status(TopicStatus.RESEARCHED)
    assert topic.topic_id == "rag"


def test_add_finding_appends_without_losing_prior_findings(store: InMemoryStore):
    store.create_topic(topic_id="rag", category="ai-llm-engineering", title="RAG", resources=[])

    store.add_finding("rag", "first finding")
    topic = store.add_finding("rag", "second finding")

    assert topic.findings == ("first finding", "second finding")


def test_query_by_category_only_returns_matching_topics(store: InMemoryStore):
    store.create_topic(topic_id="rag", category="ai-llm-engineering", title="RAG", resources=[])
    store.create_topic(
        topic_id="docker", category="platform-infra-devops", title="Docker", resources=[]
    )

    [topic] = store.query_by_category("ai-llm-engineering")
    assert topic.topic_id == "rag"


def test_phase_defaults_to_learning(store: InMemoryStore):
    assert store.get_phase() == Phase.LEARNING


def test_set_phase_changes_what_get_phase_returns(store: InMemoryStore):
    store.set_phase(Phase.RUNTIME)

    assert store.get_phase() == Phase.RUNTIME


def test_new_topic_does_not_need_better_sources_by_default(store: InMemoryStore):
    store.create_topic(topic_id="rag", category="ai-llm-engineering", title="RAG", resources=[])

    topic = store.get_topic("rag")
    assert topic.needs_better_sources is False


def test_flag_needs_better_sources_sets_the_flag_without_changing_status(store: InMemoryStore):
    store.create_topic(topic_id="rag", category="ai-llm-engineering", title="RAG", resources=[])

    topic = store.flag_needs_better_sources("rag")

    assert topic.needs_better_sources is True
    assert topic.status == TopicStatus.NEEDS_RESEARCH


def test_post_category_rollup_is_recorded_for_that_category(store: InMemoryStore):
    store.post_category_rollup("ai-llm-engineering", "1/3 topics researched")

    assert store.posted_rollups["ai-llm-engineering"] == ["1/3 topics researched"]


def test_post_category_rollup_keeps_history_per_category(store: InMemoryStore):
    store.post_category_rollup("ai-llm-engineering", "0/3 topics researched")
    store.post_category_rollup("ai-llm-engineering", "1/3 topics researched")

    assert store.posted_rollups["ai-llm-engineering"] == [
        "0/3 topics researched",
        "1/3 topics researched",
    ]


def test_operating_on_an_unknown_topic_id_raises(store: InMemoryStore):
    with pytest.raises(ValueError):
        store.update_status("does-not-exist", TopicStatus.RESEARCHED)

    with pytest.raises(ValueError):
        store.add_finding("does-not-exist", "finding")
