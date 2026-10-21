# APIs Design

Category: core-software-engineering · Topic ID: apis-design

## Sources

- [fetched] https://roadmap.sh/api-design — real content.
- [fetched] https://www.ibm.com/think/topics/api-design — real content, independently converging.
- [could not fetch] https://www.youtube.com/watch?v=WXsD0ZgxjRw — only footer/legal links, no transcript, standard YouTube failure pattern.

## Findings

**What API design is, converging across both sources**: the decision-making process for how
an API exposes data/functionality to developers/users — endpoints, request/response formats,
protocols, how the API interacts with other systems. Part of broader "API governance" — the
standards/policies an org sets for API development.

**Protocol landscape** (both sources): REST, SOAP, GraphQL named by roadmap.sh; IBM adds RPC
and WebSocket to the same list, with REST singled out as particularly valued for "flexibility,
scalability, and compatibility with microservices architectures" — directly connects to the
separate `graphql.md` topic in this same category.

**Four-stage design lifecycle** (IBM): Plan (use cases, stakeholder requirements) → Develop
(endpoints, data models, security, documentation) → Test (mocking, contract testing, load
testing) → Deploy (finalized docs, versioning). A clean, reusable framework.

**Concrete best practices** (IBM): governance/documentation via OpenAPI standard (directly
corroborates `learn-a-programming-language.md`'s earlier finding that "OpenAPI/Swagger specs
should be written before code"); stakeholder collaboration throughout; strong auth (API keys,
OAuth, JWT — connects to `authentication.md`, not yet researched); consistent error handling;
versioning strategy decided before release, not retrofitted; uniform naming/request-response
patterns across endpoints.

**API security as a first-class design concern** (roadmap.sh): data protection, unauthorized-
access prevention, securing the hosting system, defending against attacks while preserving
performance/privacy — explicitly treated as inseparable from design, not a separate
afterthought, directly connecting to `api-security.md`, the next topic in this category.

**Direct relevance to this system**: this system's own `cimcime.cli` is itself a small,
internal "API" in the broad sense IBM describes — a stable set of subcommands
(`get-topic`, `update-status`, `category-rollup`, etc.) with a deliberate, versioned-in-spirit
contract that topic-agents/category-agents depend on; the "uniform naming conventions across
endpoints" principle maps directly onto the CLI's own consistent verb-noun subcommand naming.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
