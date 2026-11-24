import os
from types import SimpleNamespace

from cimcime.doctor import data_protection_checks


def _run(out):
    return lambda *a, **k: SimpleNamespace(stdout=out, stderr="", returncode=0)


def test_filevault_and_perms(tmp_path):
    db = tmp_path / ".config" / "alfred" / "alfred.db"
    db.parent.mkdir(parents=True)
    db.write_text("x")
    os.chmod(db, 0o644)
    checks = {c.name: c for c in data_protection_checks(tmp_path, "darwin", _run("FileVault is Off."))}
    assert not checks["FileVault"].ok and not checks["FileVault"].required
    assert not checks["perms alfred.db"].ok
    os.chmod(db, 0o600)
    checks = {c.name: c for c in data_protection_checks(tmp_path, "darwin", _run("FileVault is On."))}
    assert checks["FileVault"].ok and checks["perms alfred.db"].ok


def test_linux_luks(tmp_path):
    c = data_protection_checks(tmp_path, "linux", _run("disk\ncrypt\n"))[0]
    assert c.ok
