from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

# Lives outside the repo on purpose: these are the user's private chat messages.
DEFAULT_MESSAGE_LOG_PATH = Path.home() / ".claude" / "channels" / "telegram" / "messages.db"
MESSAGE_LOG_ENV_VAR = "CIMCIME_MESSAGE_LOG"


class Direction(Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


@dataclass(frozen=True)
class LoggedMessage:
    chat_id: str
    direction: Direction
    message_id: str | None
    sent_at: str
    text: str


def default_path() -> Path:
    override = os.environ.get(MESSAGE_LOG_ENV_VAR)
    return Path(override) if override else DEFAULT_MESSAGE_LOG_PATH


class MessageLog:
    """Append-only record of every Telegram message in or out, so a restarted or compacted
    session can recover the conversation. Idempotent per (chat_id, direction, message_id):
    logging the same Telegram message twice keeps one row."""

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT NOT NULL,
                direction TEXT NOT NULL,
                message_id TEXT,
                sent_at TEXT NOT NULL,
                text TEXT NOT NULL
            )
            """
        )
        self._conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS messages_unique_telegram_id
            ON messages (chat_id, direction, message_id) WHERE message_id IS NOT NULL
            """
        )
        self._conn.commit()

    def log(
        self,
        chat_id: str,
        direction: Direction,
        text: str,
        message_id: str | None = None,
        sent_at: str | None = None,
    ) -> None:
        self._conn.execute(
            "INSERT OR IGNORE INTO messages (chat_id, direction, message_id, sent_at, text)"
            " VALUES (?, ?, ?, ?, ?)",
            (
                chat_id,
                direction.value,
                message_id,
                sent_at or datetime.now(timezone.utc).isoformat(),
                text,
            ),
        )
        self._conn.commit()

    def recent(self, chat_id: str, limit: int = 20) -> list[LoggedMessage]:
        """Oldest-first, so the result reads as a conversation."""
        rows = self._conn.execute(
            "SELECT chat_id, direction, message_id, sent_at, text FROM messages"
            " WHERE chat_id = ? ORDER BY id DESC LIMIT ?",
            (chat_id, limit),
        ).fetchall()
        return [
            LoggedMessage(chat, Direction(direction), message_id, sent_at, text)
            for chat, direction, message_id, sent_at, text in reversed(rows)
        ]

    def unanswered(self, chat_id: str, limit: int = 50) -> list[LoggedMessage]:
        """Every inbound message after the last outbound one - oldest-first. Empty
        if the most recent message is already outbound (fully caught up).

        Exists for usage-limit recovery: whether or not a --channels session queues
        a Telegram message while Claude Code's own usage limit has it paused is not
        documented (checked directly against code.claude.com) - this log already
        records every inbound message regardless, so on resume Cimcime can check
        this instead of trusting undocumented platform behavior to not have
        dropped anything."""
        messages = self.recent(chat_id, limit)
        pending: list[LoggedMessage] = []
        for message in reversed(messages):
            if message.direction == Direction.OUTBOUND:
                break
            pending.append(message)
        return list(reversed(pending))
