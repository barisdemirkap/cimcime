#!/usr/bin/env python3
"""Claude Code PreToolUse hook (Bash matcher) that enforces Cimcime's approval_gate (ADR-0001, ADR-0016).

This is a guard against model mistakes, not a security boundary. A same-user process can always
bypass it (see docs/approval-hook.md for the known bypasses).

Contract (Claude Code hooks): the tool call arrives as JSON on stdin. Exit 0 allows it. Exit 2
blocks it and shows stderr to the model. Any internal error, unparseable input or unverifiable
command exits 2: the hook fails closed.

Standard library only, so it can run as a plain script: `python3 -I approval_hook.py`.
"""
from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    from cimcime.approval_gate import ActionType, requires_approval
except ImportError:  # run as a bare script, package not installed
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from cimcime.approval_gate import ActionType, requires_approval

OWNER = "barisdemirkap"
PUBLIC_MIRROR = re.compile(r"(?i)\bbarisdemirkap/cimcime(\.git)?(?![\w-])")
MAX_DEPTH = 8
SUB = "\x00"  # marks a command/process substitution inside a word: its value is unknown

_GATE_NUMBER = {
    ActionType.PRODUCTION_DEPLOY: 1,
    ActionType.THIRD_PARTY_COMMUNICATION: 2,
    ActionType.SPEND_OR_ACCOUNT_CHANGE: 3,
}


@dataclass(frozen=True)
class Verdict:
    gate: ActionType | None  # None: the command could not be verified, or guard tamper
    rule: str
    reason: str

    def message(self) -> str:
        if self.gate is None:
            head = f"cimcime approval_gate: BLOCKED, unverifiable or guard-tamper ({self.rule})"
        else:
            head = (
                f"cimcime approval_gate: BLOCKED [{self.gate.value}] "
                f"(ADR-0001 gate {_GATE_NUMBER[self.gate]}, rule {self.rule})"
            )
        return (
            f"{head}\n{self.reason}\n"
            "This needs the owner's approval before it runs. Do not retry, rephrase or split the "
            "command. Ask the owner; if they approve, they run it themselves.\n"
            "(This hook is a guard against model mistakes, not a security boundary.)"
        )


def _v(gate: ActionType | None, rule: str, reason: str) -> Verdict:
    return Verdict(gate, rule, reason)


def _unverifiable(why: str) -> Verdict:
    return _v(None, "unverifiable", f"Cannot verify that this command stays outside the approval gates: {why}.")


# --------------------------------------------------------------------------- shell parsing


class ParseError(ValueError):
    pass


@dataclass
class Cmd:
    words: list[str] = field(default_factory=list)
    redirs: list[str] = field(default_factory=list)
    stdin: list[str] = field(default_factory=list)  # heredoc and here-string bodies


class _Parser:
    """Quote-aware splitter. Pulls commands out of chains, subshells, substitutions and heredocs."""

    def __init__(self, s: str, i: int = 0, depth: int = 0):
        if depth > MAX_DEPTH:
            raise ParseError("nesting too deep")
        self.s, self.i, self.depth = s, i, depth
        self.cmds: list[Cmd] = []
        self.cur = Cmd()
        self.pending: list[tuple[str, bool, bool, Cmd]] = []

    def end(self) -> None:
        if self.cur.words or self.cur.redirs or self.cur.stdin:
            self.cmds.append(self.cur)
        self.cur = Cmd()

    def run(self, in_paren: bool = False) -> None:
        s, paren = self.s, 0
        n = len(s)
        while self.i < n:
            c = s[self.i]
            if c in " \t":
                self.i += 1
            elif c == "\n":
                self.i += 1
                self._heredocs()
                self.end()
            elif c == "\\" and s[self.i + 1 : self.i + 2] == "\n":
                self.i += 2
            elif c == "#":
                j = s.find("\n", self.i)
                self.i = n if j < 0 else j
            elif c == "&" and s[self.i + 1 : self.i + 2] == ">":
                self.i += 1
                self._redirect()
            elif c in ";|&":
                self.i += 1
                self.end()
            elif c == "(":
                paren += 1
                self.i += 1
                self.end()
            elif c == ")":
                self.i += 1
                self.end()
                if paren > 0:
                    paren -= 1
                elif in_paren:
                    return
            elif c in "<>":
                self._redirect()
            else:
                w = self._word()
                if w.isdigit() and self.i < n and s[self.i] in "<>":
                    continue  # file descriptor number such as the 2 in 2>&1
                self.cur.words.append(w)
        if in_paren:
            raise ParseError("unclosed substitution")
        self._heredocs()
        self.end()

    def _sub(self, start: int) -> int:
        p = _Parser(self.s, start, self.depth + 1)
        p.run(True)
        self.cmds.extend(p.cmds)
        return p.i

    def _backtick(self) -> None:
        s, i = self.s, self.i + 1
        inner = []
        while i < len(s) and s[i] != "`":
            if s[i] == "\\" and s[i + 1 : i + 2] in ("`", "\\", "$"):
                i += 1
            inner.append(s[i])
            i += 1
        if i >= len(s):
            raise ParseError("unclosed backtick")
        self.cmds.extend(parse("".join(inner), self.depth + 1))
        self.i = i + 1

    def _redirect(self) -> None:
        s, n = self.s, len(self.s)
        c = s[self.i]
        self.i += 1
        nxt = s[self.i : self.i + 1]
        if nxt == "(":  # process substitution <( ) or >( )
            self.i = self._sub(self.i + 1)
            self.cur.words.append(SUB)
            return
        if c == "<" and nxt == "<":
            self.i += 1
            if s[self.i : self.i + 1] == "<":  # here-string
                self.i += 1
                self._skip_ws()
                self.cur.stdin.append(self._word())
                return
            strip = s[self.i : self.i + 1] == "-"
            if strip:
                self.i += 1
            self._skip_ws()
            j = self.i
            while j < n and s[j] not in " \t\n;|&()<>":
                j += 1
            raw = s[self.i : j]
            self.i = j
            quoted = any(ch in raw for ch in "'\"\\")
            self.pending.append((re.sub(r"['\"\\]", "", raw), strip, quoted, self.cur))
            return
        while self.i < n and s[self.i] in "<>&|":
            self.i += 1
        self._skip_ws()
        if self.i < n and s[self.i] not in "\n;|&()<>":
            w = self._word()
            if w:
                self.cur.redirs.append(w)

    def _skip_ws(self) -> None:
        while self.i < len(self.s) and self.s[self.i] in " \t":
            self.i += 1

    def _heredocs(self) -> None:
        s, n = self.s, len(self.s)
        for delim, strip, quoted, cmd in self.pending:
            lines = []
            while self.i < n:
                j = s.find("\n", self.i)
                line = s[self.i :] if j < 0 else s[self.i : j]
                self.i = n if j < 0 else j + 1
                if (line.lstrip("\t") if strip else line) == delim:
                    break
                lines.append(line)
            body = "\n".join(lines)
            cmd.stdin.append(body)
            if not quoted:
                self._scan_subs(body)
        self.pending = []

    def _scan_subs(self, text: str) -> None:
        i = 0
        while True:
            j = text.find("$(", i)
            if j < 0:
                break
            p = _Parser(text, j + 2, self.depth + 1)
            p.run(True)
            self.cmds.extend(p.cmds)
            i = p.i
        for m in re.finditer(r"`([^`]*)`", text):
            self.cmds.extend(parse(m.group(1), self.depth + 1))

    def _word(self) -> str:
        s, n = self.s, len(self.s)
        out: list[str] = []
        while self.i < n:
            c = s[self.i]
            if c in " \t\n;|&()<>":
                break
            if c == "\\":
                nx = s[self.i + 1 : self.i + 2]
                if nx != "\n":
                    out.append(nx)
                self.i += 2
            elif c == "'":
                j = s.find("'", self.i + 1)
                if j < 0:
                    raise ParseError("unterminated quote")
                out.append(s[self.i + 1 : j])
                self.i = j + 1
            elif c == '"':
                self._dquote(out)
            elif c == "$":
                nx = s[self.i + 1 : self.i + 2]
                if nx == "(":
                    out.append(SUB)
                    self.i = self._sub(self.i + 2)
                elif nx == "'":
                    out.append(self._ansi_c())
                elif nx == '"':
                    self.i += 1
                else:
                    out.append("$")
                    self.i += 1
            elif c == "`":
                self._backtick()
                out.append(SUB)
            else:
                out.append(c)
                self.i += 1
        return "".join(out)

    def _ansi_c(self) -> str:
        s = self.s
        j = self.i + 2
        while j < len(s) and s[j] != "'":
            j += 2 if s[j] == "\\" else 1
        if j >= len(s):
            raise ParseError("unterminated quote")
        raw = s[self.i + 2 : j]
        self.i = j + 1
        try:
            return raw.encode("utf-8").decode("unicode_escape")
        except (UnicodeError, ValueError):
            return raw

    def _dquote(self, out: list[str]) -> None:
        s, n = self.s, len(self.s)
        self.i += 1
        while True:
            if self.i >= n:
                raise ParseError("unterminated quote")
            c = s[self.i]
            if c == '"':
                self.i += 1
                return
            if c == "\\":
                nx = s[self.i + 1 : self.i + 2]
                if nx in ('$', "`", '"', "\\"):
                    out.append(nx)
                elif nx != "\n":
                    out.append("\\" + nx)
                self.i += 2
            elif c == "$" and s[self.i + 1 : self.i + 2] == "(":
                out.append(SUB)
                self.i = self._sub(self.i + 2)
            elif c == "`":
                self._backtick()
                out.append(SUB)
            else:
                out.append(c)
                self.i += 1


def parse(command: str, depth: int = 0) -> list[Cmd]:
    p = _Parser(command, 0, depth)
    p.run(False)
    return p.cmds


# --------------------------------------------------------------------------- rules

# Routine commands that never reach the network or change external state by themselves.
# They skip the network heuristics (an `echo "curl -X POST"` is not a POST). Gated tools
# (git, gh, curl, cloud CLIs, ...) are deliberately absent and always go through their rules.
ROUTINE_COMMANDS = frozenset(
    "ls cat echo printf pwd cd grep egrep fgrep rg sed awk head tail wc sort uniq tr cut diff cmp find fd "
    "mkdir cp mv touch rm ln chmod stat file du df tree basename dirname realpath date sleep true false test "
    "which whoami uname pytest ruff mypy black make jq yq tee xxd base64 shasum md5 sha256sum "
    "tar zip unzip gzip gunzip less more bat".split()
)
_RESERVED = frozenset({"{", "}", "!", "if", "then", "else", "elif", "fi", "do", "done", "while", "until", "time", "esac"})
_ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\+?=")
_SHELLS = frozenset({"bash", "sh", "zsh", "dash", "ksh", "fish", "ash"})
_INTERPRETERS = frozenset({"python", "node", "nodejs", "deno", "bun", "ruby", "perl", "php", "lua"})
_OPT_VALUES = {
    "sudo": {"-u", "-g", "-h", "-p", "-C", "-D", "-R", "-T", "-U", "-r", "-t"},
    "doas": {"-u", "-C"},
    "env": {"-u", "-C"},
    "nice": {"-n"},
    "ionice": {"-c", "-n", "-p"},
    "timeout": {"-s", "-k"},
    "stdbuf": {"-i", "-o", "-e"},
    "xargs": {"-I", "-n", "-P", "-d", "-L", "-s", "-E", "-a", "-l"},
    "watch": {"-n", "-d"},
    "exec": {"-a"},
    "caffeinate": {"-t", "-w"},
}
_SIMPLE_WRAPPERS = frozenset(
    {"sudo", "doas", "env", "nohup", "nice", "ionice", "timeout", "stdbuf", "xargs", "watch", "exec", "builtin",
     "command", "setsid", "caffeinate", "unbuffer", "chronic"}
)
_UV_VALUE_OPTS = {"--with", "--python", "-p", "--directory", "--project", "--env-file", "--extra", "--group",
                  "--package", "--with-requirements", "--with-editable", "--index", "-w"}


def _positionals(args: list[str], value_opts: set[str] | frozenset[str] = frozenset()) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--":
            out.extend(args[i + 1 :])
            break
        if a.startswith("-") and len(a) > 1:
            i += 2 if a in value_opts else 1
            continue
        out.append(a)
        i += 1
    return out


def _skip_opts(name: str, args: list[str]) -> list[str]:
    vals = _OPT_VALUES.get(name, set())
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--":
            i += 1
            break
        if a.startswith("-") and len(a) > 1:
            i += 2 if a in vals else 1
            continue
        if name == "env" and _ASSIGN.match(a):
            i += 1
            continue
        break
    return args[i:]


def _strip_prefix(words: list[str]) -> list[str]:
    i = 0
    while i < len(words) and (_ASSIGN.match(words[i]) or words[i] in _RESERVED):
        i += 1
    return words[i:]


def _norm(name: str) -> str:
    base = os.path.basename(name).lower()
    if base.endswith(".exe"):
        base = base[:-4]
    m = re.fullmatch(r"(python|pip|ruby|perl|php|node|lua)[\d.\-]*", base)
    return m.group(1) if m else base


def _runner_rest(base: str, args: list[str]) -> list[str] | None:
    """`uv run X`, `npx X`, `python -m X` ...: the command that is really executed, else None."""
    pos = _positionals(args, _UV_VALUE_OPTS)
    if base == "uv" and pos[:1] == ["run"] or base in {"poetry", "pdm", "hatch", "rye", "conda", "pipx"} and pos[:1] == ["run"]:
        return _skip_after(args, "run")
    if base == "uv" and pos[:2] == ["tool", "run"]:
        return _skip_after(args, "run")
    if base in {"uvx", "npx", "bunx", "pnpx"}:
        return _skip_opts("x", args) if base != "npx" else _skip_npx(args)
    if base in {"pnpm", "yarn"} and pos[:1] in (["dlx"], ["exec"]):
        return _skip_after(args, pos[0])
    if base == "npm" and pos[:1] in (["exec"], ["x"]):
        return _skip_after(args, pos[0])
    return None


def _skip_after(args: list[str], word: str) -> list[str]:
    rest = args[args.index(word) + 1 :] if word in args else []
    out, i = rest, 0
    while i < len(out) and out[i].startswith("-") and out[i] != "--":
        i += 2 if out[i] in _UV_VALUE_OPTS else 1
    return out[i + 1 :] if i < len(out) and out[i] == "--" else out[i:]


def _skip_npx(args: list[str]) -> list[str]:
    i = 0
    while i < len(args) and args[i].startswith("-"):
        i += 2 if args[i] in {"-p", "--package", "-c"} else 1
    return args[i:]


def check(command: str) -> Verdict | None:
    """Return a Verdict if the command crosses an approval gate (or cannot be verified), else None."""
    try:
        cmds = parse(command)
    except ParseError as exc:
        return _unverifiable(f"shell parse error ({exc})")
    return _check_cmds(cmds, 0)


def _check_cmds(cmds: list[Cmd], depth: int) -> Verdict | None:
    for c in cmds:
        v = _check_words(list(c.words), c.redirs, c.stdin, depth)
        if v:
            return v
    return None


def _check_string(text: str, depth: int) -> Verdict | None:
    if depth > MAX_DEPTH:
        return _unverifiable("nesting too deep")
    try:
        return _check_cmds(parse(text, depth + 1), depth + 1)
    except ParseError as exc:
        return _unverifiable(f"shell parse error ({exc})")


def _check_words(words: list[str], redirs: list[str], stdin: list[str], depth: int) -> Verdict | None:
    if depth > MAX_DEPTH:
        return _unverifiable("nesting too deep")
    words = _strip_prefix(words)
    if not words:
        return None
    name = words[0]
    if name in ("[", "[["):
        return None
    if SUB in name or any(ch in name for ch in "$*?[{"):
        return _unverifiable("the command name is built from a variable, glob or substitution")
    base = _norm(name)
    args = words[1:]

    # ---- wrappers: judge the command they run
    if base == "command" and any(a in ("-v", "-V") for a in args):
        return None
    if base == "env" and any(a == "-S" or a.startswith("--split-string") for a in args):
        i = next(i for i, a in enumerate(args) if a == "-S" or a.startswith("--split-string"))
        s = args[i + 1] if args[i] == "-S" and i + 1 < len(args) else args[i].partition("=")[2]
        return _check_string(s, depth)
    if base in _SIMPLE_WRAPPERS:
        rest = _skip_opts(base, args)
        if base == "timeout" and rest:
            rest = rest[1:]
        if base == "watch" and len(rest) == 1:
            return _check_string(rest[0], depth)
        return _check_words(rest, redirs, stdin, depth + 1)
    rest = _runner_rest(base, args)
    if rest is not None:
        return _check_words(rest, redirs, stdin, depth + 1)
    if base == "find":
        for i, a in enumerate(args):
            if a in ("-exec", "-execdir", "-ok", "-okdir"):
                sub = []
                for b in args[i + 1 :]:
                    if b in (";", "+"):
                        break
                    sub.append(b)
                v = _check_words(sub, redirs, stdin, depth + 1)
                if v:
                    return v
    if base == "eval":
        if any(SUB in a or "$" in a for a in args):
            return _unverifiable("eval of a value built from a variable or substitution")
        return _check_string(" ".join(args), depth)

    # ---- shells and interpreters that read code
    if base in _SHELLS:
        return _shell(args, stdin, depth)
    if base in ("ssh",):
        return _ssh(args, stdin, depth)
    if base in _INTERPRETERS:
        v = _interpreter(base, args, stdin, depth)
        if v:
            return v

    # ---- guard tamper
    v = _tamper(base, args, redirs)
    if v:
        return v
    if base in ROUTINE_COMMANDS:
        return None

    handler = _RULES.get(base)
    if handler:
        return handler(args, stdin)
    return None


def _shell(args: list[str], stdin: list[str], depth: int) -> Verdict | None:
    for i, a in enumerate(args):
        if re.fullmatch(r"-[a-zA-Z]+", a) and "c" in a and i + 1 < len(args):
            return _check_string(args[i + 1], depth)
    pos = _positionals(args, {"-o", "-O", "--rcfile", "--init-file"})
    if pos and "-s" not in args:
        return None  # `bash script.sh`: the script body is not inspected (known gap)
    if stdin:
        for body in stdin:
            v = _check_string(body, depth)
            if v:
                return v
        return None
    return _unverifiable("a shell is reading commands from a pipe or stdin")


def _ssh(args: list[str], stdin: list[str], depth: int) -> Verdict | None:
    pos = _positionals(args, set("-p -i -l -o -F -J -L -R -D -W -b -c -E -I -m -O -S -w -B -e -Q".split()))
    if len(pos) > 1:
        return _check_string(" ".join(pos[1:]), depth)
    for body in stdin:
        v = _check_string(body, depth)
        if v:
            return v
    return None


_INLINE_FLAGS = {"-c", "-e", "-E", "-p", "--eval", "--print", "-r"}
_NET_CODE = re.compile(
    r"\b(requests|httpx|urllib\d?|http\.client|httplib|aiohttp|smtplib|imaplib|ftplib|poplib|paramiko|boto3|"
    r"botocore|stripe|twilio|sendgrid|socket|telebot|nodemailer|axios|XMLHttpRequest|child_process|subprocess|"
    r"os\.system|os\.popen|Net::HTTP|LWP|IO::Socket)\b|\bfetch\s*\(|\bhttps?\.request|\bexecSync\b|\bspawn\w*\(|"
    r"\bsystem\s*\(|\bProcess\.spawn|`"
)


def _interpreter(base: str, args: list[str], stdin: list[str], depth: int) -> Verdict | None:
    if base == "python" and "-m" in args:
        i = args.index("-m")
        if i + 1 < len(args):
            return _check_words(args[i + 1 :], [], stdin, depth + 1)
    code = list(stdin)
    for i, a in enumerate(args):
        if a in _INLINE_FLAGS and i + 1 < len(args):
            code.append(args[i + 1])
    for text in code:
        if _NET_CODE.search(text):
            return _v(
                ActionType.THIRD_PARTY_COMMUNICATION,
                "inline-network-code",
                f"Inline {base} code that uses the network, mail or a subprocess cannot be verified as routine.",
            )
    pos = [p for p in _positionals(args, _INLINE_FLAGS) if p != "-"]
    if not code and not pos and not any(a in ("-h", "--help", "-V", "--version", "-v", "-i") for a in args):
        return _unverifiable(f"{base} is reading a program from a pipe or stdin")
    return None


_SETTINGS_PATH = re.compile(r"\.claude/(settings[^/\s]*\.json|hooks/)|(^|/)approval_hook\.py$")
_READONLY_FOR_TAMPER = frozenset(
    "cat less more head tail grep egrep fgrep rg ls diff cmp jq wc file stat bat python pytest cimcime".split()
)


def _tamper(base: str, args: list[str], redirs: list[str]) -> Verdict | None:
    if base in _READONLY_FOR_TAMPER:
        return None
    if base == "git" and _positionals(args, {"-C", "-c"})[:1] and _positionals(args, {"-C", "-c"})[0] in (
        "diff", "log", "show", "status", "blame", "grep", "ls-files"
    ):
        return None
    if any(_SETTINGS_PATH.search(w) for w in [*args, *redirs]):
        return _v(None, "guard-tamper", "This command touches Claude Code settings or the approval hook itself, which the guard protects.")
    return None


def _git(args: list[str], stdin: list[str]) -> Verdict | None:
    i, sub, rest = 0, None, []
    while i < len(args):
        a = args[i]
        if a in ("-c", "--config-env") and i + 1 < len(args):
            val = args[i + 1].lower()
            if re.match(r"(alias\.|.*pushurl|url\..*insteadof|remote\..*\.url)", val):
                return _v(ActionType.PRODUCTION_DEPLOY, "git-retarget", "Per-command git config that aliases commands or retargets a remote.")
            i += 2
        elif a in ("-C", "--git-dir", "--work-tree", "--namespace", "--exec-path", "--super-prefix"):
            i += 2
        elif a.startswith("-"):
            i += 1
        else:
            sub, rest = a, args[i + 1 :]
            break
    if sub == "push":
        return _git_push(rest)
    if sub == "send-email":
        return _v(ActionType.THIRD_PARTY_COMMUNICATION, "git-send-email", "git send-email mails real third parties.")
    if sub == "remote":
        pos = _positionals(rest)
        if pos[:1] and pos[0] in ("add", "set-url", "rename", "remove", "rm"):
            return _v(ActionType.PRODUCTION_DEPLOY, "git-retarget", "Changing a git remote can redirect pushes to the public mirror or another repo.")
    if sub == "config" and not any(a in ("--get", "--get-all", "--list", "-l", "--get-regexp") for a in rest):
        for a in _positionals(rest):
            if re.match(r"(?i)(alias\.|.*\.(push)?url$|url\..*insteadof)", a):
                return _v(ActionType.PRODUCTION_DEPLOY, "git-retarget", "Setting a git alias or remote URL can hide or redirect a push.")
    return None


def _git_push(rest: list[str]) -> Verdict | None:
    if any(a.startswith("--repo") for a in rest):
        return _v(ActionType.PRODUCTION_DEPLOY, "git-push-remote", "git push --repo targets a non-origin repository.")
    for a in rest:
        if a in ("-f", "--force", "--mirror", "--delete", "-d", "--prune") or a.startswith("--force-with-lease") or re.fullmatch(r"-[a-zA-Z]*f[a-zA-Z]*", a):
            return _v(ActionType.PRODUCTION_DEPLOY, "git-push-force", "Force, mirror, prune or delete pushes rewrite published history (ADR-0014: fast-forward only).")
    pos = _positionals(rest, {"-o", "--push-option", "--receive-pack", "--exec", "--signed"})
    if pos and pos[0] != "origin":
        return _v(ActionType.PRODUCTION_DEPLOY, "git-push-remote", "Only `git push origin ...` is routine (CI mirrors main to the public repo, ADR-0014). Any other remote or URL needs approval.")
    if any(p.startswith("+") for p in pos[1:]):
        return _v(ActionType.PRODUCTION_DEPLOY, "git-push-force", "A `+refspec` is a force push.")
    if any(PUBLIC_MIRROR.search(p) for p in rest):
        return _v(ActionType.PRODUCTION_DEPLOY, "git-push-public", "Pushing to the public mirror is done only by the ADR-0014 CI workflow.")
    return None


_GH_READ = frozenset({"view", "list", "status", "diff", "checks", "browse", "download", "watch", "get", "clone", "ls", "search"})
_GH_WRITE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def _gh(args: list[str], stdin: list[str]) -> Verdict | None:
    pos = _positionals(args, {"-R", "--repo", "--hostname"})
    group = pos[0] if pos else ""
    verb = pos[1] if len(pos) > 1 else ""
    if group == "api":
        method = None
        for i, a in enumerate(args):
            if a in ("-X", "--method") and i + 1 < len(args):
                method = args[i + 1].upper()
            elif a.startswith("--method="):
                method = a.split("=", 1)[1].upper()
        has_fields = any(a in ("-f", "-F", "--field", "--raw-field", "--input") or a.startswith(("--field=", "--raw-field=", "--input=")) for a in args)
        if len(pos) > 1 and pos[1] == "graphql":
            low = " ".join(args).lower()
            if "mutation" in low or "query=@" in low or "-f query=@" in low:
                return _v(ActionType.THIRD_PARTY_COMMUNICATION, "gh-api-write", "GraphQL mutations change GitHub state.")
            return None
        if (method in _GH_WRITE_METHODS) or (method is None and has_fields):
            return _v(ActionType.THIRD_PARTY_COMMUNICATION, "gh-api-write", "A non-GET GitHub API call changes remote state (use `gh issue`/`gh pr` for routine work).")
        return None
    repo_opt = None
    for i, a in enumerate(args):
        if a in ("-R", "--repo") and i + 1 < len(args):
            repo_opt = args[i + 1]
        elif a.startswith("--repo="):
            repo_opt = a.split("=", 1)[1]
    candidates = [repo_opt] if repo_opt else []
    candidates += [m.group(1) for a in args for m in re.finditer(r"github\.com/([^/\s]+)/", a)]
    if any(PUBLIC_MIRROR.search(a) for a in args) and verb not in _GH_READ:
        return _v(ActionType.PRODUCTION_DEPLOY, "gh-public-mirror", "Writing to the public mirror repo is done only by the ADR-0014 CI workflow.")
    if verb not in _GH_READ and group in ("issue", "pr", "release", "label", "project"):
        for c in candidates:
            owner = c.split("/")[0].lower()
            if owner and owner != OWNER:
                return _v(ActionType.THIRD_PARTY_COMMUNICATION, "gh-foreign-repo", f"Writing to a repo not owned by {OWNER} is communication with a third party.")
    table = {
        "repo": {"create", "delete", "edit", "rename", "archive", "unarchive", "transfer", "fork", "sync", "deploy-key"},
        "release": {"create", "edit", "delete", "upload", "delete-asset"},
        "secret": {"set", "delete", "remove"},
        "variable": {"set", "delete", "remove"},
        "workflow": {"enable", "disable"},
        "gist": {"create", "edit", "delete", "rename"},
        "ssh-key": {"add", "delete"},
        "gpg-key": {"add", "delete"},
        "auth": {"login", "logout", "refresh", "token", "setup-git"},
        "alias": {"set", "import", "delete"},
        "extension": {"install", "upgrade", "remove"},
        "codespace": {"create", "delete", "stop", "edit"},
        "ruleset": {"create", "delete", "edit"},
        "org": {"create", "delete"},
    }
    if verb in table.get(group, ()):
        gate = ActionType.SPEND_OR_ACCOUNT_CHANGE if group in ("secret", "variable", "ssh-key", "gpg-key", "auth", "codespace", "org") else ActionType.PRODUCTION_DEPLOY
        return _v(gate, f"gh-{group}-{verb}", f"`gh {group} {verb}` publishes or changes account/repo settings.")
    return None


_LOOPBACK = re.compile(r"^(localhost|127\.\d+\.\d+\.\d+|\[?::1\]?|0\.0\.0\.0)$", re.I)
_COMM_ENDPOINT = re.compile(
    r"(?i)api\.telegram\.org/.*/send|hooks\.slack\.com|discord(app)?\.com/api/webhooks|api\.twilio\.com|"
    r"api\.sendgrid\.com|api\.mailgun\.net|api\.resend\.com|api\.postmarkapp\.com|slack\.com/api/chat\."
)


def _hosts(words: list[str]) -> list[str]:
    out = []
    for w in words:
        m = re.match(r"^(?:[a-z][a-z0-9+.\-]*://)?(?:[^/@\s]*@)?(\[[^\]]+\]|[^/:?#\s]+)", w, re.I)
        if m and ("://" in w or "." in m.group(1) or _LOOPBACK.match(m.group(1))):
            out.append(m.group(1))
    return out


def _curl(args: list[str], stdin: list[str]) -> Verdict | None:
    joined = " ".join(args)
    if _COMM_ENDPOINT.search(joined):
        return _v(ActionType.THIRD_PARTY_COMMUNICATION, "http-comm-endpoint", "That endpoint sends messages to real third parties.")
    write = False
    for i, a in enumerate(args):
        nxt = args[i + 1].upper() if i + 1 < len(args) else ""
        if a in ("-X", "--request"):
            write |= nxt not in ("GET", "HEAD", "OPTIONS")
        elif a.startswith("--request="):
            write |= a.split("=", 1)[1].upper() not in ("GET", "HEAD", "OPTIONS")
        elif re.fullmatch(r"-X[A-Za-z]+", a):
            write |= a[2:].upper() not in ("GET", "HEAD", "OPTIONS")
        elif a.startswith("--") and re.match(r"--(data|data-\w+|form|form-string|upload-file|json)(=|$)", a):
            write = True
        elif re.fullmatch(r"-[A-Za-z]*[dFT][A-Za-z]*", a) and not a.startswith("--"):
            write = True
        elif re.fullmatch(r"-[A-Za-z]*X[A-Za-z]*", a):
            write |= nxt not in ("GET", "HEAD", "OPTIONS")
    if not write:
        return None
    urls = [a for a in args if not a.startswith("-")]
    hosts = _hosts(urls)
    if hosts and all(_LOOPBACK.match(h) for h in hosts):
        return None
    return _v(ActionType.THIRD_PARTY_COMMUNICATION, "http-write", "A POST/PUT/PATCH/DELETE (or upload) to a non-local host is outbound communication.")


def _wget(args: list[str], stdin: list[str]) -> Verdict | None:
    joined = " ".join(args)
    if _COMM_ENDPOINT.search(joined):
        return _v(ActionType.THIRD_PARTY_COMMUNICATION, "http-comm-endpoint", "That endpoint sends messages to real third parties.")
    write = any(a.startswith(("--post-data", "--post-file", "--body-data", "--body-file")) for a in args)
    write |= any(a.startswith("--method") and a.partition("=")[2].upper() not in ("", "GET", "HEAD") for a in args)
    if "--method" in args:
        i = args.index("--method")
        write |= i + 1 < len(args) and args[i + 1].upper() not in ("GET", "HEAD")
    hosts = _hosts([a for a in args if not a.startswith("-")])
    if write and not (hosts and all(_LOOPBACK.match(h) for h in hosts)):
        return _v(ActionType.THIRD_PARTY_COMMUNICATION, "http-write", "A wget POST to a non-local host is outbound communication.")
    return None


def _httpie(args: list[str], stdin: list[str]) -> Verdict | None:
    pos = _positionals(args)
    write = bool(pos and pos[0].upper() in ("POST", "PUT", "PATCH", "DELETE"))
    write |= any(("=" in p and "==" not in p and "://" not in p) or p.startswith("@") for p in pos)
    if write and not (_hosts(pos) and all(_LOOPBACK.match(h) for h in _hosts(pos))):
        return _v(ActionType.THIRD_PARTY_COMMUNICATION, "http-write", "An HTTP write to a non-local host is outbound communication.")
    return None


def _netcat(args: list[str], stdin: list[str]) -> Verdict | None:
    if any(a in ("-l", "-lk", "-h", "--help") for a in args):
        return None
    pos = _positionals(args, {"-p", "-w", "-s", "-q"})
    if pos and all(_LOOPBACK.match(p) for p in pos[:1]):
        return None
    return _v(ActionType.THIRD_PARTY_COMMUNICATION, "raw-network", "Raw network clients can send data to any third party.")


def _mail(args: list[str], stdin: list[str]) -> Verdict | None:
    return _v(ActionType.THIRD_PARTY_COMMUNICATION, "mail-cli", "Mail clients send messages to real third parties.")


def _osascript(args: list[str], stdin: list[str]) -> Verdict | None:
    text = " ".join([*args, *stdin])
    if re.search(r"(?i)\b(mail|messages|imessage|telegram|slack|facetime|send)\b", text):
        return _v(ActionType.THIRD_PARTY_COMMUNICATION, "osascript-send", "AppleScript that drives Mail/Messages or sends can contact real third parties.")
    return None


def _launchctl(args: list[str], stdin: list[str]) -> Verdict | None:
    pos = _positionals(args)
    sub = pos[0] if pos else ""
    if sub in ("list", "print", "print-cache", "print-disabled", "blame", "version", "help", "managerpid", "manageruid", "managername", "hostinfo", "error", "") and not (sub == "" and args):
        return None
    if sub == "kickstart":
        target = pos[-1] if len(pos) > 1 else ""
        if re.fullmatch(r"(?i)(gui|user)/[^/\s]+/[^/\s]*alfred[^/\s]*", target) and all(a in ("-k", "-p", "kickstart", target) for a in args):
            return None
        return _v(ActionType.PRODUCTION_DEPLOY, "launchctl", "The standing permission covers only `launchctl kickstart [-k] gui/<uid>/<alfred bot label>`.")
    return _v(ActionType.PRODUCTION_DEPLOY, "launchctl", f"`launchctl {sub}` changes a production service beyond the standing alfred kickstart permission.")


def _systemctl(args: list[str], stdin: list[str]) -> Verdict | None:
    pos = _positionals(args)
    sub = pos[0] if pos else ""
    if sub in ("status", "is-active", "is-enabled", "is-failed", "show", "cat", "list-units", "list-unit-files", "list-timers", "list-sockets", "") :
        return None
    if sub in ("restart", "start") and len(pos) == 2 and "alfred" in pos[1].lower():
        return None
    return _v(ActionType.PRODUCTION_DEPLOY, "systemctl", f"`systemctl {sub}` changes a production service beyond the standing alfred restart permission.")


def _svc(args: list[str], stdin: list[str]) -> Verdict | None:
    pos = _positionals(args)
    if pos[:1] and pos[0] in ("stop", "uninstall", "install"):
        return _v(ActionType.PRODUCTION_DEPLOY, "runner-service", "Stopping or reinstalling the CI runner service takes down CD (ADR-0011).")
    return None


_PUBLISH = {
    "npm": {"publish", "unpublish", "deprecate", "dist-tag", "access", "owner", "token", "adduser", "login", "team"},
    "pnpm": {"publish"}, "yarn": {"publish", "npm"}, "bun": {"publish"},
    "uv": {"publish"}, "poetry": {"publish"}, "twine": {"upload", "register"}, "flit": {"publish"},
    "hatch": {"publish"}, "maturin": {"publish", "upload"}, "cargo": {"publish", "yank", "owner", "login"},
    "gem": {"push", "yank", "owner"}, "docker": {"push"}, "podman": {"push"}, "buildah": {"push"},
    "nerdctl": {"push"}, "helm": {"push"}, "oras": {"push"}, "mvn": {"deploy"}, "gradle": {"publish"},
    "gradlew": {"publish"}, "vsce": {"publish"}, "ovsx": {"publish"}, "dotnet": {"nuget"},
}


def _publish_rule(base: str):
    verbs = _PUBLISH[base]

    def rule(args: list[str], stdin: list[str]) -> Verdict | None:
        pos = _positionals(args)
        if base in ("docker", "podman", "buildah", "nerdctl") and any(a == "--push" or a.startswith("--output=type=registry") for a in args):
            return _v(ActionType.PRODUCTION_DEPLOY, "package-publish", "Building with --push publishes an image.")
        if base == "dotnet" and not (pos[:2] == ["nuget", "push"]):
            return None
        if any(p in verbs for p in pos[:2]) or (base in ("gradle", "gradlew") and any("publish" in p for p in pos)):
            return _v(ActionType.PRODUCTION_DEPLOY, "package-publish", f"`{base} {' '.join(pos[:2])}` publishes an artifact or changes registry/account state.")
        return None

    return rule


_READISH = ("describe", "list", "get", "show", "ls", "view", "status", "info", "whoami", "logs", "plan", "validate", "preview", "diff", "version", "help", "search", "check", "doctor", "inspect")
_DEPLOY_WORDS = frozenset({"deploy", "apply", "publish", "release", "up", "push", "rollout", "promote", "launch", "ship", "upgrade", "install", "destroy", "delete"})


def _readish(v: str) -> bool:
    v = v.lower()
    return v.startswith(_READISH)


def _cloud_verdict(base: str, pos: list[str]) -> Verdict:
    deploy = any(p.lower() in _DEPLOY_WORDS for p in pos[:3])
    gate = ActionType.PRODUCTION_DEPLOY if deploy else ActionType.SPEND_OR_ACCOUNT_CHANGE
    return _v(gate, f"cloud-cli-{base}", f"`{base} {' '.join(pos[:3])}` can deploy to production or spend/modify real cloud resources. Only read-only verbs and --help/--version are routine.")


def _cloud_rule(base: str):
    def rule(args: list[str], stdin: list[str]) -> Verdict | None:
        if any(a in ("--version", "--help", "-h", "-version", "-v") for a in args[:2]):
            return None
        pos = _positionals(args, {"--profile", "--region", "--output", "--query", "--project", "--zone", "--namespace", "-n", "--context", "--kubeconfig", "-c", "--filter", "--format"})
        strict_empty_ok = base in ("aws", "gcloud", "az", "terraform", "tofu", "terragrunt", "kubectl", "oc", "helm", "gsutil", "pulumi")
        if not pos:
            return None if strict_empty_ok else _cloud_verdict(base, pos)
        if base == "aws":
            svc, verb = pos[0], (pos[1] if len(pos) > 1 else "")
            ok = svc == "help" or (svc == "s3" and verb in ("ls",)) or (svc != "s3" and _readish(verb))
        elif base in ("gcloud", "az", "doctl", "hcloud", "linode-cli", "oci", "aliyun", "ibmcloud"):
            ok = _readish(pos[-1])
        elif base == "gsutil":
            ok = pos[0] in ("ls", "cat", "stat", "du", "version", "help", "hash")
        elif base in ("terraform", "tofu", "terragrunt"):
            ok = pos[0] in ("plan", "validate", "fmt", "init", "show", "version", "output", "providers", "graph", "help", "workspace-list") or (pos[0] == "state" and pos[1:2] in (["list"], ["show"]))
        elif base == "pulumi":
            ok = pos[0] in ("preview", "version", "whoami", "about", "logs") or (pos[0] == "stack" and pos[1:2] and pos[1] in ("ls", "output", "history", "graph"))
        elif base in ("kubectl", "oc"):
            ok = pos[0] in ("get", "describe", "logs", "top", "explain", "version", "diff", "api-resources", "api-versions", "cluster-info", "events") or (pos[0] == "config" and pos[1:2] and pos[1] in ("view", "get-contexts", "current-context")) or (pos[0] == "rollout" and pos[1:2] and pos[1] in ("status", "history")) or (pos[0] == "auth" and pos[1:2] == ["can-i"])
        elif base == "helm":
            ok = pos[0] in ("list", "ls", "status", "get", "show", "search", "template", "lint", "version", "history", "env", "dependency", "repo-list")
        else:
            ok = _readish(pos[0]) or pos[0] in ("whoami", "logs", "dashboard")
        return None if ok else _cloud_verdict(base, pos)

    return rule


def _remote_copy(args: list[str], stdin: list[str]) -> Verdict | None:
    for a in _positionals(args, {"-e", "-P", "-i", "-o", "-F", "-J", "-c", "-l", "-S"}):
        if re.match(r"^(rsync|scp|sftp|ssh)://|^[^/\s:.~][^/\s]*:", a):
            return _v(ActionType.PRODUCTION_DEPLOY, "remote-copy", "Copying files to a remote host is a deploy-like action.")
    return None


_RULES: dict = {
    "git": _git, "gh": _gh, "curl": _curl, "wget": _wget, "http": _httpie, "https": _httpie, "xh": _httpie,
    "httpie": _httpie, "nc": _netcat, "ncat": _netcat, "netcat": _netcat, "socat": _netcat, "telnet": _netcat,
    "sendmail": _mail, "mail": _mail, "mailx": _mail, "mutt": _mail, "msmtp": _mail, "ssmtp": _mail, "swaks": _mail,
    "s-nail": _mail, "osascript": _osascript, "launchctl": _launchctl, "systemctl": _systemctl, "svc.sh": _svc,
    "scp": _remote_copy, "rsync": _remote_copy, "sftp": _remote_copy,
}
for _b in _PUBLISH:
    _RULES[_b] = _publish_rule(_b)
for _b in ("aws", "gcloud", "gsutil", "az", "doctl", "hcloud", "linode-cli", "oci", "aliyun", "ibmcloud", "heroku",
           "flyctl", "fly", "vercel", "netlify", "railway", "render", "wrangler", "firebase", "supabase", "stripe",
           "pulumi", "terraform", "tofu", "terragrunt", "kubectl", "oc", "helm", "eksctl", "sam", "cdk", "serverless",
           "sls", "ansible", "ansible-playbook", "packer"):
    _RULES[_b] = _cloud_rule(_b)
# `docker`/`helm` appear in both tables: publish verbs first, then (for helm) the cloud rule.
_helm_pub, _helm_cloud = _publish_rule("helm"), _cloud_rule("helm")
_RULES["helm"] = lambda a, s: _helm_pub(a, s) or _helm_cloud(a, s)
_uv_pub = _publish_rule("uv")
_RULES["uv"] = _uv_pub


# --------------------------------------------------------------------------- hook entry point


def main(argv: list[str] | None = None, stdin=None, stderr=None) -> int:
    stdin = stdin or sys.stdin
    stderr = stderr or sys.stderr

    def block(v: Verdict) -> int:
        print(v.message(), file=stderr)
        return 2

    try:
        payload = json.loads(stdin.read())
        if not isinstance(payload, dict):
            return block(_unverifiable("hook input is not a JSON object"))
        if payload.get("tool_name") != "Bash":
            return 0
        tool_input = payload.get("tool_input")
        command = tool_input.get("command") if isinstance(tool_input, dict) else None
        if not isinstance(command, str):
            return block(_unverifiable("the Bash tool call has no command string"))
        if not command.strip():
            return 0
        verdict = check(command)
    except Exception as exc:  # fail closed on any bug or odd input
        return block(_unverifiable(f"hook error {type(exc).__name__}"))
    if verdict is None:
        return 0
    if verdict.gate is not None and not requires_approval(verdict.gate):
        return 0
    return block(verdict)


if __name__ == "__main__":
    sys.exit(main())
