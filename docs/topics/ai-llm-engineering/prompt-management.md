# Prompt Management

Category: ai-llm-engineering · Topic ID: prompt-management

## Sources

- [fetched] https://www.braintrust.dev/articles/what-is-prompt-management — real content.
- [fetched] https://humanloop.com/blog/prompt-management — real content, independently confirms braintrust.dev.
- [could not fetch] https://www.youtube.com/watch?v=Qddc_DNo9qY — title only, no transcript.

## Findings

**What it is, converging definition from two independent sources**: treating prompts as
production assets — versioned, reviewed, tested, deployed independently of application code —
rather than static text embedded directly in a codebase. humanloop.com's phrasing: "the
systematic approach to creating, storing, versioning, and optimizing prompts for LLM
applications."

**Problems this discipline solves** (braintrust.dev): version chaos (prompt variants scattered
across repos/docs with no clear "which one is live"); deployment friction (a prompt embedded in
code needs a full app redeploy for a wording tweak); quality invisibility (anecdote-driven
changes with no measurable before/after validation).

**Five converging practices across both sources**: versioning (immutable, diffable, each change
identified); cross-functional collaboration (role-based access, review workflows — explicitly
including non-engineers like product managers and domain experts, not just engineers);
staged/safe deployment (dev → staging → production, automated quality gates); quality control
via evaluation datasets and baselines (test before *and* after a change, not just before);
production monitoring (live-traffic evaluation feeding back into future iterations).

**Direct relevance to this system — a real gap worth naming**: this project's own "prompts" (the
9 category-agent `.md` files, `topic-agent.md`, `cimcime.md`) are currently version-controlled
via plain git, which covers *versioning* but has none of the other four practices: no staged
deployment (an agent-file edit takes effect immediately on next invocation, no dev/staging gate),
no evaluation dataset or baseline (edits like the ADR-0007/ADR-0008 corrections were reactive
fixes after an observed problem, not caught by a pre-existing eval), and no structured
non-engineer collaboration workflow (there's only one "editor" in this project so far). This is
a legitimate, concrete finding about this project's own maturity level versus documented best
practice — not something to fix unilaterally, but worth surfacing.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
