"""`cimcime init`: write a starter cimcime.toml for the given GitHub repo."""
from __future__ import annotations

from pathlib import Path

from cimcime.config import user_config_dir


def write_config(repo: str, *, local: bool = False, force: bool = False) -> Path:
    if repo.count("/") != 1 or not all(repo.split("/")):
        raise ValueError("repo must look like owner/name")
    path = Path("cimcime.toml") if local else user_config_dir() / "cimcime.toml"
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists (use --force to overwrite)")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'repo = "{repo}"\n', encoding="utf-8")
    return path
