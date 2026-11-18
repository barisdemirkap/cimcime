# Accessibility

Category: ui-product-development · Topic ID: accessibility

## Sources

- [fetched] https://www.w3.org/WAI/standards-guidelines/wcag/ — WCAG 2 overview: versions, POUR, conformance levels, related docs.
- [fetched, partial] https://web.dev/learn/accessibility — the fetch returned only one module of the course (evaluating patterns, components, design systems), not the course index. Other modules (AT testing, testing techniques) were only seen as references and are not covered here.

## Findings

WCAG (source: W3C page)
- WCAG is the international technical standard for accessible web content, developed by the W3C WAI Accessibility Guidelines Working Group. It covers text, images, sound, code, dynamic content, multimedia, mobile web and AI web interfaces. WCAG2ICT applies it to non-web software. The page itself says it is "not an introduction to accessibility"; it targets content developers, authoring-tool developers and evaluation-tool developers.
- Versions: 2.0 (Dec 2008, 12 guidelines); 2.1 (June 2018, adds 1 guideline and 17 success criteria); 2.2 (Oct 2023, adds 9 success criteria, removes only 4.1.1 Parsing as obsolete). Versions are backward compatible: meeting 2.2 also meets 2.1 and 2.0. W3C recommends the latest version. WCAG 2.2 is also ISO/IEC 40500:2025. EN 301 549 (European standard) uses WCAG 2.2 in its 2026 version. WCAG 3 is a separate early draft.
- Four principles (POUR): perceivable, operable, understandable, robust. WCAG 2.2 has 13 guidelines under them.
- Each guideline has testable success criteria at levels A, AA and AAA; conformance is determined by meeting the relevant criteria.
- Supporting material: How to Meet WCAG (Quick Reference), Understanding WCAG 2, Techniques, Test Rules.

web.dev module on patterns, components and design systems (source: web.dev)
- Component-driven development gives speed, parallel work and a living style guide, but raises questions of which accessible pattern to use, adopt versus build, and how to verify it helps users.
- Before choosing, ask: does an accessible pattern or design system already exist, which browsers and assistive technologies (AT) must be supported, and what code/framework/user-need constraints apply.
- Existing resources named: Deque University ARIA library, GOV.UK, USWDS, Inclusive Components, MagentaA11y, plus framework options (Reach UI, Reakit, Chakra, Angular Material, Vuetensils). Treat all as starting points; copying code untested is a mistake even if the library claims full accessibility.
- Screen reader and browser pairings matter (JAWS, NVDA, Narrator, VoiceOver, Orca, TalkBack). AT support is complex and ARIA adds to it. Check a11ysupport.io and HTML5 Accessibility.
- CMS or legacy code can narrow the options sharply; modern JS frameworks give more flexibility. Also weigh performance, security, SEO, translation, third-party integrations, and the skill level of the developers and content editors who will use the patterns.

Glossary: no new term is clearly needed. "POUR" and "AT" (assistive technology) could be added if the glossary covers UI topics.

## Practitioner notes (you)

