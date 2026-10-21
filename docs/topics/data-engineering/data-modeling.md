# Data Modeling

Category: data-engineering · Topic ID: data-modeling

## Sources

- [fetched] https://www.ibm.com/think/topics/data-modeling — real content.
- [could not fetch] https://www.youtube.com/watch?v=CUR6rKrIEGc — title only, no transcript.

## Findings

**What it is**: a visual representation of an information system's data and the relationships
between data points — the goal, per IBM, is to "illustrate the types of data used and stored
within the system and the relationships among these data types."

**Three levels of abstraction, each less abstract than the last**: **conceptual** (high-level
system organization and business rules, simple notation, entity classes + relationships);
**logical** (more detail on concepts/relationships, formal notation, no technical/implementation
specifics yet); **physical** (least abstract — a finalized database schema, primary/foreign keys,
ready to implement). This three-level progression is a useful general vocabulary for describing
*how far along* a data design is, independent of any specific notation.

**The process, 6 steps**: identify entities → define their properties → map relationships → fully
assign attributes → apply normalization → iteratively validate. Named specialized approaches:
relational models, entity-relationship diagrams, object-oriented models, dimensional models
(built specifically for analytics).

**Why it matters, concretely**: fewer development errors, more consistency across the
enterprise, better database performance, and (the least obvious benefit) better communication
between technical and business teams — a shared, precise model gives both sides the same
vocabulary, which is the same value `GLOSSARY.md`/domain-modeling practice already provides in
this very project, just applied to database schema design instead of a codebase's domain
language.

**Direct relevance to this system**: this project's own `TopicRecord` dataclass and `StateStore`
protocol are literally a conceptual-to-logical data model for Cimcime's own domain (topics,
categories, phases) — the same conceptual→logical→physical progression described here maps
onto: ADR-0004's design discussion (conceptual) → the `StateStore` Protocol (logical) → the
`GitHubIssuesStore` label/marker encoding (physical).

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
