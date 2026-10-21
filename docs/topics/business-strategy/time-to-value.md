# Time-to-Value

Category: business-strategy · Topic ID: time-to-value

## Sources

- [fetched] https://amplitude.com/explore/analytics/time-to-value — real content, including a concrete 4-step measurement process and 5 reduction tactics.
- [fetched] https://baremetrics.com/academy/time-to-value-ttv — real content, including a concrete TTV formula and reduction strategies.
- [could not fetch] https://www.youtube.com/watch?v=Ae5-shAAU-s&t=17s — only the page title ("What Is Time to Value (TTV) — And How Do You Measure It?") recoverable, no transcript. Consistent with every other YouTube resource seen across this roadmap so far.

## Findings

**Definition** (both sources agree): Time to Value is the elapsed time from a customer's
sign-up/engagement start to the moment they experience the product's core benefit — their first
genuinely meaningful outcome, not just activity (clicks, logins). Baremetrics frames the end point
as the "Aha! moment"; Amplitude frames it as a defined "value event" (e.g. "first order placed").

**Why it matters**: both sources tie TTV directly to retention — churn risk peaks during
onboarding, and if a customer doesn't reach value quickly they leave. Baremetrics: "If customers
don't see value quickly, they're gone." This is a direct, practical link to this roadmap's own
framing of Time-to-Value: "sequencing so trust builds incrementally" — a slow TTV doesn't just
delay revenue, it actively erodes the trust an FDE engagement depends on.

**How to measure**: Amplitude's 4-step process — define the value event, mark the start event,
calculate elapsed time, track medians/percentiles (not averages, since outliers skew badly).
Baremetrics gives the same idea as a formula: `TTV = Date of First Value − Date of Signup`,
measured via analytics tooling (it names Mixpanel and Amplitude specifically) plus cohort
analysis across user segments.

**How to reduce it**: both sources converge on streamlining onboarding (targeted guides,
progressive disclosure, guided checklists, contextual help) and reducing friction (removing
unnecessary required inputs, smart defaults, session replay to find friction points). Baremetrics
adds a distinct point relevant to complex/enterprise engagements specifically: offering hands-on
human support (customer success managers, webinars) when the product is too complex for
self-service onboarding alone — directly relevant to FDE-style engagements, which are themselves
a form of hands-on TTV reduction for complex enterprise deployments.

**Direct relevance to this system**: this is a real-world instance of ADR-0003's two-phase design
applied to a different context — Cimcime's own Learning Phase is itself a (long) time-to-value
investment before Runtime Phase delivers ongoing value, and the same "don't let the gap erode
trust" logic that motivates short TTV in a product is why ADR-0003 was explicit that Learning
Phase should complete and transition, not run forever.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
