import json
from pathlib import Path

import pytest

from cimcime import voice


def test_kill_switch_env_disables_everything(monkeypatch, tmp_path):
    monkeypatch.setenv(voice.VOICE_DISABLED_ENV, "off")
    with pytest.raises(voice.VoiceError, match="switched off"):
        voice.transcribe(tmp_path / "x.ogg")
    with pytest.raises(voice.VoiceError, match="switched off"):
        voice.synthesize("merhaba", tmp_path / "x.ogg")


def test_kill_switch_file_disables(monkeypatch, tmp_path):
    flag = tmp_path / "voice.off"
    flag.write_text("")
    monkeypatch.delenv(voice.VOICE_DISABLED_ENV, raising=False)
    monkeypatch.setattr(voice, "VOICE_DISABLED_FLAG", flag)
    assert not voice.is_enabled()


def test_transcribe_rejects_oversize_file(monkeypatch, tmp_path):
    monkeypatch.delenv(voice.VOICE_DISABLED_ENV, raising=False)
    monkeypatch.setattr(voice, "VOICE_DISABLED_FLAG", tmp_path / "none")
    big = tmp_path / "big.ogg"
    big.write_bytes(b"0")
    monkeypatch.setattr(voice, "MAX_AUDIO_BYTES", 0)
    with pytest.raises(voice.VoiceError, match="too large"):
        voice.transcribe(big)


def test_transcribe_rejects_long_audio(monkeypatch, tmp_path):
    monkeypatch.delenv(voice.VOICE_DISABLED_ENV, raising=False)
    monkeypatch.setattr(voice, "VOICE_DISABLED_FLAG", tmp_path / "none")
    f = tmp_path / "a.ogg"
    f.write_bytes(b"0")
    monkeypatch.setattr(voice, "audio_duration_seconds", lambda p: 999.0)
    with pytest.raises(voice.VoiceError, match="longer than"):
        voice.transcribe(f)


def test_synthesize_rejects_long_text(monkeypatch, tmp_path):
    monkeypatch.delenv(voice.VOICE_DISABLED_ENV, raising=False)
    monkeypatch.setattr(voice, "VOICE_DISABLED_FLAG", tmp_path / "none")
    with pytest.raises(voice.VoiceError, match="too long"):
        voice.synthesize("a" * (voice.MAX_TTS_CHARS + 1), tmp_path / "o.ogg")


def test_synthesize_falls_back_to_local_voice_when_edge_fails(monkeypatch, tmp_path):
    monkeypatch.delenv(voice.VOICE_DISABLED_ENV, raising=False)
    monkeypatch.setattr(voice, "VOICE_DISABLED_FLAG", tmp_path / "none")
    monkeypatch.setattr(voice, "_find_tool", lambda name, fallback=None: name)

    def boom(*a, **k):
        raise voice.VoiceError("offline")

    calls = []
    monkeypatch.setattr(voice, "_synthesize_edge", boom)
    monkeypatch.setattr(voice, "_synthesize_local", lambda t, p: calls.append("local"))
    monkeypatch.setattr(voice, "_run", lambda cmd, timeout: calls.append(cmd[0]))
    assert voice.synthesize("merhaba", tmp_path / "o.ogg") == "macos-say"
    assert calls[0] == "local"


def test_bot_token_never_appears_in_network_error(monkeypatch, tmp_path):
    monkeypatch.delenv(voice.VOICE_DISABLED_ENV, raising=False)
    monkeypatch.setattr(voice, "VOICE_DISABLED_FLAG", tmp_path / "none")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "SECRET123")
    import urllib.error

    def fail(*a, **k):
        raise urllib.error.URLError("https://api.telegram.org/botSECRET123/sendVoice")

    monkeypatch.setattr(voice.urllib.request, "urlopen", fail)
    ogg = tmp_path / "r.ogg"
    ogg.write_bytes(b"x")
    with pytest.raises(voice.VoiceError) as err:
        voice.send_voice("1", ogg)
    assert "SECRET123" not in str(err.value)


def test_cli_voice_reports_failure_as_json(monkeypatch, capsys):
    monkeypatch.setenv(voice.VOICE_DISABLED_ENV, "off")
    from cimcime.cli import _local_command

    assert _local_command(["voice", "transcribe", "/nope.ogg"]) == 1
    assert json.loads(capsys.readouterr().out)["ok"] is False
