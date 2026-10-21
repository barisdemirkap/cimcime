---
status: accepted
---

# Two-phase lifecycle: autonomous Learning Phase, then on-demand Runtime Phase

Cimcime starts in a **Learning Phase**: it runs continuously and autonomously on its host machine,
working every topic-agent through the full roadmap.sh Forward Deployed Engineer path, unprompted,
until all ~97 topics are deep-dived. Once that completes, Cimcime permanently switches to a
**Runtime Phase**, acting only on demand (a Telegram message or CLI invocation) with no further
unprompted background work. This resolves an apparent conflict between "learn continuously on its
own" and "only act when asked": both are true, just in sequence rather than at once.
