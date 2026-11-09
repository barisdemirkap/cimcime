# Cimcime installer for Windows (PowerShell). macOS/Linux: use install.sh.
# Usage: irm https://raw.githubusercontent.com/barisdemirkap/cimcime/master/install.ps1 | iex
$ErrorActionPreference = "Stop"
$RepoUrl = if ($env:CIMCIME_REPO_URL) { $env:CIMCIME_REPO_URL } else { "https://github.com/barisdemirkap/cimcime" }

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "git is required: https://git-scm.com"; exit 1
}
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing uv (Python package manager)..."
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
}

Write-Host "Installing cimcime..."
uv tool install --force "git+$RepoUrl"

Write-Host ""
Write-Host "Installed. Next steps:"
Write-Host "  cimcime doctor                 # check prerequisites (git, gh, claude)"
Write-Host "  cimcime init <owner>/<repo>    # GitHub repo that will track Cimcime's issues"
Write-Host ""
Write-Host "If 'cimcime' is not found, restart the terminal or run: uv tool update-shell"
