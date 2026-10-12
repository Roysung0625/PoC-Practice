from pathlib import Path

import pytest

from poc import idempiere


def test_macos_restore_uses_psql_from_path(monkeypatch):
    monkeypatch.setattr(idempiere.sys, "platform", "darwin")
    monkeypatch.setattr(idempiere.shutil, "which", lambda name: "/opt/homebrew/opt/postgresql@18/bin/psql")
    assert idempiere.psql_executable() == "/opt/homebrew/opt/postgresql@18/bin/psql"


def test_windows_keeps_project_postgres_before_path(tmp_path, monkeypatch):
    executable = tmp_path / "PostgreSQL/18/bin/psql.exe"
    executable.parent.mkdir(parents=True)
    executable.touch()
    monkeypatch.setattr(idempiere.sys, "platform", "win32")
    monkeypatch.setenv("ProgramFiles", str(tmp_path))
    monkeypatch.setattr(idempiere.shutil, "which", lambda name: "unrelated/psql.exe")
    assert Path(idempiere.psql_executable()) == executable


def test_missing_psql_explains_required_path(monkeypatch):
    monkeypatch.setattr(idempiere.sys, "platform", "darwin")
    monkeypatch.setattr(idempiere.shutil, "which", lambda name: None)
    with pytest.raises(RuntimeError, match="PostgreSQL 18.*PATH"):
        idempiere.psql_executable()
