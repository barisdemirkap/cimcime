# Rust

Category: core-software-engineering · Topic ID: rust

## Sources

- [could not fetch] https://roadmap.sh/rust — only navigation/header/footer, no curriculum content, the standard roadmap.sh JS-SPA limitation.
- [fetched] https://doc.rust-lang.org/stable/rust-by-example/index.html — real content.
- [could not fetch] https://edu.anarcho-copy.org/Programming%20Languages/Rust/rust-programming-language-steve-klabnik.pdf — the fetch returned raw/corrupted PDF binary data and the tool then explicitly offered to substitute "general knowledge" about the book's typical structure instead of real extracted content; that substituted content was discarded per this project's no-fabrication rule and is not used below.
- [could not fetch] https://www.youtube.com/playlist?list=PLPoSdR46FgI412aItyJhj2bF66cudB6Qs — only footer/legal links, no real playlist/video content, standard YouTube failure pattern.

## Findings

**What Rust is** (Rust By Example): a modern systems programming language built on three
pillars — safety (memory-safe without a garbage collector), speed (high-performance systems
work), concurrency (built-in support for concurrent programming). This is the no-GC,
compile-time-safety model already described abstractly in the roadmap doc's own one-line
summary for this topic ("ownership model with strict compile-time checks... without a garbage
collector") — now confirmed from an official Rust-project source rather than just the roadmap's
own framing.

**24-chapter structure, by theme** (Rust By Example): fundamentals (Hello World, primitives,
custom types via `struct`/`enum`, variable bindings with mutability/scope/shadowing); language
features (expressions, control flow, functions/closures, generics, traits, macros); code
organization (modules, crates, Cargo as the official package manager, attributes); advanced
topics (scoping rules — ownership/borrowing/lifetimes — error handling, unsafe operations,
standard library types, testing, compatibility, documentation/benchmarking).

**Honest gap, explicitly flagged rather than filled**: the official Rust book (the single most
authoritative Rust-learning resource) could not actually be read — the PDF fetch returned
corrupted binary data, and rather than accept the tool's offered substitute ("general
knowledge" about what the book typically covers), that content was discarded. This leaves
ownership/borrowing/lifetimes documented only via Rust By Example's chapter list (names, not
depth) — a real, acknowledged limitation of this topic's research, not glossed over.

**Direct relevance to this system**: none directly — no Rust code in this project — but
ownership/borrowing as a compile-time safety mechanism is conceptually adjacent to this
project's own emphasis on reviewable, safe, reversible state changes (ADR-0001's approval
gates, git-based rollback) — a different mechanism (language-enforced vs. process-enforced)
aimed at a similar goal: catching unsafe operations before they cause damage.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
