"""/api/config: every viewer learns their own rights; only professors and demo mode see the model setup."""

import pytest
from fastapi.testclient import TestClient

SETUP = ("provider", "api_key", "stages")


def _reconfigure(api: TestClient) -> None:
    api.app.state.tutor.config.__init__()  # re-read the environment


@pytest.fixture
def production_like(api: TestClient, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("TUTOR_CLAU_PROFESSOR", "secret")
    monkeypatch.delenv("TUTOR_DEMO")
    _reconfigure(api)
    return api


def test_students_see_their_rights_and_no_model_setup(production_like: TestClient) -> None:
    body = production_like.get("/api/config").json()
    assert body["panell_professor"] is False and body["pot_generar"] is False
    assert all(key in body and body[key] is None for key in SETUP)


def test_professors_see_the_model_setup(production_like: TestClient) -> None:
    body = production_like.get("/api/config", headers={"X-Clau-Professor": "secret"}).json()
    assert body["panell_professor"] is True
    assert body["provider"] == "openai" and body["api_key"] is True
    assert set(body["stages"]["diagnosis"]) == {"model", "effort", "max_tokens"}


def test_demo_mode_shows_the_model_setup_to_everyone(api: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    assert api.get("/api/config").json()["provider"] == "openai"
    monkeypatch.setenv("TUTOR_CLAU_PROFESSOR", "secret")  # demo with a key: solutions stay closed, the setup not
    _reconfigure(api)
    body = api.get("/api/config").json()
    assert body["panell_professor"] is False and body["stages"]
