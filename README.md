# Cimcime

An autonomous forward-deployed-engineer agent system. Cimcime learns the FDE skillset from
roadmap.sh on its own, then does FDE work on demand — it is not a curriculum that teaches a
human the skillset (see ADR-0001).

## Status

**Learning Phase: complete.** All 97 topics across all 9 categories are settled (`researched`
or, where a topic's linked resources were genuinely unfetchable, flagged
`needs-better-sources` per ADR-0007). Cimcime has switched to **Runtime Phase** (ADR-0003):
it does no unprompted background work now, and acts only when invoked.

The Telegram bridge (ADR-0009, Cimcime's Runtime-Phase human interface) is partially set up:
the `telegram` channel plugin is installed, but configuration/pairing/live verification are
blocked on the user generating a fresh bot token and knowing their own Telegram user ID — see
issue #7. Until then, invoke Cimcime directly in a Claude Code session.

## Using it

Invoke the **`cimcime`** agent in a Claude Code session in this repo. It checks which phase
it's in (`uv run python -m cimcime.cli get-phase`) and acts accordingly — driving the Learning
Phase loop if one is still open, or taking a direct request in Runtime Phase, subject to the
three approval gates in ADR-0001 (production deploy, real third-party communication, real
spend/account change).

Useful CLI commands directly (`uv run python -m cimcime.cli <command>`):

- `phase-check` — read-only; reports per-category progress against the true roadmap roster
- `get-phase` / `set-phase` — read/flip Learning vs. Runtime
- `category-status <category>` — read-only tally for one category
- `category-rollup <category>` — posts a rollup comment to that category's tracking issue
- `get-topic` / `update-status` / `add-finding` / `flag-needs-better-sources` — per-topic state

## Where things live

- `GLOSSARY.md` — domain vocabulary (Cimcime, category-agent, topic-agent, Approval gate,
  Learning/Runtime Phase, State store, Model backend, Telegram bridge).
- `docs/adr/0001`–`0009` — every architecture decision and why it was made, in order.
- `docs/research/forward-deployed-engineer-roadmap.md` — the full 97-topic curriculum index.
- `docs/topics/<category>/<topic>.md` — one study file per researched topic.
- `src/cimcime/` — the Python package (state store, approval gate, roadmap parser, CLI,
  notification formatting).
- `.claude/agents/` — the orchestrator (`cimcime.md`), ~9 category-agents, and the generic
  topic-agent.
- `tests/` — `uv run pytest -q` runs the fast suite; integration tests (live GitHub) are
  excluded by default, run with `uv run pytest -m integration`.

## Design principles, in short

Cimcime acts autonomously on everything except three approval gates (production delivery/
deployment, real third-party communication, real spend/account change) — reversible work is
protected by git/backups instead of per-action permission (ADR-0001). It's a strict three-level
hierarchy: Cimcime dispatches category-agents only, category-agents dispatch their own
topic-agents only, never sideways (ADR-0002, ADR-0008). GitHub Issues plus this repo's own
markdown are the source of truth for all tracked state (ADR-0004).
