# Git & GitHub

Category: core-software-engineering · Topic ID: git-github

## Sources

- [fetched, thin] https://roadmap.sh/git-github — only landing-page header/community-stats, no detailed curriculum.
- [fetched] https://git-scm.com/book/en/v2/Getting-Started-Installing-Git — real content, official source.
- [could not fetch] https://www.atlassian.com/git/tutorials/what-is-version-control — only navigation, the article body never rendered.
- [could not fetch] https://www.youtube.com/watch?v=mAFoROnOfHs — only footer/legal links, no transcript, standard YouTube failure pattern.

## Findings

**Installation, the one concretely verified piece of content** (git-scm.com): package-manager
installs per OS (`dnf`/`apt` on Linux, Xcode CLI Tools or a binary installer on macOS, the
official Git for Windows installer or Chocolatey on Windows), plus a from-source path for the
latest version requiring autotools/curl/zlib/openssl/expat/libiconv, compiled via the standard
`./configure && make && make install` sequence. Git itself can self-update by cloning its own
kernel.org source repo.

**Honest gap**: no resource for this topic actually explained Git's conceptual model
(commits, branches, merging) or GitHub's collaboration features (PRs, issues, CI/CD) beyond
what the roadmap doc's own one-line topic description already states — the Atlassian
version-control article and the roadmap.sh curriculum page both failed to render their actual
body content, and the video failed in the standard pattern. This topic is settled per ADR-0007
(≥1 real resource was read) but its coverage is unusually thin relative to other topics in this
category.

**Direct relevance to this system — the most load-bearing topic in this entire category for
Cimcime's own operation, even though barely documented by its sources**: this project's whole
state-store design (`GitHubIssuesStore`) and its "commit per ticket/category, push
immediately" workflow (already established and repeatedly used throughout every category in
this research project) depend entirely on Git/GitHub fundamentals — this is infrastructure the
system uses continuously, not background knowledge for a hypothetical future engagement like
most other topics in this category.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
