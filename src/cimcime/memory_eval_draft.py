"""Draft candidate gold questions for the memory eval from RAW message-log rows (ADR-0017).

The owner writes and approves the gold set; this only proposes. Deterministic heuristics, no model:
questions are cut from raw `messages` and `decisions` rows (never from summaries or the memory
index), and the review file carries the private excerpts, so it is written under
~/.local/state/cimcime/eval-candidates/ and refuses any path inside a git work tree. Rows that
mention or belong to a sensitive scope are skipped entirely."""

from __future__ import annotations

import json
import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from cimcime import memory as mem_mod
from cimcime.memory import normalize

DEFAULT_OUT_DIR = Path.home() / ".local" / "state" / "cimcime" / "eval-candidates"
PER_CATEGORY = 15
_EXCERPT = 240
_SIMILAR = 0.4
# Neutral topics nobody plausibly discussed; kept only when absent from the whole corpus.
_PROBES = ("submarine hull coating", "quantum flux capacitor", "elephant transport schedule",
           "regional chess championship", "tractor museum wifi password", "volcano evacuation drill",
           "ice cream flavour vote", "satellite radar dish provider", "cryptocurrency payroll wallet",
           "opera house ticket lottery")


class UnsafeOutputPath(ValueError):
    """The review file would land inside a git work tree (private text must never reach the repo)."""


def _words(text: str, n: int = 6) -> list[str]:
    terms = [t for t in re.findall(r"\w+", normalize(text)) if t not in mem_mod._STOPWORDS and len(t) > 2]
    return list(dict.fromkeys(terms))[:n]


def _excerpt(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= _EXCERPT else text[: _EXCERPT - 1] + "…"


def _jaccard(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def _load_rows(source: Path) -> tuple[list[dict], set[str]]:
    rows: list[dict] = []
    vocab: set[str] = set()
    src = sqlite3.connect(f"file:{source}?mode=ro", uri=True)
    try:
        tables = {r[0] for r in src.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if "messages" in tables:
            for rid, direction, at, text in src.execute("SELECT id, direction, sent_at, text FROM messages ORDER BY id"):
                vocab |= mem_mod._terms(text or "")
                if (text or "").strip() and mem_mod._message_scope(text) not in mem_mod.SENSITIVE_SCOPES:
                    rows.append({"table": "messages", "id": str(rid), "at": mem_mod._utc(at), "text": text,
                                 "trust": "owner" if direction == "inbound" else "agent", "project": None})
        if "decisions" in tables:
            for rid, at, project, decision, rationale in src.execute(
                    "SELECT id, decided_at, project, decision, rationale FROM decisions ORDER BY id"):
                text = f"{decision} — {rationale}" if rationale else decision
                vocab |= mem_mod._terms(text)
                if normalize(project or "") in mem_mod.SENSITIVE_SCOPES or "camondo" in normalize(text):
                    continue
                rows.append({"table": "decisions", "id": str(rid), "at": mem_mod._utc(at), "text": text,
                             "trust": "owner", "project": normalize(project or "") or mem_mod.DEFAULT_SCOPE})
    finally:
        src.close()
    return rows, vocab


def _cand(category: str, query: str, gold: list[dict], superseded: list[dict] | None = None, note: str = "") -> dict:
    return {
        "category": category, "query": query,
        "gold": [f"{r['table']}:{r['id']}" for r in gold],
        "superseded": [f"{r['table']}:{r['id']}" for r in superseded or []],
        "evidence": {f"{r['table']}:{r['id']}": {"at": r["at"], "excerpt": _excerpt(r["text"])}
                     for r in [*gold, *(superseded or [])]},
        "note": note, "status": "draft", "owner_decision": None,  # owner sets: approve | edit | reject
        "owner_query": None, "owner_gold": None,
    }


def draft_candidates(source: Path, now: datetime | None = None) -> dict:
    rows, vocab = _load_rows(source)
    decisions = [r for r in rows if r["table"] == "decisions"]
    out: list[dict] = []

    for r in decisions[-PER_CATEGORY:]:
        words = _words(r["text"])
        if words:
            out.append(_cand("extraction", "what was decided about " + " ".join(words), [r]))

    prefs = [r for r in rows if r["trust"] == "owner" and r["table"] == "messages"
             and mem_mod._PREFERENCE.search(normalize(r["text"]))]
    for r in prefs[-PER_CATEGORY:]:
        words = _words(r["text"])
        if words:
            out.append(_cand("preference", "what is the owner's rule about " + " ".join(words[:5]), [r]))

    # Similar decisions in one project form a chain; the newest wins (knowledge-update), and a chain of
    # three or more also yields a "latest" temporal question.
    chains: list[list[dict]] = []
    for r in decisions:
        terms = set(_words(r["text"], 30))
        for chain in chains:
            if chain[0]["project"] == r["project"] and any(_jaccard(terms, set(_words(c["text"], 30))) >= _SIMILAR for c in chain):
                chain.append(r)
                break
        else:
            chains.append([r])
    ku = temporal = 0
    for chain in chains:
        if len(chain) < 2:
            continue
        words = _words(chain[-1]["text"])
        if ku < PER_CATEGORY:
            out.append(_cand("knowledge-update", " ".join(words), [chain[-1]], chain[:-1],
                             "newest decision of a chain of similar decisions; check it truly supersedes the others"))
            ku += 1
        if len(chain) >= 3 and temporal < PER_CATEGORY:
            out.append(_cand("temporal", "latest " + " ".join(words), [chain[-1]], note="newest of 3+ similar decisions"))
            temporal += 1

    for probe in _PROBES:
        if not (mem_mod._terms(probe) - mem_mod._STOPWORDS) & vocab:
            out.append(_cand("abstention", "what was decided about " + probe, [],
                             note="probe topic absent from every raw row"))

    for i, c in enumerate(out, start=1):
        c["id"] = f"c{i:03d}"
    now = now or datetime.now(timezone.utc)
    return {
        "format": 1, "kind": "eval-candidates", "generated_at": now.isoformat(), "source": str(source),
        "instructions": ("DRAFT, not gold. For each candidate set owner_decision to approve, edit or reject; for edit "
                         "fill owner_query and/or owner_gold. Add multi-session questions by hand (the drafter cannot "
                         "judge split evidence). Contains private excerpts: never copy into the repo."),
        "counts": {c: sum(x["category"] == c for x in out) for c in {x["category"] for x in out}},
        "candidates": out,
    }


def _inside_git_tree(path: Path) -> bool:
    for parent in [path.resolve(), *path.resolve().parents]:
        if (parent / ".git").exists():
            return True
    return False


def render_review_markdown(doc: dict) -> str:
    lines = ["# Draft eval candidates (private, owner review)", "", doc["instructions"], ""]
    for c in doc["candidates"]:
        lines += [f"## {c['id']} [{c['category']}] {c['query']}", f"- gold: {', '.join(c['gold']) or '(none: abstention)'}"]
        if c["superseded"]:
            lines.append(f"- superseded: {', '.join(c['superseded'])}")
        lines += [f"- {k} ({v['at'][:10]}): {v['excerpt']}" for k, v in c["evidence"].items()]
        if c["note"]:
            lines.append(f"- note: {c['note']}")
        lines.append("- decision: approve / edit / reject")
        lines.append("")
    return "\n".join(lines)


def write_review(doc: dict, out_dir: Path | None = None) -> list[Path]:
    out_dir = Path(out_dir) if out_dir else DEFAULT_OUT_DIR
    if _inside_git_tree(out_dir):
        raise UnsafeOutputPath(f"{out_dir} is inside a git work tree; private excerpts must stay out of the repo")
    out_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(out_dir, 0o700)
    stamp = doc["generated_at"][:19].replace(":", "").replace("-", "")
    paths = []
    for suffix, body in ((".json", json.dumps(doc, indent=1, ensure_ascii=False) + "\n"),
                         (".md", render_review_markdown(doc))):
        path = out_dir / f"candidates-{stamp}{suffix}"
        fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(body)
        paths.append(path)
    return paths
