# OpenClaw

Category: ai-coding-tools · Topic ID: openclaw

## Sources

- [fetched] https://roadmap.sh/openclaw — real content.
- [fetched] https://docs.openclaw.ai/ — real content, the official docs.
- [fetched] https://roadmap.sh/openclaw/installation-guide — real content, including explicit Mac Mini and VPS setup instructions.
- [fetched] https://roadmap.sh/openclaw/security-best-practices — real content.
- [fetched] https://roadmap.sh/openclaw/vs-claude-code — real comparison content.
- [could not fetch] https://www.youtube.com/watch?v=u4ydH-QvPeg — title only, no transcript.

## Findings

**What it is**: an open-source, self-hosted AI agent gateway that bridges messaging apps
(Telegram, WhatsApp, Discord, Signal) to AI models the user controls, running as a persistent
"Gateway daemon" process on the user's own hardware — explicitly framed around data sovereignty
(keeping conversations and credentials on hardware you control, not a third party's).

**Architecture**: one Gateway process serves every configured channel plugin simultaneously.
Message flow: channel (e.g. Telegram) → Gateway → routed to an agent/CLI/web UI/mobile app →
agent processes with tool/session access → response flows back through the same channel.
Sessions are isolated per agent/workspace/sender depending on configuration.

**vs. Claude Code** (roadmap.sh comparison, directly relevant to this system's own design):
OpenClaw is "a general-purpose platform designed to run 24/7 across messaging channels" and
**operates proactively** (runs scheduled tasks without user initiation); Claude Code is reactive
("open a session, describe a task, it executes"). OpenClaw needs 15-60 min of infra setup
(Docker/VPS); Claude Code installs via npm in ~30 seconds. OpenClaw: no subscription, pay only for
LLM API tokens, data stays on your own hardware. Claude Code: $20-200+/mo subscription, processes
on Anthropic's infrastructure.

**This maps almost exactly onto this system's own Learning-Phase/Runtime-Phase split
(ADR-0003)**: OpenClaw's "proactive, runs 24/7" mode is structurally the same shape as Cimcime's
Learning Phase (autonomous, continuous, unprompted); its "reactive" mode once paired to a channel
is the same shape as Runtime Phase (acts only when messaged).

**Directly, concretely relevant to tickets #6 and #7 — more so than Claude Code's own Channels
feature found while researching `claude-code.md`**:

- **Telegram setup is the exact same shape already planned**: create a bot via @BotFather, copy
  the token, `openclaw channels add` → select Telegram, then `openclaw pairing approve telegram
  [code]` — a pairing/allowlist model equivalent to what Claude Code's Channels plugin does.
- **The installation guide names a Mac Mini explicitly** ("For always-on operation on Mac mini")
  with concrete settings: disable sleep, "Wake for network access," "Start up automatically after
  power failure," and recommends a separate Apple ID/email for security isolation. This is
  ADR-0005's exact deployment target, with ready-made setup steps — not a coincidence given the
  roadmap.sh curriculum likely wrote this with FDE-style always-on personal-agent setups in mind.
- **Security guidance is directly applicable to this system's own secrets handling** (ADR-0005's
  gitignored `secrets/` requirement): explicit deny-lists for sensitive paths (`~/.ssh`,
  `~/.aws`, `**/.env`), least-privilege scoped API tokens (never admin/production credentials),
  explicit consent gates for destructive operations (directly analogous to ADR-0001's three
  approval gates), secrets stored via a dedicated manager or `600`-permission files — never in a
  git repo, hardcoded script, or a `SKILL.md` file — plus a 90-day rotation schedule and weekly
  usage-dashboard monitoring.
- **Gateway port 18789** should be firewalled from public access if ever run on a VPS instead of
  locally — not this system's current plan (local Mac Mini only), but worth knowing if that ever
  changes.

**Open question this raises, flagging rather than deciding**: there are now two real candidate
mechanisms for ticket #6/#7 — Claude Code's own built-in Telegram Channels plugin (found via
`claude-code.md`) and OpenClaw as a separate, purpose-built gateway tool. They solve overlapping
problems slightly differently (Channels pushes events *into* an already-running Claude Code
session; OpenClaw is its own standalone gateway that then calls out to a model/agent). Which one
tickets #6/#7 should actually build on is a real architecture decision for when that work
resumes, not something to pick unilaterally while doing unrelated research.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
