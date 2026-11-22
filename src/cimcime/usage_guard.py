"""Freshness-checked usage verdict (owner-critical: never act on or quote stale limit data)."""
from __future__ import annotations

import json
import time
from pathlib import Path

STATE_DIR = Path.home() / ".local" / "state" / "cimcime"
MAX_AGE_S = 15 * 60


def check(state_dir: Path = STATE_DIR, now: float | None = None) -> dict:
    now = time.time() if now is None else now
    best: dict | None = None
    try:
        sl = json.loads((state_dir / "statusline.json").read_text())
        rl = sl["data"]["rate_limits"]
        best = {
            "source": "statusline", "t": float(sl["captured_at"]),
            "five_hour": rl["five_hour"]["used_percentage"], "seven_day": rl["seven_day"]["used_percentage"],
            "resets": {"five_hour": rl["five_hour"].get("resets_at"), "seven_day": rl["seven_day"].get("resets_at")},
        }
    except (OSError, ValueError, KeyError, TypeError):
        pass
    try:
        u = json.loads((state_dir / "usage.json").read_text())
        t = float(u["checked_at"])
        if best is None or t > best["t"]:
            best = {"source": "usage.json", "t": t, "five_hour": u["percent"]["five_hour"],
                    "seven_day": u["percent"]["seven_day"], "resets": {}}
    except (OSError, ValueError, KeyError, TypeError):
        pass
    if best is None:
        return {"verdict": "unknown", "reason": "no usage data; do not start large jobs, do not quote numbers"}
    age = int(now - best["t"])
    if age > MAX_AGE_S:
        return {"verdict": "unknown", "age_s": age, "last_seen": {"five_hour": best["five_hour"], "seven_day": best["seven_day"]},
                "reason": f"data is {age}s old (> {MAX_AGE_S}s): NOT current. Never quote these numbers or any reset time derived from them as current; say the limit is unknown."}
    peak = max(best["five_hour"], best["seven_day"])
    mode = "defer" if peak >= 90 else "watch" if peak >= 80 else "normal"
    return {"verdict": mode, "age_s": age, "source": best["source"],
            "five_hour": best["five_hour"], "seven_day": best["seven_day"], "resets_at": best["resets"]}
