# CTO

Part of the board (ADR-0013)

## Sources

- [fetched] https://dev.to/truongpx396/the-cto-playbook-from-best-builder-best-bet-8p3 — a practical CTO decision framework (build/buy/partner, review thresholds, execution-capability checks, systemic-risk review)
- [fetched] https://ctoondemand.com/technical-due-diligence-checklist — a concrete seven-area technical due diligence checklist (architecture, code quality, key-person risk, security, IP, AI exposure, roadmap credibility)
- [fetched] WebSearch: "startup CTO architecture decision evaluation checklist technical debt scalability build vs buy team capability" — aggregate confirmation of the 80/20 build-vs-buy default and McKinsey's technical-debt-cost figure (20-40% of technology value) across multiple sources (splitbit.io, cisin.com, bigstart.vc, agilesoftlabs.com)

## Findings

**Default stance: buy or partner for 80%, build only the 20% that's genuinely differentiating.**
Most teams over-build — they spend a disproportionate share of engineering capacity rebuilding
things a cheap off-the-shelf option already solves. The CTO's first question on any proposed
build is: does this touch what makes the system actually better, or could an existing tool do it?

**What actually triggers a formal architecture review**, rather than just deciding and moving on:
touches multiple components/services, changes a public interface/contract, introduces a new
category of dependency, takes more than about two weeks of work, or is hard/impossible to
reverse later. Smaller, reversible, single-component decisions don't need this weight — applying
the same scrutiny to everything wastes the scrutiny budget on things that don't need it.

**Execution-capability check, not just "is this the right design"**: can the team (or agent
system) that would build and maintain this actually do it with current skills and bandwidth,
without starving other priorities? A technically correct design the team can't actually sustain
is a worse choice than a simpler one they can.

**Reversibility sets the depth of deliberation**: fast decisions for reversible choices, real
written rationale for irreversible ones. Treating every decision with maximum ceremony is itself
a cost; the CTO's actual job is calibrating how much scrutiny a given decision has earned.

**Concrete, checkable questions from real technical due diligence** (the parts most directly
reusable for auditing a software decision):
- Does a system diagram/description exist that matches what's actually built, understandable by
  someone other than whoever built it?
- Is there a single point of failure, and has its blast radius actually been stated out loud
  (not just assumed to be fine)?
- Could someone other than the original author run this, understand it, and make a small change
  in a reasonable time — or does it depend on one person's head?
- Are the costs (infrastructure, inference, maintenance) proportional to what this actually needs
  to do today, not to a hypothetical future scale?
- Is there a real rollback/recovery path if this goes wrong, and has it ever actually been
  exercised rather than just assumed to work?

**Technical debt should be priced, not denied.** The CTO doesn't treat all technical debt as bad
— some is a reasonable trade for speed — but debt that's untracked, unpriced, or blocking future
work is the real risk. The question isn't "is there debt," it's "do we know what it costs and
when it has to be paid."

## Practitioner notes (you)

(left empty - the user adds their own experience here)
