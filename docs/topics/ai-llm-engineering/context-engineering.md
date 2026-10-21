# Context Engineering

Category: ai-llm-engineering · Topic ID: context-engineering

## Sources

- [fetched] https://www.ibm.com/think/topics/context-engineering — real content, the general overview.
- [fetched] https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — real content, Anthropic's own practitioner guidance.
- [could not fetch] https://towardsdatascience.com/deep-dive-into-context-engineering-for-ai-agents/ — HTTP 403 Forbidden, consistent with every other towardsdatascience.com resource in this roadmap.
- [could not fetch] https://www.youtube.com/watch?v=BBPQYtR7oUk — title only, no transcript.

## Findings

**What it is**: deliberately designing, structuring, and optimizing the information given to an
LLM — a broader discipline than prompt engineering alone, encompassing system prompts,
conversation history, retrieval (RAG), and tool integration together. IBM's framing: "the
quality and structure of the context window directly influence the model's reasoning, tool use
and outputs" — often mattering more than model size.

**IBM's six practices**: context selection (filter relevant info, keep poisoned/false data out);
context structuring (JSON/markdown formatting, few-shot examples); prompt design (clear
instructions, explicit output format); context compression (summarization, dedup, fit more
useful signal per token); context sequencing (instructions first, most-relevant content
prominent); tool/memory integration (how external data enters the working context).

**Anthropic's own practitioner guidance — the most directly relevant source in this whole
category**: the core principle is to "identify the smallest set of high-signal tokens that
maximize desired outcomes," because of **context rot** — performance degrading as the context
window fills, an architectural attention-mechanism limitation, not just a capacity limit. Named
techniques: system prompts balanced between specificity and flexibility (avoid brittle hardcoded
logic *and* vague shared-understanding assumptions); focused, non-overlapping tool design (an
ambiguous toolset actively misleads an agent); curated diverse canonical examples rather than
exhaustive edge-case lists ("examples are the 'pictures' worth a thousand words" for an LLM);
**just-in-time retrieval** (load data at runtime via tools rather than pre-loading everything,
mirroring human cognition, preventing bloat). For long-horizon tasks exceeding one context
window: **compaction** (summarize/compress history, preserve key decisions), **structured
note-taking** (persistent memory outside the context window), and **sub-agent architectures**
(specialized agents handle focused work, return condensed summaries).

**Direct relevance to this system — nearly every technique named here is already a real,
deliberate design decision in this project, not a coincidence**: sub-agent architecture =
ADR-0002/0008's orchestrator→category-agent→topic-agent hierarchy, built specifically so a
topic-agent's 97-topics'-worth of fetched article text never pollutes Cimcime's own context;
structured note-taking = the `docs/topics/*.md` study files (persistent memory outside any
agent's context window); just-in-time retrieval = the lazy, per-topic dispatch this whole
Learning Phase already does rather than front-loading all 97 topics' content at once; focused
non-overlapping tools = the CLI's deliberately narrow commands (`category-status` vs.
`category-rollup` split specifically to avoid one ambiguous command doing two different things,
per the ticket #4 review finding). This topic is less new information discovered and more
independent, authoritative confirmation that this project's existing architecture already follows
the state of the art for exactly this problem.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
