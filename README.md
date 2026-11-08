# Cimcime

An autonomous forward-deployed-engineer agent system. Cimcime learns the FDE skillset from
roadmap.sh on its own, then does FDE work on demand — it is not a curriculum that teaches a
human the skillset (see ADR-0001).

## Status

**Learning Phase: complete.** All 97 topics across all 9 categories are settled (`researched`
or, where a topic's linked resources were genuinely unfetchable, flagged
`needs-better-sources` per ADR-0007). Cimcime has switched to **Runtime Phase** (ADR-0003):
it does no unprompted background work now, and acts only when invoked.

The Telegram bridge (ADR-0009, Cimcime's Runtime-Phase human interface) is **live** on the Mac
Mini as of 2026-11-08: bot created, plugin configured and paired, allowlisted to the user's own
Telegram account, and running as the always-on `com.cimcime.telegram-channel` `launchd` service
(see issue #7 for the real bring-up issues found and fixed along the way).

`scripts/telegram-setup-wizard.sh` walks through the whole thing on a fresh Mac Mini: creating
the bot via @BotFather, installing the `telegram` channel plugin itself, the Claude Code
commands to configure and pair it, and installing the always-on `launchd` service
(`scripts/install_telegram_launchd.sh`) so the bridge survives a reboot.

This repo is **private** (made private specifically to run a self-hosted GitHub Actions
runner safely — public repos + self-hosted runners are a known risk, since a fork's pull
request could otherwise execute on the runner's host). A self-hosted runner on the Mac Mini
handles continuous deployment (`.github/workflows/deploy.yml`): on every push to `main`, it
re-runs the fast test suite and reinstalls the Telegram bridge's `launchd` service so it
always reflects the latest code.

The runner itself is installed as a persistent launchd service (`./svc.sh install && ./svc.sh start`
in `~/actions-runner/actions-runner`), so it comes back after a reboot. Claude permissions for the
Telegram session live in the committed `.claude/settings.json`, because the deployed checkout
has no gitignored local settings.

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
- `delegate-summarize <text|->` — ADR-0012: summarize tool output via the local Qwen
  backend instead of spending a Claude token on it; refuses anything under ADR-0001's
  three approval gates before ever calling the backend. Needs a real llama.cpp server
  running (`CIMCIME_QWEN_URL`, not yet deployed - the code is ready, the Mac Mini
  server setup is a separate step)
- `log-delegation <haiku|sonnet|qwen_local>` — records a Haiku/Sonnet delegation that
  already happened through the Agent tool, so the log covers both backend families
- `recent-delegations` — read-only: the last N delegation decisions, newest first

## Where things live

- `GLOSSARY.md` — domain vocabulary (Cimcime, category-agent, topic-agent, Approval gate,
  Learning/Runtime Phase, State store, Model backend, Telegram bridge).
- `docs/adr/0001`–`0013` — every architecture decision and why it was made, in order.
- `docs/research/forward-deployed-engineer-roadmap.md` — the full 97-topic curriculum index.
- `docs/topics/<category>/<topic>.md` — one study file per researched topic.
- `docs/board/<role>.md` — researched grounding for each board persona (ADR-0013).
- `src/cimcime/` — the Python package (state store, approval gate, roadmap parser, CLI,
  message/delegation logging, notification formatting).
- `.claude/agents/` — the orchestrator (`cimcime.md`), ~9 category-agents, the generic
  topic-agent, the board (`board.md` plus one agent per persona, ADR-0013), and
  `turkish-translator` — the one place Turkish is ever handled; everything else stays English.
- `tests/` — `uv run pytest -q` runs the fast suite; integration tests (live GitHub) are
  excluded by default, run with `uv run pytest -m integration`.
- `.github/workflows/tests.yml` — CI runs the fast suite on every push/PR to `main`, on
  GitHub's own hosted runners.
- `.github/workflows/deploy.yml` — on push to `main` only (never `pull_request` — this repo
  is private, but that trigger restriction is the actual safety boundary for a self-hosted
  runner), reinstalls/restarts the Telegram bridge's `launchd` service on the Mac Mini via a
  self-hosted runner registered on that machine.
- `scripts/` — `telegram-setup-wizard.sh` (plus its launchd plist and install script) walks
  through the remaining Telegram bridge setup once a bot token exists.

## Design principles, in short

Cimcime acts autonomously on everything except three approval gates (production delivery/
deployment, real third-party communication, real spend/account change) — reversible work is
protected by git/backups instead of per-action permission (ADR-0001). It's a strict three-level
hierarchy: Cimcime dispatches category-agents only, category-agents dispatch their own
topic-agents only, never sideways (ADR-0002, ADR-0008). GitHub Issues plus this repo's own
markdown are the source of truth for all tracked state (ADR-0004).
