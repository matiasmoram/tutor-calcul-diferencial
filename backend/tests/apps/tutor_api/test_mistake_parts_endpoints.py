"""The per-parts ("Pas a pas") HTTP contract read by frontend/errades.js."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from apps.tutor_api import server
from core.mistakes.domain.entities.parted_mistake_exercise import MistakeDocument, PartedMistakeExercise
from core.mistakes.infra.json_file_source import JsonFileMistakeSource
from core.mistakes.infra.sqlmodel_repository import SQLModelMistakeExerciseRepository
from core.shared.llm.client import JsonObject, Stage
from core.shared.storage.session_provider import SQLModelSessionProvider
from tests.core.mistakes.builders import PARTS, parted, solution, theory_parted
from tests.fakes.llm import ScriptedLLMClient

DOC = parted()  # t2-4c, normal: part 1 clean, parts 2 and 3 with one error each ("pista 2", "pista 3")
THEORY_DOC = PartedMistakeExercise.model_validate(theory_parted().model_dump(mode="json") | {"id": "0000000000cc"})
START = {"exercici_id": "t2-4c", "dificultat": "normal", "format": "per_parts"}
GRADING_KEYS = {"nota", "trobats", "total", "falsos_positius", "anotacions", "errors", "resum", "crida"}


def _store(api: TestClient, *documents: MistakeDocument) -> None:
    """Into the running app's database, on its event loop."""
    repository = SQLModelMistakeExerciseRepository(api.app.state.tutor.sessions)
    assert api.portal is not None
    for document in documents:
        api.portal.call(repository.save, document)


def _start(api: TestClient, body: JsonObject = START) -> str:
    out = api.post("/api/errades/sessions", json=body)
    assert out.status_code == 200, out.text
    return out.json()["session_id"]


def _on(k: int) -> JsonObject:
    """An annotation on the quote of the document's k-th error (document-wide fragment numbers)."""
    m = DOC.mistakes[k]
    return {"id": f"meva-{k}", "fragment": m.fragment, "inici": m.start, "fi": m.end, "comentari": "està girada"}


def _found(mistake: str) -> JsonObject:
    """The grader's answer: the first annotation finds `mistake` and explains it."""
    return {
        "avaluacions": [{"anotacio": "a1", "error": mistake, "explicacio": "correcta", "feedback": "Bé."}],
        "resum": "Molt bé.",
    }


def _strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in _strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in _strings(v)]
    return []


def test_a_per_parts_session_shows_the_titles_and_the_first_flawed_part_only(api: TestClient) -> None:
    _store(api, DOC)
    out = api.post("/api/errades/sessions", json=START).json()
    assert out["generada_ara"] is False and out["font"] == "problema" and out["exercici"]["id"] == "t2-4c"
    assert out["solucio"] == {
        "id": DOC.id,
        "font": "problema",
        "dificultat": "normal",
        "format": "per_parts",
        "n_enunciat": 0,
        "n_errors": 2,
        "parts": [
            {"part": 1, "titol": DOC.parts[0].title, "revisar": False},
            {"part": 2, "titol": DOC.parts[1].title, "revisar": True},
            {"part": 3, "titol": DOC.parts[2].title, "revisar": True},
        ],
        "actual": {
            "part": 2,
            "primer_fragment": 3,
            "fragments": DOC.parts[1].flawed_fragments,
            "anteriors": [{"part": 1, "fragments": PARTS[0][1]}],
        },
    }
    # Never the errors, the correct text of the part under review, nor anything of the parts after it.
    shown = "\n".join(_strings(out))
    clean_of_flawed = PARTS[1][1][0]
    assert clean_of_flawed not in DOC.parts[1].flawed_fragments  # the fragment the error changed
    hidden = [clean_of_flawed, *PARTS[2][1], *(DOC.parts[2].flawed_fragments or []), "pista 2", "pista 3"]
    assert not [h for h in hidden if h in shown]


def test_the_layout_is_validated_and_the_whole_document_is_the_default(api: TestClient) -> None:
    _store(api, DOC)
    assert api.post("/api/errades/sessions", json=START | {"format": "tot"}).status_code == 422
    whole = api.post("/api/errades/sessions", json={"exercici_id": "t1-10b"}).json()["solucio"]
    assert set(whole) == {"id", "font", "dificultat", "fragments", "n_enunciat", "n_errors"}


def test_parts_are_graded_in_order_up_to_the_final_result(api: TestClient, scripted_llm: ScriptedLLMClient) -> None:
    _store(api, DOC)
    scripted_llm.then(Stage.MISTAKES_GRADING, _found("e1"))
    sid = _start(api)
    url = f"/api/errades/sessions/{sid}/parts"
    early = api.post(f"{url}/3/correccio", json={"anotacions": []})
    assert early.status_code == 409 and early.json()["detail"] == "Primer cal corregir la part anterior."
    for clean_or_missing in (1, 4):
        assert api.post(f"{url}/{clean_or_missing}/correccio", json={"anotacions": []}).status_code == 404

    first = api.post(f"{url}/2/correccio", json={"anotacions": [_on(0)]}).json()
    assert set(first) == GRADING_KEYS | {"part", "correcte", "seguent", "final"}
    assert first["part"] == 2 and first["nota"] == 100 and first["trobats"] == 1 and first["total"] == 1
    assert first["errors"] == [DOC.mistakes[0].model_dump(mode="json")]
    assert first["anotacions"] == [
        {
            "id": "meva-0",
            "error": "e1",
            "localitzacio": "exacta",
            "explicacio": "correcta",
            "feedback": "Bé.",
            "punts": 1.0,
        }
    ]
    assert first["resum"] == "Molt bé." and first["crida"]["model"] == "scripted"
    assert first["correcte"] == PARTS[1][1]
    assert first["seguent"] == {
        "part": 3,
        "primer_fragment": 5,
        "fragments": DOC.parts[2].flawed_fragments,
        "anteriors": [],
    }
    assert first["final"] is None

    # "No el trobo": nothing marked, no model call, 0 for the part, and the session's result.
    last = api.post(f"{url}/3/correccio", json={"anotacions": []}).json()
    assert last["nota"] == 0 and last["errors"] == [DOC.mistakes[1].model_dump(mode="json")]
    assert last["seguent"] is None and scripted_llm.calls(Stage.MISTAKES_GRADING) == 1
    assert last["final"] == {
        "nota": 50,
        "trobats": 1,
        "total": 2,
        "falsos_positius": 0,
        "parts": [{"part": 2, "nota": 100, "pista": False}, {"part": 3, "nota": 0, "pista": False}],
        "resolucio": [{"part": i, "fragments": fragments} for i, (_, fragments) in enumerate(PARTS, 1)],
    }

    # A graded part is graded once: a resubmission gets the stored result.
    again = api.post(f"{url}/2/correccio", json={"anotacions": []}).json()
    assert again | {"final": None, "seguent": first["seguent"]} == first and again["final"] == last["final"]
    assert again["seguent"] is None
    assert scripted_llm.calls(Stage.MISTAKES_GRADING) == 1


def test_a_hint_is_recorded_once_and_costs_its_part(api: TestClient, scripted_llm: ScriptedLLMClient) -> None:
    _store(api, DOC)
    scripted_llm.then(Stage.MISTAKES_GRADING, _found("e1"))
    sid = _start(api)
    url = f"/api/errades/sessions/{sid}/parts"
    later = api.post(f"{url}/3/pista")
    assert later.status_code == 409 and later.json()["detail"] == "Primer cal corregir la part anterior."
    assert api.post(f"{url}/1/pista").status_code == 404
    hint = api.post(f"{url}/2/pista")
    assert hint.status_code == 200 and hint.json() == {"pista": "pista 2"}
    assert api.post(f"{url}/2/pista").json() == {"pista": "pista 2"}

    graded = api.post(f"{url}/2/correccio", json={"anotacions": [_on(0)]}).json()
    assert graded["nota"] == 85
    last = api.post(f"{url}/3/correccio", json={"anotacions": []}).json()
    assert last["final"]["nota"] == 42
    assert last["final"]["parts"] == [{"part": 2, "nota": 85, "pista": True}, {"part": 3, "nota": 0, "pista": False}]


def test_each_layout_answers_only_on_its_own_endpoints(api: TestClient) -> None:
    _store(api, DOC)
    parts_sid = _start(api)
    r = api.post(f"/api/errades/sessions/{parts_sid}/correccio", json={"anotacions": []})
    assert r.status_code == 409 and r.json()["detail"] == "Aquest document es corregeix part per part."
    whole_sid = _start(api, {"exercici_id": "t1-10b"})
    for path in ("pista", "correccio"):
        r = api.post(f"/api/errades/sessions/{whole_sid}/parts/1/{path}", json={"anotacions": []})
        assert r.status_code == 409 and r.json()["detail"] == "Aquest document es corregeix sencer, no per parts."
    for unknown in ("nope", "0" * 32):
        for path in ("pista", "correccio"):
            r = api.post(f"/api/errades/sessions/{unknown}/parts/2/{path}", json={"anotacions": []})
            assert r.status_code == 404


def test_a_theory_session_reveals_the_notes_only_with_the_final_result(api: TestClient) -> None:
    _store(api, THEORY_DOC)
    out = api.post("/api/errades/sessions", json={"teoria_id": "T3.21", "format": "per_parts"}).json()
    assert out["teoria"]["id"] == "T3.21" and "exercici" not in out
    assert out["solucio"]["font"] == "teoria" and out["solucio"]["n_enunciat"] == 2
    url = f"/api/errades/sessions/{out['session_id']}/parts"
    first = api.post(f"{url}/1/correccio", json={"anotacions": []}).json()
    assert "original" not in first and first["final"] is None
    last = api.post(f"{url}/3/correccio", json={"anotacions": []}).json()
    assert "original" not in last and last["final"]["original"]["id"] == "T3.21"


def test_availability_is_listed_by_layout(api: TestClient) -> None:
    _store(api, DOC, THEORY_DOC)
    whole = api.get("/api/errades/disponibles").json()
    assert whole and api.get("/api/errades/disponibles?format=sencer").json() == whole
    assert api.get("/api/errades/disponibles?format=per_parts").json() == {
        "t2-4c": {"normal": 1},
        "T3.21": {"normal": 1},
    }
    assert api.get("/api/errades/disponibles?format=tot").status_code == 422

    def theory(query: str) -> dict[str, dict[str, int]]:
        temes = api.get(f"/api/errades/teoria{query}").json()["temes"]
        return {i["id"]: i["disponibles"] for t in temes for i in t["items"]}

    per_parts = theory("?format=per_parts")
    assert per_parts["T3.21"] == {"normal": 1} and per_parts["T2.12"] == {}
    assert theory("") == theory("?format=sencer") and theory("")["T2.12"]
    assert api.get("/api/errades/teoria?format=tot").status_code == 422


async def test_seeding_imports_the_missing_documents_of_both_layouts(
    session_provider: SQLModelSessionProvider, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    mistakes = SQLModelMistakeExerciseRepository(session_provider)
    edited = THEORY_DOC.model_copy(update={"created_at": 2.0})
    await mistakes.save(edited)  # already stored: its file does not overwrite it
    files = JsonFileMistakeSource(tmp_path / "generats" / "errades")
    for document in (DOC, THEORY_DOC, solution()):
        files.save(document)
    monkeypatch.setattr(server, "BACKEND_DIR", tmp_path)
    await server._seed_generated(session_provider)
    assert [d.id for d in await mistakes.of_source("t2-4c", "normal", "per_parts")] == [DOC.id]
    assert [d.id for d in await mistakes.of_source("t2-4c", "normal")] == [solution().id]
    assert await mistakes.get(THEORY_DOC.id) == edited
