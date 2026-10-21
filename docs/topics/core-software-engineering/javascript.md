# JavaScript

Category: core-software-engineering · Topic ID: javascript

## Sources

- [fetched] https://roadmap.sh/javascript — real content.
- [could not fetch] https://www.netacad.com/courses/javascript-essentials-1?courseLang=en-US — only a title returned, no curriculum content.
- [fetched] https://developer.mozilla.org/en-US/docs/Web/JavaScript — real content, independently converging.
- [could not fetch] https://www.youtube.com/watch?v=EerdGm-ehJQ — only footer/legal links, no transcript, standard YouTube failure pattern.

## Findings

**What JavaScript is** (MDN): a lightweight, interpreted/JIT-compiled language with
first-class functions; prototype-based, garbage-collected, dynamically typed; supports
imperative, functional, and object-oriented styles. Explicitly **not** "Interpreted Java"
despite the naming — different syntax, semantics, use cases entirely. Standardized as
ECMAScript (ECMA-262); MDN documents browser-implemented features sometimes ahead of official
spec publication (stage 3-4).

**Where it runs** (roadmap.sh): "the only language natively supported by all browsers," but
also runs server-side (Node.js, Bun, Deno) and in automation tooling — one language spanning
front-end, back-end, and scripting, unlike Python which roadmap.sh's own `python.md` finding
described as backend-only in practice.

**Specialization paths** (roadmap.sh): front-end (web standards, DOM API, web components, UX
basics, React) vs. back-end (API design, data modeling, server-side rendering, database
querying, NextJS) — the same domain-branching pattern already seen in `python.md` and
`learn-a-programming-language.md`.

**MDN's documentation structure, a genuinely useful learning-path map**: beginner tutorials →
guides (fundamentals: grammar/control-flow/functions/objects; intermediate: async patterns,
client-side APIs, data structures, closures; advanced: prototype chain, memory management) →
full reference (standard objects, expressions/operators, classes, regex). This progression
(fundamentals → async/APIs → prototypes/memory) is a reusable map for assessing where in the
JS learning curve any future client codebase or hire sits.

**Direct relevance to this system**: none of this system's own code is JavaScript — it is a
pure Python backend (per `python.md`) — but `learn-a-programming-language.md` already flagged
TypeScript (JS's typed superset) as the FDE's standard client-facing-dashboard choice, so this
topic is prerequisite background for a future engagement requiring a frontend, not something
this system itself currently needs.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
