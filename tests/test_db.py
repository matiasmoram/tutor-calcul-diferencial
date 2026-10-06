"""Storage layer (backend/tutor/db.py) on a throwaway SQLite database."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from tutor import db  # noqa: E402
from tutor.llm import CallMeta  # noqa: E402


@pytest.fixture()
def tmpdb(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{(tmp_path / 't.db').as_posix()}")
    db.init()
    return db


def test_content_round_trip(tmpdb):
    from test_harness import EX, LLISTES, TEORIA
    from tutor.fitxes import Exercici
    from tutor.teoria import ItemTeoria, load_temes

    counts = tmpdb.import_contingut(LLISTES, EX, TEORIA, load_temes())
    assert counts["exercicis"] == len(EX) and tmpdb.compta_contingut() == len(EX)
    temes, items, llistes, exs = tmpdb.load_contingut()
    back = {e["id"]: Exercici(**e) for e in exs}
    assert back["t2-4c"] == EX["t2-4c"]
    assert {i["id"]: ItemTeoria(**i) for i in items}["T2.6"] == TEORIA["T2.6"]
    assert len(temes) == 6 and {l["id"] for l in llistes} == set(LLISTES)


def test_session_turns_and_professor_flags(tmpdb):
    tmpdb.desa_sessio("s1", "tutor", "t2-4c", {"torns": 0}, [])
    tr = {"pla": {"accio": "pista", "pas_objectiu": "candidat", "nivell_pista": 1}, "fallback": False, "intents": [{}],
          "diagnosi": {"intencio": "demana_pista"}}
    tmpdb.afegeix_torn("s1", 1, "no sé", "Què obtens sobre les rectes?", tr)
    tmpdb.afegeix_torn("s1", 2, "res", "Què obtens sobre les rectes?", tr)
    tmpdb.desa_sessio("s1", "tutor", "t2-4c", {"torns": 2}, [{"rol": "alumne", "text": "no sé"}])
    s = tmpdb.carrega_sessio("s1")
    assert s["estat"] == {"torns": 2} and s["historial"][0]["text"] == "no sé"
    [row] = tmpdb.llista_sessions()
    assert row["torns"] == 2 and row["bucles"] == 1 and not row["tancat"]
    assert [t["n"] for t in tmpdb.torns_de("s1")] == [1, 2]


def test_every_llm_call_is_logged_with_its_session_even_failures(tmpdb):
    class Fake:
        stages = {}

        def __init__(self):
            self.fail = False

        def structured(self, stage, system, user, schema, image=None, context=None):
            if self.fail:
                raise RuntimeError("boom")
            return {"text": "hola"}, CallMeta(stage=stage, model="m", latency_ms=5, input_tokens=10, output_tokens=2)

    inner = Fake()
    llm = tmpdb.LoggingLLM(inner)
    with tmpdb.context(sessio_id="s9", torn=3):
        assert llm.structured("resposta", "sys", "user", None)[0] == {"text": "hola"}
        inner.fail = True
        with pytest.raises(RuntimeError):
            llm.structured("guardia", "sys", "user", {})
    calls = tmpdb.crides_de("s9")
    assert [(c["stage"], c["ok"], c["torn"]) for c in reversed(calls)] == [("resposta", True, 3), ("guardia", False, 3)]
    assert calls[1]["resposta"] == {"text": "hola"} and calls[1]["input_tokens"] == 10
    assert calls[0]["prompt"] is None  # prompts are only kept with TUTOR_LOG_PROMPTS=1


def test_generated_content_store(tmpdb):
    tmpdb.desa_generat("errades", "a1", "t2-4c", "normal", {"id": "a1", "x": 1})
    tmpdb.desa_generat("errades", "a1", "t2-4c", "normal", {"id": "a1", "x": 2})  # upsert
    tmpdb.desa_generat("errades", "a2", "t2-4c", "facil", {"id": "a2"})
    assert tmpdb.generats("errades", "t2-4c", "normal") == [{"id": "a1", "x": 2}]
    assert tmpdb.recompte_generats("errades") == {"t2-4c": {"normal": 1, "facil": 1}}


def test_api_turn_is_persisted_logged_and_survives_a_restart(monkeypatch):
    """End to end through FastAPI: session row, turn row, one log row per model call, rehydration from the DB."""
    from fastapi.testclient import TestClient

    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    import app as app_module
    from test_harness import TEORIA, ScriptedLLM, _diag_json
    from tutor.pipeline import Tutor

    ok = {"veredicte": "ok", "infraccions": [], "explicacio": ""}
    llm = ScriptedLLM({"diagnosi": [_diag_json(), _diag_json()], "resposta": [{"text": "Què has provat?"}] * 2,
                       "guardia": [ok, ok]})
    monkeypatch.setattr(app_module, "_tutor", Tutor(db.LoggingLLM(llm), TEORIA))
    client = TestClient(app_module.app)
    sid = client.post("/api/sessions", json={"exercici_id": "t2-4c"}).json()["session_id"]
    assert client.post(f"/api/sessions/{sid}/missatges", json={"text": "no sé per on començar"}).status_code == 200

    [torn] = db.torns_de(sid)
    assert torn["alumne"] == "no sé per on començar" and torn["tutor"] == "Què has provat?" and torn["accio"]
    assert {c["stage"] for c in db.crides_de(sid)} == {"diagnosi", "resposta", "guardia"}
    assert db.carrega_sessio(sid)["estat"]["torns"] == 1

    app_module.SESSIONS.clear()  # restart / eviction: the session is rebuilt from the database
    assert client.post(f"/api/sessions/{sid}/missatges", json={"text": "he provat rectes"}).status_code == 200
    assert [t["n"] for t in db.torns_de(sid)] == [1, 2]
    assert len(app_module.SESSIONS[sid].historial) == 4
