# Data Pipelines

Category: data-engineering · Topic ID: data-pipelines

## Sources

- [fetched] https://www.ibm.com/topics/data-pipeline — real content.
- [could not fetch] https://www.youtube.com/watch?v=oKixNpz6jNo — title only, no transcript.
- [could not fetch] https://www.youtube.com/playlist?list=PLf0swTFhTI8pRV9DDzae2o1m-cqe5PtJ2 — title only ("Build a Data Engineering Pipeline using Python and Airflow"), no content.
- [could not fetch] https://www.youtube.com/playlist?list=PLa7VYi0yPIH1MculjFWJxs-aENPxRHHOS — title only ("Building Data Pipelines with Apache Kafka and Confluent"), no content.

## Findings

**What a data pipeline is**: a system that "ingests raw data from multiple sources, transforms
it, then loads it into a data store" — foundational infrastructure for analytics, BI, and ML.
Same three-stage structure as `data-engineering.md`'s findings, now confirmed from the same
source family but phrased independently: **ingestion** (IoT, SaaS apps, databases, varied
formats) → **transformation** (automated cleaning/enrichment/standardization) →
**storage/serving** (warehouse/lake/lakehouse, for stakeholder access).

**Pipeline types**: batch (scheduled intervals), streaming (continuous, real-time), data
integration (merging multiple sources), cloud-native. The two unfetched playlist titles name the
two most common concrete technology choices for implementing these types — Airflow for
batch/scheduled orchestration (the next topic in this category), Kafka for the streaming case —
useful as pointers even without their actual content.

**Design considerations an FDE needs to weigh**: data variety (structured vs. unstructured,
multiple source formats), throughput (volume the pipeline must sustain), latency (how fast data
needs to arrive for the use case), error management (failures shouldn't silently corrupt
downstream data), security (access control, encryption). The source notes modern pipelines
increasingly add automation and AI-assisted self-healing to manage this complexity at scale.

**Direct relevance to this system**: the `seed` CLI command built in ticket #2 is, in this
topic's vocabulary, a small batch data pipeline — ingestion (parsing the research doc),
transformation (slugifying titles into topic_ids, structuring into `RoadmapTopic`), and loading
(into the GitHub-Issues state store). The "error management" consideration maps directly onto
that command's idempotency guarantee (a duplicate topic is skipped, not silently double-created).

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
