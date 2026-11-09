"""Configuration: env vars override cimcime.toml, which overrides defaults.

Lookup order for the config file: $CIMCIME_CONFIG, ./cimcime.toml, <user config dir>/cimcime.toml.
"""
from __future__ import annotations

import os
import sys
import tomllib
from pathlib import Path

REPO_ENV_VAR = "CIMCIME_REPO"


class ConfigError(RuntimeError):
    pass


def user_config_dir() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming")
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return base / "cimcime"


def config_paths() -> list[Path]:
    paths = []
    if os.environ.get("CIMCIME_CONFIG"):
        paths.append(Path(os.environ["CIMCIME_CONFIG"]))
    paths += [Path("cimcime.toml"), user_config_dir() / "cimcime.toml"]
    return paths


def load_config() -> dict:
    for path in config_paths():
        if path.is_file():
            return tomllib.loads(path.read_text(encoding="utf-8"))
    return {}


def get_repo() -> str:
    repo = os.environ.get(REPO_ENV_VAR) or load_config().get("repo")
    if not repo:
        raise ConfigError(
            f"No GitHub repo configured. Set ${REPO_ENV_VAR}=owner/name or add "
            'repo = "owner/name" to cimcime.toml.'
        )
    return repo
