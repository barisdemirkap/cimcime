# Context memory (slices 0 and 1)

Design notes and the decision record are kept in the maintainer's private planning notes (not part of this repository).
Status: proposed. Code: `src/cimcime/memory.py`, CLI in `src/cimcime/cli.py`, tests in `tests/test_memory.py`.

## Model: checkpoint and rotate

Claude Code compacts its own window on its own schedule; hooks cannot force or replace that. So
memory keeps a durable copy alongside it:

1. **Snapshot (checkpoint).** Archive the transcript bytes since the session's last snapshot
   verbatim (zlib-compressed) into `memory.db`, and store a deterministic handoff summary: session,
   context size, the last owner requests, the last reply, files edited, and a pointer to the archive.
   - `Stop` hook: only when the context has grown by about 50k tokens (`--interval`) since the last
     snapshot of this session, or since Claude's own last compaction (`compact_boundary.postTokens`).
   - `PreCompact` hook: always, so nothing is lost when Claude compacts.
2. **Brief (rotate).** At `SessionStart` a new or compacted session receives at most 3k tokens:
   the latest handoff, recent decisions, promise candidates and owner preferences, each line citing
   its source row (`[decisions#154 ...]`, `[messages#975 ...]`).

"50k" is the durable snapshot interval, not a forced Claude compaction.

Slice 1 is deterministic: no model writes summaries yet. Promise candidates are pattern matches
over the last 14 days of messages ("remind me", "I will", "-acağım/-eceğim") and are not tracked as
open or done until slice 2 adds pins. Preferences are owner messages matching "always", "never",
"from now on", "do not", "her zaman", "asla", "bundan sonra", "-meli/-malı".

## Storage and privacy

- `memory.db` is a separate file, mode 0600, next to the message log:
  `~/.claude/channels/telegram/memory.db`, override with `CIMCIME_MEMORY_DB`. Never in the repo.
- The message log (`messages`, `decisions`) is the source of truth. `memory-index` opens it
  read-only; `memory.db` can be deleted and rebuilt from it at any time (archives cannot: they come
  from transcripts).
- **Indexed for search:** Telegram messages, decisions, and snapshot summaries only. Transcripts
  are archived verbatim but never indexed.
- **Retention:** 365 days. Rows older than that are not indexed and are pruned on every
  `memory-index` and `memory-snapshot`.
- **Scopes.** Decisions take their `project` as scope. Telegram messages have no project: any
  message that names Camondo is filed under `camondo`, everything else under `cimcime` (fails
  closed). `camondo` is sensitive: search and the brief leave it out unless asked by name
  (`--scope camondo`).
- **Untrusted data.** Stored text is never executed as instructions. The brief is wrapped in
  `<memory-data trust="untrusted">`, says so in its first line, collapses every item to one line and
  escapes any `memory-data` tag inside stored text, so a stored message cannot close the wrapper
  or forge a section. Hits carry `trust` (`owner` for inbound messages and decisions, `agent` for
  outbound messages and summaries).
- Archive size: transcripts with large tool results compress poorly (a 9.6 MB transcript
  archived as 6.4 MB). At 365 days this is roughly the transcript volume of a year.

## CLI

All print JSON and need no GitHub configuration.

```sh
uv run python -m cimcime.cli memory-index                       # ingest messages + decisions (idempotent)
uv run python -m cimcime.cli memory-search "weekly stop 90%"     # FTS5, BM25; --scope X (repeatable), --limit N
uv run python -m cimcime.cli memory-snapshot --session-id ID --transcript PATH [--trigger manual|stop|precompact] [--if-due]
uv run python -m cimcime.cli memory-snapshot --hook              # reads a Stop/PreCompact payload on stdin
uv run python -m cimcime.cli memory-brief [--scope X]            # {"brief": ..., "tokens": N}
uv run python -m cimcime.cli memory-brief --hook                 # SessionStart additionalContext JSON
```

Search is keyword only and says so (`"mode": "keyword"`). Queries are reduced to quoted terms, so
FTS5 syntax in a query is inert. Matching folds case, diacritics and Turkish dotted/dotless i.

In `--hook` mode the commands print nothing on error (the message goes to stderr) and exit 0, so a
memory failure never blocks a session.

Measured on the real log (2026-11-23): 951 rows indexed in 0.09 s; a 9.6 MB transcript
snapshotted in 0.36 s; brief of 1,614 tokens in 0.07 s.

## Slice 0: real hook payloads

Captured 2026-11-23 with Claude Code 2.1.323 from an isolated `claude -p` run
(`--setting-sources project --settings <hooks file>` in a scratch directory, so no user hooks or
plugins ran), then `/compact` on the resumed session. Raw log: `logs/hook-payloads-slice0.jsonl`
(gitignored, 0600). Paths and ids redacted below.

```jsonc
// SessionStart (startup)
{"session_id", "transcript_path", "cwd", "hook_event_name": "SessionStart", "source": "startup"}
// SessionStart (resume) adds context size
{..., "source": "resume", "seconds_since_last_response": 6, "context_tokens": 18168,
 "prompt_cache_likely_expired": false, "estimated_cache_write_usd": 0.0036}
// SessionStart (after compaction)
{..., "prompt_id", "source": "compact", "model": "claude-haiku-..."}
// Stop: no token count
{..., "prompt_id", "permission_mode": "default", "effort": {"level": "medium"},
 "hook_event_name": "Stop", "stop_hook_active": false, "last_assistant_message": "ok",
 "background_tasks": [], "session_crons": []}
// PreCompact
{..., "prompt_id", "hook_event_name": "PreCompact", "trigger": "manual", "custom_instructions": "keep the word ok"}
// PostCompact: carries Claude's own summary text
{..., "prompt_id", "hook_event_name": "PostCompact", "trigger": "manual", "compact_summary": "<analysis>...</analysis>\n\n<summary>...</summary>"}
// SessionEnd
{..., "prompt_id", "hook_event_name": "SessionEnd", "reason": "other"}
```

Findings that changed the design:

- `Stop` has no token count, so the 50k check reads the transcript: the latest main-thread
  (`isSidechain` false) assistant `message.usage` (`input_tokens + cache_creation_input_tokens +
  cache_read_input_tokens + output_tokens`), falling back to bytes / 4.
- The transcript records each compaction as `{"type": "system", "subtype": "compact_boundary",
  "compactMetadata": {"trigger", "preTokens", "postTokens", ...}}`; the interval rebases on
  `postTokens`.
- `PostCompact` **does** receive the summary (`compact_summary`); the design doc assumed it might
  not. Slice 2 can store it as a model-written summary at no extra cost.
- Not observed: `PreCompact` with `trigger: "auto"` (needs a long session; the matcher value is
  documented). In the transcript sampled, owner Telegram turns and subagent hand-backs arrive as
  `queued_command` attachments, not `user` entries; slice 1 reads owner words from the message
  log instead, and excludes hand-backs (model output, not owner authority).

## Proposed hook configuration (not installed)

`~/.claude/settings.json` was **not** edited. To enable, the owner adds this (adjust the repo path;
`--directory` makes `uv` use the repo's environment from any working directory):

```json
{
  "hooks": {
    "SessionStart": [
      {"hooks": [{"type": "command", "timeout": 15,
        "command": "uv run --quiet --directory /path/to/forward-deployed-engineer python -m cimcime.cli memory-brief --hook"}]}
    ],
    "Stop": [
      {"hooks": [{"type": "command", "timeout": 30,
        "command": "uv run --quiet --directory /path/to/forward-deployed-engineer python -m cimcime.cli memory-snapshot --hook"}]}
    ],
    "PreCompact": [
      {"matcher": "manual|auto", "hooks": [{"type": "command", "timeout": 30,
        "command": "uv run --quiet --directory /path/to/forward-deployed-engineer python -m cimcime.cli memory-snapshot --hook"}]}
    ]
  }
}
```

Run `memory-index` before the first brief (and periodically, for example from the watchdog) so
new messages and decisions are searchable. These hooks apply to every Claude Code session of the
user; for Camondo sessions pass `--scope camondo` to both commands in a project-level settings
file instead.

## What remains

- Slice 0: the 40-question gold set (owner-written) and the keyword recall baseline.
- Slice 1 leftovers: `export`/`erase` per ADR-C, a `memory` skill, and running `memory-index`
  from the watchdog.
- Slice 2: model-written rolling summaries (store `PostCompact.compact_summary`), pins with
  open/done status and provenance, `PreCompact` stdout steering Claude's summary, savings log.
- Slice 3 (embeddings): Ollama `nomic-embed-text`, brute-force cosine, RRF; gated by the eval.
  Nothing in slices 0-1 pulls a model or starts Ollama.

## Slices 2-4 (implemented)

- Embeddings: optional Ollama `nomic-embed-text` (`CIMCIME_OLLAMA_URL`, default `127.0.0.1:11434`), float32 vectors in the `embeddings` table of `memory.db`. `cimcime memory-embed` (also run by `memory-index`) fills missing vectors; with Ollama absent it reports `available: false` and nothing else changes.
- Hybrid search: `cimcime memory-search` fuses FTS5 BM25 and cosine ranks by reciprocal rank fusion (k=60) over messages, decisions and summaries; sensitive-scope exclusion still applies. `mode` is `hybrid` or `keyword`; `--no-embed` forces keyword.
- Checkpoint and rotate: `cimcime memory-checkpoint --session-id S --transcript T [--if-due] [--interval 50000] [--max-age-minutes N]` archives verbatim, stores the handoff summary, embeds, and returns `{rotate, brief}`; a due check passes on tokens or elapsed time. `memory-snapshot --max-age-minutes` shares the time trigger.

## Concurrency and evaluation

`memory.db` runs in WAL mode with a 30 s busy timeout and `snapshot()` holds the write lock for its whole
read-then-write sequence, so Stop and PreCompact firing together are safe (ADR-0017). Retrieval changes are
judged by `cimcime eval-memory` against pre-registered gates: see `docs/memory-eval.md`.
