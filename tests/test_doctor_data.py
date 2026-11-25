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


def test_backup_checks(tmp_path):
    from cimcime.doctor import backup_checks

    assert not backup_checks(tmp_path)[0].ok  # no backup yet
    root = tmp_path / ".local" / "state" / "cimcime" / "backups"
    root.mkdir(parents=True)
    (root / "b.tar").write_text("x")
    c = backup_checks(tmp_path)
    assert not c[0].ok and "NOT encrypted" in c[0].detail
    (root / "b.tar").unlink()
    (root / "b.tar.age").write_text("x")
    c = {x.name: x for x in backup_checks(tmp_path)}
    assert c["backup"].ok and not c["restore drill"].ok
    (root / "restore-drill").write_text("")
    assert {x.name: x for x in backup_checks(tmp_path)}["restore drill"].ok
    import time
    assert not backup_checks(tmp_path, now=time.time() + 20 * 86400)[0].ok  # stale
