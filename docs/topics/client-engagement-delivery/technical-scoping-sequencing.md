# Technical Scoping & Sequencing

Category: client-engagement-delivery · Topic ID: technical-scoping-sequencing

## Sources

- [could not fetch] https://medium.com/free-code-camp/how-to-effectively-scope-your-software-projects-from-planning-to-execution-e96cbcac54b9 — HTTP 403 Forbidden, consistent with every other medium.com resource in this roadmap.
- [fetched] https://consultingquest.com/insights/scoping-consulting-projects-framework/ — real content.
- [fetched] https://brainsensei.com/glossary/sequence-activities/ — real content.
- [could not fetch] https://www.youtube.com/watch?v=QDLk2QIuJkg — title only, no transcript.

## Findings

**Why scoping is foundational** (consultingquest.com): "getting your scope right is the single
most powerful move you can make to ensure your project delivers results" — framed as the highest
-leverage single decision in a consulting engagement, not one input among many.

**A two-stage scoping framework** (consultingquest.com): **RFP development** — establish
strategic intent/context, frame the *problem* rather than jumping to a solution (the same
instinct `roles-responsibilities.md`'s "find the real obstacle beneath the surface-level
request" already named), define objectives tied to real business decisions, explicitly state
what's in/out of scope, detail deliverables/timelines/milestones, identify internal roles and
support needs, and balance precision against leaving room for innovation. **Negotiation** —
optimize staffing/team composition, cut unnecessary elements via cost-benefit analysis, decide
in-house vs. outsourced delivery, consider alternative engagement models.

**Named mistakes to avoid**: over-scoping (trying too much at once); under-scoping
(insufficient detail); failing to align stakeholders internally before committing; treating
scope as fixed/immutable rather than something that can adapt; dismissing expert input.

**Sequencing, as a distinct discipline from scoping** (brainsensei.com): identifying and
documenting *relationships* between tasks to establish execution order, specifically to avoid
bottlenecks and meet deadlines. Four named dependency types: Finish-to-Start, Start-to-Start,
Finish-to-Finish, Start-to-Finish. Technique named: Precedence Diagramming Method (PDM) plus
visual network diagrams and the Critical Path Method. Common mistakes: misidentified
dependencies, ignored resource constraints, inaccurate time estimates, neglected external
dependencies.

**Direct, concrete relevance to this system**: "sequencing" in this topic's vocabulary is
exactly what ticket #2's "Blocked by" edges already are — Finish-to-Start dependencies, encoded
as GitHub's native issue-dependency feature rather than a Precedence Diagramming Method chart.
The scoping framework's "frame the problem before the solution" and "state what's explicitly out
of scope" principles are the same discipline `/to-spec`'s own template already enforces (its
"Out of Scope" section is a required part of every spec this project produces).

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
