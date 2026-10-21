# Debugging Agent Logic

Category: ai-llm-engineering · Topic ID: debugging-agent-logic

## Sources

- [fetched] https://arize.com/glossary/debugging-agents/ — real content.
- [fetched] https://nhimg.org/glossary/ai-agent-debugging/ — real content, complementary security angle.
- [could not fetch] https://www.youtube.com/watch?v=oSjAbx67f0k — title only, no transcript.

## Findings

**Why agent debugging differs from normal debugging** (arize.com): there's usually no stack
trace or exception to point at the bug — you have to "read a transcript of decisions in order
and find the first one that does not follow." Most agent failures aren't actually model
problems; they're "missing scaffolding around the model" — budgets, retries, validation, and
state handling that require real engineering, not a better prompt.

**A concrete 5-step process** (arize.com): find the specific failed run (not aggregate metrics —
surface real session IDs so failures are traceable at all); read the transcript forward,
span by span (prompt → retrieved context → tool call → response), asking "is this output right
given this input?" at each step — the first "no" is the origin of the failure; classify what
kind of failure it is (bad tool selection, malformed arguments, ignored context, control-flow
bug, or infrastructure issue) since each points at a different layer to actually fix; reproduce
using *recorded* state (pinned model version, captured tool responses) rather than replaying
live, since agents generally aren't reproducible through a live replay alone; retain the failing
session as a permanent regression test case so a future model/prompt change can't silently
reintroduce the same bug — the same principle `building-eval-pipelines.md` already named from
the eval side.

**The security/governance angle** (nhimg.org), genuinely different emphasis from arize.com:
debugging requires preserving execution evidence (reasoning artifacts, tool outputs, state
transitions) specifically so a team can later tell whether a failure was the system behaving as
designed or an attacker manipulating inputs — critical once an agent touches sensitive data,
privileged credentials, or non-human identities. Cites OWASP's Agentic AI Top 10, NIST AI RMF,
and CSA MAESTRO as frameworks that treat execution tracing as a governance control, not just a
debugging convenience.

**Direct relevance to this system**: this project already does a version of the "recorded
state, not live replay" principle — every topic-agent run's real fetch results and real
reasoning are captured in a study file's "Findings" and "Sources" sections, not just a final
"researched" status flag. If a topic-agent's output were ever wrong, the study file itself *is*
the reproducible transcript arize.com's process describes reading. What this system doesn't yet
have: a formal regression-test retention step (per `building-eval-pipelines.md`'s same gap) or
any session-ID-level tracing beyond GitHub issue comments — both real, now-doubly-corroborated
gaps rather than single flags.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
