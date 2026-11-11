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
    assert watchdog.decide(25, "1", {"notified": "1"}, "idle") == (False, True)
    assert watchdog.decide(25, "1", {"notified": "1", "restarted": "1"}, "idle") == (False, False)


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


def test_busy_session_is_never_restarted():
    # the 2026-11-11 bug: 20+ min of silent work killed by the old hard fallback
    assert watchdog.decide(25, "k", {}, None) == (True, False)
    assert watchdog.decide(120, "k", {"notified": "k"}, None) == (False, False)


def test_restart_rules():
    assert watchdog.decide(4, "k", {}, "prompt") == (True, True)
    assert watchdog.decide(4, "k", {}, "idle") == (False, False)
    assert watchdog.decide(16, "k", {}, "idle") == (True, True)
    assert watchdog.decide(4, "k", {"notified": "k", "restarted": "k"}, "prompt") == (False, False)


def test_stuck_signal(tmp_path):
    import os
    f = tmp_path / "channel.out"
    f.write_text("Do you want to proceed?")
    now = datetime.now(timezone.utc)
    assert watchdog.stuck_signal(f, now) is None  # fresh output = busy
    old = now.timestamp() - 600
    os.utime(f, (old, old))
    assert watchdog.stuck_signal(f, now) == "prompt"
    f.write_text("working")
    os.utime(f, (old, old))
    assert watchdog.stuck_signal(f, now) == "idle"


def test_fresh_transcript_means_busy_even_if_terminal_silent(tmp_path):
    import os
    out = tmp_path / "channel.out"
    out.write_text("quiet")
    old = datetime.now(timezone.utc).timestamp() - 3600
    os.utime(out, (old, old))
    log = tmp_path / "s.jsonl"
    log.write_text("{}")  # just written
    assert watchdog.stuck_signal([out, log]) is None
    os.utime(log, (old, old))
    assert watchdog.stuck_signal([out, log]) == "idle"
    assert watchdog.stuck_signal([tmp_path / "missing"]) is None
