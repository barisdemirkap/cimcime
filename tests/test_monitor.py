import json
from datetime import datetime, timezone

from cimcime import monitor


def _ev(ts, content):
    return json.dumps({"type": "assistant", "timestamp": ts, "message": {"content": content}})


def test_parse_transcript_finds_running_tool(tmp_path):
    f = tmp_path / "s.jsonl"
    f.write_text("\n".join([
        _ev("2026-11-11T10:00:00Z", [{"type": "tool_use", "id": "a", "name": "Bash", "input": {"command": "ls"}}]),
        _ev("2026-11-11T10:00:01Z", [{"type": "tool_result", "tool_use_id": "a"}]),
        _ev("2026-11-11T10:00:02Z", [{"type": "tool_use", "id": "b", "name": "Agent",
                                      "input": {"subagent_type": "board", "description": "audit"}}]),
        json.dumps({"type": "api-request-blob", "message": {"content": [
            {"type": "tool_use", "id": "a", "name": "Bash", "input": {}}]}}),
        "not json",
    ]))
    info = monitor.parse_transcript(f)
    assert [d for _, d in info["running"]] == ["Agent board: audit"]
    assert len(info["trail"]) == 2 and info["last_event"] == "2026-11-11T10:00:02Z"


def test_age_formats():
    now = datetime(2026, 11, 11, 10, 10, tzinfo=timezone.utc)
    assert monitor._age("2026-11-11T10:09:30Z", now) == "30s ago"
    assert monitor._age("2026-11-11T10:00:00Z", now) == "10m ago"
