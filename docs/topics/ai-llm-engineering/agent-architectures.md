# Agent Architectures

Category: ai-llm-engineering · Topic ID: agent-architectures

## Sources

- [fetched] https://www.ibm.com/think/topics/agentic-architecture — real content.
- [fetched] https://fme.safe.com/guides/ai-agent-architecture/ — real content.
- [could not fetch] https://www.youtube.com/watch?v=FwOTs4UxQS4 — title only, no transcript.

## Findings

**Four factors enabling agent autonomy** (IBM): intentionality (planning/goal-setting),
forethought (anticipating outcomes), self-reactiveness (responding to environment changes),
self-reflectiveness (evaluating and adapting its own performance).

**Three multi-agent coordination patterns** (IBM) — directly names this project's own design:
**vertical** (hierarchical, leader oversight, centralized control — this *is* ADR-0002/0008's
Cimcime→category-agent→topic-agent structure, by name); **horizontal** (decentralized peer
collaboration, parallel processing — explicitly rejected for this system in favor of vertical,
per the ADR-0008 "vertical-only dispatch" decision); **hybrid** (leadership shifts dynamically by
task — not this system's model).

**Framework types by reasoning depth** (IBM): reactive (direct stimulus→action, no learning);
deliberative (reasons over an environment model before acting); cognitive (human-like —
perception, memory, adaptation together). The BDI model (Beliefs-Desires-Intentions) is named as
the canonical cognitive-pattern example.

**Five architectural patterns, independently from fme.safe.com, with real overlap but different
emphasis**: routing-based (rules/semantics/hierarchy/auction/LLM-logic decide what runs next);
ReAct (thought→action→action-input→observation loop); **human-in-the-loop** (approval gates at
critical junctures — this is ADR-0001's three approval gates, named and described independently
by a completely different source); reflective (a self-criticism layer evaluates and refines its
own output — not yet a feature of this system, though `topic-agent.md`'s "never silently skip"
rule is a weaker, rule-based version of the same instinct); multi-agent (specialized sub-agents
per domain, with coordination — same shape as IBM's "vertical" pattern).

**Best practices** (fme.safe.com): favor simple, scalable patterns over clever ones; establish
evaluation metrics early (directly connects to the still-open `prompt-management.md` finding
about this project lacking a formal eval/baseline step); favor prompt engineering over
fine-tuning as the first lever; prioritize data quality; implement guardrails; choose tooling
flexible enough to support multiple LLMs/integrations long-term.

**Direct, concrete relevance to this system**: between the two sources, this topic independently
names and validates essentially every major architectural decision already made —
vertical/hierarchical dispatch (ADR-0002/0008), human-in-the-loop approval gates (ADR-0001), and
multi-agent specialization by domain (the 9 category-agents). It also surfaces one real gap
worth carrying forward: no formal evaluation metrics exist yet for how well a topic-agent's
research actually turns out, echoing `prompt-management.md`'s same finding from a different
angle.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
