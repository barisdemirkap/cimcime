# Tradeoffs: Scope, Speed, Quality

Category: client-engagement-delivery · Topic ID: tradeoffs-scope-speed-quality

## Sources

- [fetched] https://asana.com/resources/project-management-triangle — real content.
- [could not fetch] https://www.youtube.com/watch?v=JHSHOAfV-uw — title only, no transcript.

## Findings

**The "iron triangle"**: scope, cost, and time are interlocking constraints — increase scope,
and time/budget must increase to match; time and cost trade off inversely (compress one, expand
the other). The key structural point: **quality sits at the center of the triangle, not at a
corner** — it's not a fourth independent lever, it's what erodes when the other three are forced
into an unsustainable combination without compensating elsewhere. This is the formal version of
"good, fast, cheap — pick two."

**Practical application**: a project manager's real job here is identifying *which* constraint
actually has flexibility in a given situation, communicating that priority clearly to
stakeholders rather than pretending all three can be optimized at once, and keeping contingency
plans + frequent updates in place since the tradeoff will eventually bite. Methodology framing:
waterfall/lean lean toward resource efficiency; agile/Scrum/Kanban lean toward speed — neither
escapes the triangle, they just pick a different default emphasis.

**Direct relevance to an FDE engagement, and to this system specifically**: every approval gate
in ADR-0001 is a place where this project deliberately chose to trade *speed* (autonomous,
no-ask execution) for *safety/quality assurance* (human review) on exactly the three categories
where getting it wrong is expensive or irreversible — production deploy, real third-party
communication, real spend. That's the iron triangle applied to an AI agent's own operating model:
Cimcime runs fast and autonomously everywhere the cost of being wrong is cheap to reverse (ADR's
"VCS/backup instead of asking"), and slows down for human review exactly where speed would trade
against real, hard-to-recover quality/safety.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
