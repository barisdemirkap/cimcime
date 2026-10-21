# Integration Engineering

Category: integration-enterprise-systems · Topic ID: integration-engineering

## Sources

- [fetched] https://www.coursera.org/articles/software-integration — real content.
- [fetched] https://latamcent.com/glossary/integration-engineer/ — real content.

## Findings

**What software integration is**: connecting different applications so they share data without
manual re-entry. Four named types: legacy systems integration (bridging old systems to new via
APIs/database connectors — directly feeds the upcoming `working-with-legacy-systems` topic);
data integration (consolidating data from separate apps for analysis); EDI (automating
paper-based exchanges like invoices between businesses); EAI (letting systems interact as a
business scales).

**Integration patterns/topologies**: star (many subsystems in one complex network);
point-to-point (two systems directly linked — simple, doesn't scale); hub-and-spoke (data routed
through a central hub, better security posture); horizontal (enterprise service bus,
cost-effective); vertical (organized by function, silo-like). Knowing these names matters for an
FDE because client environments usually already have one of these topologies in place
(undocumented), and a new integration has to fit into it, not replace it.

**The Integration Engineer role, specifically** (latamcent.com): works with APIs, webhooks,
middleware, and data mapping; five core functions — design connections, transform data between
formats, build/maintain integrations, automate workflows, troubleshoot before bad data
propagates. Explicitly distinguished from adjacent roles: backend developers build product
features (not external connections); data engineers build pipelines for analysis (not live
system-to-system connections); API developers focus on API design/security specifically. Skills
named: REST APIs, OAuth flows, webhooks, JSON/XML, iPaaS tools, strong error handling, clear
documentation.

**Direct relevance to this system**: the five integration-engineer functions map closely onto
what this project's own `GitHubIssuesStore` class actually does — design the connection (the
state-store `Protocol`), transform data between formats (`TopicRecord` ↔ GitHub issue
body/labels), build/maintain the integration (the adapter itself), troubleshoot before bad data
propagates (the eventual-consistency bugs already fixed in ADR-0004's area during earlier
tickets). This repo's own first real ticket was, in this topic's vocabulary, an integration
engineering task.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
