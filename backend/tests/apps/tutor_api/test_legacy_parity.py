"""TEMPORARY (phase 6 of work/ARQUITECTURA.md): the new endpoints answer exactly like the old app.

Deleted together with backend/app.py."""

import importlib
import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def legacy(tmp_path_factory: pytest.TempPathFactory) -> TestClient:
    db = tmp_path_factory.mktemp("legacy") / "legacy.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db.as_posix()}"
    module = importlib.import_module("app")  # the old backend/app.py syncs its database at import
    return TestClient(module.app)


@pytest.mark.parametrize(
    "path",
    [
        "/api/llistes",
        "/api/llistes/tema-1",
        "/api/llistes/tema-2",
        "/api/llistes/tema-6",
        "/api/teoria",
        "/api/teoria/T3.12",
        "/api/teoria/T2.6",
        "/api/llistes/nope",
        "/api/errades/teoria",
        "/api/errades/disponibles",
    ],
)
def test_same_json(legacy: TestClient, api: TestClient, path: str) -> None:
    old, new = legacy.get(path), api.get(path)
    assert new.status_code == old.status_code
    assert new.json() == old.json()


def _without_session_id(out: dict[str, object]) -> dict[str, object]:
    return {k: v for k, v in out.items() if k != "session_id"}


@pytest.mark.parametrize(
    "body",
    [
        {"exercici_id": "t1-10b", "dificultat": "normal"},
        {"teoria_id": "T2.12", "dificultat": "normal"},
        {"exercici_id": "t9-1"},
        {"teoria_id": "T2.1"},
        {"exercici_id": "t1-10b", "teoria_id": "T2.12"},
    ],
)
def test_same_mistake_sessions_from_ready_documents(legacy: TestClient, api: TestClient, body: dict[str, str]) -> None:
    old, new = legacy.post("/api/errades/sessions", json=body), api.post("/api/errades/sessions", json=body)
    assert new.status_code == old.status_code, (old.json(), new.json())
    if old.status_code == 200:
        assert set(new.json()) == set(old.json())
        assert new.json()["solucio"]["fragments"] and new.json()["font"] == old.json()["font"]
        assert {k: v for k, v in _without_session_id(new.json()).items() if k != "solucio"} == {
            k: v for k, v in _without_session_id(old.json()).items() if k != "solucio"
        }
    else:
        assert new.json() == old.json()
