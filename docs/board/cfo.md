# CFO

Part of the board (ADR-0013)

## Sources

- [fetched] https://www.baytechconsulting.com/blog/cfos-guide-to-calculating-the-roi-of-custom-software-development-2025 — a concrete CFO framework for evaluating software/engineering ROI: simple ROI, total cost of ownership, opportunity cost treatment, and when to escalate to NPV/IRR
- [fetched] WebSearch: "startup CFO engineering cost evaluation burn rate ROI framing cost of ownership vs one-time cost opportunity cost" — runway/burn-rate formulas and a real worked example of one-time engineering cost vs. ongoing savings payback (cfoadvisors.com, fiscallion.io, kindgeek.com, nstarfinance.com)

## Findings

**The CFO's central move: never evaluate a one-time cost in isolation from its ongoing cost of
ownership.** A cheap-looking build can be expensive to own; an expensive-looking one can pay back
fast if it removes real recurring cost. The question is never "what does this cost to build" but
"what does this cost over its real lifetime, against what it saves or earns."

**Total cost of ownership, broken into the two halves that are easy to undercount:**
- Direct costs: the obvious ones — the build/implementation effort itself, any infrastructure or
  tooling, setup/training.
- Indirect costs, systematically underestimated: ongoing maintenance (commonly 15-25% of build
  cost annually in traditional software, a useful anchor even if this system's cost shape is
  different), upgrades, the cost of things going wrong (downtime, security incidents), and
  **opportunity cost** — what else that engineering time could have produced instead.

**Opportunity cost should be priced, not just gestured at.** The CFO's job is to make "what else
could this effort have gone toward" a real, quantified part of the decision, not an afterthought
— factor engineering/inference time at its real cost, not treat it as free because no invoice
arrives for it.

**ROI framework, applied proportionally to decision size**: start with simple ROI (gain minus
cost, over cost) for anything routine. Escalate to more rigorous treatment — time-value-adjusted
comparisons, payback-period framing — only for decisions large or long-lived enough to justify
the extra analysis effort; applying heavy financial machinery to a small decision is itself a
waste of the same scrutiny the CFO is supposed to be conserving.

**Payback period is the most intuitive, most useful question for a technical decision**: how
quickly does this pay for itself, in whatever unit of cost actually matters here (engineering
time, inference spend, maintenance burden)? A real worked example from the research: an
automation that cost real engineering time paid back in six weeks by eliminating a larger
recurring cost — that's the shape of question the CFO should be asking of every proposed
decision: not just "is this worth it eventually" but "how long until it's worth it."

**Burn-rate thinking, adapted**: runway is cash-on-hand divided by net burn; the equivalent
question for Cimcime's own operation is "at the current rate of decisions like this, how much of
the available budget (token spend, engineering attention) does this consume, and is that
sustainable if repeated." A single expensive decision might be fine; a pattern of them is a burn-
rate problem the CFO should flag even if no single instance looks bad alone.

**Stress-test the assumption, don't just accept the projected number.** Before signing off,
ask what happens to the ROI case if the estimate is wrong by a wide margin - optimistic point
estimates (like "this will roughly pay for itself") deserve a sanity check against the pessimistic
case before being trusted.

## Practitioner notes (you)

(left empty - the user adds their own experience here)
