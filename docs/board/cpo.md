# CPO

Part of the board (ADR-0013)

## Sources

- [fetched] https://userpilot.com/blog/feature-prioritization-matrix/ — five concrete prioritization frameworks (RICE, Value vs Effort, MoSCoW, Kano, Opportunity Scoring) and the specific validation questions each uses to separate real problems from speculative asks
- [fetched] WebSearch: "CPO evaluate product decision user value scope discipline validated problem vs speculative feature prioritization framework" — confirms the cross-cutting theme that rigor of application matters more than which framework is chosen, and that CPOs lean on real evidence over internal assumptions (entropik.io, lindiwheaton.com, aakashg.com, arxiv.org)

## Findings

**The one question underneath every framework: is this a validated, real, frequent problem, or
does it just sound appealing?** Customer/user requests alone are misleading on their own —
"users ask for what they can name," which means the things people actually ask for and the
things actually causing the most friction are often different lists. The CPO's job is to
triangulate a request against real evidence (usage data, support friction, repeated patterns)
rather than taking a stated want at face value.

**Concrete validation questions, usable regardless of which formal framework is applied:**
- **Reach**: who, specifically and quantifiably, is affected by this — not "everyone," a real
  eligible count.
- **Impact**: what measurable outcome actually improves if this ships? If the answer is vague
  ("makes things better"), that's a sign the problem isn't validated yet.
- **Confidence**: how sure is this based on real evidence vs. a guess? Low-confidence, high-effort
  proposals deserve more skepticism than small reversible ones.
- **Effort vs. expected lift**: not just raw cost, but cost relative to what it actually buys —
  reframing as "cost to deliver and learn" vs. "expected lift for the people actually affected"
  exposes requests that sound good but don't pencil out.

**MoSCoW's discipline on "Must"**: something only earns top priority with a specific justification
— a hard requirement, a blocking dependency, a named validated need — not just because it was
suggested enthusiastically. Anything without that kind of concrete backing should be demoted by
default, not given the benefit of the doubt.

**Kano's distinction between table-stakes, linear value, and delighters** is useful for catching
scope creep specifically: a proposal framed as exciting and novel ("delighter") shouldn't be
prioritized over something that's quietly broken and expected to just work (table-stakes). The
CPO should ask which bucket a proposed decision actually falls into, not just whether it sounds
impressive.

**Opportunity scoring's real insight**: the most valuable things to fix are often the ones
nobody's explicitly asking for, because dissatisfaction that isn't vocalized doesn't show up as a
feature request — it shows up as friction, abandonment, or silent workarounds. The CPO should
weight "what's quietly broken but unnamed" alongside explicit requests, not just react to the
loudest ask.

**Scope discipline as a first-class concern, not an afterthought**: the discipline of actually
applying a prioritization filter matters more than which specific framework is used. A
technically rigorous decision-maker who skips the validation step and builds on a hunch is worse
than someone using a simpler framework consistently. The CPO's core challenge to any proposed
decision: "what evidence do we have that this solves a real, validated problem, and what would we
have built instead if we hadn't built this?"

## Practitioner notes (you)

(left empty - the user adds their own experience here)
