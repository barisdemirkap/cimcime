# Python

Category: core-software-engineering · Topic ID: python

## Sources

- [fetched] https://roadmap.sh/python — real content (this specific sub-page rendered, unlike roadmap.sh's usual JS-SPA landing pages).
- [could not fetch] https://www.digitalocean.com/community/tutorials/how-to-write-your-first-python-3-program — only nav/footer returned, no article body.
- [fetched] https://developers.google.com/edu/python — real content.
- [could not fetch] https://www.youtube.com/watch?v=4M87qBgpafk — only footer/legal links, no transcript, standard YouTube failure pattern.

## Findings

**What a Python developer does** (roadmap.sh): building web services, automating tasks,
performing data analysis — spanning web dev (Django/Flask/FastAPI), data science/ML/AI,
automation, cloud/backend services, and (less commonly) cybersecurity/embedded/games.

**Core learning path** (roadmap.sh): Python basics (data types, functions, OOP); essential
libraries (NumPy, Pandas, Requests); data structures (linked lists, trees, hash maps — overlaps
directly with the separate `data-structures-algorithms` topic in this same category);
version control (Git); portfolio projects for practical problem-solving.

**Key framing — Python is backend-only in practice**: "Python functions as a backend language
since JavaScript dominates browser environments." PyScript exists for frontend Python but
"this is not a normal practice as it adds dependencies" — a clear, source-stated boundary
rather than an assumption.

**Domain-specific skill branching** (roadmap.sh): backend devs need RESTful design/APIs/SQL;
data scientists need ML tooling; automation specialists need IaC and cloud platforms — the same
"match the stack to the engagement" principle already found in `learn-a-programming-language.md`.

**Google's Python Class structure**: sequential curriculum — setup, fundamentals, strings/lists/
sorting, dictionaries/file handling, regex, utilities — delivered as written guides + two days
of lecture videos (mirrors Google's own internal training) + exercises building up to full
programs handling text files, processes, and HTTP connections. CC-BY-4.0 licensed, with a
community forum.

**Direct relevance to this system**: this project IS a Python backend system in roadmap.sh's
own sense — no frontend, `cimcime.cli`/`state_store.py`/`roadmap.py` as a pure
automation/orchestration tool talking to GitHub's API, matching the "automation specialists
need IaC and cloud platforms" domain branch almost exactly (GitHub Issues as the state backend
instead of a database, `gh` CLI instead of a cloud SDK).

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
