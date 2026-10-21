# PostgreSQL

Category: core-software-engineering · Topic ID: postgresql

## Sources

- [fetched, thin] https://roadmap.sh/postgresql-dba — only landing-page header/community-stats, no curriculum.
- [fetched] https://www.postgresql.org/docs/ — real content, official source.
- [fetched] https://www.w3schools.com/postgresql/postgresql_intro.php — real content, independently converging.
- [could not fetch] https://www.youtube.com/watch?v=qw--VYLpxG4 — only footer/legal links, no transcript, standard YouTube failure pattern.

## Findings

**What PostgreSQL is** (w3schools): a free, open-source database system supporting both
relational (SQL) and non-relational (JSON) queries — this dual relational/JSON capability is
the specific feature `learn-a-programming-language.md` and `scaler.com`'s tech-stack finding
already flagged ("PostgreSQL is the pragmatic universal default, now handling document-style
data and vector search too") — this topic confirms the JSON half of that claim directly from
PostgreSQL's own framing.

**Language compatibility** (w3schools): Python, Java, C/C++, C#, Node.js, Go, Ruby, Perl, Tcl —
effectively every language already researched in this category has first-class PostgreSQL
support, reinforcing why it's the "pragmatic universal default" rather than a niche choice.

**Origin** (w3schools): development began in 1986 at UC Berkeley, originally UNIX-only, now
cross-platform (Windows/macOS/etc.) — a genuinely old, mature, battle-tested system, not a
recent entrant.

**Documentation structure** (postgresql.org): versioned manuals (v14 through v19 RC, each with
online + PDF A4/Letter formats), release notes, books, tutorials, FAQ, wiki, and translated
manuals (Chinese/French/Japanese/Russian) — a mature, heavily-versioned documentation
ecosystem reflecting the project's own long history.

**Direct relevance to this system**: this project doesn't use PostgreSQL (its state store is
GitHub Issues, not a relational DB) — but this topic closes a loop opened in
`learn-a-programming-language.md`: PostgreSQL's dual relational+JSON+vector-search capability
is exactly why multiple earlier sources named it the FDE's default database choice regardless
of client stack, now independently confirmed from PostgreSQL's own documentation.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
