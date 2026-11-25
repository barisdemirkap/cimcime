---
status: accepted
---

# Memory changes are judged by a deterministic, retrieval-first eval with pre-registered thresholds

Hybrid search shipped under ADR-E with a gate ("RRF recall@5 at least 10 points above FTS5") that was never
measured. Phase 7 planning (Lore, Mastra, LongMemEval) proposed much more. The board (ADR-0013) found the plan
needed revision; the owner adopted a narrower scope, recorded in the decisions table on 2026-11-25.

## Decision

Build only slices 1-4 and the concurrency fix:

- **Race fix first.** The `Stop` and `PreCompact` hooks are separate processes and can write `memory.db`
  together. `memory.db` now runs in WAL mode with a 30 s `busy_timeout`, and `snapshot()` takes the write
  lock (`BEGIN IMMEDIATE`) before reading the last archive offset, so concurrent hooks archive disjoint byte
  ranges once. A snapshot with no new bytes is skipped for hook triggers. `tests/test_memory_race.py`
  covers threads and real processes.
- **Eval harness** (`cimcime.memory_eval`, `cimcime eval-memory`): one JSON fixture format (rows plus gold
  questions), scored by row-id recall@k, MRR and nDCG with stdlib code (`ir_measures` is not installed and is
  not added), by category (extraction, multi-session, knowledge-update, temporal, preference,
  abstention), with paired bootstrap CIs over questions. No model is called; the hybrid path can run on a
  stdlib hashing embedder (plumbing only) or local Ollama on request. Reports include degraded-mode rate
  (hybrid asked, keyword served) and brief-absent rate.
- **Pre-registered thresholds** live in `docs/memory-eval/thresholds.toml`, committed before the first measured
  run; fixtures are pinned by SHA-256 and a mismatch aborts.
- **Fixture data.** The repo holds one frozen fixture of invented (synthetic) rows to test the harness. The
  validator rejects sensitive-scope rows and requires `provenance: synthetic` in a synthetic fixture. Real gold
  questions are owner-written: `scripts/draft_eval_candidates.py` only drafts candidates from raw message and
  decision rows into `~/.local/state/cimcime/eval-candidates/`, refuses any path inside a git work tree, and
  skips sensitive scopes.
- **Slice 4**, each behind its own eval variant and off by default: abstention (`evidence=False`, "no
  evidence", when the best hit covers under a set share of the query's content words), neighbour expansion
  (adjacent message chunks, same scope, flagged, bounded), recency tiebreak (near-tied scores ordered newest
  first). They are enabled in production only after their gates pass on the owner's real gold set.

## Not decided here

Slices 5-6 (typed pins, supersession, contradiction detection, citation verification) wait for a measured
failure and for pin storage and concurrency prerequisites. The code-progress eval and the costly model layers
(observer, generative eval, cross-family grader, A/B runs) stay held behind a named need and kill criteria.

## Consequences

- The first synthetic run (84 rows, 41 questions) says: keyword search is already strong on a tiny haystack,
  abstention gates pass, neighbour and recency gates do not clear their pre-registered bars (CIs include zero
  at n=6 and n=8), and the hashing stand-in embedder does not beat FTS5. None of this is evidence about
  production quality; it proves the harness. The real answer needs the owner's gold set and a larger haystack.
- Owner time: about 1-2 hours to approve or edit candidates and write the multi-session ones (first 40
  questions), plus a decision on turning each slice-4 flag on or off from its gate.

## Unverified external numbers

The planning notes quote figures taken from web pages through a small summarizing model, never re-checked
against primary pages. They are context only, not evidence and not targets: Mastra Observational Memory
LongMemEval 84.23% (gpt-4o) and 94.87% (gpt-5-mini), RAG top-20 80.05%, full context 60.2%, 97-99% prompt cache hits,
about 57M tokens to ingest LongMemEval S; Lore 17/20 versus 10/20 on its own 20-question eval; LongMemEval sizes
(500 questions, S about 115k tokens, dataset about 270 MB) and cost estimates in tokens. Re-verify from the primary
pages before quoting any of them in a later decision.
