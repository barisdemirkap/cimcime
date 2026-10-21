# NoSQL Databases

Category: core-software-engineering · Topic ID: nosql-databases

## Sources

- [fetched, thin] https://roadmap.sh/mongodb — mostly landing-page header, but the FAQ section rendered a real MongoDB-vs-PostgreSQL comparison.
- [fetched, thin] https://roadmap.sh/redis — only landing-page header/community-stats, no curriculum.
- [fetched] https://roadmap.sh/backend/types-of-nosql-databases — real content, substantive, the strongest source in this topic.
- [could not fetch] https://www.youtube.com/watch?v=0buKQHokLK8 — only footer/legal links, no transcript, standard YouTube failure pattern.
- [not fetched] https://www.youtube.com/watch?v=ruz-vK8IesE — not attempted; same domain/pattern confirmed failing on the sibling resource above.

## Findings

**The four main NoSQL types, with named real examples** (roadmap.sh/backend): key-value
(Redis, DynamoDB — ultra-fast lookups, no field-level queries or relationship modeling);
document (MongoDB — self-contained JSON/BSON documents with queryable internal structure,
good for hierarchical/object-like data like catalogs/profiles, but no native JOINs); wide-column
(Cassandra — column families distributed across servers, "built for managing data at scale,"
excels at massive write volumes for time-series/event logs); graph (Neo4j, Amazon Neptune —
nodes/edges, ideal "when relationships between data points are as important as the data
itself").

**Selection framework, three factors**: data shape (match structure to the database's model);
query patterns (NoSQL is "designed around the application's read patterns" rather than
flexible SQL joins — the inverse tradeoff from `sql.md`'s relational-join-centric model); scale
requirements (write volume, horizontal scaling, consistency needs).

**MongoDB vs. PostgreSQL, not a clear winner** (roadmap.sh/mongodb FAQ): MongoDB's strengths —
document model, flexible schema, built-in horizontal scaling; PostgreSQL's strengths — mature
relational model, powerful querying, reliability — explicitly framed as complementary, not
competing, strengths. This nuances `postgresql.md`'s "universal default" finding: PostgreSQL
is a strong default precisely because it also handles JSON, but pure-NoSQL databases still win
for specific shapes (graph relationships, massive write-heavy time-series).

**Direct relevance to this system**: this project uses neither — GitHub Issues as the state
store is closer in spirit to a document database (each issue is a self-contained record with
structured markers/labels) than a relational one, though it was chosen for its native
dependency-tracking and human-reviewable UI rather than for NoSQL-style scale properties.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
