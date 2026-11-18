# Frontend Implementation

Category: ui-product-development · Topic ID: frontend-implementation

## Sources

- [fetched] https://react.dev/learn — React "Quick Start": components, JSX, state, hooks, props. Read via a summarizing fetch (not raw page text).
- [fetched] https://web.dev/learn/design — the fetch returned only the "macro layouts" lesson content, not a course index. The other modules of the Learn Design course were not seen. Read via a summarizing fetch.

## Findings

### React Quick Start (react.dev/learn)
- Components are JavaScript functions returning markup; names start with a capital letter (lowercase = HTML tags). Composed by nesting.
- JSX is stricter than HTML: close all tags, single root element (or `<>...</>` fragment), `className` instead of `class`. Curly braces escape into JS for values, attributes (`src={user.imageUrl}`), and `style={{}}` objects.
- Conditional rendering is plain JS: `if/else`, ternary, or `&&` when there is no else branch.
- Lists: `array.map()` to JSX, each item needs a stable `key` (usually a data ID) so React can track inserts, deletes, reorders.
- Events: pass the handler function itself (`onClick={handleClick}`), not a call (`handleClick()`).
- State: `useState` returns value plus setter; calling the setter re-renders. Each component instance has its own state.
- Hooks (functions starting with `use`) may only be called at the top level of a component or another Hook, never in conditions or loops.
- Sharing data: "lift state up" to the nearest common parent and pass down via props. Data flows down through props; events flow up through handler functions passed as props.
- React does not prescribe how CSS is added (link tag or whatever build tool/framework supports).

### Macro layouts (web.dev/learn/design)
- Macro layout = page-level arrangement (header, main, sidebar, footer); micro layouts (components within a page) are the next lesson.
- Get source/content order right first, since small screens show it as one column.
- CSS Grid suits macro layouts: a media query can switch main to a two-column (2:1) grid at a min width. Logical properties do not work in media queries yet, so `min-width` is used rather than `min-inline-size`.
- Flexbox can do the same but needs per-column rules; grid keeps sizing in one container rule.
- Avoid breakpoint sprawl for card grids: `repeat(auto-fill, minmax(...))` in grid, or flex-wrap with flex-grow. Grid keeps rows/columns aligned; flexbox stretches the last row's items.
- Fluid layouts can be responsive with minimal CSS and no media queries (1linelayouts.com referenced).
- Quiz takeaway: macro layouts are large-area layouts, often but not always adjusted with media queries.

### Glossary
No new terms obviously needed; "lifting state up" and "macro/micro layout" are generic frontend terms, optional additions.

## Practitioner notes (you)

