---
status: proposed
---

# Voice assistant and any rich UI stay deferred; when built, prefer native desktop apps over a web UI

Cimcime's Jarvis-style voice assistant and any accompanying visual interface remain deferred
(reaffirming ADR-0005's original deferral) — Telegram and the CLI stay the only interfaces for
now. When this work does resume, the UI should be native desktop applications (macOS
`.pkg`/`.dmg`, Windows `.exe`) that run only locally, not a browser-based web UI.

## Considered options

- A web UI (custom app talking to Claude via the Agent SDK, with a Jarvis-style HUD and an
  embedded mic/voice mode) — discussed and designed in some detail (single always-reachable
  surface, cloud STT/TTS, one consistent persona across text/voice) before any code was
  written, then dropped in favor of native apps.
