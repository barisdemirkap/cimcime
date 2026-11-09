# Contributing

1. Fork and clone, then `uv sync`.
2. Run the tests: `uv run pytest -q` (CI runs them on Linux, macOS and Windows).
3. Keep code cross-platform: no bash-only or macOS-only assumptions in the Python package.
4. Record architecture-level changes as an ADR in `docs/adr/`.
5. Open a pull request describing what and why.

Be kind and constructive in issues and reviews.
