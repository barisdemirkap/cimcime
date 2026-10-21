# Learn a Programming Language

Category: core-software-engineering · Topic ID: learn-a-programming-language

## Sources

- [fetched] https://fde.academy/blog/best-programming-languages-to-learn-for-an-fde-role — real content.
- [fetched] https://fde.academy/blog/forward-deployed-engineer-tech-stack — real content, independently converging.
- [fetched] https://www.scaler.com/topics/forward-deployed-engineer-tools-frameworks-language/ — real content, independently converging.

## Findings

**Priority order, consistent across all three sources**: Python first ("non-negotiable" —
dominates AI orchestration, RAG, LLM APIs, agent frameworks like LangChain); SQL as a mandatory
baseline, not optional (joins, window functions, CTEs, subqueries, optimization — nearly every
engagement starts with exploring/transforming client data); TypeScript as the strongest
secondary choice for client-facing dashboards/integrations; Go/Java situationally, matched to
the target client's actual stack (Go for infra-heavy/startups, Java for enterprise/government
with existing Java codebases) rather than learned equally across the board.

**Key framing — match the language to the client, not to personal preference**: scaler.com
notes FDEs "often inherit the client's stack" (Java at banks, TypeScript at dashboard-heavy
companies), making language choice itself a discovery/scoping decision, not a fixed personal
toolkit — directly connects to `discovery-scoping.md`-category topics not yet researched and to
the general FDE-role framing in `fde-role-career` (already fully settled).

**Concrete named tool stack, independently converging across sources** — directly validates
much of this project's own tool choices against real-world FDE practice: Postman for API
testing/sharing ("a shared Postman collection is often the actual first deliverable on a new
engagement" — scaler.com); OpenAPI/Swagger-before-code; PostgreSQL as "the pragmatic universal
default" (now handling vector search too, connecting to `vector-dbs.md`); LangChain/LangGraph
as "the most common agent orchestration frameworks in current FDE deployments"; LangSmith,
Braintrust, HoneyHive for AI tracing/observability — **the same Braintrust and LangSmith
already independently cited in `observability.md` and `prompt-management.md`**, now a third
independent confirmation that these are real, widely-used tools and not research artifacts;
OpenTofu recommended over Terraform for new engagements specifically (Terraform viable only
when the client is already committed to HashiCorp's commercial platform) — nuances
`terraform.md`'s earlier finding.

**Direct relevance to this system**: this project is itself Python-based
(`uv run python -m cimcime.cli`), uses GitHub (not just git) for its state store, and already
independently identified Braintrust/Arize/LangSmith-class tools as the right fit for an
eval/observability gap — this topic is the first source in the whole research project to
describe the *exact role this system's own human operator performs*, and the stack it
describes is close to what the project already uses.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
