# SQL

Category: core-software-engineering · Topic ID: sql

## Sources

- [fetched, thin] https://roadmap.sh/sql — only landing-page header/community-stats, no curriculum.
- [fetched] https://roadmap.sh/courses/sql — real content, substantive, this specific sub-page rendered.
- [fetched] https://www.sqltutorial.org/ — real content, substantive, independently converging.
- [could not fetch] https://www.youtube.com/watch?v=p3qvj9hO_Bo — only footer/legal links, no transcript, standard YouTube failure pattern.

## Findings

**Converging core SQL structure, confirmed across two independent sources**: both roadmap.sh's
course (9 modules, 55+ lessons, 100+ challenges) and sqltutorial.org (15 sections) follow the
same progression — basics (SELECT/WHERE/ORDER BY/LIMIT) → data manipulation (INSERT/UPDATE/
DELETE) → schema design (table creation, data types, constraints) → multi-table joins (inner/
left/right/full outer/cross/self — sqltutorial.org names all six join types explicitly) →
aggregation/grouping → subqueries and CTEs, including recursive CTEs → window functions for
advanced analytics/ranking.

**Additional named constructs** (sqltutorial.org): set operations (UNION, INTERSECT, MINUS);
views and triggers; conditional expressions (CASE, COALESCE, NULLIF); scalar function
categories — string, date, math, window functions — aggregate functions named specifically
(AVG, COUNT, SUM, MAX, MIN).

**Target audience is broader than "developer"** (sqltutorial.org): developers, database
administrators, data analysts, *and* data scientists — directly corroborating
`learn-a-programming-language.md`'s and `python.md`'s earlier finding that SQL is a mandatory
baseline skill regardless of specialization, cutting across every domain branch named so far
in this category.

**Direct relevance to this system**: this project doesn't use SQL at all — its persistence
layer is GitHub Issues via `GitHubIssuesStore`, not a relational database — but window
functions/CTEs/joins remain directly relevant background if a future engagement's data work
(per `sql.md`'s own cross-domain framing) requires relational-database fluency, which multiple
earlier topics (`backend.md`, `learn-a-programming-language.md`) already flagged as a near-
universal FDE requirement.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
