---
status: accepted
---

# Deployment target is a physical M1 Mac Mini (16GB), Telegram is the human-interface channel, Claude is the only model backend for now

Cimcime runs as an always-on persistent service on a physical M1 Mac Mini (16GB RAM), the same
`launchd`-based pattern as the music-pipeline repo's autopilot. The user reaches it, and it reaches
the user, through a Telegram bot scoped to the user's own Telegram ID — used both for
approval-gate/progress notifications and for issuing remote commands. All credentials (bot token,
etc.) live in a gitignored `secrets/` directory on that machine, never committed or echoed back in
chat or logs. Claude, via Claude Code, is the only model backend in the initial build; a
self-hosted Hermes model (NousResearch Hermes 4.3, run locally via Ollama) is a planned optional
secondary backend for low-stakes, non-critical subtasks, deferred until the core product is
finished. A voice-assistant mode (Jarvis-style) was also discussed and deferred to well after that.
