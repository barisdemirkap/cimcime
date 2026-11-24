"""`cimcime doctor`: check the prerequisites Cimcime needs, on any OS."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
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
    checks.append(approval_hook_check())
    checks += data_protection_checks()
    if sys.platform.startswith("linux"):
        checks += linux_vm_checks()
    return checks


def approval_hook_check(home: Path | None = None, cwd: Path | None = None) -> Check:
    """Is the ADR-0016 approval-gate hook wired into a Claude Code settings file? (warn only: installing is the owner's step)"""
    home, cwd = home or Path.home(), cwd or Path.cwd()
    for path in (cwd / ".claude" / "settings.local.json", cwd / ".claude" / "settings.json", home / ".claude" / "settings.json"):
        try:
            hooks = json.loads(path.read_text()).get("hooks", {}).get("PreToolUse", [])
            for entry in hooks:
                if "Bash" in str(entry.get("matcher", "")) and any(
                    "approval_hook" in str(h.get("command", "")) for h in entry.get("hooks", [])
                ):
                    return Check("approval hook", True, f"installed in {path}", required=False)
        except (OSError, ValueError, AttributeError, TypeError):
            continue
    return Check(
        "approval hook",
        False,
        "not installed: agent Bash calls are not gated. See docs/approval-hook.md (guard against model mistakes, not a security boundary)",
        required=False,
    )


def _private_perms_check(path: Path) -> Check | None:
    """Group/other access to a private data file or dir is a leak (warn only)."""
    if not path.exists():
        return None
    mode = path.stat().st_mode & 0o777
    ok = mode & 0o077 == 0
    fix = "chmod 700" if path.is_dir() else "chmod 600"
    return Check(f"perms {path.name}", ok, f"{oct(mode)[2:]}" + ("" if ok else f" is group/other accessible: run `{fix} {path}`"), required=False)


def data_protection_checks(home: Path | None = None, platform: str | None = None, run=subprocess.run) -> list[Check]:
    """Directive 7: disk encryption + private permissions on local data (all warn-only; fixing is the owner's step)."""
    home, platform = home or Path.home(), platform or sys.platform
    out: list[Check] = []
    if platform == "darwin":
        try:
            r = run(["fdesetup", "status"], capture_output=True, text=True, timeout=15)
            on = "FileVault is On" in r.stdout
        except (OSError, subprocess.SubprocessError):
            on = False
        out.append(Check("FileVault", on, "disk encryption on" if on else "off or unknown: enable it in System Settings so local databases are encrypted at rest", required=False))
    elif platform.startswith("linux"):
        try:
            r = run(["lsblk", "-o", "TYPE"], capture_output=True, text=True, timeout=15)
            on = "crypt" in r.stdout
        except (OSError, subprocess.SubprocessError):
            on = False
        out.append(Check("disk encryption", on, "LUKS volume found" if on else "no LUKS/crypt volume detected: enable full-disk encryption", required=False))
    for rel in (".claude/channels/telegram/messages.db", ".config/alfred/alfred.db", ".local/state/cimcime"):
        c = _private_perms_check(home / rel)
        if c:
            out.append(c)
    return out


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
