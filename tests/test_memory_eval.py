"""Memory eval harness (ADR-0017): metrics, paired bootstrap, fixture validation and pinning,
degraded-mode reporting, the slice-4 search refinements, and the CLI.

Hermetic and synthetic: the only fixture is tests/fixtures/memory_eval/synthetic-v1.json (invented
greenhouse chatter), no network, no model."""

import json
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pytest

from cimcime import cli, memory_eval as ev
from cimcime.memory import Memory

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "memory_eval" / "synthetic-v1.json"
CONFIG = ROOT / "docs" / "memory-eval" / "thresholds.toml"


# --- metrics ------------------------------------------------------------------------------------


def test_recall_mrr_ndcg_known_values():
    ranked = ["x", "a", "y", "b", "z"]
    gold = {"a", "b"}
    assert ev.recall_at_k(ranked, gold, 2) == 0.5
    assert ev.recall_at_k(ranked, gold, 5) == 1.0
    assert ev.reciprocal_rank(ranked, gold) == 0.5
    expected = (1 / math.log2(3) + 1 / math.log2(5)) / (1 / math.log2(2) + 1 / math.log2(3))
    assert ev.ndcg_at_k(ranked, gold, 5) == pytest.approx(expected)
    assert ev.ndcg_at_k(["a", "b"], gold, 5) == pytest.approx(1.0)
    assert ev.recall_at_k([], gold, 5) == ev.reciprocal_rank(["q"], gold) == ev.ndcg_at_k([], gold, 5) == 0.0


def test_duplicates_in_a_ranking_do_not_inflate_scores():
    assert ev.recall_at_k(["a", "a", "a", "b"], {"a", "b"}, 2) == 1.0  # dedup: a, b are the top 2
    assert ev.ndcg_at_k(["a", "a", "b"], {"a", "b"}, 3) == pytest.approx(1.0)


def test_latest_above_superseded():
    assert ev.latest_above_superseded(["new", "old"], {"new"}, {"old"}) == 1.0
    assert ev.latest_above_superseded(["old", "new"], {"new"}, {"old"}) == 0.0
    assert ev.latest_above_superseded(["new"], {"new"}, {"old"}) == 1.0
    assert ev.latest_above_superseded(["old"], {"new"}, {"old"}) == 0.0


# --- bootstrap ----------------------------------------------------------------------------------


def test_paired_bootstrap_is_seeded_and_brackets_the_delta():
    a = [0.0] * 10 + [1.0] * 10
    b = [1.0] * 10 + [1.0] * 10
    r1 = ev.paired_bootstrap(a, b, 1000, seed=7, level=0.95)
    assert r1 == ev.paired_bootstrap(a, b, 1000, seed=7, level=0.95)
    assert r1["delta"] == pytest.approx(0.5)
    assert r1["ci_low"] <= 0.5 <= r1["ci_high"] and r1["ci_low"] > 0.0


def test_paired_bootstrap_of_identical_samples_is_exactly_zero():
    r = ev.paired_bootstrap([0.2, 0.9, 0.5], [0.2, 0.9, 0.5], 500, seed=1, level=0.95)
    assert (r["delta"], r["ci_low"], r["ci_high"]) == (0.0, 0.0, 0.0)


def test_paired_bootstrap_rejects_unpaired_samples_and_handles_empty():
    with pytest.raises(ValueError):
        ev.paired_bootstrap([1.0], [1.0, 0.0], 10, 1, 0.95)
    assert ev.paired_bootstrap([], [], 10, 1, 0.95)["delta"] is None


# --- fixture ------------------------------------------------------------------------------------


def _fixture_data():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_repo_fixture_is_valid_synthetic_pinned_and_covers_every_category():
    data = _fixture_data()
    assert ev.validate_fixture(data) == []
    assert data["synthetic"] is True and all(d["provenance"] == "synthetic" for d in data["docs"])
    assert {q["category"] for q in data["questions"]} == set(ev.CATEGORIES)
    assert ev.sha256_file(FIXTURE) == ev.load_config(CONFIG)["fixtures"]["synthetic-v1.json"]


def test_validator_names_every_kind_of_problem():
    data = _fixture_data()
    data["questions"][0]["gold"] = ["messages:99999"]
    data["questions"].append({"id": "qx", "category": "abstention", "query": "q", "gold": ["messages:101"]})
    data["questions"].append({"id": "qy", "category": "extraction", "query": "q", "gold": []})
    data["docs"].append({**data["docs"][0], "id": "9999", "scope": "camondo"})
    data["docs"].append({**data["docs"][1], "id": "9998", "provenance": "real"})
    joined = " | ".join(ev.validate_fixture(data))
    for needle in ("unknown row id messages:99999", "abstention questions have no gold", "sensitive scope",
                   "provenance 'synthetic'"):
        assert needle in joined
    assert "qy" in joined


def test_tampered_fixture_fails_the_manifest_check(tmp_path):
    copy = tmp_path / "synthetic-v1.json"
    shutil.copy(FIXTURE, copy)
    copy.write_text(copy.read_text(encoding="utf-8").replace("propagation cable", "propagation wire"), encoding="utf-8")
    with pytest.raises(ev.ManifestError):
        ev.evaluate(copy, CONFIG)


def test_malformed_fixture_is_rejected_before_any_run(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"format": 1, "now": "2026-11-01T00:00:00+00:00", "docs": [], "questions": [
        {"id": "q1", "category": "extraction", "query": "x", "gold": ["messages:1"]}]}))
    with pytest.raises(ev.FixtureError):
        ev.evaluate(bad, CONFIG)


# --- evaluation ---------------------------------------------------------------------------------


def test_keyword_only_run_skips_hybrid_and_reports_every_category():
    report = ev.evaluate(FIXTURE, CONFIG, embedder="none")
    assert report["variants"]["hybrid"]["skipped"]
    gates = {g["id"]: g for g in report["gates"]}
    assert gates["adr-e-hybrid-vs-fts5"]["status"] == "skipped"
    keyword = report["variants"]["keyword"]
    assert set(keyword["by_category"]) == set(ev.CATEGORIES)
    assert keyword["modes"] == {"keyword": 41} and keyword["degraded_rate"] == 0.0
    assert 0.0 <= report["brief"]["absent_rate"] <= 1.0 and report["brief"]["hit_rate"] is not None
    assert report["fixture"]["pinned"] is True


def test_report_is_deterministic():
    one = json.dumps(ev.evaluate(FIXTURE, CONFIG, embedder="hash"), sort_keys=True)
    two = json.dumps(ev.evaluate(FIXTURE, CONFIG, embedder="hash"), sort_keys=True)
    assert one == two


def test_hybrid_with_the_stand_in_embedder_runs_in_hybrid_mode():
    report = ev.evaluate(FIXTURE, CONFIG, embedder="hash")
    assert report["variants"]["hybrid"]["modes"] == {"hybrid": 41}
    assert report["variants"]["hybrid"]["degraded_rate"] == 0.0


def test_an_embedding_outage_is_reported_as_degraded_and_fails_the_hybrid_gate():
    report = ev.evaluate(FIXTURE, CONFIG, embedder="unavailable")
    hybrid = report["variants"]["hybrid"]
    assert hybrid["degraded_rate"] == 1.0 and hybrid["modes"] == {"keyword": 41}
    gate = {g["id"]: g for g in report["gates"]}["adr-e-hybrid-vs-fts5"]
    assert gate["status"] == "fail" and any("degraded" in r for r in gate["reasons"])
    assert report["ok"] is False


def test_slice4_abstention_is_measurable_on_the_fixture():
    report = ev.evaluate(FIXTURE, CONFIG)
    gates = {g["id"]: g for g in report["gates"]}
    assert gates["abstain-detects-absence"]["status"] == "pass"
    assert gates["abstain-keeps-answers"]["status"] == "pass"
    assert report["variants"]["keyword"]["overall"]["abstention_recall"]["mean"] < 0.5
    assert report["variants"]["abstain"]["overall"]["abstention_recall"]["mean"] == 1.0


def test_markdown_report_has_the_required_sections():
    text = ev.render_markdown(ev.evaluate(FIXTURE, CONFIG, embedder="hash"))
    for needle in ("fixture sha256", "brief: absent", "degraded", "Per category", "Pre-registered gates", "recall@5"):
        assert needle in text


# --- slice 4 on Memory --------------------------------------------------------------------------

NOW = datetime(2026, 11, 1, tzinfo=timezone.utc)


@pytest.fixture
def mem(tmp_path):
    m = Memory(tmp_path / "m.db", now=lambda: NOW)
    rows = [
        ("cimcime", "messages", "1", "2026-10-01T10:00:00+00:00", "Planning the pump replacement for the cellar", "owner"),
        ("cimcime", "messages", "2", "2026-10-01T10:01:00+00:00", "Bought model PX-9 from the depot", "owner"),
        ("cimcime", "messages", "3", "2026-10-01T10:02:00+00:00", "Unrelated note about window cleaning", "owner"),
        ("camondo", "messages", "4", "2026-10-01T10:03:00+00:00", "Private neighbour note about the cellar", "owner"),
        ("cimcime", "decisions", "7", "2026-09-01T10:00:00+00:00", "The deploy window is Friday afternoon only", "owner"),
        ("cimcime", "decisions", "8", "2026-10-20T10:00:00+00:00", "The deploy window is Friday afternoon only, changed after incident", "owner"),
    ]
    for r in rows:
        m.add_row(*r)
    return m


def test_defaults_are_unchanged(mem):
    res = mem.search("pump replacement cellar")
    assert res.evidence and not any(h.expanded for h in res.hits) and res.hits[0].source_id == "1"


def test_abstain_when_the_best_hit_covers_too_little_of_the_query(mem):
    weak = mem.search("quantum flux capacitor in the cellar", abstain_min_coverage=0.5)
    assert weak.evidence is False and weak.hits == [] and weak.note.startswith("no evidence")
    strong = mem.search("pump replacement cellar", abstain_min_coverage=0.5)
    assert strong.evidence and strong.hits


def test_abstain_with_no_matches_at_all(mem):
    res = mem.search("zzzz qqqq", abstain_min_coverage=0.5)
    assert res.evidence is False


def test_neighbour_expansion_appends_flagged_adjacent_messages(mem):
    res = mem.search("pump replacement cellar", neighbours=1)
    primary = [h.source_id for h in res.hits if not h.expanded]
    assert primary[0] == "1"
    expanded = [h.source_id for h in res.hits if h.expanded]
    assert "2" in expanded and "2" not in primary
    assert all(h.score == 0.0 for h in res.hits if h.expanded)
    assert [h.source_id for h in res.hits][: len(primary)] == primary  # ranking untouched


def test_neighbour_expansion_never_crosses_scope_or_table(mem):
    res = mem.search("window cleaning", neighbours=3)
    assert "4" not in [h.source_id for h in res.hits]  # camondo row next to row 3
    assert all(h.scope == "cimcime" for h in res.hits)
    assert all(h.source_table == "messages" for h in res.hits if h.expanded)


def test_neighbour_expansion_is_bounded(tmp_path):
    m = Memory(tmp_path / "b.db", now=lambda: NOW)
    for i in range(60):
        m.add_row("cimcime", "messages", str(i), "2026-10-01T10:00:00+00:00", f"pump note {i}", "owner")
    res = m.search("pump", k=10, neighbours=5)
    assert len(res.hits) <= 10 + 20


def test_recency_breaks_near_ties_towards_the_newer_row(mem):
    assert mem.search("deploy window friday afternoon", k=2).hits[0].source_id == "7"  # shorter text scores higher
    res = mem.search("deploy window friday afternoon", k=2, recency_tolerance=0.5)
    assert res.hits[0].source_id == "8"


def test_recency_does_not_promote_a_clearly_worse_match(mem):
    res = mem.search("pump replacement cellar", k=5, recency_tolerance=0.05)
    assert res.hits[0].source_id == "1"


# --- CLI ----------------------------------------------------------------------------------------


def _mini(tmp_path, tamper=False):
    docs = [{"table": "messages", "id": str(i), "at": "2026-10-01T10:00:00+00:00", "scope": "demo", "trust": "owner",
             "text": t, "provenance": "synthetic"} for i, t in enumerate(
                 ["alpha beam setting is seven", "gamma ray log rotates daily", "delta note about the weather"], start=1)]
    fx = {"format": 1, "name": "mini", "synthetic": True, "now": "2026-11-01T00:00:00+00:00", "docs": docs,
          "questions": [{"id": "q1", "category": "extraction", "query": "alpha beam setting", "gold": ["messages:1"], "scope": "demo"},
                        {"id": "q2", "category": "abstention", "query": "volcano submarine harbour", "scope": "demo"}]}
    path = tmp_path / "mini.json"
    path.write_text(json.dumps(fx), encoding="utf-8")
    digest = "0" * 64 if tamper else ev.sha256_file(path)
    cfg = tmp_path / "cfg.toml"
    cfg.write_text(f'[run]\nseed = 1\nbootstrap_resamples = 50\n[fixtures]\n"mini.json" = "{digest}"\n'
                   '[variants.keyword]\nmode = "keyword"\n[[gates]]\nid = "floor"\ncandidate = "keyword"\n'
                   'metric = "recall@5"\nmin = 0.9\n')
    return path, cfg


def test_cli_eval_memory_writes_reports_and_exits_zero(tmp_path, capsys):
    fx, cfg = _mini(tmp_path)
    out = tmp_path / "out"
    code = cli._local_command(["eval-memory", "--fixture", str(fx), "--config", str(cfg), "--out-dir", str(out)])
    assert code == 0
    assert "Pre-registered gates" in capsys.readouterr().out
    assert json.loads((out / "report.json").read_text())["ok"] is True and (out / "report.md").exists()


def test_cli_eval_memory_exits_one_on_a_failed_gate_and_two_on_tampering(tmp_path, capsys):
    fx, cfg = _mini(tmp_path)
    cfg.write_text(cfg.read_text().replace("min = 0.9", "min = 1.5"))
    assert cli._local_command(["eval-memory", "--fixture", str(fx), "--config", str(cfg), "--json"]) == 1
    capsys.readouterr()
    fx2, cfg2 = _mini(tmp_path, tamper=True)
    assert cli._local_command(["eval-memory", "--fixture", str(fx2), "--config", str(cfg2)]) == 2
    assert "ManifestError" in capsys.readouterr().err
