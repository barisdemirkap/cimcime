# Cimcime

Cimcime is an autonomous **forward-deployed-engineer (FDE) agent system** built on
[Claude Code](https://claude.com/claude-code). It first teaches itself the FDE skillset from
[roadmap.sh](https://roadmap.sh/forward-deployed-engineer), then does FDE-style work when you ask it
to, either from a terminal session or from your phone over Telegram.

It runs on **macOS, Linux and Windows**.

## How it works

- **Three-level agent hierarchy** (ADR-0002/0008): the `cimcime` orchestrator dispatches
  category-agents; each category-agent dispatches its own topic-agents. Never sideways.
- **Two phases** (ADR-0003): *Learning* (autonomously research all 97 roadmap topics) and then
  *Runtime* (act only when asked).
- **Three approval gates** (ADR-0001): Cimcime works autonomously except for production deploys,
  real third-party communication, and real spend/account changes. Those always ask you first.
- **State lives in GitHub** (ADR-0004): issues track every topic and category; study notes are plain
  markdown in `docs/topics/`.
- **A board of five personas** (ADR-0013) audits significant decisions before they are proposed to you.
- **Optional Telegram bridge** (ADR-0009): talk to Cimcime from your phone via Claude Code's
  `telegram` channel plugin.

## Requirements

| Tool | Why | Install |
|---|---|---|
| git | clone and version | https://git-scm.com |
| GitHub CLI `gh` (logged in) | issue-based state store | https://cli.github.com, then `gh auth login` |
| Claude Code `claude` | runs the agents | https://claude.com/claude-code |
| Python 3.11+ and [uv](https://docs.astral.sh/uv) | the `cimcime` CLI (the installer sets up uv for you) | |

## Quick start

**macOS / Linux**

```sh
curl -fsSL https://raw.githubusercontent.com/barisdemirkap/cimcime/master/install.sh | sh
```

**Windows (PowerShell)**

```powershell
irm https://raw.githubusercontent.com/barisdemirkap/cimcime/master/install.ps1 | iex
```

**Or manually, on any OS**

```sh
uv tool install git+https://github.com/barisdemirkap/cimcime
```

Then:

```sh
cimcime doctor                      # verify git, gh, claude are installed and logged in
cimcime init <your-user>/<your-repo>  # the GitHub repo that tracks Cimcime's issues
```

Clone the repo and open Claude Code in it, then invoke the `cimcime` agent:

```sh
git clone https://github.com/barisdemirkap/cimcime && cd cimcime
claude --agent cimcime
```

It checks its phase and acts accordingly. The repo's `.claude/agents/` and `.claude/skills/` are
what make the agents available, so run Claude Code from the checkout.

## Always-on mode and Telegram (optional)

```sh
cimcime service install     # launchd (macOS), systemd --user (Linux), Task Scheduler (Windows)
cimcime service status | restart | uninstall
```

This keeps a persistent Cimcime session alive plus a watchdog that restarts it if it gets stuck.
To reach it from Telegram, create a bot with @BotFather and pair it with Claude Code's
`telegram` channel plugin (see `docs/adr/0009-telegram-bridge-via-claude-code-channels.md`).

## Configuration

Settings come from environment variables, then `cimcime.toml`, then defaults. The file is looked up
in `$CIMCIME_CONFIG`, `./cimcime.toml`, then your user config dir
(`~/Library/Application Support/cimcime`, `~/.config/cimcime`, or `%APPDATA%\cimcime`).
See `cimcime.toml.example`. `cimcime.toml`, `logs/` and `secrets/` are gitignored, so your
personal configuration is never committed.

## CLI cheatsheet

`cimcime phase-check`, `get-phase`, `set-phase`, `category-status <cat>`, `category-rollup <cat>`,
`get-topic`, `update-status`, `add-finding`, `doctor`, `init`, `service`, `watchdog`.

## Safety notes

- Cimcime acts autonomously; review `.claude/settings.json` style permissions before running it on
  a machine with sensitive data. Grant only the tools you are comfortable with.
- Approval gates are enforced by the agents' instructions and `cimcime.approval_gate`; they are a
  guardrail, not a sandbox. Run it in a dedicated account or machine for real work.
- Never commit tokens. Report vulnerabilities per [SECURITY.md](SECURITY.md).

## Repository map

- `src/cimcime/` Python package (CLI, state store, approval gate, service, watchdog)
- `.claude/agents/`, `.claude/skills/` agents and skills
- `docs/adr/` every architecture decision; `GLOSSARY.md` the vocabulary
- `docs/topics/`, `docs/research/` study notes (derived from roadmap.sh, with source links)
- `tests/` run with `uv run pytest -q`

## Contributing and license

See [CONTRIBUTING.md](CONTRIBUTING.md). MIT licensed; third-party skills are credited in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
