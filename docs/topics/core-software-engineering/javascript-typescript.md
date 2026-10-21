# JavaScript / TypeScript

Category: core-software-engineering · Topic ID: javascript-typescript

## Sources

- [fetched, thin] https://roadmap.sh/typescript — only the landing-page header/community-stats section rendered, not the actual curriculum breakdown; treated as a partial fetch, not discarded, since it did return real (if shallow) page content.
- [fetched] https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html — real, substantive content.
- [not re-fetched] https://roadmap.sh/javascript and https://developer.mozilla.org/en-US/docs/Web/JavaScript — already fetched for the separate `javascript` topic in this same category; not re-fetched here to avoid duplicate work, findings carried over by reference.
- [could not fetch] https://www.youtube.com/watch?v=XIOLqoPHCJ4 — not attempted; same domain/pattern as the other YouTube failures already confirmed for this exact topic area (see `ZvZ7gvcmPmI` below).
- [could not fetch] https://www.youtube.com/watch?v=ZvZ7gvcmPmI — only footer/legal links, no transcript, standard YouTube failure pattern.

## Findings

**What TypeScript is** (typescriptlang.org): a static type checker built on top of
JavaScript, catching type errors before execution — e.g. a typo like `obj.heigth` instead of
`obj.height` is silently `NaN` in plain JS but a compile-time error in TS; `4 / []` silently
logs `Infinity` in JS but TS flags the right-hand side as needing to be `any`/`number`/`bigint`/
enum.

**TypeScript is a strict superset, not a separate language**: "You can't learn TypeScript
without learning JavaScript! TypeScript shares syntax and runtime behavior with JavaScript."
All valid JS is valid TS; TS **never** changes JS's runtime behavior; types are fully erased at
compile time, producing plain JS. The accomplishing-a-task mechanics (sorting, DOM manipulation)
stay identical to JavaScript — TS only adds a compile-time layer on top.

**Why it matters in practice**: catches mistakes early, before they become production bugs —
most valuable in larger applications where JS's loose typing and quirks compound into real
risk. Directly reinforces `learn-a-programming-language.md`'s finding that TypeScript (not
plain JS) is the FDE's standard choice for client-facing dashboards/integrations — larger,
longer-lived client deliverables are exactly where this compile-time safety pays off.

**Direct relevance to this system**: this project has no JS/TS code (it's pure Python per
`python.md`), but this topic completes the earlier finding: if a future engagement needs a
client-facing frontend, TypeScript is the documented default — and the reason is now concrete
(static error-catching), not just "it's the standard."

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
