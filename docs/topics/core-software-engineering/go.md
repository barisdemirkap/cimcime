# Go

Category: core-software-engineering · Topic ID: go

## Sources

- [fetched] https://roadmap.sh/golang — real content.
- [fetched] https://go.dev/doc/ — real content, independently converging.
- [fetched] https://go.dev/doc/tutorial/getting-started — real content, concrete worked example.
- [could not fetch] https://www.youtube.com/watch?v=8uiZC0l4Ajw — only footer/legal links, no transcript, standard YouTube failure pattern.

## Findings

**What Go is** (go.dev + roadmap.sh, converging): open-source, built at Google; "expressive,
concise, clean, and efficient"; fast, statically typed, compiled, but "feels dynamically typed"
in use; built-in garbage collection; excellent/novel concurrency mechanisms and type system.

**Primary use cases** (roadmap.sh): backend development and platform programming —
microservices, APIs, server-side apps — with named real-world adopters (Uber, Dropbox) for
scalable services. Go developer work centers on RESTful microservices, integration systems,
and optimization — directly corroborating `learn-a-programming-language.md`'s earlier finding
that Go is the FDE's preferred choice for "infrastructure-heavy or startup environments."

**Required skills** (roadmap.sh): Go fundamentals, pointer management, standard library,
garbage collection, testing/debugging tooling, version control — standard, no surprises.

**Concrete worked "Hello World" tutorial** (go.dev): `go mod init` → write `hello.go` → `go run
.` → discover external packages via pkg.go.dev → `go mod tidy` to pull dependencies and update
`go.mod`/`go.sum`. Notably simple, minimal-ceremony onboarding compared to, e.g., Java's
roadmap (`java-scala.md`) which emphasized JVM/Hibernate/Spring Boot complexity even at the
"required skills" stage — a real, source-grounded contrast in onboarding friction between the
two backend languages.

**Go's own documentation structure** (go.dev): notably includes a first-class "Accessing
Databases" guide covering `database/sql` — handles, querying, prepared statements,
transactions, SQL-injection prevention — named explicitly as a top-level doc section, not
buried; also covers module publishing/versioning as a first-class concern (release workflow,
semantic versioning, repository conventions) — reflecting Go's own ecosystem emphasis on
clean, versioned module distribution.

**Direct relevance to this system**: this project is Python, not Go, but the "infra-heavy,
microservices, scalable services" framing is exactly `cimcime`'s own category-agent/topic-agent
dispatch model in spirit — many small, concurrent, independent units of work — even though the
actual implementation uses Python + GitHub Issues rather than Go + goroutines.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
