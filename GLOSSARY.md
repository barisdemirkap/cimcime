# Glossary

## Cimcime

The orchestrator agent and persona of this self-learning Forward Deployed Engineer system — the
top-level entity the user invokes directly (e.g. via Telegram or CLI). Dispatches category-agents
(its direct children), and owns the system's lifecycle (see **Learning Phase** / **Runtime
Phase**). Does not dispatch topic-agents directly — that's each category-agent's own job, per
ADR-0008's vertical-only dispatch rule.

## Category-agent

A subagent scoped to one of the functional domains derived from the roadmap.sh Forward Deployed
Engineer path (e.g. AI & LLM Engineering, Client Engagement & Delivery, Platform/Infra). Dispatches
and coordinates the topic-agents within its own domain only (ADR-0008: never another category's
topic-agents), and rolls their aggregate status up into its category tracking issue. There are ~9
category-agents.

## Topic-agent

A subagent scoped to exactly one roadmap.sh topic (~97 total, one per topic in
`docs/research/forward-deployed-engineer-roadmap.md`). Owns the deep-dive learning for that single
topic: reading every linked resource, writing findings to that topic's study file, and holding its
own tracking issue state.

## Needs-better-sources

A topic whose linked resources turned out to be entirely unfetchable (per ADR-0007) — distinct
from a plain `needs-research` topic, which just hasn't been attempted yet. Tagged
`fde:needs-better-sources`, stays at `needs-research` status rather than being marked
`researched` on an empty study file.

## Approval gate

An explicit point requiring the user's sign-off before Cimcime proceeds, regardless of its general
autonomy. Exactly three gates exist:

1. Production-level delivery/deployment
2. Outbound communication to a real third party (client, vendor, stakeholder)
3. Any action that spends real money or changes external account/billing settings

Outside these three, Cimcime acts autonomously using logic and analysis; the standing rule is that
**execution ("how") is Cimcime's job, rationale ("why") is the user's**.

## Learning Phase (Phase 1)

The bootstrap period during which Cimcime runs continuously on its host machine, working
topic-agents through the entire roadmap.sh Forward Deployed Engineer path on its own — unprompted,
autonomous — until every topic-agent has completed its deep-dive. Ends when the full roadmap is
researched.

## Runtime Phase (Phase 2)

The steady-state period that begins once the Learning Phase completes. Cimcime does no unprompted
background work in this phase; it acts only when invoked (a Telegram message or a CLI command).

## State store

The pluggable persistence layer for Cimcime's tracking and coordination data. GitHub Issues (one
per topic, nested under a per-category tracking issue) plus this repo's own markdown
(`GLOSSARY.md`, `docs/adr/`) are the **source of truth**. A local, self-hosted Postgres instance is
an optional secondary mirror for offline use and analytics, independently toggleable, off by
default. If the two ever disagree, GitHub/markdown wins.

## Model backend

The pluggable inference layer an agent calls into to do its reasoning. Claude, via Claude Code, is
the default and only backend in the initial build. A self-hosted Hermes model (NousResearch, run
locally via Ollama) is a planned optional secondary backend for low-stakes, non-critical subtasks —
deferred until after the core product is finished.
