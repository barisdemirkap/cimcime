# Data Engineering

Category: data-engineering · Topic ID: data-engineering

## Sources

- [could not fetch] https://roadmap.sh/data-engineer — the roadmap.sh main landing page, consistent with that site's client-rendered pages failing (distinct from its comparison sub-pages, which have fetched successfully elsewhere in this roadmap).
- [fetched] https://www.ibm.com/think/topics/data-engineering — real content.
- [could not fetch] https://www.youtube.com/watch?v=PHsC_t0j1dU — title only, no transcript.

## Findings

**What it is**: designing and building systems for aggregating, storing, and analyzing data at
scale — the infrastructure layer that turns raw data into something decision-making can actually
use.

**Three core phases of a data pipeline**: **ingestion** (pulling data in from databases, cloud
platforms, IoT devices, websites into one unified system); **transformation** (cleaning,
error-correction, standardization); **serving** (delivering the processed result via
visualization, reporting, or as input to ML models). These three phases will recur as the
organizing structure for `data-pipelines.md`, the next topic in this category.

**Two integration approaches**: **ETL** (extract-transform-load — standardize before storing;
the most common approach) vs. **ELT** (extract-load-transform — store centrally first, transform
later, more flexible). Core tooling: cloud platforms (AWS/Azure/GCP), SQL/NoSQL databases,
storage systems (warehouses/lakes/lakehouses), and languages (SQL, Python, Scala, Java).

**Organizational placement**: data engineers work alongside data scientists and analysts,
specifically responsible for the reliability and quality of the datasets those other roles then
build on — a useful boundary to know when an FDE engagement touches both data engineering and
data science/ML work: who owns correctness of the underlying data vs. who owns what's built on
top of it.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
