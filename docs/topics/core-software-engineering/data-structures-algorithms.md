# Data Structures & Algorithms

Category: core-software-engineering · Topic ID: data-structures-algorithms

## Sources

- [fetched] https://algomaster.io/learn/system-design/what-is-system-design — real content.
- [fetched] https://www.tutorialspoint.com/data_structures_algorithms/index.htm — real content, independently converging on the DSA-specific content.
- [could not fetch] https://www.youtube.com/watch?v=bum_19loj9A — only footer/legal links, no transcript, standard YouTube failure pattern.
- [not fetched] https://www.youtube.com/watch?v=RpLnQnurpLY — not attempted; same YouTube domain/pattern confirmed failing on the sibling resource above, assumed to recur.

## Findings

**Note on source mismatch**: the roadmap doc links a System Design article as this topic's
first resource even though the topic itself is DSA — both are covered below since both were
linked, but they are genuinely different subjects (System Design = architecture at scale; DSA
= algorithmic fundamentals), not duplicate coverage of the same concept.

**DSA core content** (tutorialspoint): foundation (time/space complexity, asymptotic
analysis); data structures (arrays, linked lists, stacks, queues, trees — BST/AVL/Red-Black —
graphs, heaps, tries); algorithms (searching, sorting, divide-and-conquer, greedy, dynamic
programming, graph algorithms); advanced (recursion, hashing, randomized/approximation
algorithms). Key insight on why structure matters: "data can be organized...such that all
items may not be required to be searched, and the required data can be searched almost
instantly" — the practical payoff of good structure choice, not just theory.

**System Design content** (algomaster.io), linked as this topic's actual first resource:
"deciding what components a system needs, what each one is responsible for, how they
communicate, and how data flows" — a level above coding, concerned with servers/databases/
caches/network interactions at scale. Functional requirements (what features users need) vs.
non-functional (latency targets, availability, durability). Named building blocks: load
balancers, app servers, databases, object storage, caches, CDNs, message queues. Quality
tradeoffs are explicit and named: "improving one of these qualities often means making a
trade-off somewhere else" — caching speeds things up but introduces staleness; redundancy
improves availability but raises cost.

**Direct relevance to this system**: the roadmap doc's own topic description frames DSA
fluency as letting an FDE "evaluate performance characteristics, debug inefficiencies in
customer systems, and reason clearly about solutions" — directly applicable to debugging this
system's own `GitHubIssuesStore._list_all()` (an O(n) full-issue-list scan chosen deliberately
to work around GitHub's search-index eventual consistency, a real example of trading raw
performance for correctness — exactly the kind of tradeoff this topic's System Design source
describes abstractly).

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
