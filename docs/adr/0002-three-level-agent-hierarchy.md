---
status: accepted
---

# Three-level agent hierarchy: orchestrator, category-agents, topic-agents

Cimcime (orchestrator) dispatches ~9 category-agents, one per functional domain in the roadmap.sh
Forward Deployed Engineer path; each category-agent coordinates its own topic-agents, one per
individual roadmap topic (~97 total). Only Cimcime dispatches subagents directly — category- and
topic-agents never call each other, they coordinate asynchronously through shared repo state (see
ADR-0004). A flat single-level design was rejected as too generic for the granularity the work
needs; a 4th hierarchy layer was considered and explicitly deferred — revisit only if the project
substantially outgrows this shape.
