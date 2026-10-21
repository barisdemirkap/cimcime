# Spark

Category: data-engineering · Topic ID: spark

## Sources

- [fetched] https://spark.apache.org/docs/latest/ — real content, the official docs.
- [fetched] https://sparkbyexamples.com — real content, a dedicated tutorial site.
- [could not fetch] https://www.youtube.com/playlist?list=PL2IsFZBGM_IHCl9zhRVC1EXTomkEp_1zm — title only ("PySpark Zero to Hero"), no content.

## Findings

**What it is**: a unified analytics engine for large-scale data processing, with high-level APIs
in Java, Scala, Python, and R, and an optimized engine that supports general execution graphs —
i.e. Spark itself is internally organized around DAGs too, the same structure `airflow.md`
already described at the orchestration level, just applied at the data-computation level
instead.

**Core API surfaces**: RDDs (Resilient Distributed Datasets — the original, lower-level API);
DataFrames/Datasets (newer, structured, relational-query style — the one sparkbyexamples.com
emphasizes for most real work); Spark SQL (SQL over structured data). Specialized modules:
Structured Streaming (newer stream processing via relational queries), MLlib (machine learning
algorithms), GraphX (graph processing), and legacy Spark Streaming (DStreams API, older).

**Execution modes**: `local`/`local[N]` for single-machine development, or distributed via
Standalone, YARN, or Kubernetes for production scale — the same "start local, scale out later"
pattern this whole roadmap has emphasized elsewhere (e.g. `docker.md`/`kubernetes.md`, not yet
researched, likely echo this).

**Learning resource structure** (sparkbyexamples.com): architecture/installation/SparkSession
basics → RDD operations → DataFrame/SQL operations → reading/writing multiple data formats
(CSV/JSON/Parquet/Avro/ORC/XML) → streaming integration (Kafka, TCP, filesystem) → advanced
(GraphFrames, HBase, Hive, performance tuning). Useful as a concrete syllabus shape for anyone
onboarding onto Spark specifically, not just an abstract "learn Spark" pointer.

**Relevance to an FDE engagement**: Spark and Airflow are frequently paired in real deployments —
Airflow orchestrates *when* a job runs (the DAG of task dependencies), Spark does the actual
heavy data transformation *within* one of those tasks. Knowing both separately, and that they
compose rather than compete, is the kind of integration knowledge this whole category is about.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
