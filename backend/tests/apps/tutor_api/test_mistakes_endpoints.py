from fastapi.testclient import TestClient

from core.shared.llm.client import Stage
from tests.fakes.llm import ScriptedLLMClient


def test_a_ready_document_opens_without_the_model_and_hides_its_errors(api: TestClient) -> None:
    out = api.post("/api/errades/sessions", json={"exercici_id": "t1-10b"}).json()
    assert out["generada_ara"] is False and out["exercici"]["id"] == "t1-10b" and out["llista"]["id"] == "tema-1"
    assert set(out["solucio"]) == {"id", "font", "dificultat", "fragments", "n_enunciat", "n_errors"}


def test_grading_without_annotations_needs_no_model_and_is_stored(
    api: TestClient, scripted_llm: ScriptedLLMClient
) -> None:
    sid = api.post("/api/errades/sessions", json={"teoria_id": "T2.12"}).json()["session_id"]
    first = api.post(f"/api/errades/sessions/{sid}/correccio", json={"anotacions": []}).json()
    assert (
        first["trobats"] == 0 and first["original"]["id"] == "T2.12" and scripted_llm.calls(Stage.MISTAKES_GRADING) == 0
    )
    again = api.post(f"/api/errades/sessions/{sid}/correccio", json={"anotacions": []}).json()
    assert again == first


def test_unknown_sessions_and_sources(api: TestClient) -> None:
    assert api.post("/api/errades/sessions/nope/correccio", json={"anotacions": []}).status_code == 404
    assert api.post("/api/errades/sessions/" + "0" * 32 + "/correccio", json={"anotacions": []}).status_code == 404
    assert api.post("/api/errades/sessions", json={}).status_code == 422


def test_a_missing_key_is_a_503_only_when_the_model_is_needed(api: TestClient, monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY")
    api.app.state.tutor.config.__init__()  # re-read the environment
    assert api.post("/api/errades/sessions", json={"exercici_id": "t1-10b"}).status_code == 200
    r = api.post("/api/errades/sessions", json={"exercici_id": "t1-10b", "nova": True})
    assert r.status_code == 503 and "OPENAI_API_KEY" in r.json()["detail"]
