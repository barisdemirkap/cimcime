# ROI & AI Impact

Category: business-strategy · Topic ID: roi-ai-impact

## Sources

- [fetched] https://www.ibm.com/think/insights/ai-roi — real content.
- [could not fetch] https://www.esade.edu/beyond/en/what-is-roi-and-how-to-calculate-return-on-investment/ — HTTP 403 Forbidden.
- [fetched] https://miragemetrics.com/guides/forward-deployed-engineering — real content, specifically about FDE-style engagements, not generic ROI theory.

## Findings

**Hard vs. soft ROI** (IBM): hard ROI is tangible financial outcome (lower labor cost,
operational efficiency, revenue), soft ROI is indirect (employee satisfaction, better decisions,
customer experience). This directly corroborates `business-acumen.md`'s finding from a
completely different source (fdetimes.net) — the same hard/soft ROI distinction and the same
"only 25% of AI initiatives deliver expected returns" statistic appear in both, which is a useful
cross-source confirmation rather than a coincidence: it's apparently a widely-cited figure in this
space, not an outlier claim from one source.

**Why ROI is hard to realize** (IBM): organizational barriers (culture, governance, data
strategy) outweigh technical limitations; only 29% of executives confidently measure AI ROI
despite 79% observing productivity gains — a measurement gap, not necessarily a value gap; only
16% of AI initiatives scale enterprise-wide; narrow one-off pilots rarely produce real financial
impact; legacy technical debt alone can cut AI ROI by up to 29%.

**What this looks like concretely for an FDE engagement** (miragemetrics.com — the most
directly relevant source, written specifically about FDE-style work): the real difficulty in an
industrial AI project "rarely lies in the model" but in data access, exception handling, and
system integration — AI's value only shows up once it's "connected to the data, rules and systems
of a specific company." Five concrete metrics an FDE should track through a deployment: time to
proof-of-concept (example given: one week after the first meeting), time to production (4-6 weeks
for the first real workflow), automation rate (% processed without human intervention), exception
rate (cases needing human review), and hours reclaimed (a concrete example given: 80-90% less
time on a specific manual task).

**Honest-measurement principles** (miragemetrics.com): establish a baseline *before* deployment
(the same point `business-acumen.md` made independently from fdetimes.net — this is now a
twice-corroborated practice, not a one-off opinion); track exceptions alongside successes, not
just the success rate alone; validate quality via sampling rather than assuming; prefer systems
that flag their own uncertainty rather than silently guessing.

**Direct relevance to this system**: "prefer systems that flag doubts rather than improvise
answers" is close to this very project's own design principle (ADR-0007: a topic-agent records
"could not fetch" honestly rather than fabricating a finding, and escalates genuine uncertainty
rather than guessing). The FDE literature and this system's own architecture converge on the same
idea from different directions.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
