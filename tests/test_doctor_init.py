import pytest

from cimcime import init_cmd
from cimcime.doctor import Check, all_required_ok, format_report, run_checks


def test_format_and_required_logic():
    checks = [Check("a", True, "x"), Check("b", False, "y", required=False)]
    assert all_required_ok(checks)
    assert "[warn] b" in format_report(checks)
    assert not all_required_ok(checks + [Check("c", False, "z")])


def test_run_checks_includes_python():
    assert any(c.name == "python" and c.ok for c in run_checks())


def test_init_writes_and_refuses_overwrite(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = init_cmd.write_config("o/n", local=True)
    assert path.read_text() == 'repo = "o/n"\n'
    with pytest.raises(FileExistsError):
        init_cmd.write_config("o/n", local=True)
    init_cmd.write_config("o/m", local=True, force=True)


def test_init_rejects_bad_repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError):
        init_cmd.write_config("nope", local=True)
