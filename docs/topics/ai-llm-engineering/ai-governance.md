# AI Governance

Category: ai-llm-engineering · Topic ID: ai-governance

## Sources

- [fetched] https://www.ibm.com/think/topics/ai-governance — real content.
- [fetched] https://www.databricks.com/blog/ai-governance-best-practices-how-build-responsible-and-effective-ai-programs — real content.
- [could not fetch] https://www.youtube.com/watch?v=4QXtObc61Lw — title only, no transcript.
- [could not fetch] https://www.youtube.com/watch?v=Q020C-Jw0o8 — title only, no transcript.

## Findings

**What it is** (IBM): the processes, standards, and guardrails that keep AI systems safe and
ethical — directing research/development/deployment while maintaining compliance and protecting
sensitive data, balancing innovation against risks like bias, privacy violation, and misuse.

**IBM's four guiding principles**: empathy (consider societal implications beyond the
technology itself); bias control (rigorously examine training data for discriminatory
outcomes); transparency (explain how the system reaches its conclusions); accountability
(organizations own AI impacts across the system's whole lifecycle, not just at launch).

**Structural elements** (IBM): dashboards, automated drift/anomaly monitoring, performance
alerts, audit trails, integration with existing infrastructure — built for continuous oversight
without constant manual checking.

**Databricks' six pillars** — a more operational, enterprise-scale framework than IBM's
principle-level one: fairness/bias mitigation, transparency/explainability, accountability with
clear ownership, privacy/security, built-in safeguards against harmful output, unified access
controls. The practical recommendation that matters most for an FDE: **align governance with
actual business risk level rather than applying uniform controls everywhere** — risk
assessments determine oversight intensity, and **approval pathways should match risk tiers**.
This is, almost verbatim, the shape of ADR-0001's design: three named, risk-matched approval
gates (production deploy, real third-party communication, real spend/account changes) rather
than a blanket "ask permission for everything" policy or a blanket "do whatever" policy.

**Scaling model** (Databricks): "centralized-federated" — a central team sets standards, domain
teams implement them locally; governance framed explicitly as "a practical foundation for
scaling AI responsibly," not bureaucratic friction, with strong leadership sponsorship as a
cultural prerequisite rather than just a policy document.

**Direct relevance to this system — the clearest and most validating finding to close this
category on**: Cimcime's entire approval-gate design (ADR-0001), its tiered autonomy model
(routine work autonomous, three specific high-risk actions gated), and its "AI owns how, human
owns why" principle are a working instance of exactly what both sources describe as AI
governance done well — risk-tiered controls, not uniform friction, with clear accountability
boundaries. This closes out `ai-llm-engineering` on a note that directly validates the project's
own foundational architecture decision, made all the way back in the very first grilling
session, before any of this roadmap research existed to confirm it.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
