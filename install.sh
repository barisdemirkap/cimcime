#!/usr/bin/env sh
# Cimcime installer for macOS and Linux. Windows: use install.ps1.
# Usage: curl -fsSL https://raw.githubusercontent.com/barisdemirkap/cimcime/master/install.sh | sh
set -eu

REPO_URL="${CIMCIME_REPO_URL:-https://github.com/barisdemirkap/cimcime}"

say() { printf '%s\n' "$*"; }
need() { command -v "$1" >/dev/null 2>&1; }

if ! need git; then say "git is required: https://git-scm.com"; exit 1; fi

if ! need uv; then
  say "Installing uv (Python package manager)..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
  export PATH
fi

say "Installing cimcime..."
uv tool install --force "git+${REPO_URL}"

say ""
say "Installed. Next steps:"
say "  cimcime doctor                 # check prerequisites (git, gh, claude)"
say "  cimcime init <owner>/<repo>    # GitHub repo that will track Cimcime's issues"
say ""
say "If 'cimcime' is not found, add \$HOME/.local/bin to your PATH (uv tool update-shell)."
