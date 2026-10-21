# OpenCode

Category: ai-coding-tools · Topic ID: opencode

## Sources

- [fetched] https://opencode.ai/v2/docs/ — real content, the official docs.
- [fetched] https://opencode.school/ — real content, a dedicated learning site.
- [fetched] https://roadmap.sh/claude-code/vs-opencode — real comparison content.
- [could not fetch] https://www.youtube.com/watch?v=QzqaZshQcJI&t=91s — title only, no transcript.

## Findings

**What it is**: a free, open-source (MIT) AI coding agent, available as terminal CLI, desktop
app, and web interface, installable via npm/Homebrew/Bun/standalone binary or Docker. Model-
agnostic by design — connects to 75+ LLM providers directly, including local models via Ollama.

**vs. Claude Code, the real architectural and licensing split** (roadmap.sh): Claude Code is an
integrated, proprietary, Anthropic-only tool with native subscription support and minimal setup;
OpenCode is a client-server (headless server, built for async/remote use), open-source,
model-agnostic tool that requires choosing your own provider/model, with real local/offline
execution via Ollama — explicitly called out as relevant "for regulated industries." One notable
fact: "as of early 2026, OpenCode dropped OAuth support," now requiring API keys instead of
subscription login — a real, dated change worth knowing before recommending it to a client who
expected subscription-style billing.

**The agent-workflow model** (opencode.school): built around **Plan** and **Build** agents as a
named workflow, with session management (resuming conversations) and workspace features for
parallel project work — conceptually close to this very system's category-/topic-agent split, and
to Claude Code's own plan-mode/execute-mode distinction.

**Why this matters for an FDE specifically**: OpenCode's local-model/offline capability is the
concrete answer to a real client constraint that Claude-Code-style cloud-only tools can't satisfy
— a regulated-industry client who can't send code to any external API at all. This is a genuine,
non-trivial tool-selection factor an FDE needs to know, not just a feature checkbox.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
