# Memory eval runbook

Decision and scope: ADR-0017. Exit criterion for this phase: someone other than the author can run the
steps below and read a pass/fail per pre-registered gate.

## Run it

```
uv run python -m cimcime.cli eval-memory --fixture tests/fixtures/memory_eval/synthetic-v1.json --embedder hash
```

- `--embedder none` (default): keyword variants only; hybrid variants and their gates show as skipped.
- `--embedder hash`: stdlib stand-in vectors, proves the hybrid plumbing; says nothing about embedding quality.
- `--embedder ollama`: local `nomic-embed-text` through Ollama, the only run that can settle the ADR-E gate. If
  Ollama is down the hybrid variant reports a degraded rate above zero and its gate fails.
- `--embedder unavailable`: simulate an outage to see the degraded report.
- `--out-dir DIR` also writes `report.json` and `report.md`; `--json` prints the JSON.
- Exit code 0: every gate passed or was skipped. 1: a gate failed. 2: fixture invalid or its SHA-256 differs from the
  pinned one.

## Read the report

Header lines give the fixture and config hashes (reproducibility), the brief-absent rate (questions whose scope has
no brief) and the brief hit rate. The variant table shows recall@5, recall@10, MRR, nDCG@10 with 95% bootstrap
CIs, the per-category recall, abstention recall, answer kept and knowledge-update latest-first rates, and the
degraded-mode rate. `recall_ctx@5` counts neighbour-expanded rows too. The gate table is the verdict: a gate only
passes when its pre-registered delta and CI condition hold.

## Real gold set (owner)

1. `uv run python scripts/draft_eval_candidates.py` writes drafts to `~/.local/state/cimcime/eval-candidates/`
   (never the repo). Open the `.md`, mark each candidate approve, edit or reject in the `.json`, and add
   multi-session questions by hand.
2. Export the approved questions and their gold rows into the fixture format (see the synthetic fixture:
   `docs` rows with `table`, `id`, `at`, `scope`, `trust`, `text`; `questions` with `category`, `query`, `gold`,
   `superseded`, `scope`). Keep it outside the repo, drop `synthetic`, and pin its SHA-256 in a private copy of
   `docs/memory-eval/thresholds.toml` before the first run.
3. Run with `--embedder ollama` and decide each flag (hybrid, abstention, neighbours, recency) from its gate.

Never commit real rows, drafts or reports. Change a threshold only in a commit that says why, never after a result.

## Slice-4 flags

`Memory.search(abstain_min_coverage=, neighbours=, recency_tolerance=)`; defaults keep the old behaviour. Nothing
in the hooks or CLI turns them on yet.
