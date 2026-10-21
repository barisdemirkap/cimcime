# Vibe Coding

Category: ai-coding-tools · Topic ID: vibe-coding

## Sources

- [fetched] https://roadmap.sh/vibe-coding/tutorial — real content, a worked Claude Code task-manager tutorial.
- [fetched] https://roadmap.sh/vibe-coding/best-practices — real content, 10 concrete practices.
- [fetched] https://roadmap.sh/vibe-coding/best-tools — real content, a ranked tool list.
- [could not fetch] https://www.youtube.com/watch?v=Y68FF_nUSWE — title only, no transcript.

## Findings

**What it is**: describing desired functionality in natural language and letting an AI tool
generate the implementation, rather than writing code line by line — framed as lowering the
barrier to software creation for non-coders and experienced developers alike, with the human
acting as supervisor for quality and consistency rather than as the one typing every line.

**The workflow** (tutorial, using Claude Code as the worked example): initialize git + a lean
`CLAUDE.md` with project context/tech-stack/conventions → use Plan Mode to outline steps before
any code is written → break work into discrete, incremental prompts (one feature at a time) →
test each feature before moving on → use `/rewind`/`/clear` for error recovery rather than
starting over.

**10 best practices, several directly matching conventions this very repo already follows**:
keep context files under ~50 lines (this repo's `CLAUDE.md` is already short); `/clear` between
discrete tasks to avoid context bleed; always Plan Mode before generating code; scoped prompts
with explicit goals/constraints/exclusions rather than open-ended asks; point at reference files
instead of describing style verbally; review every diff for deleted files, API changes, new
dependencies, and off-limits touches; test/typecheck/lint immediately after accepting changes;
**declare off-limits zones for sensitive code (auth, payments, migrations)** — this is the same
shape as this system's own ADR-0001 approval gates, just applied to code regions instead of
action categories; require written approval for schema/migration changes before implementation;
save recurring prompt patterns as reusable skills in `.claude/skills/` — exactly this repo's own
Matt Pocock skill set, already installed.

**Best-tools ranking** (2026, this specific source): Claude Code, Gemini CLI, OpenAI Codex (on
GPT-5.3), Cursor, Windsurf, Lovable, Bolt.new, v0, GitHub Copilot, Replit — split into **AI app
builders** (Lovable/Bolt/Replit: generate and host complete apps, no coding needed) vs. **AI
coding assistants** (Cursor/Claude Code: integrate into a real dev environment to help engineers
ship faster). Selection criteria given: skill level, deployment preference, pricing model, and
prototype-vs-production intent.

**Direct relevance to this system**: "vibe coding best practices" is effectively a description of
how this entire Cimcime project has actually been built so far in this session — plan before
building (the `/grill-with-docs` interview before any code), scoped incremental work (one ticket
at a time via `/implement`), reviewed diffs (`/code-review`'s two-axis review before every
commit), and off-limits zones (ADR-0001's three approval gates). This topic is less "new
information" and more independent confirmation that the working method already in use matches
documented best practice.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
