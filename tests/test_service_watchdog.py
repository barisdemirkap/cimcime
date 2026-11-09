import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cimcime import service, watchdog


def _spec():
    return service.Spec(Path("/work"), "/bin/claude", "/bin/cimcime", "/bin:/usr/bin", Path("/logs"))


def test_launchd_plists_are_wellformed():
    import xml.dom.minidom as md

    md.parseString(service.render_launchd_channel(_spec()))
    md.parseString(service.render_launchd_watchdog(_spec()))


def test_channel_uses_pty_wrapper():
    assert "script -q /dev/null" in service.channel_shell_command(_spec(), "darwin")
    assert "script -qfec" in service.channel_shell_command(_spec(), "linux")


def test_systemd_units_reference_commands():
    assert "ExecStart=/bin/cimcime watchdog" in service.render_systemd_watchdog_service(_spec())
    assert "Restart=always" in service.render_systemd_channel(_spec())


def test_decide_once_per_message():
    assert watchdog.decide(5, "1", {}) == (False, False)
    assert watchdog.decide(10, "1", {}) == (True, False)
    assert watchdog.decide(25, "1", {"notified": "1"}) == (False, True)
    assert watchdog.decide(25, "1", {"notified": "1", "restarted": "1"}) == (False, False)


def test_oldest_unanswered(tmp_path):
    db = tmp_path / "m.db"
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id TEXT, direction TEXT, message_id TEXT, sent_at TEXT, text TEXT)")
    now = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    def add(d, mins):
        c.execute("INSERT INTO messages (chat_id,direction,sent_at,text) VALUES ('7',?,?,'x')", (d, (now - timedelta(minutes=mins)).isoformat()))
    add("inbound", 50); add("outbound", 40); add("inbound", 15)
    c.commit(); c.close()
    un = watchdog.oldest_unanswered(db, now)
    assert un and un.chat_id == "7" and un.age_min == 15
    assert watchdog.oldest_unanswered(tmp_path / "none.db", now) is None
