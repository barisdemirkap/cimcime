---
status: accepted
---

# The runtime is portable: whatever runs on the Mac mini runs on a Linux VM

Owner request (2026-11-23): the solution produced on the Mac mini with Claude Code must also run on VMs.

- Service installers already cover launchd, systemd --user and Task Scheduler (`cimcime service install`).
- A headless Linux VM needs three extra things: the `script` pty wrapper, systemd linger so the user service outlives logout, and a one-time Claude Code sign-in. `cimcime doctor` checks the first two on Linux; `service install` enables linger; `docs/VM.md` covers the sign-in.
- One Telegram token has one poller: two hosts must not share a token.
- Using an API key instead of a subscription login is real spend, so it stays the owner's decision (ADR-0001 gate).
- Not yet verified on a real VM; the unit rendering and the doctor checks are unit-tested.
