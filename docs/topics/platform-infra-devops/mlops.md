# MLOps

Category: platform-infra-devops · Topic ID: mlops

## Sources

- [fetched] https://aws.amazon.com/what-is/mlops/ — real content.
- [could not fetch] https://towardsdatascience.com/machine-learning-operations-mlops-for-beginners-a5686bfe02b2/ — HTTP 403, consistent with this domain's repeated failures throughout this project.
- [could not fetch] https://web.archive.org/web/20251126053103/https://neptune.ai/blog/mlops — Claude Code is unable to fetch from web.archive.org at all (tool-level restriction, not a page error).
- [could not fetch] https://www.youtube.com/watch?v=-dJPoLm_gtE — only navigation/footer content returned, no transcript or description, the standard YouTube failure pattern for this entire project.

## Findings

**What MLOps is** (AWS): "a set of practices that automate and simplify machine learning
workflows and deployments" — unifying ML application development (Dev) with ML system
deployment and operations (Ops) to standardize processes across the whole ML lifecycle
(development, testing, integration, release, infrastructure management). This is the DevOps
pattern (`devops-skills.md`) applied specifically to ML systems, not a separate discipline.

**Four core principles, named directly**:
- **Version control** — tracking changes in ML assets for reproducibility and rollback;
  training code and model specs go through code review and versioning, same as application
  code — the same version-control-as-safety-net pattern already seen generally in
  `version-control-systems.md` and specifically backing ADR-0001's design (git/backups as the
  safe-rollback mechanism that lets AI act autonomously on routine work).
- **Automation** — automating pipeline stages end-to-end: data ingestion, preprocessing,
  training, validation, deployment, triggered by data changes, code changes, or messaging
  events.
- **"Continuous X"** — four continuous activities: continuous integration (validation extended
  to data and models, not just code), continuous delivery (automatic deployment of trained
  models), continuous training (automatic model retraining), continuous monitoring (tracking
  data and model metrics over time) — directly extends `devops-skills.md`'s CI/CD pattern with
  two ML-specific additions (continuous training, continuous monitoring) that have no analogue
  in plain software CI/CD.
- **Model governance** — collaboration among data scientists/engineers/stakeholders, feedback
  mechanisms to collect prediction-quality signal and retrain further, plus data
  protection/compliance — connects to the human-approval-gate principle (ADR-0001) and to
  `ai-governance.md`'s broader governance findings.

**Named AWS tooling**: Amazon SageMaker Experiments (tracking training artifacts), SageMaker
Pipelines (automated scheduling), SageMaker Model Registry (centralized version/metadata
tracking) — a concrete implementation of the version-control + automation principles above.

**Direct relevance to this system**: this project doesn't train ML models itself, so MLOps
doesn't apply literally — but its structure (version everything, automate the pipeline,
continuously monitor, govern via human-in-the-loop feedback) is the same shape as this
project's own git-per-ticket + CI test suite + two-axis review + ADR-0001 approval gates,
just applied to agent/code artifacts instead of trained models. One more instance of the
recurring pattern: Dev/Ops discipline generalizes across whatever is being shipped.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
