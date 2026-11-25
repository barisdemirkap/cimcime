"""Candidate-question drafter (ADR-0017): drafts from raw rows only, skips sensitive rows, and never
writes into a git work tree. Synthetic message logs only."""

import json
import stat
import subprocess
import sys
from pathlib import Path

import pytest

from cimcime import memory_eval_draft as draft
from cimcime.decision_log import DecisionLog
from cimcime.message_log import Direction, MessageLog

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def source(tmp_path):
    path = tmp_path / "messages.db"
    m, d = MessageLog(path), DecisionLog(path)
    m.log("1", Direction.INBOUND, "From now on always label trays with the green marker", message_id="1",
          sent_at="2026-10-01T10:00:00+00:00")
    m.log("1", Direction.INBOUND, "Camondo rent is due on the fifth", message_id="2", sent_at="2026-10-02T10:00:00+00:00")
    m.log("1", Direction.OUTBOUND, "Noted the marker rule", message_id="3", sent_at="2026-10-01T10:01:00+00:00")
    d.log("cimcime", "Watering schedule is every six hours in summer", "", decided_at="2026-09-01T00:00:00+00:00")
    d.log("cimcime", "Watering schedule is every four hours in summer", "after audit", decided_at="2026-09-10T00:00:00+00:00")
    d.log("cimcime", "Watering schedule is every three hours in summer", "heat wave", decided_at="2026-09-20T00:00:00+00:00")
    d.log("camondo", "Budget cap for the flat", "", decided_at="2026-09-05T00:00:00+00:00")
    d.log("cimcime", "Licence is MIT", "owner chose permissive", decided_at="2026-09-06T00:00:00+00:00")
    return path


def test_drafts_each_category_from_raw_rows(source):
    doc = draft.draft_candidates(source)
    cats = {c["category"] for c in doc["candidates"]}
    assert {"extraction", "preference", "knowledge-update", "temporal", "abstention"} <= cats
    ku = next(c for c in doc["candidates"] if c["category"] == "knowledge-update")
    assert len(ku["gold"]) == 1 and len(ku["superseded"]) == 2
    assert all(c["status"] == "draft" and c["owner_decision"] is None for c in doc["candidates"])
    assert all(c["gold"] == [] for c in doc["candidates"] if c["category"] == "abstention")
    assert [c["id"] for c in doc["candidates"]] == [f"c{i:03d}" for i in range(1, len(doc["candidates"]) + 1)]


def test_sensitive_rows_never_appear(source):
    blob = json.dumps(draft.draft_candidates(source)).lower()
    assert "camondo" not in blob and "flat" not in blob and "rent" not in blob


def test_drafting_is_deterministic(source):
    a = draft.draft_candidates(source)
    b = draft.draft_candidates(source)
    a.pop("generated_at"), b.pop("generated_at")
    assert a == b


def test_abstention_probes_are_absent_from_the_corpus(source):
    for c in draft.draft_candidates(source)["candidates"]:
        if c["category"] == "abstention":
            assert "watering" not in c["query"]


def test_review_files_are_private_and_outside_the_repo(source, tmp_path):
    out = tmp_path / "state" / "eval-candidates"
    paths = draft.write_review(draft.draft_candidates(source), out)
    assert {p.suffix for p in paths} == {".json", ".md"}
    assert all(stat.S_IMODE(p.stat().st_mode) == 0o600 for p in paths)
    assert stat.S_IMODE(out.stat().st_mode) == 0o700


def test_refuses_to_write_inside_a_git_work_tree(source):
    with pytest.raises(draft.UnsafeOutputPath):
        draft.write_review(draft.draft_candidates(source), ROOT / "tests" / "leak")
    assert not (ROOT / "tests" / "leak").exists()


def test_default_output_directory_is_under_the_state_dir():
    assert str(draft.DEFAULT_OUT_DIR).endswith(".local/state/cimcime/eval-candidates")


def test_script_runs_and_refuses_repo_paths(source, tmp_path):
    script = ROOT / "scripts" / "draft_eval_candidates.py"
    ok = subprocess.run([sys.executable, str(script), "--source", str(source), "--out-dir", str(tmp_path / "o")],
                        capture_output=True, text=True)
    assert ok.returncode == 0 and "draft candidates" in ok.stdout
    bad = subprocess.run([sys.executable, str(script), "--source", str(source), "--out-dir", str(ROOT / "docs" / "x")],
                         capture_output=True, text=True)
    assert bad.returncode == 2 and "refused" in bad.stderr
