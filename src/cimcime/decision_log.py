from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from cimcime.message_log import default_path


@dataclass(frozen=True)
class Decision:
    decided_at: str
    project: str
    decision: str
    rationale: str


class DecisionLog:
    """Append-only record of important user decisions and project requirements, kept next to the
    message log (private, outside the repo) so a lost session never loses 'what was decided'."""

    def __init__(self, path: Path | None = None) -> None:
        path = path or default_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                decided_at TEXT NOT NULL,
                project TEXT NOT NULL,
                decision TEXT NOT NULL,
                rationale TEXT NOT NULL DEFAULT ''
            )
            """
        )
        self._conn.commit()

    def log(self, project: str, decision: str, rationale: str = "", decided_at: str | None = None) -> None:
        self._conn.execute(
            "INSERT INTO decisions (decided_at, project, decision, rationale) VALUES (?, ?, ?, ?)",
            (decided_at or datetime.now(timezone.utc).isoformat(), project, decision, rationale),
        )
        self._conn.commit()

    def recent(self, project: str | None = None, limit: int = 50) -> list[Decision]:
        query = "SELECT decided_at, project, decision, rationale FROM decisions"
        params: list = []
        if project:
            query += " WHERE project = ?"
            params.append(project)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        rows = self._conn.execute(query, params).fetchall()
        return [Decision(*r) for r in reversed(rows)]
