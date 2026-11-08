---
status: accepted
---

# Claude stays the sole orchestrator; it delegates low-stakes subtasks to Haiku or a local Qwen model, starting with tool-output summarization, to cut token cost

Every Cimcime interaction today runs entirely on Claude, at full cost, for every subtask no
matter how trivial - summarizing a long tool output, classifying a message, drafting text that
will be reviewed anyway. ADR-0005 named a self-hosted Hermes model via Ollama as a planned,
never-built "low-stakes secondary backend." Investigating two sibling projects
(`barisdemirkap/agent-farm`, `barisdemirkap/private-agent-farm`) found a real, already-measured
alternative: `private-agent-farm` runs Qwen3-4B (generation) and Qwen3-Embedding-0.6B natively
via llama.cpp on an M1/16GB Mac - the same hardware class as this system's own Mac Mini - with
real numbers (6.2 GB peak RAM both models loaded, 9-20 s/answer, 0 swap) and a working,
already-adapted-from-elsewhere provider contract (`providers/base.py`, `providers/llama_cpp.py`).
That project also has a bounded, human-gated self-improvement pipeline (propose → experiment →
evaluate → promote/rollback, never auto-merging a candidate, with a protected regression suite
that has already caught one real sabotage attempt) that this decision adapts in miniature.

**Claude remains the only orchestrator and is never bypassed.** No separate gateway process
reads Telegram messages before Claude does - every message still reaches the already-running
`claude --channels plugin:telegram@claude-plugins-official` session first, so conversational
context never breaks. Claude itself decides, per subtask, whether to do the work directly or
hand it to a cheaper backend through one shared tool available to every Cimcime agent (not a
separate tool per agent). That tool can route to Haiku or Sonnet (via the existing Agent tool's
`model` override - no new infrastructure) or to a local Qwen3 model served over llama.cpp,
running as a persistent, always-on `launchd` service on the Mac Mini (the same pattern as the
Telegram bridge's own service), started at the smallest viable size (Qwen3-1.7B, not the 4B
`private-agent-farm` measured) until real free-RAM headroom alongside the Telegram session and
the GitHub Actions runner is confirmed on the actual machine. The llama.cpp provider contract is
copied and adapted into this repo, not a live dependency on `private-agent-farm` - the two
projects should keep evolving independently, and the contract itself is small.

**Hard rule, not a judgment call**: nothing that falls under ADR-0001's three approval gates
(production deploy, real third-party communication, real spend/account change) is ever
delegated, to either Haiku or Qwen. Everything else is Claude's discretion. Qwen's purpose here
is specifically near-zero marginal cost for applicable subtasks, not privacy or latency - data
sensitivity was never the concern raised for this decision.

**Scope for this first version is deliberately narrow: only tool-output summarization/
compression**, applied before a long tool result re-enters Claude's own context. This is the
single task type Qwen's measured reliability (69-72% recall, one observed fabrication in
`private-agent-farm`'s own baseline eval) is adequate for, because it's the lowest-risk
candidate: a bad summary just means Claude re-reads the original (still available, nothing is
destroyed or acted on), and it directly targets the actual cost driver - large tool outputs
bloating Claude's own context - rather than open-ended reasoning Qwen hasn't earned trust for
yet. Classification, drafting, and extraction are explicitly deferred until this narrower case
has real data behind it.

**Every delegation decision is logged**: task description, which backend handled it, timestamp,
and outcome, in a local SQLite table (same `~/.claude/channels/telegram/` storage convention
`message_log.py` already uses, a separate table, not the message-history log itself). This is
intentionally not `private-agent-farm`'s full PostgreSQL job/worker/lease machinery - a
delegation decision is one fast call, not a long-running job needing crash recovery, so a plain
log is enough until proven otherwise. This log is what the self-improvement pipeline (next)
measures against, and what the exit criteria (below) are read from.

**Self-improvement is included now, not deferred, but scoped narrowly**: only the delegation
policy itself (which task type goes to which backend) improves over time, via the same
propose → experiment → evaluate → promote shape `private-agent-farm` already proved out, and
promotion is never automatic - a human approves every change, exactly as in the source pattern.
Cimcime's broader capabilities (category-agent/topic-agent skills) are explicitly out of scope
for this pipeline.

**This sits outside the three-level agent hierarchy (ADR-0002/0008)**: delegating a subtask is
not a dispatch and creates no new agent - it's a tool call any agent in the hierarchy can make
mid-task, governed only by the hard rule above, not by the hierarchy's dispatch rules.

**Exit criteria for this first version**: seven days of real Telegram traffic, zero violations
of the hard rule, and a log-derived report of how many summarization tasks were delegated and
how many required a Claude correction. No fixed dollar savings target yet - real traffic volume
isn't known until this runs for real.

## Considered options

- A separate gateway process that triages messages before Claude ever sees them - rejected:
  breaks conversational context and defeats the always-present-orchestrator model this decision
  is built around; also the entire point of staying in Claude's own `--channels` session.
- Hermes 4.3 via Ollama, ADR-0005's original (never-built) idea - rejected in favor of Qwen3 +
  llama.cpp, the only option with real measured numbers on matching hardware.
- `private-agent-farm`'s full PostgreSQL-coordinated job/worker/lease machinery - rejected for
  this scope: a delegation decision is a single fast call, not a crash-recoverable long-running
  job; a SQLite log is enough until traffic proves otherwise.
- A live dependency (submodule/package) on `private-agent-farm` - rejected: keeps both projects
  independently evolving; the actual provider contract needed here is small enough to copy.
- Self-improvement targeting Cimcime's broader capabilities, not just the delegation policy -
  deferred: no real data exists yet to design that against.
