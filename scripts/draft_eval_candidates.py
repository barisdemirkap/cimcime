#!/usr/bin/env python3
"""Draft candidate gold questions for `cimcime eval-memory` from raw message-log rows.

Writes a review file (JSON + Markdown) to ~/.local/state/cimcime/eval-candidates/ for the owner to
approve or edit. Never writes inside a git work tree. Usage:

    uv run python scripts/draft_eval_candidates.py [--source PATH] [--out-dir DIR]
"""

import argparse
import sys
from pathlib import Path

from cimcime.memory_eval_draft import UnsafeOutputPath, draft_candidates, write_review
from cimcime.message_log import DEFAULT_MESSAGE_LOG_PATH


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--source", default=str(DEFAULT_MESSAGE_LOG_PATH), help="message log db (opened read-only)")
    p.add_argument("--out-dir", default=None, help="default ~/.local/state/cimcime/eval-candidates/")
    args = p.parse_args()
    try:
        doc = draft_candidates(Path(args.source))
        paths = write_review(doc, Path(args.out_dir) if args.out_dir else None)
    except UnsafeOutputPath as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    print(f"{len(doc['candidates'])} draft candidates {doc['counts']}")
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
