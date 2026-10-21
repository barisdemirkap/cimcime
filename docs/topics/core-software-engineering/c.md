# C++

Category: core-software-engineering · Topic ID: c

## Sources

- [fetched, thin] https://roadmap.sh/cpp — mostly navigation, but the FAQ section did render one real fact (C++ is a C superset; C compiles faster).
- [fetched] https://www.learncpp.com/ — real content, substantive.
- [fetched] https://roadmap.sh/cpp/vs-c — real content, substantive, this specific sub-page rendered fully unlike the landing page.
- [not fetched] https://youtu.be/vLnPwxZdW4Y — redirects to a standard YouTube watch URL; not followed, since every YouTube resource fetched in this entire project has returned only navigation/footer with no real transcript or description — the same failure pattern, assumed to recur here.

## Findings

**What C++ is** (roadmap.sh FAQ): "a superset of C, meaning it includes all of C's features
along with additional capabilities." C generally compiles faster; the actual choice depends on
problem type and tradeoffs, not a strict hierarchy.

**LearnCpp.com's 28-chapter structure, by theme**: foundational (0-11: dev environment,
compilers, basics, functions, debugging, data types, overloading/templates); intermediate
(12-18: references/pointers, user-defined types, OOP fundamentals, `std::vector`/`std::array`,
iterators/algorithms); advanced (19-28: dynamic memory, operator overloading, move
semantics/smart pointers, inheritance/virtual functions, template specialization, exceptions,
I/O). Covers C++11 through C++23 — actively maintained across standard versions.

**C vs. C++ decision framework** (roadmap.sh/cpp/vs-c, the most concrete source in this topic):
choose C++ for complex OOP systems, game engines, enterprise apps, real-time simulation, or
where RAII/smart pointers add value; choose C for embedded/firmware/microcontrollers, OS
kernels, device drivers, or anywhere minimal overhead and predictable hardware access matter
most. Memory: C is manual (`malloc`/`free`); C++ adds smart pointers for automatic release.
Concurrency: C relies on platform-specific POSIX threads; C++ has standardized `std::thread`/
`std::mutex`. Ecosystem: C evolves slowly/deliberately (valuable for long-lived systems); C++
evolves faster to stay competitive. **Named real systems**: C powers Linux, PostgreSQL,
SQLite, networking infra; C++ powers Unreal Engine, Chrome, Firefox, high-frequency trading.

**Direct relevance to this system**: none directly — no C/C++ in this project — but the
"minimal overhead + predictable behavior wins for long-lived systems" tradeoff echoes this
project's own preference for simple, explicit code (CLAUDE.md's "no premature abstraction," no
speculative flexibility) over more "modern"/abstracted but heavier alternatives.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
