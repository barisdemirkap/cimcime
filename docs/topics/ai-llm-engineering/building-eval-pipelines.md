# Building Eval Pipelines

Category: ai-llm-engineering · Topic ID: building-eval-pipelines

## Sources

- [fetched] https://arize.com/glossary/evaluation-pipeline/ — real content.
- [fetched] https://roadmap.sh/ai-engineer/automated-regression-testing — real content (another roadmap.sh comparison/detail sub-page that fetched successfully, unlike its landing pages).
- [could not fetch] https://www.youtube.com/playlist?list=PLEneLIDJFpcA — no title or content recovered at all.

## Findings

**What an evaluation pipeline actually is** (arize.com): a multi-stage data flow, not just the
scoring step — selection (which records to evaluate) → preparation (extract/format eval inputs)
→ execution (run the system) → scoring (apply evaluators) → persistence (store results +
metadata) → aggregation (summarize) → action (trigger a response to the result). The key point:
"the pipeline is the path data travels before and after that [scoring] step," not the scorer
itself.

**Reproducibility requirement**: version five things together — dataset, prompt, model, scorer,
and harness — otherwise a result can't be trusted to mean the same thing next time it's run.
Pipelines should run asynchronously off production traces (not inline in the request path);
sampling rates must be deliberate and recorded, not incidental; storage must distinguish a
*scorer* failure from an actual *model* failure (conflating them corrupts the signal).

**Offline vs. online** (arize.com): offline pipelines run against a fixed dataset for
gating/release decisions; online pipelines continuously sample live traffic to watch production
quality. Most real teams run both, for different purposes.

**LLM-specific regression testing** (roadmap.sh) — the sharpest, most actionable source in this
topic: LLM regressions are **semantic**, not functional — the app still responds, but the answer
may be subtly wrong, lower quality, or inconsistent with a previous run, with no code change at
fault. Three common triggers: prompt changes (even minor wording shifts response quality/
hallucination rate); model updates (provider switch, version bump, temperature change); retrieval
config changes in RAG systems (chunk size, embedding model, retrieval threshold — can silently
reduce faithfulness with zero code changes). Suite components: a golden dataset with
representative prompts + quality rubrics, evaluation metrics (faithfulness, relevance,
hallucination rate, task completion), LLM-based scoring for open-ended answers, human annotation
for high-stakes cases. CI/CD pattern: eval-gated deployment — block the deploy if a critical
metric falls below threshold (tools named: MLflow, Braintrust, Langfuse).

**Direct, concrete relevance to this system — closes a gap flagged twice already**: both
`prompt-management.md` and `agent-architectures.md` independently noted this project has no
formal evaluation/baseline mechanism for judging whether a topic-agent's research output is
actually good. This topic gives the concrete shape such a thing could take: a "golden dataset"
of a handful of already-researched topics with known-good study files, a rubric scoring whether
a new topic-agent run's output is faithful to its sources and substantive (not just "did it run
without error"), run offline before trusting a batch of new research. Not something to build
right now mid-research, but now a concretely specified gap rather than a vague one.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
