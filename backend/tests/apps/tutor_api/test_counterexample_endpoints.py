import pytest
from fastapi.testclient import TestClient

from core.shared.math.infra.sympy_pool import SympyCheckPool

SPEC = "/api/contraexemples/parcials-sense-continuitat"
DIAGONAL = {"discontinua": {"camins": [{"x": "t", "y": "t"}]}}
GOOD = {"funcio": "x*y/(x**2+y**2)", "valor": "0", "certificats": DIAGONAL}
BAD = {"funcio": "x**2+y**2", "valor": "0", "certificats": DIAGONAL}


@pytest.fixture
def student(api: TestClient, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """A student (a professor key is configured and not sent), with sympy inline instead of worker processes."""
    monkeypatch.setenv("TUTOR_CLAU_PROFESSOR", "secret")
    api.app.state.tutor.config.__init__()  # re-read the environment
    api.app.state.tutor.sympy = SympyCheckPool(in_process=True)
    return api


def test_list_and_a_spec_without_its_example(student: TestClient) -> None:
    specs = student.get("/api/contraexemples").json()
    assert len(specs) >= 10 and all(s["propietats"] for s in specs)
    spec = student.get(SPEC).json()
    assert spec["enunciat"] and spec["pista"] and spec["exemple"] is None
    assert [p["certificat"] for p in spec["propietats"]] == ["cap", "camins"]
    # Tied to the notes: the challenge's items, each property's definition (with its PDF page).
    assert spec["teoria"] and all(it["pdf"].startswith("/pdf/") for it in spec["teoria"])
    assert all(p["teoria"] for p in spec["propietats"])
    assert student.get("/api/contraexemples/nope").status_code == 404
    assert student.get(SPEC, headers={"X-Clau-Professor": "secret"}).json()["exemple"]["funcio"]


def test_the_example_is_revealed_only_after_passing(student: TestClient) -> None:
    good = student.post(f"{SPEC}/comprova", json=GOOD).json()
    assert good["superat"] and good["rigoros"] and good["exemple"]["explicacio"]
    assert [it["id"] for it in good["exemple"]["teoria_reservada"]] == ["T3.6"]
    assert [v["estat"] for v in good["veredictes"]] == ["ok", "ok"] and good["veredictes"][1]["calculs"]
    bad = student.post(f"{SPEC}/comprova", json=BAD).json()
    assert not bad["superat"] and bad["exemple"] is None and bad["veredictes"][1]["estat"] == "indeterminat"


def test_unreadable_input_is_a_422_with_the_reason(student: TestClient) -> None:
    res = student.post(f"{SPEC}/comprova", json={"funcio": "x*y*z"})
    assert res.status_code == 422 and "només de x, y" in res.json()["detail"]
    assert student.post(f"{SPEC}/comprova", json={"funcio": "x" * 400}).status_code == 422
