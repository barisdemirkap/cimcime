from pathlib import Path

from cimcime.roadmap import DEFAULT_RESEARCH_DOC_PATH, expected_topic_counts, expected_topics, topic_entries

RESEARCH_DOC = (
    Path(__file__).parent.parent / "docs" / "research" / "forward-deployed-engineer-roadmap.md"
)


def test_default_path_points_at_the_real_research_doc():
    assert DEFAULT_RESEARCH_DOC_PATH == RESEARCH_DOC
    assert DEFAULT_RESEARCH_DOC_PATH.exists()


def test_expected_counts_sum_to_97_real_topics():
    counts = expected_topic_counts(RESEARCH_DOC)

    assert sum(counts.values()) == 97


def test_ai_llm_engineering_has_19_topics():
    counts = expected_topic_counts(RESEARCH_DOC)

    assert counts["ai-llm-engineering"] == 19


def test_documentation_folds_into_client_engagement_delivery():
    counts = expected_topic_counts(RESEARCH_DOC)

    # 10 Client Engagement & Delivery topics + 1 Documentation (Technical Writing) topic
    assert counts["client-engagement-delivery"] == 11


def test_gaps_and_notes_section_is_not_counted_as_topics():
    counts = expected_topic_counts(RESEARCH_DOC)

    assert "gaps" not in counts
    assert "notes" not in counts


def test_expected_topics_gives_slugified_ids_matching_counts():
    topics = expected_topics(RESEARCH_DOC)

    assert len(topics["ai-llm-engineering"]) == 19
    assert "rags" in topics["ai-llm-engineering"]
    assert "mcp" in topics["ai-llm-engineering"]
    assert "multi-agents" in topics["ai-llm-engineering"]


def test_expected_topics_counts_and_expected_topic_counts_agree():
    topics = expected_topics(RESEARCH_DOC)
    counts = expected_topic_counts(RESEARCH_DOC)

    assert {category: len(ids) for category, ids in topics.items()} == counts


def test_time_to_value_slug_matches_the_already_created_real_topic():
    topics = expected_topics(RESEARCH_DOC)

    assert "time-to-value" in topics["business-strategy"]


def test_topic_entries_returns_97_entries_with_titles_and_resources():
    entries = topic_entries(RESEARCH_DOC)

    assert len(entries) == 97
    rags = next(e for e in entries if e.topic_id == "rags")
    assert rags.title == "RAGs"
    assert rags.category == "ai-llm-engineering"
    assert rags.resources == (
        "https://cloud.google.com/use-cases/retrieval-augmented-generation",
        "https://towardsdatascience.com/rag-explained-understanding-embeddings-similarity-and-retrieval/",
        "https://www.youtube.com/watch?v=T-D1OfcDW1M",
    )


def test_topic_entries_handles_a_topic_with_no_resources():
    entries = topic_entries(RESEARCH_DOC)

    managed_ml = next(e for e in entries if e.topic_id == "managed-ml-services")
    assert managed_ml.resources == ()


def test_topic_entries_agrees_with_expected_topics():
    entries = topic_entries(RESEARCH_DOC)
    topics = expected_topics(RESEARCH_DOC)

    by_category: dict[str, set[str]] = {}
    for entry in entries:
        by_category.setdefault(entry.category, set()).add(entry.topic_id)

    assert by_category == topics


def test_no_research_doc_has_an_unmapped_category_heading():
    from cimcime.roadmap import EXTENSION_RESEARCH_DOC_PATHS, unmapped_category_headings

    for doc in (RESEARCH_DOC, *EXTENSION_RESEARCH_DOC_PATHS):
        assert unmapped_category_headings(doc) == [], doc


def test_iot_extension_doc_yields_nine_topics_in_its_own_category():
    from cimcime.roadmap import EXTENSION_RESEARCH_DOC_PATHS

    entries = topic_entries(EXTENSION_RESEARCH_DOC_PATHS[0])

    assert len(entries) == 9
    assert {e.category for e in entries} == {"iot-electronics"}
    assert all(e.resources for e in entries)
