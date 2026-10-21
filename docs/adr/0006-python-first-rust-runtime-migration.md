---
status: accepted
---

# Build the state-store adapter and Telegram bridge in Python first, with an explicit intent to port the always-on runtime to Rust

The state-store adapter and Telegram bridge (the only real "code," as opposed to agent prompts)
are built in Python first, for iteration speed and because it matches music-pipeline's existing
convention. This is a deliberate first step, not the final answer: the always-on Mac Mini runtime
(the persistent `launchd` service — Telegram listener + state-store writes) is intended to be
ported to Rust once the design is stable, to cut the memory footprint of a process that runs 24/7
alongside local model inference on a 16GB machine. Agent definitions themselves (orchestrator,
category-agents, the generic topic-agent) are Claude Code prompt files either way and are
unaffected by this migration.

## Consequences

The state-store adapter's interface (ADR-0004) should be designed with a Rust port in mind: avoid
Python-only idioms that don't translate (e.g. prefer explicit schemas/typed structures over loose
dicts), so the eventual rewrite is a port, not a redesign.
