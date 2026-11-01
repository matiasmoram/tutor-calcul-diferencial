"""The schema snapshot of scripts/db.py: `schema --write` writes what `schema --check` accepts."""

from pathlib import Path

import pytest

from tests.scripts.loader import load_script

db = load_script("db")


def test_the_committed_snapshot_matches_the_code(capsys: pytest.CaptureFixture[str]) -> None:
    assert db.check_schema() == 0
    assert "supabase/schema.sql matches the code" in capsys.readouterr().out


def test_write_then_check_and_a_stale_snapshot_is_reported_with_its_diff(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "schema.sql"
    assert db.write_schema(path) == 0
    assert path.read_bytes() == db.schema().encode("utf-8") and b"\r" not in path.read_bytes()
    assert db.check_schema(path) == 0
    capsys.readouterr()

    stale = path.read_text(encoding="utf-8").replace("ENABLE ROW LEVEL SECURITY", "DISABLE ROW LEVEL SECURITY", 1)
    path.write_text(stale, encoding="utf-8", newline="\n")
    assert db.check_schema(path) == 1
    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    assert lines[:2] == [f"--- {path}", "+++ scripts/db.py schema"]
    assert any(line.startswith("-ALTER TABLE") and "DISABLE" in line for line in lines)
    assert any(line.startswith("+ALTER TABLE") and "ENABLE" in line for line in lines)
    assert "schema --write" in captured.err

    path.unlink()
    assert db.check_schema(path) == 1
