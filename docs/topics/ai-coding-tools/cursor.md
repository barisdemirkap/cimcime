# Cursor

Category: ai-coding-tools · Topic ID: cursor

## Sources

- [fetched] https://cursor.com/docs — real content, the official docs.
- [fetched] https://roadmap.sh/claude-code/vs-cursor — real comparison content (another instance of a roadmap.sh sub-page partially rendering, like `claude-code.md` noted).
- [could not fetch] https://www.youtube.com/watch?v=3289vhOUdKA — title only, no transcript.
- [could not fetch] https://www.youtube.com/watch?v=ocMOZpuAMw4 — title only, no transcript.

## Findings

**What it is**: Cursor's own framing: "a coding agent for building ambitious software" — a VS
Code fork with an integrated AI agent, not a terminal tool. Supports multiple model providers
(Anthropic, OpenAI, Google, others) with a choice of model per task, up to 1M-token context on
some models. Integrates with GitHub, GitLab, Azure DevOps, Slack, Linear.

**Claude Code vs. Cursor, the core philosophical split** (roadmap.sh comparison page): Claude Code
is "the one you hand work to" (autonomous, terminal-based, "go do this for me"); Cursor is "the
one you stay with" (IDE-native, "help me write this," you review changes as they happen).
Concretely: Claude Code "executes full tasks across the codebase start to finish" and "dynamically
explores the codebase during task execution"; Cursor "assists code writing and editing in real
time" and "pre-indexes the entire codebase for fast suggestions." Risk profile differs
accordingly: Cursor is framed as lower operational risk (you review before changes land) vs.
Claude Code as higher operational risk (autonomous execution needs monitoring, but moves faster
on well-scoped tasks).

**Direct relevance to this system**: this autonomy/risk framing is close to this system's own
ADR-0001 autonomy model — Cimcime is explicitly built in the "hand it work, it executes
autonomously" mode (Claude Code's own described mode), with the three approval gates as the
analogue to "needs monitoring" rather than "review every change." The FDE's own tool choice
(which assistant for which task) is itself informed by this exact tradeoff: delegate fully-scoped
autonomous work to a Claude-Code-style tool, keep a Cursor-style stay-with-it tool for exploratory
or high-stakes edits you want to watch happen.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
