"""TEMPORARY (phase 6 of work/ARQUITECTURA.md): the new endpoints answer exactly like the old app.

Deleted together with backend/app.py."""

import importlib
import os
import sys

import pytest
from fastapi.testclient import TestClient

from core.shared.llm.client import Stage
from settings import ROOT_DIR
from tests.core.tutoring.builders import OK, diagnosis_json

sys.path.insert(0, str(ROOT_DIR / "tests"))  # the legacy suite's helpers
from test_harness import TEORIA, ScriptedLLM, _diag_json

from tutor.pipeline import Tutor


@pytest.fixture(scope="module")
def legacy(tmp_path_factory: pytest.TempPathFactory) -> TestClient:
    db = tmp_path_factory.mktemp("legacy") / "legacy.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db.as_posix()}"
    module = importlib.import_module("app")  # the old backend/app.py syncs its database at import
    return TestClient(module.app)


@pytest.fixture
def legacy_app(legacy: TestClient):
    return importlib.import_module("app")


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


def _comparable(trace: dict[str, object]) -> dict[str, object]:
    # Timing and the model metadata (fake names, stage labels) legitimately differ between the two fakes.
    return {k: v for k, v in trace.items() if k not in ("latencia_ms", "crides")}


def test_same_turns_end_to_end(
    legacy: TestClient, legacy_app, api: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    diagnoses = [_diag_json(), _diag_json(passos={"candidat": "completat"}, nivell_desorientacio="en_cami")]
    replies = [
        {"text": "Què has provat?"},
        {"text": r"El límit és 0 perquè $\le |x|$."},
        {"text": "Com fitaries el quocient?"},
    ]
    guards = [OK, OK]  # the leaking second draft is rejected by the deterministic check, not the model
    monkeypatch.setattr(
        legacy_app,
        "_tutor",
        Tutor(ScriptedLLM({"diagnosi": diagnoses, "resposta": replies, "guardia": guards}), TEORIA),
    )
    scripted = api.app.state.tutor.llm._inner
    scripted.then(
        Stage.DIAGNOSIS,
        diagnosis_json(),
        diagnosis_json(steps={"candidat": "completat"}, nivell_desorientacio="en_cami"),
    )
    scripted.then(Stage.REPLY, *replies)
    scripted.then(Stage.GUARD, *guards)

    old_sid = legacy.post("/api/sessions", json={"exercici_id": "t2-4c"}).json()["session_id"]
    new_sid = api.post("/api/sessions", json={"exercici_id": "t2-4c"}).json()["session_id"]
    for text in ["no sé per on començar", "He provat y=kx i y=kx^2 i dona 0"]:
        old = legacy.post(f"/api/sessions/{old_sid}/missatges", json={"text": text}).json()
        new = api.post(f"/api/sessions/{new_sid}/missatges", json={"text": text}).json()
        assert new["missatge"] == old["missatge"] and new["referencies"] == old["referencies"]
        assert _comparable(new["trace"]) == _comparable(old["trace"])


def test_same_quiz_sources(legacy: TestClient, api: TestClient) -> None:
    assert api.get("/api/afirmacions/fonts").json() == legacy.get("/api/afirmacions/fonts").json()


def test_same_quiz_flow_on_a_ready_quiz(legacy: TestClient, api: TestClient) -> None:
    body = {"font": "T2.12", "dificultat": "facil"}
    old, new = legacy.post("/api/afirmacions/sessions", json=body).json(), api.post("/api/afirmacions/sessions", json=body).json()
    assert _without_session_id(new) == _without_session_id(old)
    first = old["questionari"]["afirmacions"][0]["id"]
    old_hint = legacy.post(f"/api/afirmacions/sessions/{old['session_id']}/pista/{first}").json()
    new_hint = api.post(f"/api/afirmacions/sessions/{new['session_id']}/pista/{first}").json()
    assert new_hint == old_hint
    unanswered = {"respostes": [{"id": first, "veredicte": "", "justificacio": ""}]}
    old_grade = legacy.post(f"/api/afirmacions/sessions/{old['session_id']}/correccio", json=unanswered).json()
    new_grade = api.post(f"/api/afirmacions/sessions/{new['session_id']}/correccio", json=unanswered).json()
    assert new_grade == old_grade
    for client, sid in ((legacy, old["session_id"]), (api, new["session_id"])):
        assert client.post(f"/api/afirmacions/sessions/{sid}/pista/zz").status_code == 404
    assert api.post("/api/afirmacions/sessions", json={"font": "T9.1"}).json() == legacy.post(
        "/api/afirmacions/sessions", json={"font": "T9.1"}
    ).json()
