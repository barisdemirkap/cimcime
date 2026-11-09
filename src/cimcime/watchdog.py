"""Health check, run every few minutes by the service manager (`cimcime watchdog`).

Restarts the channel service if it has died, and handles "alive but not answering": the headless
session can sit forever on an interactive prompt with the process alive. If the oldest inbound
Telegram message is unanswered and the session shows a stuck signal (silent output / prompt text) for
>=3 min it is restarted and the user told; with no signal, alert at 10 min and restart at 20 min (once per message; the new session recovers via `unanswered-messages`).
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
RESTART_AFTER_MIN = 20  # hard fallback: unanswered this long, restart regardless of signals
FAST_AFTER_MIN = 3  # unanswered this long AND a stuck signal (below) -> restart now
IDLE_AFTER_MIN = 3  # session output untouched this long counts as a stuck signal
PROMPT_RE = re.compile(
    r"do you want to proceed|password:|\(y/n\)|\[y/n\]|permission to|allow this|esc to cancel",
    re.I,
)
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


def decide(age_min: int, key: str, state: dict, signal: str | None = None) -> tuple[bool, bool]:
    """Return (alert, restart) given the message age, a stuck signal, and what was already done."""
    due = age_min >= RESTART_AFTER_MIN or (signal is not None and age_min >= FAST_AFTER_MIN)
    restart = due and state.get("restarted") != key
    alert = (restart or age_min >= ALERT_AFTER_MIN) and state.get("notified") != key
    return alert, restart


def stuck_signal(out_file: Path, now: datetime | None = None) -> str | None:
    """Return why the session looks stuck ('prompt' or 'idle'), or None if it looks busy.

    A thinking/working session keeps redrawing its spinner, so the pty output file keeps changing;
    a session frozen on a dialog or password prompt goes silent, and the dialog text is on screen.
    """
    try:
        raw = out_file.read_bytes()[-4000:].decode("utf-8", "ignore")
        mtime = datetime.fromtimestamp(out_file.stat().st_mtime, timezone.utc)
    except OSError:
        return None
    text = re.sub(r"\x1b\[[0-9;?]*[a-zA-Z]", "", raw)
    now = now or datetime.now(timezone.utc)
    idle = (now - mtime).total_seconds() / 60 >= IDLE_AFTER_MIN
    if idle and PROMPT_RE.search(text):
        return "prompt"
    if idle:
        return "idle"
    return None


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
        signal = stuck_signal(logs / "channel.out")
        alert, restart = decide(un.age_min, un.key, state, signal)
        if alert and token:
            send_alert(token, un.chat_id, (
                f"Cimcime has not answered your message for {un.age_min} min (stuck signal: "
                f"{signal or 'none'}). {'Restarting now.' if restart else 'Auto-restart soon.'}"))
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
