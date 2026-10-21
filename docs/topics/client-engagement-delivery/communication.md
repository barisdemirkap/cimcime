# Communication

Category: client-engagement-delivery · Topic ID: communication

## Sources

- [fetched] https://www.talaera.com/industry-specific-english/communication-skills-software-developers/ — real content.
- [fetched] https://dev.to/thawkin3/beyond-code-communication-skills-every-software-engineer-needs-5714 — real content.
- [could not fetch] https://www.youtube.com/watch?v=VtUpRjAqdKM — title only ("Talk Like a Strategy Consultant"), no transcript.
- [could not fetch] https://www.youtube.com/watch?v=ppokRtCeuyI — title only ("Top-down communication explained"), no transcript.

## Findings

**The core argument** (dev.to): communication matters as much as technical skill because most
engineering work is coordination with other people, not solo coding — and "technical excellence
alone doesn't drive advancement, visibility through clear communication does."

**Concrete, actionable patterns** (dev.to): PR descriptions need real context, screenshots, and
testing steps — a reviewer with no context is "nothing frustrates me more"; code review
feedback should distinguish optional suggestions from blocking requirements, explain *why*, and
offer a concrete fix, not just a complaint; bug reports need reproduction steps plus
expected-vs-actual behavior to avoid back-and-forth; when asking for help, explain the actual
goal rather than the attempted solution (avoiding the classic "XY problem" — asking about your
workaround instead of your real need); requests for action need an explicit owner and deadline,
especially in meetings, or nothing happens. Overarching principle: "aim for respect and clarity,
reduce cognitive load for the other person" — make yourself impossible to misunderstand.

**A different, complementary angle** (talaera.com): practical techniques specifically for
non-native-English engineers — learn in context (GitHub discussions, standups, switching dev
tools to English) rather than generic language lessons; revise written artifacts (tickets, PRs,
Slack messages) for clarity before sending; practice speaking with peers in short, focused
sessions; audio-shadow technical podcasts for natural rhythm; use AI tools for instant
correction feedback; frame a request for formal training to an employer as an efficiency gain,
not a personal deficiency.

**Direct relevance to this system**: dev.to's PR-description standard ("real context,
screenshots, testing steps") is exactly the bar this project's own commit messages have been
held to throughout — e.g. every ticket-closing commit in this repo states what was proved live
and how, not just "implemented X." The "avoid the XY problem" principle is the same instinct
behind escalating a genuine "why" question (ADR-0007's unfetchable-sources decision, ADR-0008's
dispatch-rule contradiction) rather than silently picking a workaround and explaining only that.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
