import json

import pytest

from cimcime.cli import run
from cimcime.state_store import InMemoryStore


@pytest.fixture
def store() -> InMemoryStore:
    store = InMemoryStore()
    store.create_topic(
        topic_id="rag",
        category="ai-llm-engineering",
        title="RAG",
        resources=["https://example.com/rag-article"],
    )
    return store


def test_get_topic_prints_the_current_record_as_json(store: InMemoryStore):
    output = run(["get-topic", "rag"], store)

    record = json.loads(output)
    assert record["topic_id"] == "rag"
    assert record["category"] == "ai-llm-engineering"
    assert record["status"] == "needs_research"
    assert record["resources"] == ["https://example.com/rag-article"]
    assert record["findings"] == []


def test_get_topic_on_an_unknown_topic_raises(store: InMemoryStore):
    with pytest.raises(ValueError):
        run(["get-topic", "does-not-exist"], store)


def test_update_status_changes_the_topic_status(store: InMemoryStore):
    output = run(["update-status", "rag", "researched"], store)

    assert json.loads(output)["status"] == "researched"


def test_add_finding_appends_to_the_topic_findings(store: InMemoryStore):
    output = run(["add-finding", "rag", "a real finding"], store)

    assert json.loads(output)["findings"] == ["a real finding"]


def test_category_status_tallies_without_posting_anything(store: InMemoryStore):
    store.create_topic(topic_id="mcp", category="ai-llm-engineering", title="MCP", resources=[])
    run(["update-status", "rag", "researched"], store)

    output = run(["category-status", "ai-llm-engineering"], store)

    result = json.loads(output)
    assert result["category"] == "ai-llm-engineering"
    assert result["total"] == 2
    assert result["researched"] == 1
    assert "ai-llm-engineering" not in store.posted_rollups


def test_category_status_on_a_category_with_no_topics_yet(store: InMemoryStore):
    output = run(["category-status", "platform-infra-devops"], store)

    result = json.loads(output)
    assert result["total"] == 0
    assert result["researched"] == 0


def test_category_rollup_posts_the_same_summary_category_status_would_report(
    store: InMemoryStore,
):
    store.create_topic(topic_id="mcp", category="ai-llm-engineering", title="MCP", resources=[])
    run(["update-status", "rag", "researched"], store)

    status_result = json.loads(run(["category-status", "ai-llm-engineering"], store))
    rollup_result = json.loads(run(["category-rollup", "ai-llm-engineering"], store))

    assert rollup_result == status_result
    assert store.posted_rollups["ai-llm-engineering"] == [status_result["summary"]]
