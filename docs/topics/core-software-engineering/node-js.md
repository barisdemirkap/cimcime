# Node.js

Category: core-software-engineering · Topic ID: node-js

## Sources

- [fetched, thin] https://roadmap.sh/nodejs — only landing-page header/community-stats, no detailed curriculum.
- [fetched] https://nodejs.org/en/learn/getting-started/introduction-to-nodejs — real content, official source, substantive.
- [fetched] https://www.w3schools.com/nodejs/nodejs_intro.asp — real content, independently converging.
- [could not fetch] https://www.youtube.com/watch?v=32M1al-Y6Ag — only footer/legal links, no transcript, standard YouTube failure pattern.

## Findings

**What Node.js is** (official nodejs.org): an open-source, cross-platform JavaScript runtime
running outside the browser, built on Chrome's V8 engine. Runs in a **single process** —
no new thread per request — using asynchronous, non-blocking I/O primitives: blocking I/O
operations don't block the thread; Node resumes when a response returns, letting a single
server handle thousands of concurrent connections without manual thread-concurrency
management. Lets frontend JS developers write server-side code in the same language, and
supports new ECMAScript features without waiting for browser rollout.

**Concrete worked example** (nodejs.org): a minimal "Hello World" HTTP server shown in both
CommonJS (`require('node:http')`) and ES module (`import { createServer } from 'node:http'`)
syntax — the one concretely runnable code sample found across all of Node's resources in this
topic.

**Why it's chosen in practice** (w3schools): excels at simultaneous-connection handling — real-
time apps, APIs, microservices, data streaming — directly corroborating
`learn-a-programming-language.md`'s earlier framing of Node.js as the backend half of the
TypeScript-based client-facing stack. Full curriculum breadth named: core modules (HTTP,
filesystem, events, streams, crypto), REST APIs, MySQL/MongoDB integration, WebSockets,
GraphQL (connects to `graphql.md`, not yet researched), testing/deployment, performance/
scaling, even Raspberry Pi hardware integration.

**Direct relevance to this system**: none directly — this project is pure Python, no Node.js —
but this is the concrete backend-runtime counterpart to the TypeScript frontend already
flagged in `learn-a-programming-language.md`/`react.md`/`frontend.md`: if a future engagement
needs a JS-based client dashboard, Node.js is the documented default server-side pairing.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
