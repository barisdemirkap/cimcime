"""Health check, run every few minutes by the service manager (`cimcime watchdog`).

Restarts the channel service if it has died, and handles "alive but not answering": the headless
session can sit forever on an interactive prompt with the process alive. If the oldest inbound
Telegram message is unanswered: a prompt on screen -> restart after 3 min; no activity at all for 5 min
and unanswered 15 min -> restart; any recent output/transcript activity = busy = never restart (it would
kill in-flight work), only a one-time alert at 10 min. Once per message; the new session recovers via
`unanswered-messages`.
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

ALERT_AFTER_MIN = 10  # unanswered this long: tell the user once (never a restart by itself)
FAST_AFTER_MIN = 3  # unanswered this long AND a permission/password prompt on screen -> restart
IDLE_RESTART_AFTER_MIN = 15  # unanswered this long AND zero activity for IDLE_AFTER_MIN -> restart
IDLE_AFTER_MIN = 5  # no terminal output and no transcript write for this long = idle
# A session that is still producing output or writing its transcript is WORKING (long research,
# subagents): silence toward the user is not a hang, and a restart would kill that work.
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
    """Return (alert, restart). Restart only for a prompt (fast) or confirmed idleness (slower).

    signal None means busy/unknown: never restart, however long the message has waited.
    """
    due = (signal == "prompt" and age_min >= FAST_AFTER_MIN) or (
        signal == "idle" and age_min >= IDLE_RESTART_AFTER_MIN
    )
    restart = due and state.get("restarted") != key
    alert = (restart or age_min >= ALERT_AFTER_MIN) and state.get("notified") != key
    return alert, restart


def activity_files(out_files: list[Path], workdir: Path | None = None) -> list[Path]:
    """Terminal output files plus the newest session transcript under ~/.claude/projects."""
    files = list(out_files)
    slug = re.sub(r"[^A-Za-z0-9]", "-", str(workdir or Path.cwd()))
    root = Path.home() / ".claude" / "projects" / slug
    try:
        newest = max((p for p in root.rglob("*.jsonl")), key=lambda p: p.stat().st_mtime, default=None)
    except OSError:
        newest = None
    if newest:
        files.append(newest)
    return files


def stuck_signal(out_file: Path | list[Path], now: datetime | None = None) -> str | None:
    """Return why the session looks stuck ('prompt' or 'idle'), or None if busy/unknown.

    Busy = ANY watched file (terminal output, session transcript) changed within IDLE_AFTER_MIN.
    A session frozen on a dialog or password prompt goes silent with the dialog text on screen.
    """
    files = out_file if isinstance(out_file, list) else [out_file]
    now = now or datetime.now(timezone.utc)
    newest, text = None, ""
    for f in files:
        try:
            m = datetime.fromtimestamp(f.stat().st_mtime, timezone.utc)
            if f.suffix != ".jsonl":
                raw = f.read_bytes()[-4000:].decode("utf-8", "ignore")
                text = re.sub(r"\x1b\[[0-9;?]*[a-zA-Z]", "", raw)
        except OSError:
            continue
        newest = m if newest is None or m > newest else newest
    if newest is None or (now - newest).total_seconds() / 60 < IDLE_AFTER_MIN:
        return None
    return "prompt" if PROMPT_RE.search(text) else "idle"


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
        signal = stuck_signal(activity_files([logs / "launchd-telegram-channel.out", logs / "channel.out"]))
        alert, restart = decide(un.age_min, un.key, state, signal)
        if alert and token:
            send_alert(token, un.chat_id, (
                f"Cimcime has not answered your message for {un.age_min} min (stuck signal: "
                f"{signal or 'busy'}). "
                + ("Restarting now." if restart else "It is still working, not restarting." if signal is None else "Will restart if it stays idle.")))
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
