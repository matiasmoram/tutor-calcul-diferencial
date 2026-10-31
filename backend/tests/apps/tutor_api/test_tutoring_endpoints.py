import base64

import pytest
from fastapi.testclient import TestClient

from core.shared.llm.client import LLMError, Stage
from tests.core.tutoring.builders import OK, diagnosis_json
from tests.fakes.llm import ScriptedLLMClient


def _start(api: TestClient, exercise: str = "t2-4c") -> str:
    return api.post("/api/sessions", json={"exercici_id": exercise}).json()["session_id"]


def test_a_session_shows_background_theory_and_the_outline_only_to_professors(
    api: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    out = api.post("/api/sessions", json={"exercici_id": "t2-4c"}).json()
    assert out["exercici"]["id"] == "t2-4c" and out["llista"]["id"] == "tema-2" and out["passos"]
    monkeypatch.setenv("TUTOR_CLAU_PROFESSOR", "k")
    api.app.state.tutor.config.__init__()
    student = api.post("/api/sessions", json={"exercici_id": "t2-4c"}).json()
    assert "passos" not in student and "resultat" not in student and "teoria" in student
    assert api.post("/api/sessions", json={"exercici_id": "t9-9"}).status_code == 404
    malformed = api.post("/api/sessions", json={"exercici_id": "../x"})
    assert malformed.status_code == 404 and malformed.json()["detail"] == "Exercici desconegut"


def test_a_turn_is_stored_and_logged_and_students_get_no_trace(
    api: TestClient, scripted_llm: ScriptedLLMClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    sid = _start(api)
    scripted_llm.then(Stage.DIAGNOSIS, diagnosis_json(), diagnosis_json())
    scripted_llm.then(Stage.REPLY, {"text": "Què has provat fins ara?"}, {"text": "I amb rectes, què obtens?"})
    scripted_llm.then(Stage.GUARD, OK, OK)
    professor = api.post(f"/api/sessions/{sid}/missatges", json={"text": "no sé per on començar"}).json()
    assert professor["missatge"] == "Què has provat fins ara?" and professor["trace"]["torn"] == 1
    monkeypatch.setenv("TUTOR_CLAU_PROFESSOR", "k")
    api.app.state.tutor.config.__init__()
    student = api.post(f"/api/sessions/{sid}/missatges", json={"text": "res"}).json()
    assert student["trace"] == {"fallback": False}
    turns = api.get(f"/api/professor/sessions/{sid}", headers={"X-Clau-Professor": "k"}).json()
    assert [t["alumne"] for t in turns] == ["no sé per on començar", "res"] and turns[0]["exercici"] == "t2-4c"
    [summary] = api.get("/api/professor/sessions", headers={"X-Clau-Professor": "k"}).json()
    assert summary["torns"] == 2
    assert api.get("/api/professor/sessions").status_code == 403


def test_a_failed_diagnosis_leaves_the_session_unchanged(api: TestClient, scripted_llm: ScriptedLLMClient) -> None:
    sid = _start(api)
    scripted_llm.then(Stage.DIAGNOSIS, LLMError("boom"))
    r = api.post(f"/api/sessions/{sid}/missatges", json={"text": "hola"})
    assert r.status_code == 502 and "La diagnosi ha fallat" in r.json()["detail"]
    scripted_llm.then(Stage.DIAGNOSIS, diagnosis_json())
    scripted_llm.then(Stage.REPLY, {"text": "Què has provat?"})
    scripted_llm.then(Stage.GUARD, OK)
    assert api.post(f"/api/sessions/{sid}/missatges", json={"text": "hola"}).json()["trace"]["torn"] == 1


def test_unknown_sessions(api: TestClient) -> None:
    malformed = api.post("/api/sessions/nope/missatges", json={"text": "x"})
    assert malformed.status_code == 404 and malformed.json()["detail"] == "Sessió desconeguda"
    assert api.post(f"/api/sessions/{'0' * 32}/missatges", json={"text": "x"}).status_code == 404
    assert api.get(f"/api/professor/sessions/{'0' * 32}").status_code == 404


def test_photo_transcription(api: TestClient, scripted_llm: ScriptedLLMClient) -> None:
    sid = _start(api)
    png = "data:image/png;base64," + base64.b64encode(b"\x89PNG fake").decode()
    scripted_llm.then(
        Stage.TRANSCRIPTION,
        {"transcripcio": "$x^2$", "llegibilitat": "bona", "contingut": "treball_matematic", "dubtes": []},
    )
    out = api.post(f"/api/sessions/{sid}/transcripcio", json={"imatge": png}).json()
    assert out["transcripcio"] == "$x^2$" and out["crida"]["stage"] == "transcription"
    assert api.post(f"/api/sessions/{sid}/transcripcio", json={"imatge": "nope"}).status_code == 400
    gif = "data:image/gif;base64," + base64.b64encode(b"GIF").decode()
    assert api.post(f"/api/sessions/{sid}/transcripcio", json={"imatge": gif}).status_code == 400
