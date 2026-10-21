# CSS

Category: core-software-engineering · Topic ID: css

## Sources

- [fetched] https://roadmap.sh/css — real content.
- [fetched] https://web.dev/learn/css/ — real content, substantive.
- [could not fetch] https://www.youtube.com/watch?v=OXGznpKZ_sA&t=25s — only footer/legal links, no transcript, standard YouTube failure pattern.

## Findings

**What CSS is** (roadmap.sh): "Cascading Style Sheets" — separates content from presentation
(layout, colors, fonts); one of the three core frontend technologies alongside HTML
(structure) and JavaScript (interactivity) — same three-layer framing already confirmed in
`html.md`.

**Three ways to apply CSS** (roadmap.sh): internal (`<style>` in `<head>`, document-scoped),
external (linked `.css` files, efficient for site-wide management at scale), inline (`style`
attribute on an element — explicitly flagged as inefficient and not recommended for
maintenance).

**web.dev's 39-module structure, the most substantive source in this topic**: foundations
(the Box Model — "everything displayed by CSS is a box" — selectors, cascade, specificity,
inheritance); styling properties (color, sizing units, borders, shadows, typography); layout
systems — three named approaches: traditional, Flexbox ("one dimension"), CSS Grid ("two
dimensional... rows and columns"); advanced (logical properties, custom properties/variables,
pseudo-elements/classes, z-index, animations/transitions, gradients, container queries);
interactive (anchor positioning, popover/dialog, view transitions for SPAs).

**Direct relevance to this system**: minimal — no frontend/CSS surface in this project.
Background knowledge only, same framing as `html.md`: relevant if a future FDE engagement
needs a self-built client demo/dashboard.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
