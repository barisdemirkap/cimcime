# AI Agents

Category: ai-llm-engineering · Topic ID: ai-agents

## Sources

- [could not fetch] https://roadmap.sh/ai-agents — the roadmap.sh landing page, consistent with its client-rendered pages failing.
- [fetched] https://aws.amazon.com/what-is/ai-agents/ — real content.
- [fetched] https://www.geeky-gadgets.com/ai-agents-explained-for-beginners/ — real content.
- [could not fetch] https://www.youtube.com/watch?v=F8NKVhkZZWI — title only, no transcript.

## Findings

**What an AI agent is** (AWS): software that interacts with its environment, gathers data, and
self-directs toward predetermined goals — distinct from traditional hard-coded software because
it determines its *own* path to a human-set objective rather than following a fixed script.

**Workflow** (AWS): goal-setting (break instructions into actionable sub-tasks) → information
gathering (pull data from APIs/external systems) → task execution (complete tasks while
evaluating progress toward the goal). Architecture: a foundation model as the reasoning engine,
plus planning, memory, tool integration, and (sometimes) learning-from-feedback components.

**Named agent types** (AWS), from simplest to most complex: simple reflex (fixed rules);
model-based reflex (evaluates likely outcomes first); goal-based (compares approaches for
efficiency); utility-based (maximizes a scored outcome across scenarios); learning agents
(improve from past experience); **hierarchical agents** (higher-tier agents delegate to
lower-tier ones — this is, structurally, exactly ADR-0002/0008's Cimcime → category-agent →
topic-agent design); **multi-agent systems** (multiple agents collaborating on a distributed
problem — the same pattern `multi-agents.md`, researched earlier in this same category, already
covered from a different angle).

**A useful three-level sophistication ladder** (geeky-gadgets.com), distinct from AWS's
type-taxonomy: **Level 1, LLMs** (generate text from a prompt, no independent action without
external wiring); **Level 2, AI workflows** (automate a fixed sequence, efficient but brittle —
can't adapt to the unexpected without a human); **Level 3, AI agents** ("reason, act, and
iterate" autonomously, analyze situations, use tools/APIs, improve over repeated use). Named
enabling frameworks: RAG (external-data access) and ReAct (interleaving reasoning and action).
The sharp distinction drawn: LLMs give static responses, workflows follow rigid paths, agents
operate with minimal human oversight.

**Where this system sits on that ladder**: Cimcime is explicitly a Level 3 agent system by this
framing — it reasons about which category needs work (`phase-check`), acts (dispatching
subagents, fetching real resources), and iterates (re-checking, re-dispatching) with the explicit
goal of autonomous completion, gated only by the three approval thresholds from ADR-0001 rather
than needing a human in the loop for routine work.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
