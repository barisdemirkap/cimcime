import json

from cimcime.cli import run
from cimcime.message_log import Direction, MessageLog
from cimcime.state_store import InMemoryStore


def test_recent_returns_the_conversation_oldest_first(tmp_path):
    log = MessageLog(tmp_path / "messages.db")
    log.log("1", Direction.INBOUND, "onay veriyorum", message_id="28")
    log.log("1", Direction.OUTBOUND, "Neyi onayladin?", message_id="29")

    texts = [m.text for m in log.recent("1")]

    assert texts == ["onay veriyorum", "Neyi onayladin?"]


def test_logging_the_same_telegram_message_twice_keeps_one_row(tmp_path):
    log = MessageLog(tmp_path / "messages.db")
    log.log("1", Direction.INBOUND, "hello", message_id="28")
    log.log("1", Direction.INBOUND, "hello", message_id="28")

    assert len(log.recent("1")) == 1


def test_log_survives_reopening_the_database(tmp_path):
    MessageLog(tmp_path / "messages.db").log("1", Direction.INBOUND, "kalici", message_id="1")

    assert [m.text for m in MessageLog(tmp_path / "messages.db").recent("1")] == ["kalici"]


def test_recent_limit_keeps_only_the_latest_messages(tmp_path):
    log = MessageLog(tmp_path / "messages.db")
    for i in range(5):
        log.log("1", Direction.INBOUND, f"m{i}", message_id=str(i))

    assert [m.text for m in log.recent("1", limit=2)] == ["m3", "m4"]


def test_cli_log_then_recent_round_trips(tmp_path, monkeypatch):
    monkeypatch.setenv("CIMCIME_MESSAGE_LOG", str(tmp_path / "messages.db"))
    store = InMemoryStore()

    run(["log-message", "1", "inbound", "hmm bu bir bug", "--message-id", "30"], store)
    result = json.loads(run(["recent-messages", "1"], store))

    assert [m["text"] for m in result["messages"]] == ["hmm bu bir bug"]
