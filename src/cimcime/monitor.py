"""`cimcime status`: a read-only snapshot of what the session is doing right now.

Built only from local files (no GitHub, no model call), so it answers even when the session is
wedged: the newest session transcript (current/last tool calls, tools still running, subagent
activity), the service state, the watchdog health log, and the Telegram message log.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from cimcime import service, watchdog
from cimcime.config import data_dir
from cimcime.message_log import default_path

TAIL_LINES = 400  # transcript lines inspected; enough for the recent tool trail


def _short(s: str, n: int = 110) -> str:
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[: n - 1] + "…"


def describe_tool(name: str, inp: dict) -> str:
    detail = inp.get("command") or inp.get("description") or inp.get("file_path") or inp.get("prompt") or inp.get("url") or ""
    if name == "Agent":
        detail = f"{inp.get('subagent_type', '')}: {inp.get('description', '')}"
    return f"{name} {_short(detail)}".strip()


def newest_transcript(workdir: Path | None = None) -> Path | None:
    files = [f for f in watchdog.activity_files([], workdir) if f.suffix == ".jsonl"]
    return files[0] if files else None


def parse_transcript(path: Path) -> dict:
    """Return recent tool trail, tools still awaiting a result, and last-event time."""
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()[-TAIL_LINES:]
    except OSError:
        return {"trail": [], "running": [], "last_event": None}
    trail: list[tuple[str, str]] = []
    pending: dict[str, tuple[str, str]] = {}
    last = None
    for line in lines:
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("type") not in ("assistant", "user"):
            continue  # skips api-request-blob copies that re-list finished tool calls
        ts = d.get("timestamp")
        if ts:
            last = ts
        content = (d.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use":
                item = (ts or "", describe_tool(block.get("name", "?"), block.get("input") or {}))
                trail.append(item)
                pending[block.get("id", "")] = item
            elif block.get("type") == "tool_result":
                pending.pop(block.get("tool_use_id", ""), None)
    return {"trail": trail[-8:], "running": list(pending.values()), "last_event": last}


def _age(ts: str | None, now: datetime) -> str:
    if not ts:
        return "unknown"
    secs = int((now - watchdog._parse(ts)).total_seconds())
    return f"{secs}s ago" if secs < 120 else f"{secs // 60}m ago"


def _tail(path: Path, n: int) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="ignore").splitlines()[-n:]
    except OSError:
        return []


def snapshot(now: datetime | None = None, workdir: Path | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    out = [f"Cimcime status @ {now:%Y-%m-%d %H:%M:%SZ}"]
    try:
        out.append(f"service: {'running' if service.is_running() else 'NOT running'}")
    except Exception as exc:  # status must never crash
        out.append(f"service: unknown ({exc})")

    tr = newest_transcript(workdir)
    if tr:
        info = parse_transcript(tr)
        out.append(f"last session activity: {_age(info['last_event'], now)} ({tr.name})")
        if info["running"]:
            out.append("running now (no result yet):")
            out += [f"  - {_age(ts, now)}: {desc}" for ts, desc in info["running"]]
        else:
            out.append("running now: nothing (idle or between steps)")
        out.append("recent tool trail:")
        out += [f"  - {_age(ts, now)}: {desc}" for ts, desc in info["trail"]] or ["  (none)"]
    else:
        out.append("session transcript: none found")

    un = watchdog.oldest_unanswered(default_path(), now)
    out.append(f"oldest unanswered Telegram message: {f'{un.age_min} min' if un else 'none'}")
    health = _tail(data_dir() / "logs" / "health.log", 3)
    out.append("watchdog health (last 3):")
    out += [f"  {h}" for h in health] or ["  (no health.log yet)"]
    return "\n".join(out)
