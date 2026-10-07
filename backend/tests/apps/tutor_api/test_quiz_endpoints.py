import pytest
from fastapi.testclient import TestClient

from core.shared.llm.client import Stage
from tests.fakes.llm import ScriptedLLMClient


def _start(api: TestClient) -> dict[str, object]:
    return api.post("/api/afirmacions/sessions", json={"font": "T2.12", "dificultat": "facil"}).json()


def test_sources_list_topics_focus_items_and_sizes(api: TestClient) -> None:
    out = api.get("/api/afirmacions/fonts").json()
    assert (
        len(out["temes"]) == 6
        and out["temes"][1]["id"] == "tema-2"
        and set(out["mida"]) == {"facil", "normal", "dificil"}
    )
    focus = {i["id"]: i for t in out["temes"] for i in t["items"]}
    assert focus["T2.12"]["disponibles"] == {"facil": 1}


def test_a_ready_quiz_opens_without_the_model_and_hides_verdicts(
    api: TestClient, scripted_llm: ScriptedLLMClient
) -> None:
    out = _start(api)
    assert out["generat_ara"] is False and out["focus"]["id"] == "T2.12"
    assert all(set(a) == {"id", "enunciat", "concepte"} for a in out["questionari"]["afirmacions"])
    assert scripted_llm.calls(Stage.QUIZ_GENERATION) == 0


def test_hints_are_recorded_and_lower_the_score(api: TestClient) -> None:
    out = _start(api)
    sid, first = out["session_id"], out["questionari"]["afirmacions"][0]["id"]
    hint = api.post(f"/api/afirmacions/sessions/{sid}/pista/{first}").json()
    assert hint["id"] == first and hint["pista"]
    assert api.post(f"/api/afirmacions/sessions/{sid}/pista/zz").status_code == 404
    graded = api.post(f"/api/afirmacions/sessions/{sid}/correccio", json={"respostes": []}).json()
    assert graded["nota"] == 0 and graded["teoria"]
    again = api.post(f"/api/afirmacions/sessions/{sid}/correccio", json={"respostes": []}).json()
    assert again == graded  # graded once: the result reveals every verdict


def test_unknown_sources_and_sessions(api: TestClient) -> None:
    assert api.post("/api/afirmacions/sessions", json={"font": "T9.1"}).status_code == 404
    assert api.post("/api/afirmacions/sessions/" + "0" * 32 + "/correccio", json={"respostes": []}).status_code == 404


def test_a_missing_key_is_a_503_only_when_the_model_is_needed(api: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY")
    api.app.state.tutor.config.__init__()
    assert _start(api)["generat_ara"] is False
    r = api.post("/api/afirmacions/sessions", json={"font": "T2.12", "dificultat": "facil", "nova": True})
    assert r.status_code == 503
