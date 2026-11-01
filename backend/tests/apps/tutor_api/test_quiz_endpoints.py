import json

import pytest
from fastapi.testclient import TestClient

from apps.tutor_api.schemas.course import TheoryItemResponse
from core.quizzes.domain.entities.statement import VerifiedCheck
from core.quizzes.infra.sqlmodel_repository import SQLModelQuizRepository
from core.shared.domain.ids import TheoryItemId
from core.shared.llm.client import Stage
from tests.core.quizzes.builders import check, graded, quiz, transcriber
from tests.fakes.llm import ScriptedLLMClient
from tests.fixtures.course import authored_course


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


UNANSWERED = (
    '"resposta":"","veredicte":"{verdict}","encert":false,"justificacio":"absent",'
    '"feedback":"No has contestat aquesta afirmació.","nota_cas":"","comprovacions_alumne":[],"idees_presents":[],'
    '"pista_usada":false,"punts":0.0,'
    '"solucio":{{"contraexemple":"{counterexample}","resolucio":"r","idees_clau":["i"],"teoria":[],"comprovacions":[]}}'
)
GRADING_JSON = (
    '{"nota":16,"encerts":1,"total":4,"afirmacions":['
    '{"id":"a1","resposta":"fals","veredicte":"fals","encert":true,"justificacio":"parcial","feedback":"f",'
    '"nota_cas":"Algun càlcul de la teva resposta no és correcte (comprovat amb sympy).",'
    '"comprovacions_alumne":[{"descripcio":"c","tipus":"igualtat","expressio":"y","variable":"","punt":"",'
    '"costat":"ambdos","valor":"x","estat":"falla","calculat":"y","detall":"","cita_alumne":"sobre $y=x$"}],'
    '"idees_presents":[1],"pista_usada":false,"punts":0.65,'
    '"solucio":{"contraexemple":"xy","resolucio":"r","idees_clau":["i"],"teoria":["T2.12"],'
    '"comprovacions":[{"descripcio":"c","tipus":"igualtat","expressio":"x+x","variable":"","punt":"",'
    '"costat":"ambdos","valor":"2*x","estat":"ok","calculat":"","detall":""}]}},'
    + ",".join(
        f'{{"id":"{sid}",{UNANSWERED.format(verdict=verdict, counterexample=counterexample)}}}'
        for sid, verdict, counterexample in (("a2", "cert", ""), ("a3", "fals", "z"), ("a4", "cert", ""))
    )
    + '],"resum":"r",'
    '"crida":{"model":"scripted","latency_ms":1,"input_tokens":10,"output_tokens":2,"cached_tokens":0},'
    '"teoria":{"T2.12":{item}}}'
)


def test_the_grading_json_is_pinned(api: TestClient, scripted_llm: ScriptedLLMClient) -> None:
    stored = quiz().model_copy(update={"source_id": "T2.12", "difficulty": "normal"})
    stored.statements[0].theory = [TheoryItemId("T2.12")]
    stored.statements[0].checks = [
        VerifiedCheck.model_validate(check("igualtat", "x+x", "2*x", variable="", point="") | {"estat": "ok"})
    ]
    assert api.portal is not None
    api.portal.call(SQLModelQuizRepository(api.app.state.tutor.sessions).save, stored)
    sid = api.post("/api/afirmacions/sessions", json={"font": "T2.12", "dificultat": "normal"}).json()["session_id"]
    scripted_llm.then(Stage.QUIZ_GRADING, graded())
    student_check = check("igualtat", "y", "x", variable="", point="") | {"cita_alumne": "sobre $y=x$"}
    scripted_llm.then(Stage.QUIZ_EXTRACTION, transcriber(a1=[student_check]))
    answers = [{"id": "a1", "veredicte": "fals", "justificacio": "sobre $y=x$"}]
    r = api.post(f"/api/afirmacions/sessions/{sid}/correccio", json={"respostes": answers})
    item = TheoryItemResponse.from_entity(authored_course().theory_item("T2.12")).model_dump()
    assert r.text == GRADING_JSON.replace("{item}", json.dumps(item, ensure_ascii=False, separators=(",", ":")))
