"""Owner-data export and delete for the private message/decision log (directive 8).

Export writes a 0600 JSON file. Delete removes one chat's messages (and, with --decisions, all
decisions) and is a no-op without confirm=True, so it can never run by accident."""
from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path

from cimcime.message_log import default_path


def export_data(out: Path, db: Path | None = None) -> dict:
    db = db or default_path()
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    tables = {t: [dict(r) for r in conn.execute(f"SELECT * FROM {t}")] for t in _tables(conn)}
    conn.close()
    fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(tables, f, ensure_ascii=False, indent=2)
    os.chmod(out, 0o600)
    return {"exported": {t: len(rows) for t, rows in tables.items()}, "file": str(out)}


def delete_data(chat_id: str | None, decisions: bool = False, confirm: bool = False, db: Path | None = None) -> dict:
    if not confirm:
        return {"deleted": False, "reason": "pass --yes to confirm; this cannot be undone"}
    conn = sqlite3.connect(db or default_path())
    counts = {}
    if chat_id:
        counts["messages"] = conn.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,)).rowcount
    if decisions:
        counts["decisions"] = conn.execute("DELETE FROM decisions").rowcount
    conn.commit()
    conn.close()
    return {"deleted": True, "counts": counts}


def _tables(conn: sqlite3.Connection) -> list[str]:
    return [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('messages','decisions')")]
