"""Hostile or unlucky input at the HTTP boundary: rejected before any model call, never a 500."""

import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from loguru import logger

from apps.tutor_api import server
from apps.tutor_api.rate_limiter import RateLimiter
from apps.tutor_api.server import create_app
from core.mistakes.infra.json_file_source import JsonFileMistakeSource
from core.mistakes.infra.sqlmodel_repository import SQLModelMistakeExerciseRepository
from core.quizzes.domain.values.quiz_id import QuizId
from core.quizzes.infra.json_quiz_files import JsonQuizFiles
from core.quizzes.infra.sqlmodel_repository import SQLModelQuizRepository
from core.shared.llm.client import Stage
from core.shared.storage.session_provider import SQLModelSessionProvider
from settings import BACKEND_DIR
from tests.core.quizzes.builders import quiz
from tests.fakes.llm import ScriptedLLMClient

DIFFICULTIES = ("facil", "normal", "dificil")


def _reconfigure(api: TestClient) -> None:
    api.app.state.tutor.config.__init__()  # re-read the environment


def _tutor_session(api: TestClient) -> str:
    return api.post("/api/sessions", json={"exercici_id": "t2-4c"}).json()["session_id"]


def test_control_characters_in_student_text_are_a_422_before_the_model(
    api: TestClient, scripted_llm: ScriptedLLMClient
) -> None:
    sid = _tutor_session(api)
    for bad in ("a\x00b", "a\x07b", "a\ud800b"):
        body = json.dumps({"text": bad})  # ASCII escapes: the client may send any code point, even a lone surrogate
        r = api.post(f"/api/sessions/{sid}/missatges", content=body, headers={"Content-Type": "application/json"})
        assert r.status_code == 422 and "input" not in r.json()["detail"][0]
    assert scripted_llm.calls(Stage.DIAGNOSIS) == 0
    quiz_sid = api.post("/api/afirmacions/sessions", json={"font": "T2.12", "dificultat": "facil"}).json()
    answer = {"id": quiz_sid["questionari"]["afirmacions"][0]["id"], "veredicte": "fals", "justificacio": "x\x00"}
    r = api.post(f"/api/afirmacions/sessions/{quiz_sid['session_id']}/correccio", json={"respostes": [answer]})
    assert r.status_code == 422 and scripted_llm.calls(Stage.QUIZ_GRADING) == 0
    msid = api.post("/api/errades/sessions", json={"exercici_id": "t1-10b"}).json()["session_id"]
    note = {"id": "a1", "fragment": 1, "inici": 0, "fi": 1, "comentari": "no\x00"}
    r = api.post(f"/api/errades/sessions/{msid}/correccio", json={"anotacions": [note]})
    assert r.status_code == 422 and scripted_llm.calls(Stage.MISTAKES_GRADING) == 0


def test_tabs_and_newlines_are_ordinary_text(api: TestClient) -> None:
    r = api.post("/api/afirmacions/sessions", json={"font": "T2.12\t", "dificultat": "facil"})
    assert r.status_code == 404  # validated as text, then an unknown source


def test_a_lone_surrogate_anywhere_in_the_body_is_a_422_not_a_500(api: TestClient) -> None:
    sid = _tutor_session(api)
    raw = b'{"text": "\\ud800", "origen": "\\udfff"}'
    r = api.post(f"/api/sessions/{sid}/missatges", content=raw, headers={"Content-Type": "application/json"})
    assert r.status_code == 422
    assert all(set(e) == {"loc", "msg", "type"} for e in r.json()["detail"])
    r = api.post(
        "/api/contraexemples/x/comprova",
        content=b'{"funcio": "x", "certificats": {"\\ud800": {}}}',
        headers={"Content-Type": "application/json"},
    )
    assert r.status_code == 422  # the surrogate is a dict key: it is in `loc`, made printable


def test_a_non_ascii_professor_header_is_compared_not_a_500(api: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TUTOR_CLAU_PROFESSOR", "clàu")
    _reconfigure(api)
    assert api.get("/api/professor/sessions", headers={"X-Clau-Professor": "sécret".encode()}).status_code == 403
    assert api.get("/api/professor/sessions", headers={"X-Clau-Professor": "clàu".encode()}).status_code == 200


def test_the_rate_limit_counts_the_hop_the_proxy_appended(api: TestClient) -> None:
    api.app.state.tutor.limiter = RateLimiter(per_minute=2)
    body = {"exercici_id": "t2-4c"}
    codes = [
        api.post("/api/sessions", json=body, headers={"X-Forwarded-For": f"10.0.0.{i}, 203.0.113.7"}).status_code
        for i in range(3)
    ]
    assert codes == [200, 200, 429]  # a forged leftmost address changes nothing
    other = api.post("/api/sessions", json=body, headers={"X-Forwarded-For": "10.0.0.1, 203.0.113.8"})
    assert other.status_code == 200


def test_model_endpoints_have_a_global_cap(api: TestClient) -> None:
    api.app.state.tutor.global_limiter = RateLimiter(per_minute=2)
    codes = [
        api.post(
            "/api/errades/sessions", json={"exercici_id": "t1-10b"}, headers={"X-Forwarded-For": f"203.0.113.{i}"}
        ).status_code
        for i in range(3)
    ]
    assert codes == [200, 200, 429]
    assert api.post("/api/sessions", json={"exercici_id": "t2-4c"}).status_code == 200  # no model: not capped


def test_oversized_bodies_are_a_413_before_parsing(api: TestClient) -> None:
    sid = _tutor_session(api)
    big = b'{"text": "' + b"a" * 300_000 + b'"}'
    r = api.post(f"/api/sessions/{sid}/missatges", content=big, headers={"Content-Type": "application/json"})
    assert r.status_code == 413

    def chunks() -> Iterator[bytes]:  # no Content-Length: counted as it arrives
        yield b'{"text": "'
        for _ in range(30):
            yield b"a" * 10_000
        yield b'"}'

    r = api.post(f"/api/sessions/{sid}/missatges", content=chunks(), headers={"Content-Type": "application/json"})
    assert r.status_code == 413
    photo = b'{"imatge": "data:image/png;base64,' + b"A" * 1_000_000 + b'"}'
    r = api.post(f"/api/sessions/{sid}/transcripcio", content=photo, headers={"Content-Type": "application/json"})
    assert r.status_code != 413  # the photo route allows 10 MB


def test_malformed_quiz_session_ids_are_a_404(api: TestClient) -> None:
    for sid in ("nope", "0" * 31 + "%00"):  # %00: a NUL once the path is decoded
        assert api.post(f"/api/afirmacions/sessions/{sid}/pista/a1").status_code == 404
        assert api.post(f"/api/afirmacions/sessions/{sid}/correccio", json={"respostes": []}).status_code == 404


def test_head_on_the_index_for_uptime_monitors(api: TestClient) -> None:
    assert api.head("/").status_code == 200
    assert api.get("/openapi.json").status_code == 200  # demo mode


@pytest.fixture
def production_api(tmp_path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{(tmp_path / 'api.db').as_posix()}")
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setenv("TUTOR_CLAU_PROFESSOR", "secret")
    monkeypatch.delenv("TUTOR_DEMO", raising=False)
    monkeypatch.delenv("TUTOR_GENERACIO", raising=False)
    monkeypatch.delenv("RENDER", raising=False)
    with TestClient(create_app(llm=ScriptedLLMClient({}))) as client:
        yield client


def test_outside_demo_mode_the_api_schema_is_not_published(production_api: TestClient) -> None:
    for path in ("/docs", "/redoc", "/openapi.json"):
        assert production_api.get(path).status_code == 404


def _missing(available: dict[str, int]) -> str:
    return next(d for d in DIFFICULTIES if not available.get(d))


def test_students_get_ready_documents_only(production_api: TestClient) -> None:
    api = production_api
    assert api.get("/api/config").json()["pot_generar"] is False
    ready = api.get("/api/errades/disponibles").json()["t1-10b"]
    first = api.post("/api/errades/sessions", json={"exercici_id": "t1-10b", "dificultat": next(iter(ready))}).json()
    again = api.post(
        "/api/errades/sessions",
        json={
            "exercici_id": "t1-10b",
            "dificultat": next(iter(ready)),
            "nova": True,
            "excepte": first["solucio"]["id"],
        },
    ).json()
    assert again["generada_ara"] is False
    r = api.post("/api/errades/sessions", json={"exercici_id": "t1-10b", "dificultat": _missing(ready)})
    assert r.status_code == 409 and r.json()["detail"].startswith("Encara no hi ha cap document preparat")
    professor = api.post(
        "/api/errades/sessions",
        json={"exercici_id": "t1-10b", "dificultat": _missing(ready)},
        headers={"X-Clau-Professor": "secret"},
    )
    assert professor.status_code != 409  # the professor starts the generation (the empty script then fails it)


def test_students_get_ready_quizzes_only(production_api: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    api = production_api
    focus = {i["id"]: i for t in api.get("/api/afirmacions/fonts").json()["temes"] for i in t["items"]}
    ready = focus["T2.12"]["disponibles"]
    level = next(d for d in DIFFICULTIES if ready.get(d))
    out = api.post("/api/afirmacions/sessions", json={"font": "T2.12", "dificultat": level, "nova": True})
    assert out.status_code == 200 and out.json()["generat_ara"] is False
    r = api.post("/api/afirmacions/sessions", json={"font": "T2.12", "dificultat": _missing(ready)})
    assert r.status_code == 409 and "Prova una altra dificultat o demana-ho al professorat." in r.json()["detail"]
    monkeypatch.setenv("TUTOR_GENERACIO", "tothom")
    _reconfigure(api)
    assert api.get("/api/config").json()["pot_generar"] is True
    r = api.post("/api/afirmacions/sessions", json={"font": "T2.12", "dificultat": _missing(ready)})
    assert r.status_code == 502  # a generation was attempted: the empty script fails every round


async def test_seeding_imports_files_by_missing_id(
    session_provider: SQLModelSessionProvider, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    quizzes = SQLModelQuizRepository(session_provider)
    mistakes = SQLModelMistakeExerciseRepository(session_provider)
    # Rows generated at run time, more than the files: the import still adds the missing ones.
    await quizzes.add(quiz().model_copy(update={"id": QuizId("bbbbbbbbbbbb")}))
    await quizzes.add(quiz().model_copy(update={"id": QuizId("cccccccccccc")}))
    real = JsonFileMistakeSource(BACKEND_DIR / "generats" / "errades").load()
    for document in real[1:3]:
        await mistakes.save(document)
    JsonQuizFiles(tmp_path / "generats" / "afirmacions").save(quiz())
    JsonFileMistakeSource(tmp_path / "generats" / "errades").save(real[0])
    monkeypatch.setattr(server, "BACKEND_DIR", tmp_path)
    await server._seed_generated(session_provider)
    assert {q.id for q in await quizzes.of_source("tema-2", "facil")} == {quiz().id, "bbbbbbbbbbbb", "cccccccccccc"}
    assert real[0].id in {e.id for e in await mistakes.of_source(real[0].source_id, real[0].difficulty)}


@pytest.fixture
def startup_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A complete production environment on a throwaway SQLite file; each test removes one piece."""
    db = tmp_path / "api.db"
    monkeypatch.setenv("RENDER", "true")
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db.as_posix()}")
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setenv("TUTOR_CLAU_PROFESSOR", "secret")
    monkeypatch.delenv("TUTOR_DEMO", raising=False)
    return db


@pytest.mark.parametrize("missing", ["OPENAI_API_KEY", "TUTOR_CLAU_PROFESSOR"])
def test_production_refuses_to_start_before_any_database_work(
    startup_env: Path, monkeypatch: pytest.MonkeyPatch, missing: str
) -> None:
    monkeypatch.delenv(missing)
    with pytest.raises(RuntimeError, match=missing), TestClient(create_app(llm=ScriptedLLMClient({}))):
        pass
    assert not startup_env.exists()


def test_production_refuses_demo_mode(startup_env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TUTOR_DEMO", "1")
    with pytest.raises(RuntimeError, match="TUTOR_DEMO=1"), TestClient(create_app(llm=ScriptedLLMClient({}))):
        pass


def test_a_local_start_without_a_key_warns_and_logs_its_configuration(
    startup_env: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("RENDER")
    monkeypatch.delenv("OPENAI_API_KEY")
    lines: list[str] = []
    sink = logger.add(lambda message: lines.append(message.strip()), level="INFO", format="{level} {message}")
    try:
        with TestClient(create_app(llm=ScriptedLLMClient({}))) as client:
            assert client.get("/health").status_code == 200
    finally:
        logger.remove(sink)
    assert "WARNING OPENAI_API_KEY is not set (LLM_PROVIDER=openai)" in lines
    [config] = [line for line in lines if line.startswith("INFO config: ")]
    assert "provider=openai models=diagnosis=" in config and "production=off demo=off" in config
    assert f"database=sqlite:{startup_env.as_posix()}" in config and "secret" not in config


def test_the_logged_database_has_no_credentials() -> None:
    url = "postgresql+psycopg://postgres.abcd:s3cr3t@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
    assert server._database_label(url) == "postgresql@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
