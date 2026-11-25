"""Deterministic, retrieval-first memory eval (ADR-0017, docs/memory-eval.md).

One fixture format (rows + gold questions), scored by row-id recall@k, MRR and nDCG with stdlib
implementations, per question category (extraction, multi-session, knowledge-update, temporal,
preference, abstention), compared across search variants by paired bootstrap confidence intervals.
Thresholds are pre-registered in a TOML config, never chosen after seeing a result.

No model is ever called: the only embedder shipped here is a hashing bag-of-words stand-in, so
hybrid mode can be exercised hermetically; `ollama` is opt-in and local. The fixture is a frozen,
SHA-256-pinned JSON file; the repo's own fixture is synthetic only."""

from __future__ import annotations

import hashlib
import json
import math
import random
import tempfile
import tomllib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from cimcime import memory as mem_mod
from cimcime.memory import EmbedderUnavailable, Memory, normalize

FORMAT = 1
CATEGORIES = ("extraction", "multi-session", "knowledge-update", "temporal", "preference", "abstention")
PRIMARY_METRICS = ("recall@5", "recall@10", "mrr", "ndcg@10")


class FixtureError(ValueError):
    """The fixture is malformed (the message lists every problem)."""


class ManifestError(ValueError):
    """The fixture bytes do not match the SHA-256 pinned in the config."""


# --- metrics (stdlib; binary relevance, deduplicated ranking) ----------------------------------


def dedup(ranked: list[str]) -> list[str]:
    return list(dict.fromkeys(ranked))


def recall_at_k(ranked: list[str], gold: set[str], k: int) -> float:
    return len(gold & set(dedup(ranked)[:k])) / len(gold) if gold else 0.0


def reciprocal_rank(ranked: list[str], gold: set[str]) -> float:
    for i, row in enumerate(dedup(ranked), start=1):
        if row in gold:
            return 1.0 / i
    return 0.0


def ndcg_at_k(ranked: list[str], gold: set[str], k: int) -> float:
    if not gold:
        return 0.0
    dcg = sum(1.0 / math.log2(i + 1) for i, row in enumerate(dedup(ranked)[:k], start=1) if row in gold)
    ideal = sum(1.0 / math.log2(i + 1) for i in range(1, min(len(gold), k) + 1))
    return dcg / ideal


def latest_above_superseded(ranked: list[str], gold: set[str], superseded: set[str]) -> float:
    """1.0 when the gold (latest) row is retrieved and ranks above every superseded row."""
    order = dedup(ranked)
    pos = [order.index(g) for g in gold if g in order]
    if not pos:
        return 0.0
    first_gold = min(pos)
    return 1.0 if all(order.index(s) > first_gold for s in superseded if s in order) else 0.0


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def bootstrap_ci(values: list[float], resamples: int, seed: int, level: float) -> tuple[float, float] | None:
    if not values:
        return None
    rng, n = random.Random(seed), len(values)
    means = sorted(sum(values[rng.randrange(n)] for _ in range(n)) / n for _ in range(resamples))
    return _percentiles(means, level)


def paired_bootstrap(a: list[float], b: list[float], resamples: int, seed: int, level: float) -> dict:
    """Mean of (b - a) over the same questions, with a percentile CI from resampling questions."""
    if len(a) != len(b):
        raise ValueError("paired samples differ in length")
    diffs = [y - x for x, y in zip(a, b)]
    out = {"n": len(diffs), "delta": mean(diffs), "ci_low": None, "ci_high": None}
    ci = bootstrap_ci(diffs, resamples, seed, level)
    if ci:
        out["ci_low"], out["ci_high"] = ci
    return out


def _percentiles(sorted_means: list[float], level: float) -> tuple[float, float]:
    r = len(sorted_means)
    tail = (1 - level) / 2
    return sorted_means[int(tail * r)], sorted_means[min(r - 1, int((1 - tail) * r))]


# --- stand-in embedder -------------------------------------------------------------------------


class HashEmbedder:
    """Deterministic hashing bag-of-words vectors: lets hybrid search run with no model at all.
    It measures the plumbing (fusion, degraded reporting), not the quality of a real embedder."""

    model = "hash-64"

    def __init__(self, dim: int = 64) -> None:
        self.dim = dim

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors = []
        for text in texts:
            vec = [0.0] * self.dim
            for term in mem_mod._terms(text) - mem_mod._STOPWORDS:
                h = hashlib.sha256(term.encode()).digest()
                vec[int.from_bytes(h[:4], "big") % self.dim] += 1.0 if h[4] % 2 else -1.0
            vectors.append(vec)
        return vectors


class UnavailableEmbedder:
    """Stands in for Ollama being down: used to prove degraded mode is reported, not hidden."""

    model = "unavailable"

    def embed(self, texts: list[str]):
        raise EmbedderUnavailable("simulated outage")


# --- fixture -----------------------------------------------------------------------------------


@dataclass(frozen=True)
class Fixture:
    name: str
    path: Path
    sha256: str
    synthetic: bool
    now: datetime
    docs: list[dict]
    questions: list[dict]

    @staticmethod
    def row_id(doc: dict) -> str:
        return f"{doc['table']}:{doc['id']}"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_fixture(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("format") != FORMAT:
        errors.append(f"format must be {FORMAT}")
    docs, questions = data.get("docs"), data.get("questions")
    if not isinstance(docs, list) or not isinstance(questions, list):
        return errors + ["docs and questions must be lists"]
    ids: set[str] = set()
    for d in docs:
        missing = [f for f in ("table", "id", "at", "scope", "trust", "text") if not str(d.get(f, "")).strip()]
        if missing:
            errors.append(f"doc {d.get('id')!r} missing {missing}")
            continue
        rid = f"{d['table']}:{d['id']}"
        if rid in ids:
            errors.append(f"duplicate doc {rid}")
        ids.add(rid)
        if d["trust"] not in ("owner", "agent", "external"):
            errors.append(f"{rid}: bad trust {d['trust']!r}")
        if normalize(d["scope"]) in mem_mod.SENSITIVE_SCOPES or "camondo" in normalize(d["text"]):
            errors.append(f"{rid}: sensitive scope or text is never allowed in an eval fixture")
        if data.get("synthetic") and d.get("provenance") != "synthetic":
            errors.append(f"{rid}: a synthetic fixture needs provenance 'synthetic' on every row")
        try:
            datetime.fromisoformat(d["at"])
        except ValueError:
            errors.append(f"{rid}: bad timestamp")
    seen_q: set[str] = set()
    for q in questions:
        qid = q.get("id", "?")
        if qid in seen_q:
            errors.append(f"duplicate question {qid}")
        seen_q.add(qid)
        if q.get("category") not in CATEGORIES:
            errors.append(f"{qid}: category must be one of {CATEGORIES}")
        if not str(q.get("query", "")).strip():
            errors.append(f"{qid}: empty query")
        gold, sup = q.get("gold", []), q.get("superseded", [])
        for g in [*gold, *sup]:
            if g not in ids:
                errors.append(f"{qid}: unknown row id {g}")
        if (q.get("category") == "abstention") != (not gold):
            errors.append(f"{qid}: abstention questions have no gold rows, every other question has at least one")
        if sup and q.get("category") != "knowledge-update":
            errors.append(f"{qid}: only knowledge-update questions list superseded rows")
        if q.get("category") == "knowledge-update" and not sup:
            errors.append(f"{qid}: knowledge-update needs superseded rows")
    return errors


def load_fixture(path: Path, pinned: dict[str, str] | None = None) -> tuple[Fixture, bool]:
    """Returns (fixture, pinned). Raises ManifestError on a hash mismatch, FixtureError on bad shape."""
    digest = sha256_file(path)
    expected = (pinned or {}).get(path.name)
    if expected is not None and expected != digest:
        raise ManifestError(f"{path.name}: sha256 {digest} does not match the pinned {expected}")
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate_fixture(data)
    if errors:
        raise FixtureError("; ".join(errors))
    fx = Fixture(data.get("name", path.stem), path, digest, bool(data.get("synthetic")),
                 datetime.fromisoformat(data["now"]), data["docs"], data["questions"])
    return fx, expected is not None


def build_memory(fx: Fixture, db_path: Path, embedder=None) -> Memory:
    mem = Memory(db_path, now=lambda: fx.now, embedder=embedder)
    for d in sorted(fx.docs, key=lambda d: (d["table"], int(d["id"]) if str(d["id"]).isdigit() else 0, d["id"])):
        mem.add_row(d["scope"], d["table"], str(d["id"]), d["at"], d["text"], d["trust"])
    if embedder is not None:
        mem.embed_pending(limit=100_000)
    return mem


# --- config ------------------------------------------------------------------------------------


def load_config(path: Path) -> dict:
    cfg = tomllib.loads(path.read_text(encoding="utf-8"))
    cfg["_sha256"] = sha256_file(path)
    if not cfg.get("variants"):
        raise ValueError("config needs at least one [variants.*] table")
    return cfg


# --- running -----------------------------------------------------------------------------------


def _run_variant(mem: Memory, fx: Fixture, variant: dict, k: int) -> list[dict]:
    results = []
    for q in fx.questions:
        res = mem.search(
            q["query"], [q.get("scope", mem_mod.DEFAULT_SCOPE)], k,
            abstain_min_coverage=variant.get("abstain_min_coverage"),
            neighbours=int(variant.get("neighbours", 0)),
            recency_tolerance=variant.get("recency_tolerance"),
        )
        primary = [f"{h.source_table}:{h.source_id}" for h in res.hits if not h.expanded]
        ctx = [f"{h.source_table}:{h.source_id}" for h in res.hits]
        gold, sup = set(q.get("gold", [])), set(q.get("superseded", []))
        m: dict[str, float] = {}
        if q["category"] == "abstention":
            m["abstention_recall"] = 0.0 if res.evidence else 1.0
        else:
            m["recall@5"] = recall_at_k(primary, gold, 5)
            m["recall@10"] = recall_at_k(primary, gold, 10)
            m["mrr"] = reciprocal_rank(primary, gold)
            m["ndcg@10"] = ndcg_at_k(primary, gold, 10)
            m["recall_ctx@5"] = recall_at_k(primary[:5] + [r for r in ctx if r not in primary], gold, 10**6)
            m["answer_kept"] = 1.0 if res.evidence else 0.0
        if q["category"] == "knowledge-update":
            m["ku_latest_first"] = latest_above_superseded(primary, gold, sup)
        results.append({"id": q["id"], "category": q["category"], "mode": res.mode, "evidence": res.evidence,
                        "degraded": variant.get("mode") == "hybrid" and res.mode != "hybrid",
                        "ranked": primary, "metrics": m})
    return results


def _brief_stats(mem: Memory, fx: Fixture) -> dict:
    briefs: dict[str, str] = {}
    absent = hits = should = 0
    for q in fx.questions:
        scope = normalize(q.get("scope", mem_mod.DEFAULT_SCOPE))
        text = briefs.setdefault(scope, mem.brief(scope))
        absent += not text
        if q.get("brief_should_answer"):
            should += 1
            hits += all(f"{g.split(':')[0]}#{g.split(':')[1]} " in text or f"{g.split(':')[0]}#{g.split(':')[1]}]" in text
                        for g in q["gold"]) if text else 0
    return {"absent_rate": absent / len(fx.questions) if fx.questions else 0.0,
            "should_answer": should, "hit_rate": hits / should if should else None}


def _vector(results: list[dict], metric: str, category: str | None = None) -> list[float]:
    return [r["metrics"][metric] for r in results
            if metric in r["metrics"] and (category is None or r["category"] == category)]


def _summarise(results: list[dict], run: dict) -> dict:
    metrics = sorted({m for r in results for m in r["metrics"]})
    overall = {}
    for m in metrics:
        vec = _vector(results, m)
        ci = bootstrap_ci(vec, run["bootstrap_resamples"], run["seed"], run["ci_level"])
        overall[m] = {"mean": mean(vec), "n": len(vec), "ci_low": ci[0] if ci else None, "ci_high": ci[1] if ci else None}
    by_cat = {}
    for cat in CATEGORIES:
        sub = [r for r in results if r["category"] == cat]
        if sub:
            by_cat[cat] = {"n": len(sub), **{m: mean(_vector(sub, m)) for m in metrics if _vector(sub, m)}}
    modes: dict[str, int] = {}
    for r in results:
        modes[r["mode"]] = modes.get(r["mode"], 0) + 1
    return {"overall": overall, "by_category": by_cat, "modes": modes,
            "degraded_rate": sum(r["degraded"] for r in results) / len(results) if results else 0.0}


def _gate(gate: dict, runs: dict[str, list[dict] | None], summaries: dict, run: dict) -> dict:
    out = {"id": gate["id"], "description": gate.get("description", ""), "status": "pass", "reasons": []}
    needed = [v for v in (gate.get("candidate"), gate.get("baseline")) if v]
    if any(runs.get(v) is None for v in needed):
        return {**out, "status": "skipped", "reasons": [f"variant not run: {[v for v in needed if runs.get(v) is None]}"]}
    metric, cat = gate["metric"], gate.get("category")
    cand = runs[gate["candidate"]]
    if "baseline" in gate:
        base = runs[gate["baseline"]]
        a, b = _vector(base, metric, cat), _vector(cand, metric, cat)
        stat = paired_bootstrap(a, b, run["bootstrap_resamples"], run["seed"], run["ci_level"])
        out["paired"] = {"metric": metric, "category": cat, **stat}
        if stat["delta"] is None:
            out["status"], out["reasons"] = "fail", ["no questions apply to this metric"]
        else:
            if "min_delta" in gate and stat["delta"] < gate["min_delta"]:
                out["reasons"].append(f"delta {stat['delta']:.3f} < min_delta {gate['min_delta']}")
            if "require_ci_lower_above" in gate and not (stat["ci_low"] is not None and stat["ci_low"] > gate["require_ci_lower_above"]):
                out["reasons"].append(f"CI lower bound {stat['ci_low']} not above {gate['require_ci_lower_above']}")
    else:
        value = mean(_vector(cand, metric, cat))
        out["value"] = value
        if value is None or ("min" in gate and value < gate["min"]):
            out["reasons"].append(f"{metric} {value} < floor {gate['min']}")
    if "max_degraded_rate" in gate and summaries[gate["candidate"]]["degraded_rate"] > gate["max_degraded_rate"]:
        out["reasons"].append(f"degraded rate {summaries[gate['candidate']]['degraded_rate']:.2f} > {gate['max_degraded_rate']}")
    if out["reasons"]:
        out["status"] = "fail"
    return out


def evaluate(fixture_path: Path, config_path: Path, embedder: str = "none", workdir: Path | None = None) -> dict:
    """Run every configured variant over the frozen fixture and return the report dict."""
    cfg = load_config(config_path)
    run = {"seed": 1, "bootstrap_resamples": 2000, "ci_level": 0.95, "k": 10, **cfg.get("run", {})}
    fx, pinned = load_fixture(fixture_path, cfg.get("fixtures"))
    emb = {"none": None, "hash": HashEmbedder(), "unavailable": UnavailableEmbedder(),
           "ollama": mem_mod.OllamaEmbedder(timeout=10)}[embedder]
    with tempfile.TemporaryDirectory(dir=workdir) as tmp:
        mem = build_memory(fx, Path(tmp) / "eval-memory.db", embedder=emb if embedder != "unavailable" else HashEmbedder())
        if embedder == "unavailable":  # vectors exist, the backend then goes away
            mem._embedder = emb
        runs: dict[str, list[dict] | None] = {}
        summaries: dict[str, dict] = {}
        skipped = {}
        for name, variant in cfg["variants"].items():
            if variant.get("mode") == "hybrid" and emb is None:
                runs[name] = None
                skipped[name] = "hybrid needs an embedder (--embedder hash|ollama)"
                continue
            mem._embedder = emb if variant.get("mode") == "hybrid" else None
            runs[name] = _run_variant(mem, fx, variant, run["k"])
            summaries[name] = _summarise(runs[name], run)
        mem._embedder = None
        brief = _brief_stats(mem, fx)
    gates = [_gate(g, runs, summaries, run) for g in cfg.get("gates", [])]
    return {
        "fixture": {"name": fx.name, "sha256": fx.sha256, "pinned": pinned, "synthetic": fx.synthetic,
                    "docs": len(fx.docs), "questions": len(fx.questions),
                    "by_category": {c: sum(q["category"] == c for q in fx.questions) for c in CATEGORIES}},
        "config_sha256": cfg["_sha256"], "run": run, "embedder": embedder,
        "variants": {n: {"definition": cfg["variants"][n], "skipped": skipped.get(n), **summaries.get(n, {})}
                     for n in cfg["variants"]},
        "per_question": {n: r for n, r in runs.items() if r is not None},
        "brief": brief, "gates": gates,
        "ok": not any(g["status"] == "fail" for g in gates),
    }


# --- report ------------------------------------------------------------------------------------


def _f(x, digits=3):
    return "-" if x is None else f"{x:.{digits}f}"


def render_markdown(report: dict) -> str:
    fx = report["fixture"]
    lines = [
        f"# Memory eval: {fx['name']}",
        "",
        f"- fixture sha256 `{fx['sha256']}` ({'pinned' if fx['pinned'] else 'UNPINNED: not in the config manifest'}),"
        f" {fx['docs']} rows, {fx['questions']} questions, synthetic={fx['synthetic']}",
        f"- config sha256 `{report['config_sha256']}`, embedder `{report['embedder']}`, seed {report['run']['seed']},"
        f" {report['run']['bootstrap_resamples']} bootstrap resamples, CI {report['run']['ci_level']}",
        f"- brief: absent for {_f(report['brief']['absent_rate'], 2)} of questions' scopes; brief hit rate"
        f" {_f(report['brief']['hit_rate'], 2)} over {report['brief']['should_answer']} brief-answerable questions",
        "",
        "## Variants (mean [95% CI] over answerable questions)",
        "",
        "| variant | mode(s) | degraded | " + " | ".join(PRIMARY_METRICS) + " | recall_ctx@5 |",
        "|---|---|---|" + "---|" * (len(PRIMARY_METRICS) + 1),
    ]
    for name, v in report["variants"].items():
        if v.get("skipped"):
            lines.append(f"| {name} | skipped: {v['skipped']} | | " + " | ".join("-" for _ in range(len(PRIMARY_METRICS) + 1)) + " |")
            continue
        cells = []
        for m in (*PRIMARY_METRICS, "recall_ctx@5"):
            o = v["overall"].get(m, {})
            cells.append(f"{_f(o.get('mean'))} [{_f(o.get('ci_low'))}, {_f(o.get('ci_high'))}]")
        modes = ", ".join(f"{m}:{c}" for m, c in v["modes"].items())
        lines.append(f"| {name} | {modes} | {_f(v['degraded_rate'], 2)} | " + " | ".join(cells) + " |")
    lines += ["", "## Other metrics", "", "| variant | abstention_recall | answer_kept | ku_latest_first |", "|---|---|---|---|"]
    for name, v in report["variants"].items():
        if not v.get("skipped"):
            o = v["overall"]
            lines.append(f"| {name} | " + " | ".join(_f(o.get(m, {}).get("mean")) for m in ("abstention_recall", "answer_kept", "ku_latest_first")) + " |")
    lines += ["", "## Per category (recall@5, n)", "", "| variant | " + " | ".join(CATEGORIES) + " |", "|---|" + "---|" * len(CATEGORIES)]
    for name, v in report["variants"].items():
        if not v.get("skipped"):
            cells = []
            for c in CATEGORIES:
                b = v["by_category"].get(c)
                cells.append("-" if not b else (f"{_f(b.get('recall@5'), 2)} (n={b['n']})" if "recall@5" in b else f"abst {_f(b.get('abstention_recall'), 2)} (n={b['n']})"))
            lines.append(f"| {name} | " + " | ".join(cells) + " |")
    lines += ["", "## Pre-registered gates", "", "| gate | status | detail |", "|---|---|---|"]
    for g in report["gates"]:
        detail = "; ".join(g["reasons"]) if g["reasons"] else ""
        if "paired" in g:
            p = g["paired"]
            detail = f"{p['metric']} delta {_f(p['delta'])} [{_f(p['ci_low'])}, {_f(p['ci_high'])}] n={p['n']}" + (f"; {detail}" if detail else "")
        elif "value" in g:
            detail = f"value {_f(g['value'])}" + (f"; {detail}" if detail else "")
        lines.append(f"| {g['id']} | {g['status']} | {detail} |")
    lines += ["", f"Overall: {'all gates pass or skipped' if report['ok'] else 'GATE FAILED'}", ""]
    return "\n".join(lines)
