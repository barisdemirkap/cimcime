# Prompt Engineering

Category: ai-llm-engineering · Topic ID: prompt-engineering

## Sources

- [could not fetch] https://roadmap.sh/prompt-engineering — the roadmap.sh landing page, consistent with its client-rendered pages failing.
- [fetched] https://www.ibm.com/think/topics/prompt-engineering — real content.
- [could not fetch] https://www.youtube.com/watch?v=2BpCk4d2Cc0 — title only, no transcript.

## Findings

**What it is**: crafting inputs to guide a generative AI model toward a desired output — "good
prompts equal good results." The discipline exists because model output quality is highly
sensitive to how intent and context are expressed, not just what's asked.

**Three named technique families**: **zero-shot** (ask directly, no examples — tests the
model's ability to generalize); **few-shot** (include sample outputs to clarify the expected
shape of the answer); **chain-of-thought** (break a complex task into explicit step-by-step
reasoning to improve accuracy on multi-step problems).

**Best practices**: clear, concise, context-rich prompts; specific instructions plus concrete
examples; iterative refinement based on observed model responses (not a one-shot write); explicit
awareness of model limitations to avoid propagating bias; testing across varied scenarios rather
than one happy-path case.

**Required skill mix**: familiarity with how LLMs actually behave, strong written communication,
programming (Python named specifically), and domain knowledge relevant to the application area.

**Direct relevance to this system**: every one of the 9 category-agent `.md` files and the
`topic-agent.md` definition in this repo is itself a piece of prompt engineering — each uses
exactly the "clear, concise, context-rich" + "specific instructions with examples" pattern this
topic describes (e.g. the literal process steps, the exact CLI commands to run, the exact study
file template). The ADR-0007 amendment to `topic-agent.md` (clarifying that "never silently skip"
applies to articles as well as videos) was a real instance of "iterative refinement based on
observed model responses" — a prompt that worked, was observed to produce an edge-case gap, and
was tightened.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
