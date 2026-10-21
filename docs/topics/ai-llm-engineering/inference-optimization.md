# Inference Optimization

Category: ai-llm-engineering · Topic ID: inference-optimization

## Sources

- [could not fetch] https://cloud.google.com/discover/inference-optimization?hl=en — the page truncated before real body content; notably, the fetch tool itself correctly refused to fabricate a summary from general knowledge and said so explicitly, offering only a disclaimed "general overview" that was not used here.
- [fetched] https://nebius.com/blog/posts/inference-optimization-techniques-solutions — real content.
- [could not fetch] https://www.youtube.com/watch?v=9tvJ_GYJA-o — title only, no transcript.
- [could not fetch] https://www.youtube.com/watch?v=_xM8scs4_x4&t=54s — title only, no transcript.

## Findings

**Why production inference needs active optimization**: models run slower in production than in
development because of infrastructure differences, unexpected real-world inputs, and
concurrency the dev environment never saw — the gap is environmental, not usually a flaw in the
model itself.

**Six metrics to actually measure before optimizing**: latency, throughput, memory usage,
CPU/GPU utilization, cost per inference, error rate — with an explicit emphasis on establishing
a *baseline* first, the same principle already seen independently in `roi-ai-impact.md` and
`last-mile-integration.md`.

**Model-simplification techniques**: pruning (remove unneeded weights/neurons/channels);
quantization (lower numeric precision, e.g. 32-bit → 8-bit, cutting memory footprint);
knowledge distillation (train a smaller "student" model to mimic a larger "teacher"); plus
weight sharing, low-rank factorization, and early-exit mechanisms named more briefly.

**Infrastructure-level techniques** (distinct from changing the model itself): deploying closer
to users/data, general infrastructure tuning, caching to avoid repeated computation; parallelism
and batching to use multiple processors/GPUs for higher throughput. Named serving frameworks:
ONNX Runtime, TensorFlow Serving, Kubeflow — these automate parallelism/batching/versioning
rather than requiring it to be hand-built per deployment.

**Direct relevance to this system**: this project doesn't do model-level inference optimization
(it calls Claude via Claude Code, not a self-hosted model it can prune/quantize), but the
infrastructure-level techniques apply directly to its own real bottleneck — the O(n) `gh issue
list` scan per write, already flagged during ticket #1's review and accepted as a known tradeoff
at small scale. "Caching to avoid repeated computation" is exactly the fix that tradeoff would
need if it ever stopped being acceptable (e.g. caching the issue list between calls within one
session rather than re-fetching on every write).

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
