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
    ],
)
def test_same_json(legacy: TestClient, api: TestClient, path: str) -> None:
    old, new = legacy.get(path), api.get(path)
    assert new.status_code == old.status_code
    assert new.json() == old.json()
