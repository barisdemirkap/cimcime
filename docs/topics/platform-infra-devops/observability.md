# Observability

Category: platform-infra-devops · Topic ID: observability

## Sources

- [fetched] https://www.ibm.com/think/topics/llm-observability — real content.
- [fetched] https://roadmap.sh/ai-engineer/observability-tools — real content, another roadmap.sh sub-page that rendered successfully.
- [could not fetch] https://www.youtube.com/watch?v=o76xU3RQ47Q — title only, no transcript.

## Findings

**What LLM observability is** (IBM): collecting real-time behavioral/performance/output data
from an LLM app — metrics, traces, logs — to monitor, debug, and optimize at scale. Three
reasons it matters: quality assurance (continuous output evaluation across
correctness/relevance/factual consistency); swift troubleshooting (pinpoint root cause — bad
training data, poor fine-tuning, a third-party service failure); performance gains (track
latency/token usage/throughput to find bottlenecks and cut cost).

**Three metric categories** (IBM): system performance (latency, throughput, error rate);
resource consumption (CPU/GPU, memory, token usage); model behavior (correctness, factual
accuracy, engagement, response quality).

**Named observability tools, with real pricing and a direct cross-corroboration** (roadmap.sh):
**Langfuse** (open-source, full tracing across LLM/tool/retriever/agent steps, self-hostable
MIT license, cloud from $29/mo); **LangSmith** (LangChain's own tool, nested trace trees, Plus
$39/seat/mo); **Arize Phoenix** (embedding-based grouping of similar production traces, free
self-hosted, AX Pro $50/mo) — **this is the same Arize already cited in
`debugging-agent-logic.md`/`building-eval-pipelines.md`**, now independently named again from a
completely different source as a leading observability tool, not just a glossary publisher;
**Braintrust** (eval-focused, can block CI/CD deployment if quality drops below threshold, Pro
$249/mo) — **also already cited**, in `prompt-management.md`, now corroborated a second time;
**AgentOps** (multi-agent debugging, session replay, loop detection); **Laminar** (open-source,
plain-language "Signals" flagging infinite loops, fully free self-hosted).

**Modern shift toward autonomous troubleshooting** (IBM): agent-based diagnostics that detect
issues instantly, analyze root cause, apply fixes automatically, and enable predictive
maintenance — the same "agentic shift" `day-2-operations.md` just named for infrastructure ops
generally, now specifically for the observability/debugging layer.

**Direct relevance to this system — closing a real, concrete gap already flagged three times**:
`prompt-management.md`, `agent-architectures.md`, and `building-eval-pipelines.md` all
independently flagged that this project has no formal eval/observability tooling for its own
agent runs. This topic now names the *specific real tools* (Braintrust, Arize, Langfuse) that
would fill that gap, not just the abstract concept — a concrete next step if that gap is ever
prioritized, rather than a vague "add evals someday."

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
