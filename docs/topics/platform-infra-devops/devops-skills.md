# DevOps Skills

Category: platform-infra-devops · Topic ID: devops-skills

## Sources

- [fetched] https://www.coursera.org/articles/what-is-devops — real content.
- [could not fetch] https://www.youtube.com/watch?v=Xrgk023l4lI — title only, no transcript.
- [could not fetch] https://www.youtube.com/watch?v=j5Zsa_eOXeY — title only, no transcript.

## Findings

**What it is**: unifying development and operations into one collaborative unit across the
whole product lifecycle, instead of sequential handoffs between siloed teams — oriented around
quick, incremental, continuous delivery.

**Four foundational principles**: systems thinking (judge overall system performance, not
individual team metrics in isolation); culture (collaboration, experimentation, continuous
learning as explicit values, not just process); automation (remove repetitive manual steps to
speed delivery); configuration management (keep the product consistent across its whole
lifecycle, not just at release).

**Three interconnected practices**: continuous testing (automated feedback woven through
development, not just at the end); continuous integration (regularly incorporate
feedback/fixes, keep branches converging); continuous delivery (changes stay in an
always-deployable state, automatable release). Together, CI/CD is what makes small, frequent
releases possible instead of large infrequent ones — directly connecting to
`tradeoffs-scope-speed-quality.md`'s iron-triangle finding: CI/CD is a structural way to shrink
the unit of "scope" per release, which shrinks the risk each individual release carries.

**Named tooling**: Git, Docker, Jenkins (CI/CD pipelines), Kubernetes — the same containerization
and orchestration tools already researched individually elsewhere in this category
(`docker.md`, `kubernetes.md`), now placed in their actual DevOps-practice context rather than
studied as standalone technologies.

**Direct relevance to this system**: this project's own git-commit-per-ticket, run-full-suite-
before-committing, two-axis-review-before-merge workflow (established across tickets #1-#7) is a
small-scale instance of exactly this CI/CD discipline — automated testing integrated throughout
(the fast + live integration suites), continuous integration (never leaving a broken state on
`main`), continuous delivery in spirit (each closed ticket is immediately pushed, deployable in
the sense that the next ticket builds directly on it).

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
