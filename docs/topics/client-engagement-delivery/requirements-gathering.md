# Requirements Gathering

Category: client-engagement-delivery · Topic ID: requirements-gathering

## Sources

- [fetched] https://www.coursera.org/learn/requirements-gathering-in-business-analysis — real content, course structure.
- [fetched] https://www.jamasoftware.com/requirements-management-guide/requirements-gathering-and-management-processes/what-is-requirements-gathering/ — real content, the substantive guide.
- [could not fetch] https://www.youtube.com/watch?v=8EBWxW5Cn1g — title only, no transcript.

## Findings

**What it is, precisely** (jamasoftware.com): identifying, documenting, and organizing what a
system must accomplish, giving engineering a shared understanding *before* design/development
starts. A useful terminology distinction drawn here: **elicitation** is actively pulling needs
from stakeholders via specific methods; **gathering** is the broader umbrella — elicitation plus
stakeholder identification, analysis, documentation, validation, and sign-off.

**Why it matters, with real numbers**: inaccurate requirements gathering was responsible for
37% of project failures (cited research); errors caught late can cost "hundreds of times more"
to fix than the same error caught during requirements work — the same economic logic
`roi-ai-impact.md` and `last-mile-integration.md` already established about baselines, just
quantified here for the requirements phase specifically.

**Five complementary elicitation techniques**: interviews (uncover tacit assumptions one-on-one);
cross-functional workshops (resolve competing priorities between teams in real time);
observation (watch actual users work — reveals environmental constraints a conversation alone
would miss); prototyping (concrete mockups let stakeholders react to something real instead of
an abstraction — the same role `prototype.md`-style throwaway builds play in software design
generally); surveys (structured input at scale, validates patterns/quantifies need across a
large or distributed group).

**Best practices**: write *verifiable* requirements (testable, not vague); check quality while
authoring, not just at the end; maintain shared documentation standards; build traceability in
from the start rather than retrofitting it after the fact.

**Course structure for the discipline as a whole** (coursera.org, Microsoft's Business Analyst
certificate): business case formulation (gap/impact analysis) → stakeholder requirements
gathering (scenario analysis, modeling) → formal documentation (user stories, UML diagrams) →
synthesis project. Distinguishes functional vs. non-functional requirements explicitly as a
named skill.

**Direct relevance to this system**: the entire `/grill-with-docs` session that designed this
very project (captured in `GLOSSARY.md` and `docs/adr/`) *is* requirements gathering in this
topic's vocabulary — rounds of interview-style elicitation, with each settled decision
documented as it crystallized rather than retrofitted afterward, matching the "build
traceability in from the start" best practice named here.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
