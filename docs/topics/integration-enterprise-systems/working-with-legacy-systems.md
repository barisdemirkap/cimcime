# Working with Legacy Systems

Category: integration-enterprise-systems · Topic ID: working-with-legacy-systems

## Sources

- [fetched] https://www.guvi.in/blog/working-with-legacy-systems-fde-guide/ — real content.
- [fetched] https://www.future-processing.com/blog/legacy-system-modernisation/ — real content.
- [could not fetch] https://www.youtube.com/watch?v=CKC47S92wA4 — title only, no transcript.

## Findings

**Five obstacles legacy systems actually present** (guvi.in): limited documentation (original
developers often gone, behavior has to be reverse-engineered); difficult integration (rarely
expose APIs — usually file exchanges or direct database access instead, directly echoing
`integration-engineering.md`'s "legacy systems integration" type); accumulated technical debt
(years of quick fixes → unpredictable dependencies); security risk (outdated libraries/auth);
operational risk (critical business processes depend on the system, so changes are inherently
risky even when clearly correct).

**The recommended approach, explicitly cautious** (guvi.in): "understand before changing" — map
the system thoroughly first; talk to actual users about real workflows and pain points (not just
read the code); build small prototypes to test an integration approach before committing;
instrument with monitoring/logging; document discoveries for whoever comes next. Philosophy:
incremental improvement (integration layers, automating manual steps, adding observability,
modernizing one component at a time) over wholesale replacement, specifically to preserve
operational stability.

**A named framework for modernization strategy choice** (future-processing.com, AWS's "7R"
framework, 5 named here): **Rehost** ("lift and shift" to cloud, minimal changes); **Replatform**
(light optimization for a new platform); **Refactor** (rewrite portions for efficiency/
compatibility); **Rearchitect** (redesign for scalability/cloud-native); **Replace** (new
solution entirely). Choice depends on business goals, budget, system complexity, and long-term
roadmap — the article explicitly recommends assessment before committing to one of these, not
defaulting to the most technically elegant option.

**Direct relevance to this system's own experience**: the "understand before changing" principle
and the preference for incremental improvement over wholesale replacement are exactly what this
project's own topic-agents are instructed to do when they hit something unexpected (ADR-0007's
"escalate, don't fabricate or guess" rule) — the FDE discipline and this system's own design
discipline are the same instinct applied to different material (a legacy codebase vs. an
ambiguous research outcome).

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
