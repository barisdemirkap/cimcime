"""Health check, run every few minutes by the service manager (`cimcime watchdog`).

Restarts the channel service if it has died, and handles "alive but not answering": the headless
session can sit forever on an interactive prompt with the process alive. If the oldest inbound
Telegram message has had no reply for >=10 min the user is alerted (once per message); at >=20 min
the service is restarted (once per message; the new session recovers via `unanswered-messages`).
"""
from __future__ import annotations

import json
import re
import sqlite3
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from cimcime import service
from cimcime.config import data_dir
from cimcime.message_log import default_path

ALERT_AFTER_MIN = 10
RESTART_AFTER_MIN = 20
ENV_FILE = Path.home() / ".claude" / "channels" / "telegram" / ".env"


@dataclass(frozen=True)
class Unanswered:
    chat_id: str
    key: str
    age_min: int


def _parse(ts: str) -> datetime:
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def oldest_unanswered(db: Path, now: datetime | None = None) -> Unanswered | None:
    if not db.is_file():
        return None
    now = now or datetime.now(timezone.utc)
    conn = sqlite3.connect(db)
    try:
        rows = conn.execute(
            "SELECT chat_id, id, direction, sent_at FROM messages ORDER BY id ASC"
        ).fetchall()
    except sqlite3.Error:
        return None
    finally:
        conn.close()
    last_out = max((_parse(r[3]) for r in rows if r[2] == "outbound"), default=None)
    for chat, rid, direction, sent in rows:
        if direction == "inbound" and (last_out is None or _parse(sent) > last_out):
            return Unanswered(str(chat), str(rid), int((now - _parse(sent)).total_seconds() // 60))
    return None


def decide(age_min: int, key: str, state: dict) -> tuple[bool, bool]:
    """Return (alert, restart) given the message age and what was already done for this message."""
    alert = age_min >= ALERT_AFTER_MIN and state.get("notified") != key
    restart = age_min >= RESTART_AFTER_MIN and state.get("restarted") != key
    return alert, restart


def read_token() -> str | None:
    try:
        text = ENV_FILE.read_text(encoding="utf-8")
    except OSError:
        return None
    m = re.search(r"^TELEGRAM_BOT_TOKEN=(.*)$", text, re.M)
    return m.group(1).strip().strip("\"'") if m else None


def send_alert(token: str, chat_id: str, text: str) -> bool:
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
    try:
        urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data, timeout=10).read()
        return True
    except OSError:
        return False


def api_ok(token: str | None) -> bool:
    if not token:
        return False
    try:
        urllib.request.urlopen(f"https://api.telegram.org/bot{token}/getMe", timeout=10).read()
        return True
    except OSError:
        return False


def run_once() -> str:
    logs = data_dir() / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    state_file = logs / "stuck.state.json"
    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        state = {}

    svc = "ok"
    if not service.is_running():
        svc = "restarted" if service.restart() else "restart-failed"

    token = read_token()
    api = "ok" if api_ok(token) else "FAIL"

    stuck = "none"
    un = oldest_unanswered(default_path())
    if un:
        alert, restart = decide(un.age_min, un.key, state)
        if alert and token:
            send_alert(token, un.chat_id, (
                f"Cimcime has not answered your message for {un.age_min} min (probably stuck on a "
                f"prompt). Auto-restart at {RESTART_AFTER_MIN} min."))
            state["notified"] = un.key
            stuck = "alerted"
        if restart:
            stuck = "restarted" if service.restart() else "restart-failed"
            state["restarted"] = un.key
        state_file.write_text(json.dumps(state), encoding="utf-8")

    line = f"{datetime.now(timezone.utc):%Y-%m-%dT%H:%M:%SZ} service={svc} telegram_api={api} stuck={stuck}"
    log = logs / "health.log"
    with log.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    lines = log.read_text(encoding="utf-8").splitlines()
    if len(lines) > 5000:
        log.write_text("\n".join(lines[-2000:]) + "\n", encoding="utf-8")
    return line
