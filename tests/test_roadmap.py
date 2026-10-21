from pathlib import Path

from cimcime.roadmap import DEFAULT_RESEARCH_DOC_PATH, expected_topic_counts, expected_topics

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
