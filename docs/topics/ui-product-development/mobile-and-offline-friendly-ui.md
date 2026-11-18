# Mobile and Offline-Friendly UI

Category: ui-product-development · Topic ID: mobile-and-offline-friendly-ui

## Sources

- [fetched, partial] https://web.dev/learn/pwa — fetch returned only the Caching chapter (Cache Storage API); the other modules (installation, manifest, serving, Workbox, tools/debug) are named but their content was not read.
- [could not fetch] https://developer.apple.com/design/human-interface-guidelines/ — client-rendered; two attempts returned only the page title, no body text. Marked [unverified]; nothing below is claimed from it.

## Findings

All from the web.dev PWA caching chapter unless noted.

- Cache Storage API: accessed via `caches`; `caches.open(name)` returns a named cache. Usually managed from a service worker (separate lifecycle, doesn't block main thread). Requires HTTPS in most contexts.
- What to cache: the minimum to render the UI (start URL HTML, CSS, UI images, required JS, basic JSON data, web fonts). Balance offline speed against storage and data use; don't cache things that must always be fresh.
- Offline is a spectrum: not every PWA needs full offline; a basic custom offline page via the service worker beats a generic browser error. Play Store PWAs should avoid showing browser HTTP error pages.
- Methods: `add()`, `addAll()` (transactional: one failure caches nothing), `put()`, `delete()`. URLs must be listed explicitly.
- When to cache: at service worker install, after first load, on navigation to a section, or when idle. Caching everything at install wastes bandwidth and can serve stale content. Use `event.waitUntil()` in `install`.
- Cache storage is per origin, so prefix cache names when multiple PWAs share an origin.
- Cross-origin (CDN) assets are opaque responses: contents/headers unreadable, sizes distort quota, non-2xx errors are not detected, so `addAll()` can't catch failures.
- The API does no versioning or stale cleanup; your code must handle it (Workbox suggested).
- Debugging: Chrome/Edge/Firefox devtools show caches; Safari Web Inspector does not (Service Worker Detector extension fills the gap). Support: Chrome 43, Edge 16, Firefox 41, Safari 11.1.

Gap: Apple HIG content (e.g., touch targets, navigation patterns) was not read; no claims made. A better source or manual paste is needed for that half.

Glossary: no new term clearly needed; possibly "offline-first / app shell" if the project adopts it.

## Practitioner notes (you)

