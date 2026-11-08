import json
import urllib.error
from unittest.mock import patch

import pytest

from cimcime.approval_gate import ActionType
from cimcime.cli import run
from cimcime.delegation import (
    Backend,
    BackendUnavailable,
    DelegationLog,
    DelegationNotAllowed,
    delegate_summarize,
    log_external_delegation,
    summarize_with_qwen,
)
from cimcime.state_store import InMemoryStore


class _FakeResponse:
    def __init__(self, payload: dict):
        self._body = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _ok_response(text: str):
    return _FakeResponse({"choices": [{"message": {"content": text}}]})


# --- summarize_with_qwen (HTTP layer) ---------------------------------------------

def test_summarize_with_qwen_returns_the_models_text():
    with patch("urllib.request.urlopen", return_value=_ok_response("short summary")) as mock_urlopen:
        result = summarize_with_qwen("a very long tool output", base_url="http://127.0.0.1:8090")

    assert result == "short summary"
    sent = json.loads(mock_urlopen.call_args[0][0].data)
    assert sent["chat_template_kwargs"] == {"enable_thinking": False}
    assert sent["messages"][-1] == {"role": "user", "content": "a very long tool output"}


def test_summarize_with_qwen_raises_backend_unavailable_when_unreachable():
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("connection refused")):
        with pytest.raises(BackendUnavailable):
            summarize_with_qwen("text", base_url="http://127.0.0.1:8090")


# --- DelegationLog -----------------------------------------------------------------

def test_delegation_log_records_round_trip(tmp_path):
    log = DelegationLog(tmp_path / "delegations.db")

    log.record("summarize", Backend.QWEN_LOCAL, "ok")

    [entry] = log.recent()
    assert entry["task_type"] == "summarize"
    assert entry["backend"] == "qwen_local"
    assert entry["outcome"] == "ok"


def test_delegation_log_recent_is_newest_first(tmp_path):
    log = DelegationLog(tmp_path / "delegations.db")
    log.record("summarize", Backend.QWEN_LOCAL, "ok", detail="first")
    log.record("summarize", Backend.HAIKU, "ok", detail="second")

    entries = log.recent()

    assert [e["detail"] for e in entries] == ["second", "first"]


def test_delegation_log_survives_reopening_the_database(tmp_path):
    DelegationLog(tmp_path / "delegations.db").record("summarize", Backend.QWEN_LOCAL, "ok")

    entries = DelegationLog(tmp_path / "delegations.db").recent()

    assert len(entries) == 1


# --- delegate_summarize (the hard rule + logging) -----------------------------------

def test_delegate_summarize_refuses_a_gated_action_without_calling_the_backend(tmp_path):
    log = DelegationLog(tmp_path / "delegations.db")

    with patch("cimcime.delegation.summarize_with_qwen") as mock_summarize:
        with pytest.raises(DelegationNotAllowed):
            delegate_summarize("text", log=log, action_type=ActionType.PRODUCTION_DEPLOY)

    mock_summarize.assert_not_called()
    [entry] = log.recent()
    assert entry["outcome"] == "refused_gated_action"


def test_delegate_summarize_logs_and_returns_on_success(tmp_path):
    log = DelegationLog(tmp_path / "delegations.db")

    with patch("cimcime.delegation.summarize_with_qwen", return_value="summary text"):
        result = delegate_summarize("text", log=log)

    assert result == "summary text"
    [entry] = log.recent()
    assert entry["backend"] == "qwen_local"
    assert entry["outcome"] == "ok"


def test_delegate_summarize_logs_and_reraises_on_backend_failure(tmp_path):
    log = DelegationLog(tmp_path / "delegations.db")

    with patch("cimcime.delegation.summarize_with_qwen", side_effect=BackendUnavailable("down")):
        with pytest.raises(BackendUnavailable):
            delegate_summarize("text", log=log)

    [entry] = log.recent()
    assert entry["outcome"] == "backend_unavailable"


def test_delegate_summarize_defaults_to_routine_work_which_is_allowed(tmp_path):
    log = DelegationLog(tmp_path / "delegations.db")

    with patch("cimcime.delegation.summarize_with_qwen", return_value="ok"):
        delegate_summarize("text", log=log)  # no action_type passed, must not raise


# --- log_external_delegation (Haiku/Sonnet, routed via the Agent tool itself) -------

def test_log_external_delegation_records_the_backend_used(tmp_path):
    log = DelegationLog(tmp_path / "delegations.db")

    log_external_delegation(log, Backend.HAIKU)

    [entry] = log.recent()
    assert entry["backend"] == "haiku"
    assert entry["outcome"] == "ok"


# --- CLI round-trips -----------------------------------------------------------------

def test_cli_delegate_summarize_round_trips(tmp_path, monkeypatch):
    monkeypatch.setenv("CIMCIME_DELEGATION_LOG", str(tmp_path / "delegations.db"))
    store = InMemoryStore()

    with patch("cimcime.delegation.summarize_with_qwen", return_value="cli summary"):
        output = run(["delegate-summarize", "some tool output"], store)

    assert json.loads(output) == {"summary": "cli summary"}


def test_cli_delegate_summarize_refuses_a_gated_action(tmp_path, monkeypatch):
    monkeypatch.setenv("CIMCIME_DELEGATION_LOG", str(tmp_path / "delegations.db"))
    store = InMemoryStore()

    with pytest.raises(DelegationNotAllowed):
        run(["delegate-summarize", "x", "--action-type", "production_deploy"], store)


def test_cli_log_delegation_then_recent_delegations_round_trips(tmp_path, monkeypatch):
    monkeypatch.setenv("CIMCIME_DELEGATION_LOG", str(tmp_path / "delegations.db"))
    store = InMemoryStore()

    run(["log-delegation", "haiku", "--detail", "classified a message"], store)
    result = json.loads(run(["recent-delegations"], store))

    assert [d["detail"] for d in result["delegations"]] == ["classified a message"]
