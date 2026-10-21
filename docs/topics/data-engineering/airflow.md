# Airflow

Category: data-engineering · Topic ID: airflow

## Sources

- [fetched] https://airflow.apache.org/docs — real content, the official docs.
- [fetched] https://github.com/apache/airflow — real content, the project README.
- [could not fetch] https://towardsdatascience.com/building-pipelines-in-apache-airflow-for-beginners-58f87a1512d5/ — HTTP 403 Forbidden, consistent with every other towardsdatascience.com resource in this roadmap.
- [could not fetch] https://www.youtube.com/watch?v=IiczxlbQb8s — title only, no transcript.

## Findings

**What it is**: a workflow orchestration platform where pipelines are defined as **DAGs**
(Directed Acyclic Graphs) in code — "pipelines are defined in code, enabling dynamic DAG
generation and parameterization," which the README frames as the source of maintainability and
testability. Core components: a scheduler (coordinates task execution respecting dependencies),
a webserver/UI (visualize, monitor, troubleshoot), a REST API (programmatic control), and a Task
SDK that deliberately decouples DAG-authoring code from Airflow's own internals for forward
compatibility.

**Design philosophy, concretely stated**: Airflow is built for *relatively static* workflows,
not ad hoc one-offs. It emphasizes idempotent tasks, and explicitly delegates high-volume data
movement to specialized external services rather than moving large datasets between its own
tasks — Airflow orchestrates, it isn't meant to be the data-transport layer itself. Supports
Kubernetes (via Helm) and Docker for execution environments; wide third-party provider
integrations for databases/cloud/messaging systems. Adoption: 47.2k GitHub stars, ~500 known
organizations.

**Direct relevance to this system**: a DAG is exactly what ticket #2's ticket-dependency graph
already is (each ticket declaring its own `Blocked by` edges, native GitHub dependencies) — same
underlying structure (nodes + directed edges, no cycles), just realized as GitHub Issues instead
of Airflow task objects. Airflow's idempotency emphasis is the same principle this project's own
`seed` command and `_find_or_create_category_issue`/`_find_or_create_phase_issue` helpers already
follow (safe to rerun, never duplicate).

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
