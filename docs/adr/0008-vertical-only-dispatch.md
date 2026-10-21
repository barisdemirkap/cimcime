---
status: accepted
amends: ADR-0002
---

# Dispatch is vertical (a parent dispatches its own children), not orchestrator-only

ADR-0002 originally said "only Cimcime dispatches subagents directly." Ticket #4's own acceptance
criteria ("running one category-agent against its full topic list dispatches the topic-agent for
each of its topics") assumed otherwise, and that ticket's breakdown was already approved. Rather
than silently pick a side, this was escalated and decided: **a parent may dispatch its own
children** — Cimcime → a category-agent, a category-agent → its own topic-agents — but never
sideways (one category-agent invoking another category's topic-agents) and never skipping a
level (Cimcime invoking a topic-agent directly, bypassing its category-agent). The spirit of
ADR-0002 — respect the hierarchy, no freeform cross-calling — holds; only the "centralize every
dispatch in one place" reading of it was too strict.

## Consequences

Category-agent definitions need `Agent`-dispatch tool access, not just `Read`/`Write`/`Bash`.
Non-dispatch coordination (status, findings, rollups) still goes through shared state
(`StateStore`, per ADR-0004) exactly as ADR-0002 described — this amendment only changes who may
call the Agent tool, not how topics/categories read or write their state.
