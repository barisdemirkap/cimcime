import pytest

from cimcime import config


def test_env_overrides_file(monkeypatch, tmp_path):
    f = tmp_path / "c.toml"
    f.write_text('repo = "a/b"')
    monkeypatch.setenv("CIMCIME_CONFIG", str(f))
    monkeypatch.delenv("CIMCIME_REPO", raising=False)
    assert config.get_repo() == "a/b"
    monkeypatch.setenv("CIMCIME_REPO", "x/y")
    assert config.get_repo() == "x/y"


def test_missing_repo_errors(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("CIMCIME_CONFIG", str(tmp_path / "none.toml"))
    monkeypatch.delenv("CIMCIME_REPO", raising=False)
    monkeypatch.setattr(config, "user_config_dir", lambda: tmp_path / "nocfg")
    with pytest.raises(config.ConfigError):
        config.get_repo()
