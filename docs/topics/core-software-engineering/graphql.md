# GraphQL

Category: core-software-engineering · Topic ID: graphql

## Sources

- [fetched, thin] https://roadmap.sh/graphql — only landing-page header/community-stats, no curriculum.
- [fetched] https://graphql.org/learn/ — real content, substantive.
- [fetched] https://graphql.org/ — real content, substantive, independently converging.
- [could not fetch] https://www.youtube.com/watch?v=5199E50O7SI — only footer/legal links, no transcript, standard YouTube failure pattern.

## Findings

**What GraphQL is, converging across both graphql.org sources**: a query language and
server-side runtime for APIs, built on a strongly-typed schema — shifts from REST's
endpoint-per-resource thinking to a graph-based model of data relationships.

**Core building blocks** (graphql.org/learn): schemas/types (strong type system defining
data shape); queries (fields/variables/fragments to fetch exactly what's needed); mutations
(update/remove records); subscriptions (real-time updates at scale); validation (catches
errors early); resolvers (execute/return data per query); response structure (data + errors +
custom-metadata extensions); introspection (dynamically inspect the schema itself).

**Five core advantages, directly named** (graphql.org homepage): precision (no
over-/under-fetching); optimization (follow relationships in one request instead of many API
calls — the specific mechanism behind "reduces over-fetching" already named abstractly in the
roadmap doc's own one-line GraphQL description); productivity (editor tooling, type safety);
consistency (type-safe, self-documenting schemas); versionless evolution (add fields/types
without breaking existing queries, deprecate cleanly).

**Concrete worked example** (graphql.org homepage): describe a `type Project` schema →
write a query asking only for `tagline` → get back exactly that shape, nothing more — the
clearest "show, don't just tell" example found in this entire category.

**Credibility signal**: backed by the Linux Foundation since 2018; named production adopters
include Meta, AWS, Airbnb, IBM, PayPal, The New York Times, Shopify, GitHub — real-world
validation, not just a spec on paper.

**Direct relevance to this system**: this project uses GitHub's REST API (via `gh` CLI), not
GraphQL — but GitHub itself is listed among GraphQL's named adopters, and GitHub does offer a
GraphQL API as an alternative to the REST endpoints this project's `GitHubIssuesStore` already
uses; not a design gap, since REST suits this project's simple CRUD-style issue operations
fine, but a documented alternative if query complexity (e.g. deep nested issue/dependency
graphs) ever grows enough to justify switching.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
