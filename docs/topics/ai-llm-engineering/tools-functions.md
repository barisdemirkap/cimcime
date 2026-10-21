# Tools & Functions

Category: ai-llm-engineering · Topic ID: tools-functions

## Sources

- [fetched] https://huggingface.co/learn/agents-course/en/unit1/tools — real content.
- [could not fetch] https://www.databricks.com/blog/what-is-tool-calling/ai-agent-tools — HTTP 404 Not Found (a broken link in the source roadmap, not a fetch block).
- [fetched, reused] https://www.geeky-gadgets.com/ai-agents-explained-for-beginners/ — same URL already fetched in full under `ai-agents.md` this session; its content (the LLM/workflow/agent sophistication ladder, naming RAG and ReAct) is general background, only thinly specific to tools, so not re-quoted here beyond that connection.
- [could not fetch] https://www.youtube.com/watch?v=h8gMhXYAv1k — title only ("Tool Calling: Connecting LLMs to Your Data"), no transcript.

## Findings

**What a tool is** (huggingface.co): "a function given to the LLM" for a specific purpose — web
search, image generation, data retrieval, API calls. They exist because an LLM is fundamentally
limited to text in/text out with a training-data knowledge cutoff; a tool lets it reach past
that (e.g. a weather tool instead of a hallucinated forecast).

**How tool calling actually works, mechanically**: the model never executes anything itself —
available tools are described in the system prompt (name, purpose, typed inputs/outputs); when a
request matches, the model generates *text representing* a tool call; the surrounding agent
harness parses that text, actually runs the tool, and feeds the real result back into the
model's context for the next step. This is the same mechanism `how-claude-code-works` (from
`claude-code.md`) already described as the five tool categories Claude Code exposes.

**Implementation detail worth keeping**: tools need precise descriptions — function, typed
inputs, typed outputs — and the hugging face material shows a decorator pattern that
auto-extracts this metadata straight from a Python function's signature and docstring, rather
than hand-writing a separate schema.

**Direct relevance to this system**: this project's own `cimcime/cli.py` commands
(`get-topic`, `update-status`, `flag-needs-better-sources`, `category-status`,
`category-rollup`, `phase-check`, `get-phase`/`set-phase`, `seed`) are exactly this pattern,
just implemented as a CLI the agent calls via Bash rather than a native tool-call API — each
command has a narrow, typed, well-described purpose (the Standards review in ticket #4 explicitly
flagged and fixed the one case, `category-rollup`, where a command's name didn't honestly
describe its side effect — the same "precise description" discipline this topic names as a
best practice).

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
