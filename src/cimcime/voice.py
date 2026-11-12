"""Voice notes over Telegram: local speech-to-text in, text-to-speech out.

Deterministic pipeline, no LLM tokens. Voice stays off the critical path: every function
raises VoiceError on failure and the caller answers in text instead. Approval gates never
accept voice input (GLOSSARY / ADR-0001) - transcripts are text for Cimcime to read, and any
action-triggering or gate-related command must be echoed and confirmed by typed text.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
import uuid
from pathlib import Path

VOICE_DISABLED_ENV = "CIMCIME_VOICE"  # set to "off" to disable
VOICE_DISABLED_FLAG = Path.home() / ".cache" / "cimcime" / "voice.off"
MODEL_ENV = "CIMCIME_WHISPER_MODEL"
DEFAULT_MODEL = Path.home() / ".cache" / "cimcime" / "models" / "ggml-large-v3-turbo-q5_0.bin"
TTS_VOICE_ENV = "CIMCIME_TTS_VOICE"
DEFAULT_TTS_VOICE = "tr-TR-EmelNeural"  # the only female Turkish neural voice edge-tts offers
TTS_RATE_ENV = "CIMCIME_TTS_RATE"
TTS_PITCH_ENV = "CIMCIME_TTS_PITCH"
DEFAULT_TTS_RATE = "+12%"  # the default pace felt too slow
DEFAULT_TTS_PITCH = "+6Hz"  # slightly younger, not thin
LOCAL_FALLBACK_VOICE = "Yelda"
TELEGRAM_ENV_FILE = Path.home() / ".claude" / "channels" / "telegram" / ".env"
EDGE_TTS_FALLBACK = Path.home() / ".local" / "bin" / "edge-tts"

MAX_AUDIO_BYTES = 20 * 1024 * 1024  # Telegram getFile limit
MAX_AUDIO_SECONDS = 180
MAX_TTS_CHARS = 700  # short summaries only; also bounds what is sent to the TTS provider
STT_TIMEOUT = 180
TTS_TIMEOUT = 60


class VoiceError(RuntimeError):
    pass


def is_enabled() -> bool:
    return os.environ.get(VOICE_DISABLED_ENV, "").lower() != "off" and not VOICE_DISABLED_FLAG.exists()


def _require_enabled() -> None:
    if not is_enabled():
        raise VoiceError("voice is switched off (CIMCIME_VOICE=off or kill-switch file present)")


def _run(cmd: list[str], timeout: int) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=True)
    except FileNotFoundError as exc:
        raise VoiceError(f"missing tool: {cmd[0]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise VoiceError(f"{cmd[0]} timed out after {timeout}s") from exc
    except subprocess.CalledProcessError as exc:
        raise VoiceError(f"{cmd[0]} failed: {(exc.stderr or '').strip()[-300:]}") from exc


def _find_tool(name: str, fallback: Path | None = None) -> str:
    found = shutil.which(name)
    if found:
        return found
    if fallback and fallback.exists():
        return str(fallback)
    raise VoiceError(f"missing tool: {name}")


def audio_duration_seconds(path: Path) -> float:
    ffprobe = _find_tool("ffprobe")
    out = _run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        timeout=15,
    ).stdout.strip()
    try:
        return float(out)
    except ValueError as exc:
        raise VoiceError("could not read audio duration") from exc


def transcribe(audio_path: Path, language: str = "tr") -> str:
    """Local whisper.cpp transcription. Language is forced (no auto-detect) because Turkish
    misdetected as another language produces confident nonsense."""
    _require_enabled()
    audio_path = Path(audio_path)
    if not audio_path.is_file():
        raise VoiceError(f"audio file not found: {audio_path}")
    if audio_path.stat().st_size > MAX_AUDIO_BYTES:
        raise VoiceError("audio file too large (over 20 MB)")
    if audio_duration_seconds(audio_path) > MAX_AUDIO_SECONDS:
        raise VoiceError(f"audio longer than {MAX_AUDIO_SECONDS}s")
    model = Path(os.environ.get(MODEL_ENV) or DEFAULT_MODEL)
    if not model.is_file():
        raise VoiceError(f"whisper model missing: {model}")
    ffmpeg = _find_tool("ffmpeg")
    whisper = _find_tool("whisper-cli")
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "in.wav"
        _run([ffmpeg, "-y", "-i", str(audio_path), "-ar", "16000", "-ac", "1", str(wav)], timeout=60)
        result = _run(
            [whisper, "-m", str(model), "-f", str(wav), "-l", language, "-nt", "-np"],
            timeout=STT_TIMEOUT,
        )
    text = " ".join(result.stdout.split())
    if not text:
        raise VoiceError("empty transcript")
    return text


def _synthesize_edge(text: str, voice: str, mp3: Path) -> None:
    edge = _find_tool("edge-tts", EDGE_TTS_FALLBACK)
    rate = os.environ.get(TTS_RATE_ENV) or DEFAULT_TTS_RATE
    pitch = os.environ.get(TTS_PITCH_ENV) or DEFAULT_TTS_PITCH
    # "=" form so a leading "-" in a value is not parsed as a flag
    _run(
        [edge, "--voice", voice, f"--rate={rate}", f"--pitch={pitch}", "--text", text, "--write-media", str(mp3)],
        timeout=TTS_TIMEOUT,
    )


def _prepare_speech_text(text: str) -> str:
    """Keep line breaks as pauses: after a sentence mark a newline stays a break, otherwise it
    becomes a comma, so the voice phrases naturally instead of running lines together."""
    out = ""
    for ln in (ln.strip() for ln in text.splitlines()):
        if not ln:
            continue
        if out:
            out += " " if out[-1] in ".!?:;," else ", "
        out += " ".join(ln.split())
    return out


def _synthesize_local(text: str, aiff: Path) -> None:
    _run(["say", "-v", LOCAL_FALLBACK_VOICE, "-o", str(aiff), text], timeout=TTS_TIMEOUT)


def synthesize(text: str, out_ogg: Path) -> str:
    """Text -> ogg/opus voice note. Returns which engine produced it. The neural voice sends
    the text to Microsoft's online service; on any failure it falls back to the local macOS voice."""
    _require_enabled()
    text = _prepare_speech_text(text)
    if not text:
        raise VoiceError("nothing to say")
    if len(text) > MAX_TTS_CHARS:
        raise VoiceError(f"text too long for a voice note ({len(text)} > {MAX_TTS_CHARS} chars)")
    ffmpeg = _find_tool("ffmpeg")
    voice = os.environ.get(TTS_VOICE_ENV) or DEFAULT_TTS_VOICE
    engine = "edge"
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "speech.mp3"
        try:
            _synthesize_edge(text, voice, src)
        except VoiceError:
            engine = "macos-say"
            src = Path(tmp) / "speech.aiff"
            _synthesize_local(text, src)
        _run(
            [ffmpeg, "-y", "-i", str(src), "-c:a", "libopus", "-b:a", "32k", "-ar", "48000", "-ac", "1", str(out_ogg)],
            timeout=60,
        )
    return engine


def _bot_token() -> str:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token and TELEGRAM_ENV_FILE.is_file():
        for line in TELEGRAM_ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line.startswith("TELEGRAM_BOT_TOKEN="):
                token = line.split("=", 1)[1].strip().strip("'\"")
    if not token:
        raise VoiceError("telegram bot token not found")
    return token


def send_voice(chat_id: str, ogg_path: Path, caption: str | None = None) -> str:
    """Bot API sendVoice. Reads the token the Telegram plugin already stores; never logs it."""
    _require_enabled()
    token = _bot_token()
    boundary = uuid.uuid4().hex
    parts: list[bytes] = []

    def field(name: str, value: str) -> None:
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode()
        )

    field("chat_id", str(chat_id))
    if caption:
        field("caption", caption[:1000])
    parts.append(
        (
            f'--{boundary}\r\nContent-Disposition: form-data; name="voice"; filename="reply.ogg"\r\n'
            "Content-Type: audio/ogg\r\n\r\n"
        ).encode()
        + Path(ogg_path).read_bytes()
        + b"\r\n"
    )
    parts.append(f"--{boundary}--\r\n".encode())
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendVoice",
        data=b"".join(parts),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = json.loads(response.read())
    except urllib.error.URLError as exc:
        # Never include the URL (it contains the token) in the message.
        raise VoiceError(f"sendVoice network error: {type(exc).__name__}") from exc
    if not body.get("ok"):
        raise VoiceError(f"sendVoice rejected: {body.get('description', 'unknown')}")
    return str(body["result"]["message_id"])


def speak(chat_id: str, text: str, caption: str | None = None) -> dict:
    """Synthesize and send. Returns {message_id, engine}. Raises VoiceError - caller falls back to text."""
    with tempfile.TemporaryDirectory() as tmp:
        ogg = Path(tmp) / "reply.ogg"
        engine = synthesize(text, ogg)
        message_id = send_voice(chat_id, ogg, caption=caption if caption is not None else text)
    return {"message_id": message_id, "engine": engine}


def doctor() -> list[tuple[str, bool, str]]:
    """(name, ok, detail) for each dependency. Run after OS or brew updates."""
    checks: list[tuple[str, bool, str]] = []
    for tool in ("ffmpeg", "ffprobe", "whisper-cli", "say"):
        path = shutil.which(tool)
        checks.append((tool, bool(path), path or "not found"))
    edge = shutil.which("edge-tts") or (str(EDGE_TTS_FALLBACK) if EDGE_TTS_FALLBACK.exists() else None)
    checks.append(("edge-tts", bool(edge), edge or "not found (uv tool install edge-tts)"))
    model = Path(os.environ.get(MODEL_ENV) or DEFAULT_MODEL)
    checks.append(("whisper model", model.is_file(), str(model)))
    checks.append(("telegram token", TELEGRAM_ENV_FILE.is_file() or bool(os.environ.get("TELEGRAM_BOT_TOKEN")), "present or missing (value never shown)"))
    checks.append(("voice enabled", is_enabled(), "off via CIMCIME_VOICE or kill-switch file" if not is_enabled() else "on"))
    return checks
