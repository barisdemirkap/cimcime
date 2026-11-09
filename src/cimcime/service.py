"""Always-on service installers: launchd (macOS), systemd --user (Linux), Task Scheduler (Windows).

One entry point, `cimcime service install|uninstall|status|restart`, installs two units:
  * the channel service: keeps a persistent `claude --agent cimcime --channels ...` session alive
  * the watchdog: runs `cimcime watchdog` every few minutes (see cimcime.watchdog)
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

from cimcime.config import data_dir

CHANNEL_LABEL = "com.cimcime.telegram-channel"
WATCHDOG_LABEL = "com.cimcime.watchdog"
SYSTEMD_CHANNEL = "cimcime-channel"
SYSTEMD_WATCHDOG = "cimcime-watchdog"
WIN_CHANNEL = "CimcimeChannel"
WIN_WATCHDOG = "CimcimeWatchdog"

CHANNEL_PROMPT = (
    'Messages arriving as <channel source="telegram"> are from the user on Telegram, who cannot '
    "see this terminal. ALWAYS answer them by calling the telegram reply tool with the chat_id "
    "from the tag; plain text output is never delivered."
)
CHANNEL_SETTINGS = '{"enabledPlugins":{"telegram@claude-plugins-official":true}}'


class ServiceError(RuntimeError):
    pass


@dataclass(frozen=True)
class Spec:
    workdir: Path
    claude: str
    cimcime: str  # absolute path of the cimcime executable
    path_env: str
    logs: Path

    def claude_args(self) -> list[str]:
        return [
            self.claude, "--agent", "cimcime", "--settings", CHANNEL_SETTINGS,
            "--channels", "plugin:telegram@claude-plugins-official",
            "--append-system-prompt", CHANNEL_PROMPT,
        ]


def _sh_quote(s: str) -> str:
    return "'" + s.replace("'", "'\\''") + "'"


def channel_shell_command(spec: Spec, system: str) -> str:
    """claude drops to non-interactive print mode when stdout is not a TTY, so wrap it in a pty
    (script(1)) and feed it a never-ending stdin so it does not see EOF and exit."""
    inner = " ".join(_sh_quote(a) for a in spec.claude_args())
    if system == "darwin":
        return f"tail -f /dev/null | /usr/bin/script -q /dev/null {inner}"
    return f"tail -f /dev/null | script -qfec {_sh_quote(inner)} /dev/null"


def render_launchd_channel(spec: Spec) -> str:
    cmd = escape(channel_shell_command(spec, "darwin"))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>{CHANNEL_LABEL}</string>
  <key>ProgramArguments</key>
  <array><string>/bin/sh</string><string>-c</string><string>{cmd}</string></array>
  <key>WorkingDirectory</key><string>{escape(str(spec.workdir))}</string>
  <key>EnvironmentVariables</key><dict><key>PATH</key><string>{escape(spec.path_env)}</string></dict>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>{escape(str(spec.logs / "channel.out"))}</string>
  <key>StandardErrorPath</key><string>{escape(str(spec.logs / "channel.err"))}</string>
</dict>
</plist>
"""


def render_launchd_watchdog(spec: Spec) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>{WATCHDOG_LABEL}</string>
  <key>ProgramArguments</key>
  <array><string>{escape(spec.cimcime)}</string><string>watchdog</string></array>
  <key>EnvironmentVariables</key><dict><key>PATH</key><string>{escape(spec.path_env)}</string></dict>
  <key>StartInterval</key><integer>300</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardErrorPath</key><string>{escape(str(spec.logs / "watchdog.err"))}</string>
</dict>
</plist>
"""


def render_systemd_channel(spec: Spec) -> str:
    cmd = channel_shell_command(spec, "linux").replace("%", "%%")
    return f"""[Unit]
Description=Cimcime Telegram channel session
After=network-online.target

[Service]
WorkingDirectory={spec.workdir}
Environment=PATH={spec.path_env}
ExecStart=/bin/sh -c {_sh_quote(cmd)}
Restart=always
RestartSec=10
StandardOutput=append:{spec.logs / "channel.out"}
StandardError=append:{spec.logs / "channel.err"}

[Install]
WantedBy=default.target
"""


def render_systemd_watchdog_service(spec: Spec) -> str:
    return f"""[Unit]
Description=Cimcime watchdog (one check)

[Service]
Type=oneshot
Environment=PATH={spec.path_env}
ExecStart={spec.cimcime} watchdog
"""


def render_systemd_watchdog_timer() -> str:
    return """[Unit]
Description=Run the Cimcime watchdog every 5 minutes

[Timer]
OnBootSec=2min
OnUnitActiveSec=5min

[Install]
WantedBy=timers.target
"""


def windows_channel_cmd(spec: Spec) -> str:
    """Task Scheduler action (experimental: Claude Code must be able to run on a ConPTY)."""
    args = " ".join(f'"{a}"' if " " in a or "<" in a else a for a in spec.claude_args()[1:])
    return f'"{spec.claude}" {args}'


def _run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    res = subprocess.run(cmd, capture_output=True, text=True)
    if check and res.returncode != 0:
        raise ServiceError(f"{' '.join(cmd)} failed: {(res.stderr or res.stdout).strip()}")
    return res


def build_spec() -> Spec:
    claude = shutil.which("claude")
    if not claude:
        raise ServiceError("'claude' not found on PATH. Install Claude Code first (run `cimcime doctor`).")
    cim = shutil.which("cimcime") or str(Path(sys.argv[0]).resolve())
    dirs = [str(Path(p).parent) for p in (claude, cim, shutil.which("bun") or str(Path.home() / ".bun/bin/bun"))]
    base = os.environ.get("PATH", os.defpath)
    path_env = os.pathsep.join(dict.fromkeys(dirs + base.split(os.pathsep)))
    logs = data_dir() / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    return Spec(Path.cwd(), claude, cim, path_env, logs)


def install(spec: Spec | None = None) -> list[str]:
    spec = spec or build_spec()
    done: list[str] = []
    if sys.platform == "darwin":
        agents = Path.home() / "Library" / "LaunchAgents"
        agents.mkdir(parents=True, exist_ok=True)
        for label, text in ((CHANNEL_LABEL, render_launchd_channel(spec)), (WATCHDOG_LABEL, render_launchd_watchdog(spec))):
            p = agents / f"{label}.plist"
            p.write_text(text, encoding="utf-8")
            _run(["launchctl", "unload", str(p)], check=False)
            _run(["launchctl", "load", str(p)])
            done.append(str(p))
    elif sys.platform.startswith("linux"):
        unit_dir = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "systemd" / "user"
        unit_dir.mkdir(parents=True, exist_ok=True)
        files = {
            f"{SYSTEMD_CHANNEL}.service": render_systemd_channel(spec),
            f"{SYSTEMD_WATCHDOG}.service": render_systemd_watchdog_service(spec),
            f"{SYSTEMD_WATCHDOG}.timer": render_systemd_watchdog_timer(),
        }
        for name, text in files.items():
            (unit_dir / name).write_text(text, encoding="utf-8")
            done.append(str(unit_dir / name))
        _run(["systemctl", "--user", "daemon-reload"])
        _run(["systemctl", "--user", "enable", "--now", f"{SYSTEMD_CHANNEL}.service", f"{SYSTEMD_WATCHDOG}.timer"])
    elif sys.platform == "win32":
        _run(["schtasks", "/Create", "/F", "/TN", WIN_CHANNEL, "/SC", "ONLOGON", "/TR", windows_channel_cmd(spec)])
        _run(["schtasks", "/Create", "/F", "/TN", WIN_WATCHDOG, "/SC", "MINUTE", "/MO", "5", "/TR", f'"{spec.cimcime}" watchdog'])
        _run(["schtasks", "/Run", "/TN", WIN_CHANNEL], check=False)
        done += [WIN_CHANNEL, WIN_WATCHDOG]
    else:
        raise ServiceError(f"unsupported platform: {sys.platform}")
    return done


def uninstall() -> None:
    if sys.platform == "darwin":
        for label in (CHANNEL_LABEL, WATCHDOG_LABEL):
            p = Path.home() / "Library" / "LaunchAgents" / f"{label}.plist"
            _run(["launchctl", "unload", str(p)], check=False)
            p.unlink(missing_ok=True)
    elif sys.platform.startswith("linux"):
        _run(["systemctl", "--user", "disable", "--now", f"{SYSTEMD_CHANNEL}.service", f"{SYSTEMD_WATCHDOG}.timer"], check=False)
        unit_dir = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "systemd" / "user"
        for n in (f"{SYSTEMD_CHANNEL}.service", f"{SYSTEMD_WATCHDOG}.service", f"{SYSTEMD_WATCHDOG}.timer"):
            (unit_dir / n).unlink(missing_ok=True)
        _run(["systemctl", "--user", "daemon-reload"], check=False)
    elif sys.platform == "win32":
        for t in (WIN_CHANNEL, WIN_WATCHDOG):
            _run(["schtasks", "/Delete", "/F", "/TN", t], check=False)


def is_running() -> bool:
    if sys.platform == "darwin":
        out = _run(["launchctl", "list", CHANNEL_LABEL], check=False)
        return out.returncode == 0 and '"PID"' in out.stdout
    if sys.platform.startswith("linux"):
        return _run(["systemctl", "--user", "is-active", "--quiet", f"{SYSTEMD_CHANNEL}.service"], check=False).returncode == 0
    if sys.platform == "win32":
        out = _run(["schtasks", "/Query", "/TN", WIN_CHANNEL, "/FO", "LIST"], check=False)
        return "Running" in out.stdout
    return False


def restart() -> bool:
    if sys.platform == "darwin":
        return _run(["launchctl", "kickstart", "-k", f"gui/{os.getuid()}/{CHANNEL_LABEL}"], check=False).returncode == 0
    if sys.platform.startswith("linux"):
        return _run(["systemctl", "--user", "restart", f"{SYSTEMD_CHANNEL}.service"], check=False).returncode == 0
    if sys.platform == "win32":
        _run(["schtasks", "/End", "/TN", WIN_CHANNEL], check=False)
        return _run(["schtasks", "/Run", "/TN", WIN_CHANNEL], check=False).returncode == 0
    return False
