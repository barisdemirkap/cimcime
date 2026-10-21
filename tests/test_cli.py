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
