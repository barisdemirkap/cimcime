from __future__ import annotations

import json
import os
import sqlite3
import urllib.error
import urllib.request
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

from .approval_gate import ActionType, requires_approval

# Lives outside the repo on purpose, same convention as message_log.py's
# CIMCIME_MESSAGE_LOG - this is operational data (what got delegated, when, how
# it went), not something that belongs in version control.
DEFAULT_LOG_PATH = Path.home() / ".claude" / "cimcime" / "delegations.db"
LOG_PATH_ENV_VAR = "CIMCIME_DELEGATION_LOG"

# Placeholder default - the real port is whatever the Mac Mini's llama.cpp server
# is actually started with (ADR-0012 Q7/Q14: persistent launchd service, smallest
# viable Qwen3 model first). Override via the env var once that's running for real.
DEFAULT_QWEN_URL = "http://127.0.0.1:8090"
QWEN_URL_ENV_VAR = "CIMCIME_QWEN_URL"

MAX_SUMMARY_TOKENS = 512
SUMMARIZE_SYSTEM_PROMPT = (
    "Summarize the following tool output for an engineering assistant that will "
    "continue working from your summary. Preserve exact error messages, file paths, "
    "numbers, and anything a human would need to debug this. Drop repeated or "
    "boilerplate lines. Be concise - a few sentences to a short paragraph, not a "
    "restatement of everything."
)


class Backend(str, Enum):
    QWEN_LOCAL = "qwen_local"
    HAIKU = "haiku"
    SONNET = "sonnet"


class DelegationError(Exception):
    """Base for every way a delegation can fail to produce a usable result."""


class DelegationNotAllowed(DelegationError):
    """ADR-0012's hard rule: nothing under ADR-0001's three approval gates is ever
    delegated, to any backend. Raised before any backend is ever called."""


class BackendUnavailable(DelegationError):
    """The backend (e.g. the local Qwen server) couldn't be reached. Callers must
    fall back to doing the work themselves, never silently drop the task."""


def default_log_path() -> Path:
    override = os.environ.get(LOG_PATH_ENV_VAR)
    return Path(override) if override else DEFAULT_LOG_PATH


def default_qwen_url() -> str:
    return os.environ.get(QWEN_URL_ENV_VAR, DEFAULT_QWEN_URL)


class DelegationLog:
    """Append-only record of every delegation decision (ADR-0012) - task type,
    backend, when, and how it went. This is what the (later, data-gated)
    self-improvement pipeline reads; nothing here is ever deleted or edited."""

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS delegations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_type TEXT NOT NULL,
                backend TEXT NOT NULL,
                decided_at TEXT NOT NULL,
                outcome TEXT NOT NULL,
                detail TEXT
            )
            """
        )
        self._conn.commit()

    def record(self, task_type: str, backend: Backend, outcome: str, detail: str | None = None) -> None:
        self._conn.execute(
            "INSERT INTO delegations (task_type, backend, decided_at, outcome, detail) VALUES (?, ?, ?, ?, ?)",
            (task_type, backend.value, datetime.now(timezone.utc).isoformat(), outcome, detail),
        )
        self._conn.commit()

    def recent(self, limit: int = 50) -> list[dict]:
        """Newest-first - a status/debugging view, not a conversation to replay."""
        rows = self._conn.execute(
            "SELECT task_type, backend, decided_at, outcome, detail FROM delegations ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [
            {"task_type": t, "backend": b, "decided_at": d, "outcome": o, "detail": det}
            for t, b, d, o, det in rows
        ]


def _post_json(url: str, payload: dict, timeout: float) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as exc:
        raise BackendUnavailable(f"Qwen server at {url} is unreachable: {exc}") from exc


def summarize_with_qwen(text: str, *, base_url: str | None = None, timeout: float = 30.0) -> str:
    """Real call to a local llama.cpp server's OpenAI-compatible endpoint. Scope is
    deliberately narrow (ADR-0012 Q12): summarization only, nothing else is routed
    to Qwen yet. Raises BackendUnavailable if the server can't be reached."""
    url = (base_url or default_qwen_url()).rstrip("/")
    result = _post_json(
        f"{url}/v1/chat/completions",
        {
            "messages": [
                {"role": "system", "content": SUMMARIZE_SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            "temperature": 0,
            "max_tokens": MAX_SUMMARY_TOKENS,
            # Qwen3 otherwise "thinks" for hundreds of tokens before answering - a
            # real, measured gotcha from private-agent-farm's own Phase 3 work
            # (docs/phase3-measurements.md there): 6s of rambling vs 1.2s.
            "chat_template_kwargs": {"enable_thinking": False},
        },
        timeout,
    )
    content = ((result.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
    return content.strip()


def delegate_summarize(
    text: str,
    *,
    log: DelegationLog,
    action_type: ActionType = ActionType.ROUTINE_WORK,
    base_url: str | None = None,
) -> str:
    """The one entry point ADR-0012's shared tool uses for Qwen delegation. Refuses
    before ever calling the backend if the task is gated (ADR-0001's three
    approval gates), and logs every outcome - success, refusal, or backend failure."""
    if requires_approval(action_type):
        log.record("summarize", Backend.QWEN_LOCAL, "refused_gated_action", action_type.value)
        raise DelegationNotAllowed(
            f"{action_type.value} requires human approval (ADR-0001) and can never be delegated"
        )
    try:
        summary = summarize_with_qwen(text, base_url=base_url)
    except BackendUnavailable as exc:
        log.record("summarize", Backend.QWEN_LOCAL, "backend_unavailable", str(exc))
        raise
    log.record("summarize", Backend.QWEN_LOCAL, "ok")
    return summary


def log_external_delegation(
    log: DelegationLog, backend: Backend, outcome: str = "ok", detail: str | None = None
) -> None:
    """For Haiku/Sonnet delegations, which happen entirely through the existing
    Agent tool (ADR-0012: no new infrastructure needed for those) - this just
    records that one happened, so the log stays a complete picture across both
    backend families, not just the ones this module calls directly."""
    log.record("summarize", backend, outcome, detail)
