# Data Privacy & Compliance

Category: data-engineering · Topic ID: data-privacy-compliance

## Sources

- [fetched] https://www.theforwarddeployed.io/production/security-compliance — real content, FDE-specific.
- [fetched] https://www.salesforce.com/platform/data-privacy-compliance/what-is-data-privacy-compliance/ — real content, general framework overview.
- [could not fetch] https://www.youtube.com/watch?v=N8xEgSe5RwE — title only, no transcript.

## Findings

**The core framing, FDE-specific** (theforwarddeployed.io) — the sharpest line in this topic:
"the environment is the constraint." Regulatory requirements shape the system's architecture
from day one, not after the fact: where data physically lives, who can access it, what gets
logged, and whether the system can reach the public internet at all.

**Four concrete design areas an FDE must address** (theforwarddeployed.io): **data residency/
retention** (customers often require in-region data that never trains a third-party model — a
constraint that cascades through the whole system design); **sensitive-data handling** (PII must
be redacted/tokenized before it reaches a model *or* a log — including debugging traces and eval
records, which are easy to overlook); **access control** (the AI system must inherit the
customer's own permission model — a user must never retrieve through an assistant what they
couldn't retrieve directly); **auditability** (regulated environments need a reconstructible
decision trail: what was retrieved, which prompt was used, who saw the output).

**Four named regulatory regimes and what each actually requires** (theforwarddeployed.io):
**GDPR** — lawful basis, data minimization, an erasure path, human review of automated decisions;
**HIPAA** — a Business Associate Agreement before any health data flows, plus audit controls;
**SOC 2** — documented controls for access, change management, monitoring; **EU AI Act** —
lifetime event logging and human oversight for high-risk systems, with deadlines running through
2028.

**General framework context** (salesforce.com): three foundational principles across most privacy
law — consent before collection, transparency about use, and the individual's right to access/
correct/delete their own data. Named frameworks beyond the four above: CCPA (California — fines
tied to data sales/opt-out rights), LGPD (Brazil), PIPEDA (Canada), Australia's Privacy Act,
FERPA (US education). Concrete cost figure: non-compliant breaches cost organizations ~$220,000
more on average than compliant ones.

**Direct relevance to this system**: "the environment is the constraint" is the same principle
underlying ADR-0001's three approval gates — this system was deliberately built *not* to touch
production, real third parties, or real spend until the environment (sandbox, this repo) proves
the pattern works, precisely because changing those constraints later is expensive, exactly as
this topic describes for a real client engagement.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
