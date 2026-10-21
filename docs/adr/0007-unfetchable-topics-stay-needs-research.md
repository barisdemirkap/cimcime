---
status: accepted
---

# A topic with zero fetchable sources stays `needs-research`, tagged `fde:needs-better-sources`

The first real topic-agent run (`rags`) found that none of its three linked resources were
fetchable (a JS-rendered page, an HTTP 403, a YouTube page with no recoverable transcript) — a
failure mode that likely recurs across other topics linking the same domains. The question of
whether such a topic counts as "researched" is a real policy call, not one the topic-agent should
make unilaterally, so it was escalated and decided: the topic stays `fde:needs-research` and gets
the new `fde:needs-better-sources` label, rather than being marked `fde:researched` on an empty or
fabricated study file.

The topic-agent definition (`.claude/agents/topic-agent.md`) now applies this automatically —
it's expected to recur, so it shouldn't need re-escalating per topic.

## Consequences

The Learning Phase's completion check (ticket #5, not yet built) must account for this: "every
topic is `researched`" is not quite the real completion condition once
`fde:needs-better-sources` topics exist. Whoever builds that check needs to decide whether Learning
Phase can complete while such topics remain open, or whether they block completion until resolved
by better sources. Not decided here — flagged for that ticket.
