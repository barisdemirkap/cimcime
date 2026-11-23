"""`cimcime doctor`: check the prerequisites Cimcime needs, on any OS."""
from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str
    required: bool = True


def _version(cmd: list[str]) -> str:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return (out.stdout or out.stderr).strip().splitlines()[0] if (out.stdout or out.stderr).strip() else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def _tool_check(binary: str, version_args: list[str], hint: str, required: bool = True) -> Check:
    path = shutil.which(binary)
    if not path:
        return Check(binary, False, f"not found on PATH. {hint}", required)
    return Check(binary, True, _version([path, *version_args]) or path, required)


def run_checks() -> list[Check]:
    checks = [
        Check("python", sys.version_info >= (3, 11), sys.version.split()[0] + " (need >= 3.11)"),
        _tool_check("git", ["--version"], "Install from https://git-scm.com"),
        _tool_check("gh", ["--version"], "Install from https://cli.github.com, then `gh auth login`"),
        _tool_check("claude", ["--version"], "Install Claude Code: https://claude.com/claude-code"),
        _tool_check("uv", ["--version"], "Optional: https://docs.astral.sh/uv", required=False),
    ]
    if shutil.which("gh"):
        try:
            ok = subprocess.run(["gh", "auth", "status"], capture_output=True, timeout=15).returncode == 0
        except (OSError, subprocess.SubprocessError):
            ok = False
        checks.append(Check("gh auth", ok, "logged in" if ok else "run `gh auth login`"))
    if sys.platform.startswith("linux"):
        checks += linux_vm_checks()
    return checks


def linux_vm_checks(which=shutil.which, run=subprocess.run, user: str | None = None) -> list[Check]:
    """Extra checks for a headless Linux VM: the channel runs under `script` in a systemd user service that must outlive logout."""
    import getpass
    out = [Check("script", bool(which("script")), "util-linux `script` gives claude a pty" if which("script") else "not found. Install util-linux (apt install bsdutils)")]
    try:
        r = run(["loginctl", "show-user", user or getpass.getuser(), "--property=Linger"], capture_output=True, text=True, timeout=15)
        linger = "Linger=yes" in r.stdout
    except (OSError, subprocess.SubprocessError):
        linger = False
    out.append(Check("linger", linger, "the service survives logout" if linger else "run `loginctl enable-linger $USER` or the service stops when you log out"))
    out.append(Check("claude auth", True, "on a VM sign in once with `claude` (device/URL login) or export ANTHROPIC_API_KEY (spend: your decision)", required=False))
    return out


def format_report(checks: list[Check]) -> str:
    lines = []
    for c in checks:
        mark = "ok  " if c.ok else ("FAIL" if c.required else "warn")
        lines.append(f"[{mark}] {c.name}: {c.detail}")
    return "\n".join(lines)


def all_required_ok(checks: list[Check]) -> bool:
    return all(c.ok for c in checks if c.required)
