import pytest
from fastapi.testclient import TestClient

from apps.tutor_api.rate_limiter import RateLimiter


def _reconfigure(api: TestClient) -> None:
    api.app.state.tutor.config.__init__()  # re-read the environment


def test_without_key_or_demo_mode_nobody_sees_solutions(api: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TUTOR_DEMO")
    _reconfigure(api)
    assert api.get("/api/config").json()["panell_professor"] is False
    assert "passos" not in api.post("/api/sessions", json={"exercici_id": "t2-4c"}).json()
    assert api.get("/api/professor/sessions").status_code == 403


def test_the_professor_key_is_checked_exactly(api: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TUTOR_CLAU_PROFESSOR", "secret")
    _reconfigure(api)
    assert api.get("/api/professor/sessions", headers={"X-Clau-Professor": "secret"}).status_code == 200
    for wrong in ("", "secre", "secret ", "SECRET"):
        assert api.get("/api/professor/sessions", headers={"X-Clau-Professor": wrong}).status_code == 403


def test_model_endpoints_are_rate_limited_per_client(api: TestClient) -> None:
    api.app.state.tutor.limiter = RateLimiter(per_minute=2)
    body = {"exercici_id": "t1-10b"}
    assert [api.post("/api/errades/sessions", json=body).status_code for _ in range(3)] == [200, 200, 429]
    assert api.get("/api/llistes").status_code == 200  # reads are not limited


def test_rate_limiter_window_slides() -> None:
    limiter = RateLimiter(per_minute=2)
    assert limiter.allow("a", now=0) and limiter.allow("a", now=1) and not limiter.allow("a", now=2)
    assert limiter.allow("b", now=2)
    assert limiter.allow("a", now=61)


def test_health(api: TestClient) -> None:
    assert api.get("/health").json() == {"status": "ok"}
