import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_harness import TEORIA, ScriptedLLM  # noqa: E402
from tutor import afirmacions as af  # noqa: E402
from tutor import comprovacions as cas  # noqa: E402
from tutor.llm import LLMError  # noqa: E402

FONT = af.Font(2)
REFS = set(FONT.refs_permeses())


def check(tipus, expressio, valor="", variable="x", punt="0"):
    return {"descripcio": "c", "tipus": tipus, "expressio": expressio, "variable": variable, "punt": punt,
            "costat": "ambdos", "valor": valor}


def item(enunciat, veredicte="fals", comprovacions=(), **kw):
    return {
        "enunciat": enunciat,
        "veredicte": veredicte,
        "trampa": "reciproc" if veredicte == "fals" else "cert_resultat",
        "concepte": "Límits iterats",
        "contraexemple": "$f(x,y)=\\frac{xy}{x^2+y^2}$" if veredicte == "fals" else "",
        "resolucio": "Resolució completa.",
        "idees_clau": ["idea"],
        "pista": "Què et diuen els iterats sobre la resta de camins?",
        "teoria": ["T2.12"],
        "comprovacions": list(comprovacions),
    } | kw


ITERATS = check("limit", "x*(m*x)/(x**2+(m*x)**2)", "m/(1+m**2)")


# ---------- sympy checks ----------


@pytest.mark.parametrize(
    "c,estat",
    [
        (ITERATS, "ok"),
        (check("limit", "x*(m*x)/(x**2+(m*x)**2)", "0"), "falla"),
        (check("no_limit", "sin(1/y)", variable="y"), "ok"),
        (check("no_limit", "y*sin(1/y)", variable="y"), "falla"),
        (check("no_limit", "Abs(x)/x"), "ok"),
        (check("igualtat", "diff(x**2*y, x)", "2*x*y", variable="", punt=""), "ok"),
        (check("igualtat", "sqrt(x**2)", "x", variable="", punt=""), "falla"),
        (check("limit", "x^2*(x^2)/(x^4+(x^2)^2)", "1/2"), "ok"),
    ],
)
def test_sympy_checks(c, estat):
    assert cas.avalua_una(c)["estat"] == estat


@pytest.mark.parametrize("expr", ["__import__('os').system('x')", "x.__class__", "open(x)", "lambda: 1", "x; y", "eval(x)"])
def test_checks_never_eval_untrusted_python(expr):
    r = cas.avalua_una(check("limit", expr, "0"))
    assert r["estat"] == "indeterminat" and r["detall"]


def test_checks_in_worker_processes():
    out = cas.avalua([ITERATS, check("no_limit", "sin(1/x)")])
    assert [r["estat"] for r in out] == ["ok", "ok"]


# ---------- validation ----------


def test_valid_item_passes():
    assert af.validate_item(item("Afirmació $a$."), REFS) == []


@pytest.mark.parametrize(
    "changes,expected",
    [
        ({"contraexemple": ""}, "contraexemple"),
        ({"pista": "Busca un contraexemple."}, "pista revela"),
        ({"pista": "És falsa?"}, "pista revela"),
        ({"enunciat": "Si $f és contínua"}, "LaTeX"),
        ({"enunciat": "$$f$$"}, "LaTeX"),
        ({"teoria": ["T9.99"]}, "inexistents"),
        ({"idees_clau": []}, "idees clau"),
    ],
)
def test_item_validation_rejects(changes, expected):
    problems = af.validate_item(item("A.") | changes, REFS)
    assert any(expected in p for p in problems), problems


def test_failing_sympy_check_rejects_statement():
    items = [item("A.", comprovacions=[ITERATS]), item("B.", comprovacions=[check("limit", "x*(m*x)/(x**2+(m*x)**2)", "0")])]
    checked = af.run_checks(items, en_proces=True)
    assert af.check_problems(checked[0]) == []
    assert any("FALSA segons sympy" in p and "m/(m**2 + 1)" in p for p in af.check_problems(checked[1]))


def test_judge_needs_blind_agreement_and_clean_audit():
    items = [item("A."), item("B.", "cert"), item("C."), item("D.")]
    sol = [
        {"num": 1, "veredicte": "fals", "confianca": "alta", "ben_plantejada": True, "justificacio": ""},
        {"num": 2, "veredicte": "fals", "confianca": "alta", "ben_plantejada": True, "justificacio": "contraexemple"},
        {"num": 3, "veredicte": "fals", "confianca": "baixa", "ben_plantejada": True, "justificacio": ""},
        {"num": 4, "veredicte": "fals", "confianca": "alta", "ben_plantejada": True, "justificacio": ""},
    ]
    ok = {"resolucio_correcta": True, "teoria_correcta": True, "pista_neutra": True, "problemes": ""}
    aud = [ok | {"num": 1}, ok | {"num": 2}, ok | {"num": 3}, ok | {"num": 4, "resolucio_correcta": False, "problemes": "no compleix H"}]
    verdicts = af.judge(items, sol, aud)
    assert verdicts[0] == []
    assert "diu que és fals, no cert" in verdicts[1][0]
    assert "no n'està segur" in verdicts[2][0]
    assert "no compleix H" in verdicts[3][0]


def test_balance_range():
    assert af.rang_falses(6) == (3, 4) and af.rang_falses(10) == (5, 8)


# ---------- generation pipeline ----------


def ok_solver(n, verdicts):
    return {"respostes": [{"num": i, "veredicte": v, "confianca": "alta", "ben_plantejada": True, "justificacio": "j"}
                          for i, v in zip(range(1, n + 1), verdicts)]}


def ok_audit(n):
    return {"revisions": [{"num": i, "resolucio_correcta": True, "teoria_correcta": True, "pista_neutra": True, "problemes": ""}
                          for i in range(1, n + 1)]}


def test_generation_replaces_only_rejected_statements():
    bad_check = check("limit", "x*(m*x)/(x**2+(m*x)**2)", "0")
    round1 = [
        item("F1 $a$.", comprovacions=[ITERATS]),
        item("F2."),
        item("F3.", comprovacions=[bad_check]),  # rejected by sympy
        item("C1.", "cert"),
        item("C2.", "cert"),  # rejected: the blind solver disagrees
    ]
    round2 = [item("F4."), item("C3.", "cert"), item("C4.", "cert")]
    llm = ScriptedLLM({
        "afirmacions_generacio": [{"afirmacions": round1}, {"afirmacions": round2}],
        # Round 1 candidates after sympy: F1, F2, C1, C2.
        "afirmacions_verificacio": [ok_solver(4, ["fals", "fals", "cert", "fals"]), ok_solver(3, ["fals", "cert", "cert"])],
        "afirmacions_auditoria": [ok_audit(4), ok_audit(3)],
    })
    q, log = af.generate(llm, FONT, "facil", en_proces=True)
    assert len(q.afirmacions) == 6 and [a.id for a in q.afirmacions] == [f"a{i}" for i in range(1, 7)]
    assert sorted(a.enunciat for a in q.afirmacions) == sorted(["F1 $a$.", "F2.", "C1.", "F4.", "C3.", "C4."])
    assert len(log) == 2 and log[0]["demanades"] == 5 and log[1]["demanades"] == 3
    f1 = next(a for a in q.afirmacions if a.enunciat.startswith("F1"))
    assert f1.cas_ok == 1 and f1.comprovacions[0].calculat == "m/(m**2 + 1)"
    # The second request carries the reasons and the statements already kept.
    req2 = [u for stage, u in llm.seen if stage == "afirmacions_generacio"][1]
    assert "FALSA segons sympy" in req2 and "diu que és fals, no cert" in req2 and "F1 $a$." in req2
    # The blind solver never sees verdicts or solutions; the audit does.
    blind = [u for stage, u in llm.seen if stage == "afirmacions_verificacio"][0]
    assert "veredicte" not in blind and "Resolució" not in blind
    assert "veredicte declarat: fals" in [u for stage, u in llm.seen if stage == "afirmacions_auditoria"][0]
    # The whole tema's notes are the cached context of every call.
    assert all("<apunts tema=\"2\"" in c for _, c in llm.contexts)
    public = q.public()
    assert set(public["afirmacions"][0]) == {"id", "enunciat", "concepte"}


def test_generation_gives_up_after_too_many_rounds():
    bad = {"afirmacions": [item(f"X{i}.", contraexemple="") for i in range(5)]}
    llm = ScriptedLLM({"afirmacions_generacio": [bad] * 10})
    with pytest.raises(LLMError):
        af.generate(llm, FONT, "facil", en_proces=True)


# ---------- grading ----------


def quiz():
    afs = [
        af.Afirmacio(id="a1", enunciat="A.", veredicte="fals", concepte="c", trampa="reciproc", contraexemple="xy",
                     resolucio="r", idees_clau=["i"], pista="p"),
        af.Afirmacio(id="a2", enunciat="B.", veredicte="cert", concepte="c", trampa="cert_resultat", resolucio="r",
                     idees_clau=["i"], pista="p"),
        af.Afirmacio(id="a3", enunciat="C.", veredicte="fals", concepte="c", trampa="reciproc", contraexemple="z",
                     resolucio="r", idees_clau=["i"], pista="p"),
        af.Afirmacio(id="a4", enunciat="D.", veredicte="cert", concepte="c", trampa="cert_resultat", resolucio="r",
                     idees_clau=["i"], pista="p"),
    ]
    return af.Questionari(id="q", font="tema-2", tema=2, dificultat="facil", afirmacions=afs)


def test_grading_is_decided_by_code_and_sympy():
    llm = ScriptedLLM({"afirmacions_correccio": [{
        "avaluacions": [
            # Right verdict, "correcta", but the student's claimed limit is false: downgraded to parcial.
            {"id": "a1", "justificacio": "correcta", "feedback": "f1",
             "comprovacions": [check("limit", "x*(m*x)/(x**2+(m*x)**2)", "0")]},
            # Wrong verdict: whatever the LLM says, no points.
            {"id": "a2", "justificacio": "correcta", "feedback": "f2", "comprovacions": []},
            {"id": "a3", "justificacio": "correcta", "feedback": "f3", "comprovacions": [ITERATS]},
        ],
        "resum": "r",
    }]})
    respostes = [
        af.Resposta(id="a1", veredicte="fals", justificacio="sobre y=mx dona 0"),
        af.Resposta(id="a2", veredicte="fals", justificacio="no"),
        af.Resposta(id="a3", veredicte="fals", justificacio="bé"),
        af.Resposta(id="a4", veredicte="", justificacio=""),
    ]
    r = af.grade(llm, FONT, quiz(), respostes, pistes={"a3"}, en_proces=True)
    it = {i["id"]: i for i in r["afirmacions"]}
    assert it["a1"]["justificacio"] == "parcial" and it["a1"]["nota_cas"] and it["a1"]["punts"] == 0.65
    assert it["a2"]["justificacio"] == "incorrecta" and it["a2"]["punts"] == 0 and not it["a2"]["encert"]
    assert it["a3"]["justificacio"] == "correcta" and it["a3"]["punts"] == 0.85  # hint used
    assert it["a4"]["punts"] == 0 and it["a4"]["resposta"] == ""
    assert r["nota"] == round(100 * (0.65 + 0 + 0.85 + 0) / 4) and r["encerts"] == 2
    # Unanswered statements are not sent to the grader.
    assert "[a4]" not in llm.seen[0][1]


def test_grading_without_answers_makes_no_call():
    r = af.grade(ScriptedLLM({}), FONT, quiz(), [], set(), en_proces=True)
    assert r["nota"] == 0 and r["crida"] is None


# ---------- API ----------


def test_api_never_leaks_verdicts_before_correction(monkeypatch, tmp_path):
    from fastapi.testclient import TestClient

    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    import app as app_module

    monkeypatch.setattr(af, "CACHE_DIR", tmp_path)
    af.save(quiz(), tmp_path)
    monkeypatch.setattr(af.get_or_generate, "__defaults__", (tmp_path, None))
    client = TestClient(app_module.app)
    fonts = client.get("/api/afirmacions/fonts").json()
    assert {t["id"] for t in fonts["temes"]} >= {"tema-1", "tema-2"}
    assert any(i["id"] == "T2.12" for t in fonts["temes"] for i in t["items"])
    s = client.post("/api/afirmacions/sessions", json={"font": "tema-2", "dificultat": "facil"}).json()
    assert "veredicte" not in str(s) and "resolucio" not in str(s) and "pista" not in str(s)
    pista = client.post(f"/api/afirmacions/sessions/{s['session_id']}/pista/a1").json()
    assert pista["pista"] == "p"
    assert client.post("/api/afirmacions/sessions", json={"font": "tema-9"}).status_code == 404
    # No answers: graded by code alone, the hint is recorded.
    r = client.post(f"/api/afirmacions/sessions/{s['session_id']}/correccio", json={"respostes": []}).json()
    assert r["nota"] == 0 and r["afirmacions"][0]["pista_usada"]


def test_focus_sources():
    f = af.font_de("T2.12")
    assert f.tema == 2 and f.id == "T2.12" and "<resultat_focus>" in f.context()
    assert af.font_de("tema-3").focus is None
    with pytest.raises(KeyError):
        af.font_de("T9.1")
    assert all(i in TEORIA for i in FONT.refs_permeses())
