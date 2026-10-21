---
status: accepted
---

# Telegram bridge is Claude Code's built-in Channels plugin, not a custom Python bridge; amends ADR-0005's credential location

The Telegram bridge (ticket #7) is built on Claude Code's official `telegram` channel plugin
(`claude-plugins-official`), not a custom `python-telegram-bot` daemon as originally scoped.
Installed and paired via `/plugin install telegram@claude-plugins-official`,
`/telegram:configure <token>`, `/telegram:access pair <code>`, and
`/telegram:access policy allowlist` — allowlisting to the user's own Telegram ID and the
two-way message bridge both come from the plugin itself, with no custom bridge code to write
or maintain. This amends ADR-0005's "all credentials live in a gitignored `secrets/` directory
on that machine" clause: the Telegram bot token instead lives in
`~/.claude/channels/telegram/.env`, the plugin's own fixed storage location, outside this
repo's `secrets/` convention — every other credential in this project still follows ADR-0005
unchanged.

Two caveats accepted as part of this choice: the Channels feature is a research preview
requiring Anthropic auth via claude.ai or a Console API key (not Bedrock/Vertex/Foundry) and
a [Bun](https://bun.sh) installation; and the bridge only delivers events while a
`claude --channels plugin:telegram@...` session stays running, which maps onto ADR-0005's
always-on Mac Mini service as the host process rather than a separate daemon.

## Considered options

- Custom Python bridge (`python-telegram-bot`) as originally scoped in ticket #7 — rejected:
  duplicates allowlisting and two-way bridging the Channels plugin already provides, and adds
  new code this project would need to maintain indefinitely.
- OpenClaw self-hosted gateway — rejected for this ticket: a real, viable alternative (has its
  own Mac Mini setup docs and strong security guidance), but means standing up and operating a
  second always-on process with its own LLM API costs, on top of the Claude Code session this
  system already runs.
