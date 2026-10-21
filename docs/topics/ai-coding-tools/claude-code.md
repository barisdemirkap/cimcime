# Claude Code

Category: ai-coding-tools · Topic ID: claude-code

## Sources

- [fetched] https://code.claude.com/docs/en/overview — real, extensive content (the official docs).
- [fetched] https://code.claude.com/docs/en/how-claude-code-works — real, extensive content.
- [fetched, partial] https://roadmap.sh/claude-code — unlike most roadmap.sh pages (which are JS-rendered shells this fetch tool can't execute), this one returned a real partial FAQ snippet (Claude Code vs. Cursor positioning). Possibly a static/SSR'd page or a lucky partial render; noting it as a partial success rather than a full failure.
- [could not fetch] https://www.youtube.com/watch?v=QoQBzR1NIqI — only the title ("CLAUDE CODE FULL COURSE 4 HOURS: Build & Sell (2026)") recoverable, no transcript.

## Findings

**What it is**: an agentic coding tool that reads a codebase, edits files, runs commands, and
integrates with dev tools — available in terminal, IDE, desktop app, and browser. The official
positioning: "Claude Code is the layer around the model that provides the tools and manages the
context the model sees" — this surrounding layer is what "agentic harness" means.

**The agentic loop**: three blending phases — gather context, take action, verify results —
repeated and adapted per task, with the model (not a fixed script) deciding what each step needs
based on what the previous step revealed. Five built-in tool categories: file operations, search,
execution (shell/git/tests), web, and code intelligence. The documented example — "fix the
failing tests" → run suite → read errors → search/read relevant files → edit → rerun tests — is
exactly the shape of the topic-agent/category-agent loops already built in this very system.

**Context management** (directly relevant to designing this system well): the context window
holds conversation history, file contents, tool outputs, CLAUDE.md, auto memory, loaded skills,
and system instructions; it auto-compacts (clears old tool outputs first, then summarizes) as it
fills. Two features exist specifically to avoid polluting a main context: **skills** (full content
loads only when used, not just its description) and **subagents** (run in their own context
window; only a summary returns to the caller). This is precisely why Cimcime's architecture
(ADR-0002/0008) dispatches category-/topic-agents as subagents rather than doing all research
inline — it keeps the orchestrator's own context from filling with 97 topics' worth of fetched
article text.

**Safety mechanisms**: checkpoints (automatic file-edit snapshots, reversible via Esc-Esc or
asking to undo — but explicitly **not** covering actions on remote systems: databases, APIs,
deployments) and permission modes (Auto/Manual/Accept-edits/Plan). The checkpoint/permission split
maps directly onto this system's own two-tier safety model: ADR-0001's three approval gates cover
exactly the irreversible-and-remote category checkpoints explicitly say they can't help with.

**Directly relevant to ticket #6, and a real plan-changing finding — fetched `/docs/en/channels`
in full**: Claude Code has an official, built-in **Telegram channel plugin**
(`claude-plugins-official`'s `telegram` plugin, source on GitHub) that already does most of what
ticket #6 set out to build from scratch in Python:

- **Bot creation**: same BotFather `/newbot` step already planned.
- **Install + configure**: `/plugin install telegram@claude-plugins-official`, then
  `/telegram:configure <token>` — saves the token to `~/.claude/channels/telegram/.env` (**not**
  this repo's gitignored `secrets/`, a real divergence from ticket #6's literal acceptance
  criterion that the token live in the repo's `secrets/`).
- **Sender allowlisting, built in**: pairing (`/telegram:access pair <code>`) plus
  `/telegram:access policy allowlist` already implements "only responds to the configured
  Telegram user ID" — exactly ticket #6's first acceptance criterion, with no custom code.
- **Two-way chat bridge**: inbound Telegram messages arrive as `<channel>` events in the running
  session; Claude replies through the same channel. This is "a command sent via Telegram can
  trigger a real Cimcime invocation" (criterion 2) and most of "approval-gate event produces a
  real Telegram notification" (criterion 3), again with no custom bridge code.
- **Caveats worth weighing before redesigning ticket #6 around this**: channels are a *research
  preview* — requires Anthropic auth via claude.ai or a Console API key (not Bedrock/Vertex/
  Foundry), requires [Bun](https://bun.sh) installed, and only delivers events while the Claude
  Code session itself stays running (`claude --channels plugin:telegram@...` in a persistent
  process) — which maps cleanly onto ADR-0005's always-on Mac Mini service, but is a different
  mechanism than a standalone Python daemon.

**This changes the real plan for ticket #6** — building a custom `python-telegram-bot` bridge may
be solving an already-solved problem. This is a "why" decision (changes ADR-0005/0006's assumed
mechanism, and the token-location criterion), not something to redesign unilaterally — flagging
for the user, to resolve when ticket #6 resumes, not acting on it now mid-research.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
