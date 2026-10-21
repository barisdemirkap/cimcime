# UAT

Category: client-engagement-delivery · Topic ID: uat

## Sources

- [fetched] https://www.guru99.com/user-acceptance-testing.html — real content.
- [fetched] https://www.splunk.com/en_us/blog/learn/user-acceptance-testing-uat.html — real content, independently converging.
- [could not fetch] https://www.youtube.com/watch?v=AU8SV7091-s — title only, no transcript.

## Findings

**What UAT is, converging across both sources**: the final validation phase — after
functional/integration/system testing — where the client or real end users confirm the system
actually meets business needs, using production-like data in an environment separate from
development. splunk.com's framing: UAT "validates the end-to-end business flow," not just
"finds bugs" — the earlier test phases already did bug-finding; UAT asks a different question.

**Six-step process, identical across both sources**: analyze business requirements → write a
UAT plan (strategy, entry/exit criteria, timeline) → derive test scenarios/cases from real
business processes → prepare realistic test data (guru99.com specifically: scrambled production
data, not synthetic) → execute and document, retest any bugs found → confirm business
objectives met and get stakeholder sign-off. Exit criteria (guru99.com): zero critical defects,
satisfactory business processes, explicit stakeholder approval — not just "testing is done."

**Four UAT variants** (splunk.com): alpha testing (internal users), beta testing (external
users), contractual acceptance testing (a vendor-client contractual agreement on what "accepted"
means), regulatory acceptance testing (compliance-focused). Useful vocabulary for distinguishing
which kind of "acceptance" a given engagement actually needs.

**Success practices**: start planning early in the development cycle, not at the end; engage
real end users throughout, not just at the final test; test realistic end-to-end scenarios, not
isolated features; think from an "unknown user" perspective specifically to catch gaps a
developer's own mental model would miss; run feedback sessions before the actual release.

**Direct relevance to this system**: every topic-agent's deep-dive run in this session is
functionally a small UAT cycle — the "acceptance criteria" in each ticket (e.g. "demonstrated
with a real round-trip," "verified against the live tracker for all 9 categories") are exactly
this topic's exit criteria, applied to a software ticket instead of a client engagement: no
sign-off (ticket close, auto-triggered by the commit's `Closes #N`) until the real, end-to-end
behavior was actually proven live, not just unit-tested in isolation.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
