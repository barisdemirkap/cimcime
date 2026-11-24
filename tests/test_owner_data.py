import json
import stat

from cimcime.decision_log import DecisionLog
from cimcime.message_log import Direction, MessageLog
from cimcime.owner_data import delete_data, export_data


def _db(tmp_path):
    db = tmp_path / "m.db"
    m = MessageLog(db)
    m.log("1", Direction.INBOUND, "hello", "1", "2026-01-01T00:00:00Z")
    m.log("2", Direction.INBOUND, "other", "1", "2026-01-01T00:00:00Z")
    DecisionLog(db).log("p", "d")
    return db


def test_export_is_private(tmp_path):
    db = _db(tmp_path)
    out = tmp_path / "out.json"
    r = export_data(out, db)
    assert r["exported"] == {"messages": 2, "decisions": 1}
    assert stat.S_IMODE(out.stat().st_mode) == 0o600
    assert json.loads(out.read_text())["messages"][0]["text"] == "hello"


def test_delete_needs_confirm_and_is_scoped(tmp_path):
    db = _db(tmp_path)
    assert not delete_data("1", db=db)["deleted"]
    assert delete_data("1", confirm=True, db=db)["counts"] == {"messages": 1}
    assert export_data(tmp_path / "o.json", db)["exported"]["messages"] == 1
