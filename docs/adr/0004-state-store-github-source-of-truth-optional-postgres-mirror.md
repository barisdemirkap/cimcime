---
status: accepted
---

# GitHub Issues/markdown is the state-store source of truth; a local Postgres mirror is optional and independently toggleable

All tracking and coordination state — per-topic progress, category rollups, reusable knowledge —
lives in GitHub Issues (one per topic, nested under a per-category tracking issue, the same
map-and-children pattern `/wayfinder` uses) plus this repo's own `GLOSSARY.md` and `docs/adr/`.
This travels with the repo (clone it, you have full history; diffable via `git log`), which matters
because this repo is itself a template meant to be reused. A local, self-hosted Postgres instance
(Docker, no cloud account, no spend) is an optional secondary mirror for offline use and richer
queries as the topic graph grows. Each backend is controlled by its own config flag and must be
individually disable-able without breaking the system; GitHub is on by default, Postgres is off by
default. If the two ever disagree, GitHub/markdown wins.

## Considered options

- Postgres as the sole source of truth (rejected — doesn't travel with a template-repo clone, adds
  hosting/credential surface area that conflicts with the "no real spend yet" sandbox scope).
- No database at all (rejected — the user wants the option available for offline/analytics use once
  the project grows; building the adapter now costs little and avoids a later rewrite).
