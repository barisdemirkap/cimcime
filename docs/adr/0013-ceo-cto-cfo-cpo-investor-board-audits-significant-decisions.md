---
status: accepted
---

# A CEO/CTO/CFO/CPO/Investor board sits above Cimcime and audits significant decisions before they're acted on

Settled via a full grilling session with the user across three rounds (autonomy scope, approval
gates, what the team governs, cost, stop condition, hierarchy position, trigger size, role
sourcing). Cimcime gains a five-persona board - CEO, CTO, CFO, CPO, and an Investor - whose job
is specifically to **audit and interrogate** a significant decision Cimcime has already reached,
not to brainstorm or co-decide alongside it. The dynamic is adversarial-by-design in the
Investor's case especially: it questions cost-effectiveness the way a real investor questions a
founder, pushing for a more optimized or cheaper option before signing off. The outcome of a
board review is Cimcime being more confident in a validated decision, or revising it - never the
board deciding *for* Cimcime.

**Hierarchy**: the board sits above Cimcime in decision-authority, not in the dispatch mechanism.
ADR-0002/0008's "Cimcime dispatches category-agents only, never skips a level" is unchanged -
Cimcime remains the one agent that reports to the user. Mechanically, Cimcime invokes the board
(via the Agent tool, the same primitive it already uses to dispatch category-agents) when it
reaches a significant decision; what changes is the *relationship*, not the dispatch rule - the
board's role is oversight of Cimcime, framed as a board auditing a founder, not a subordinate
Cimcime manages.

**What triggers a board review**: only significant decisions - a new feature, an architecture
change, or real resource spend. The UI/UX redesign pass just completed on FarmWatch is the
user's own worked example of the kind of decision this is for. Routine work - bug fixes, small
patches, answering a question - never goes through the board; the added cost and latency
wouldn't be justified, and "decision or change" is the line, not task size alone.

**ADR-0001's three approval gates are completely unchanged.** Production deploy, real
third-party communication, and real spend/account change still require the user's prior
approval exactly as before - the board is a separate, additional quality layer for significant-
but-not-necessarily-gated decisions (e.g. an architecture choice that spends no money and
touches no third party still gets board scrutiny; it just doesn't *also* need a pre-approval gate
unless it independently crosses one of the three).

**Operating rhythm is cyclic and user-gated, not unchecked continuous execution.** Cimcime may
start a review cycle on its own initiative and have the board deliberate - that part is
autonomous. But nothing a cycle concludes is acted on until it's presented to the user, board-
meeting-style, and approved. Approval lets that cycle's decisions proceed and the loop advances
to the next cycle; a "improve this" response keeps the same cycle going with that feedback
folded in. The autonomy is in starting cycles and doing the deliberation work, never in acting on
their output unapproved.

**No defined completion state.** Unlike Learning Phase's 97-topic roster with a clear "complete"
trigger (ADR-0003), this has none - "final product" is a continuously receding target the board
and Cimcime re-assess each cycle, not a finish line. The loop runs for as long as the user keeps
engaging with it.

**Cost**: the board's internal back-and-forth (the Investor's cost-effectiveness questioning,
the CTO/CFO/CPO's own challenges) routes through ADR-0012's delegation tool to cheap/local
backends wherever the question is structured enough for that - the same decision-model shape
`private-agent-farm`'s own `DecisionProvider` protocol already uses (`decide(allowed_outcomes,
context) -> outcome`), not a full Claude conversation for every back-and-forth. Full Claude is
reserved for the decision Cimcime ultimately stands behind and the summary actually shown to the
user - running an entire C-suite debate at full price on every significant decision would
undercut the exact cost discipline ADR-0012 was just built for.

**Role definitions are researched, not invented.** Each of the five personas gets defined the
same way Learning Phase already researches an FDE topic - real web research via the existing
infrastructure, written up as reference material under `docs/`, provenance kept - rather than
Claude inventing what a CFO does from priors. This reuses proven infrastructure instead of
building a second research mechanism.

## Considered options

- Board as an internal council Cimcime consults *before* deciding, rather than auditing *after* -
  rejected: the user wants a genuine external audit/oversight dynamic (the board making Cimcime
  more confident in, or revising, a decision it already reached), not an internal brainstorming
  aid folded into Cimcime's own reasoning.
- Running board review on every task regardless of size - rejected: far too costly and slow for
  routine work; scoped to decisions a reasonable founder would actually bring to a board.
- Fully autonomous continuous execution, reporting to the user only at major milestones - this
  was the first framing raised, refined during grilling into the cycle-based, user-gated model
  above: the team may initiate and deliberate autonomously, but nothing is acted on without the
  user's approval at that cycle's checkpoint.
- Running all board deliberation on full-price Claude - rejected in favor of ADR-0012's cheap-
  backend delegation for the routine back-and-forth, reserving full Claude for the decision
  Cimcime stands behind and what's actually shown to the user.
