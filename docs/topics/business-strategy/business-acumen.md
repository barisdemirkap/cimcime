# Business Acumen

Category: business-strategy · Topic ID: business-acumen

## Sources

- [fetched] https://fdetimes.net/en/guides/fde-business-acumen-follow-the-money/ — real content, written specifically for FDEs, not a generic business article.
- [fetched] https://en.wikipedia.org/wiki/Business_acumen — real content, the general/definitional framing.
- [could not fetch] https://www.youtube.com/watch?v=JwhPhS26Mos — only partial page metadata ("Business Acumen 101" implied by context), no transcript. Consistent with the YouTube pattern already seen across this roadmap.

## Findings

**What it means, FDE-specifically** (fdetimes.net — this is the most directly relevant source
found so far for this whole category, since it's written for this exact role): business acumen
means understanding how the customer makes money and tying technical work to that financial
reality. The guide's own line is sharp and worth keeping verbatim: "A pilot that works technically
can still die in a budget meeting if the FDE cannot say how the customer makes money."

**Hard ROI vs. soft ROI**: most engineers report "soft ROI" (latency, accuracy, uptime) when what
actually keeps a project alive is "hard ROI" — revenue up, costs down, or an expense avoided,
i.e. something that moves a line on the P&L. The guide cites IBM data: only 25% of AI initiatives
hit their expected returns, and 95% of generative AI pilots fail — mostly for organizational
reasons, not technical ones. This is a direct, concrete reason business acumen matters for an
FDE specifically: technical success is necessary but not sufficient.

**Four concrete discovery questions** (fdetimes.net) an FDE should be able to answer about any
engagement: which P&L line changes if this succeeds; what the baseline is today and who measures
it; which department's budget actually funds the work; who approves scaling it beyond a pilot.

**Three common mistakes** (fdetimes.net): reporting technical metrics instead of financial
impact; skipping a baseline measurement before deployment (so there's nothing to compare the
"after" against); building relationships only with friendly end-users rather than the people who
actually hold budget authority.

**General definition and components** (Wikipedia): business acumen is the knowledge/skill/
experience to understand an organization's operations and external environment, combining
executive-level systems thinking, financial literacy (growth, profitability, cash flow,
statements), strategic "big picture" perspective, leadership, and structured decision-making.
Described as "the most critical competency area for global leaders" in the sources it cites —
this is a general leadership-development finding, not FDE-specific, but it corroborates why this
is treated as a core (not optional) FDE skill rather than a nice-to-have.

**Direct relevance to this system**: this is the clearest concrete grounding so far for
`docs/adr/0001`'s approval-gate design — the reason Cimcime escalates "why" decisions to the
human rather than just optimizing technical metrics autonomously is exactly this gap between
soft ROI (what an AI system can measure and act on) and hard ROI (what the business actually
needs, which requires human context Cimcime doesn't have).

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
