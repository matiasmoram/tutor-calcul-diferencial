import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_harness import EX, ScriptedLLM  # noqa: E402
from tutor import errades  # noqa: E402
from tutor.errades import Anotacio, compare_verification, locate, validate_generation  # noqa: E402
from tutor.llm import LLMError  # noqa: E402

FRAGS = [
    "Provem camins: amb $y=kx$ el quocient tendeix a $0$.",
    "Com que $x^4 \\ge x^4+y^2$, el quocient està fitat per $|x|$.",
    "Això demostra que el límit existeix.",
    "Pel criteri del sandvitx, $|f|\\le |x|\\to 0$.",
    "Per tant el límit és $0$.",
]


def gen(errors, frags=FRAGS):
    return {"fragments": frags, "errors": errors}


def err(fragment, cita):
    return {"fragment": fragment, "cita": cita, "tipus": "desigualtat", "explicacio": "x", "correccio": "y", "pista": "z"}


def test_locate_tolerates_whitespace_only():
    assert locate("a  b   c", "a b c") == (0, 8)
    assert locate("abc", "abd") is None


def test_validation_accepts_well_formed_generation():
    frags, errs, problems = validate_generation(gen([err(2, "$x^4 \\ge x^4+y^2$"), err(3, "demostra que el límit existeix")]), 2)
    assert problems == []
    assert errs[0].cita == "$x^4 \\ge x^4+y^2$" and frags[1][errs[0].inici : errs[0].fi] == errs[0].cita


@pytest.mark.parametrize(
    "errors,n,expected",
    [
        ([err(2, "$x^4 \\ge x^4+y^2$")], 2, "exactament 2 errors"),
        ([err(2, "$x^4 \\ge x^4+y^2$"), err(2, "fitat")], 2, "dos errors al fragment 2"),
        ([err(9, "x")], 1, "fragment inexistent"),
        ([err(1, "text que no hi és")], 1, "no apareix literalment"),
    ],
)
def test_validation_rejects(errors, n, expected):
    _, _, problems = validate_generation(gen(errors), n)
    assert any(expected in p for p in problems), problems


def test_validation_rejects_unbalanced_math():
    frags = FRAGS[:4] + ["Per tant el límit és $0."]
    _, _, problems = validate_generation(gen([err(2, "fitat")], frags), 1)
    assert any("senar" in p for p in problems)


def test_verification_must_find_all_declared_and_nothing_else():
    _, errs, _ = validate_generation(gen([err(2, "$x^4 \\ge x^4+y^2$")]), 1)
    ok = [{"fragment": 2, "cita": "x", "gravetat": "error", "explicacio": ""},
          {"fragment": 5, "cita": "y", "gravetat": "consequencia", "explicacio": ""},
          {"fragment": 1, "cita": "z", "gravetat": "imprecisio", "explicacio": ""}]
    assert compare_verification(errs, ok) == []
    missing = compare_verification(errs, [])
    assert "no l'ha detectat" in missing[0]
    extra = compare_verification(errs, ok + [{"fragment": 3, "cita": "demostra", "gravetat": "error", "explicacio": "salt"}])
    assert "NO intencionat" in extra[0]


def test_generate_regenerates_until_verified(tmp_path):
    bad_quote = gen([err(2, "no hi és")])
    good = gen([err(2, "$x^4 \\ge x^4+y^2$")])
    llm = ScriptedLLM({
        "errades_generacio": [bad_quote, good, good],
        "errades_verificacio": [
            {"problemes": [{"fragment": 3, "cita": "demostra", "gravetat": "error", "explicacio": "salt"},
                           {"fragment": 2, "cita": "x", "gravetat": "error", "explicacio": ""}], "valoracio": ""},
            {"problemes": [{"fragment": 2, "cita": "x", "gravetat": "error", "explicacio": ""}], "valoracio": "ok"},
        ],
    })
    sol, log = errades.generate(llm, errades.FontProblema(EX["t2-4c"]), "facil")
    assert len(log) == 3 and log[0]["validacio"] and log[1]["discrepancies"] and not log[2]["discrepancies"]
    # Feedback from the failed attempts reaches the generator.
    gen_prompts = [u for stage, u in llm.seen if stage == "errades_generacio"]
    assert "no apareix literalment" in gen_prompts[1] and "NO intencionat" in gen_prompts[2]
    # The verifier never sees the declared errors.
    ver_prompt = next(u for stage, u in llm.seen if stage == "errades_verificacio")
    assert "correccio" not in ver_prompt and "pista" not in ver_prompt and "no hi és" not in ver_prompt
    # The solution sheet travels as the cacheable context, identical for generation and verification.
    ctxs = {c for stage, c in llm.contexts}
    assert len(ctxs) == 1 and "RESULTAT CORRECTE" in next(iter(ctxs))
    assert sol.public()["n_errors"] == 1 and "errors" not in sol.public()

    errades.save(sol, tmp_path)
    assert errades.cached("t2-4c", "facil", tmp_path)[0].id == sol.id


def test_generate_gives_up_after_max_attempts():
    llm = ScriptedLLM({"errades_generacio": [gen([])] * 3})
    with pytest.raises(LLMError):
        errades.generate(llm, errades.FontProblema(EX["t2-4c"]), "normal")


def _solution():
    frags, errs, _ = validate_generation(gen([err(2, "$x^4 \\ge x^4+y^2$"), err(3, "demostra que el límit existeix")]), 2)
    return errades.SolucioAmbErrors(id="s", exercici="t2-4c", dificultat="normal", fragments=frags, errors=errs)


def test_grading_scores_in_code_and_enforces_candidates():
    sol = _solution()
    e1 = sol.errors[0]
    anots = [
        Anotacio(id="a1", fragment=2, inici=e1.inici, fi=e1.fi, comentari="la desigualtat va al revés"),
        Anotacio(id="a2", fragment=3, inici=0, fi=4, comentari="no se segueix"),  # right fragment, off the quote
        Anotacio(id="a3", fragment=1, inici=0, fi=10, comentari="crec que està malament"),
    ]
    llm = ScriptedLLM({"errades_correccio": [{
        "avaluacions": [
            {"anotacio": "a1", "error": "e1", "explicacio": "correcta", "feedback": "Molt bé."},
            {"anotacio": "a2", "error": "e2", "explicacio": "parcial", "feedback": "Gairebé."},
            # The LLM tries to credit a1's error to an annotation in another fragment: code must refuse.
            {"anotacio": "a3", "error": "e1", "explicacio": "correcta", "feedback": "?"},
        ],
        "resum": "Bé.",
    }]})
    r = errades.grade(llm, errades.FontProblema(EX["t2-4c"]), sol, anots)
    by = {a["id"]: a for a in r["anotacions"]}
    assert by["a1"]["localitzacio"] == "exacta" and by["a1"]["punts"] == 1.0
    assert by["a2"]["localitzacio"] == "aproximada" and by["a2"]["punts"] == pytest.approx(0.6 * 0.8)
    assert by["a3"]["error"] == "cap"
    assert r["trobats"] == 2 and r["falsos_positius"] == 1
    assert r["nota"] == round(100 * ((1.0 + 0.48) / 2 - 0.1))


def test_grading_without_annotations_skips_llm():
    r = errades.grade(ScriptedLLM({}), errades.FontProblema(EX["t2-4c"]), _solution(), [])
    assert r["nota"] == 0 and r["trobats"] == 0 and len(r["errors"]) == 2


# ---------- theory activity ----------

TFRAGS = [
    r"Sigui $f:U\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciable en un obert $U$.",
    r"Aleshores $f$ és de classe $\mathcal{C}^1$ a $U$.",
    r"Prenem $a\in U$ i una direcció $v$.",
    "Per la definició de diferencial, $D_vf(a)=Df(a)v$.",
    "Com que $v$ és arbitrari, les parcials són contínues.",
]


def tgen(errors, n_enunciat=2, frags=TFRAGS):
    return {"n_enunciat": n_enunciat, "fragments": frags, "errors": errors}


def terr(fragment, cita, tipus="hipotesi"):
    return {"fragment": fragment, "cita": cita, "tipus": tipus, "explicacio": "x", "correccio": "y", "pista": "z"}


def test_theory_items_are_results_with_proof():
    items = errades.items_teoria()
    assert items and all(it.tipus in errades.TIPUS_TEORIA and it.demostracio.strip() and it.num for it in items)
    ids = {it.id for it in items}
    assert "T3.21" in ids  # Regla de la cadena
    assert not any(errades._teoria()[i].tipus == "definicio" for i in ids)


def test_theory_validation_requires_statement_error_and_split():
    ok = tgen([terr(2, r"de classe $\mathcal{C}^1$", "conclusio"), terr(5, "les parcials són contínues", "pas_injustificat")])
    _, errs, problems = validate_generation(ok, 2, teoria=True)
    assert problems == [] and len(errs) == 2
    # Both errors in the proof: the statement must carry one.
    _, _, p = validate_generation(tgen([terr(4, "Per la definició", "pas_injustificat"), terr(5, "són contínues", "pas_injustificat")]), 2, teoria=True)
    assert any("enunciat" in x for x in p)
    # Two errors, both in the statement: one must be in the proof.
    _, _, p = validate_generation(tgen([terr(1, "diferenciable"), terr(2, "de classe", "conclusio")]), 2, teoria=True)
    assert any("demostració" in x for x in p)
    # n_enunciat must leave a proof.
    _, _, p = validate_generation(tgen([terr(1, "diferenciable")], n_enunciat=4), 1, teoria=True)
    assert any("n_enunciat" in x for x in p)
    # Problem error types are not valid for theory documents and vice versa.
    _, _, p = validate_generation(tgen([terr(1, "diferenciable", "teorema_mal_aplicat")]), 1, teoria=True)
    assert any("tipus no vàlid" in x for x in p)


def test_display_math_is_rejected():
    frags = FRAGS[:4] + ["Per tant el límit és $$0$$."]
    _, _, problems = validate_generation(gen([err(2, "fitat")], frags), 1)
    assert any("$$" in p for p in problems)


def test_theory_generation_uses_notes_as_reference_and_never_shows_errors_to_verifier():
    item = errades._teoria()["T3.21"]
    font = errades.FontTeoria(item)
    good = tgen([terr(1, "diferenciable"), terr(5, "les parcials són contínues", "pas_injustificat")])
    llm = ScriptedLLM({
        "errades_generacio": [good],
        "errades_verificacio": [{"problemes": [
            {"fragment": 1, "cita": "diferenciable", "gravetat": "error", "explicacio": ""},
            {"fragment": 5, "cita": "contínues", "gravetat": "error", "explicacio": ""},
            {"fragment": 3, "cita": "Prenem", "gravetat": "imprecisio", "explicacio": ""}], "valoracio": "ok"}],
    })
    sol, _ = errades.generate(llm, font, "normal")
    assert sol.font == "teoria" and sol.exercici == "T3.21" and sol.n_enunciat == 2
    assert sol.public()["n_enunciat"] == 2 and "errors" not in sol.public()
    ctx = llm.contexts[0][1]
    assert "versió CORRECTA" in ctx and item.demostracio.strip()[:40] in ctx
    ver = next(u for stage, u in llm.seen if stage == "errades_verificacio")
    assert "(enunciat)" in ver and "(demostració)" in ver and "pista" not in ver
    # The generator's schema asks for the statement split.
    assert "n_enunciat" in errades.generacio_schema(True)["required"]


def test_disponibles_and_avoid_repeating(tmp_path):
    font = errades.FontProblema(EX["t2-4c"])
    a, b = _solution(), _solution()
    a.id, b.id = "aaa", "bbb"
    errades.save(a, tmp_path)
    errades.save(b, tmp_path)
    assert errades.disponibles(tmp_path) == {"t2-4c": {"normal": 2}}
    for _ in range(10):
        sol, fresh = errades.get_or_generate(ScriptedLLM({}), font, "normal", False, tmp_path, excepte="aaa")
        assert sol.id == "bbb" and not fresh


def test_grading_tolerates_malformed_llm_evaluation():
    sol = _solution()
    e1 = sol.errors[0]
    llm = ScriptedLLM({"errades_correccio": [{"avaluacions": [{"anotacio": "a1", "error": "e1", "explicacio": "genial"}], "resum": ""}]})
    r = errades.grade(llm, errades.FontProblema(EX["t2-4c"]), sol, [Anotacio(id="a1", fragment=2, inici=e1.inici, fi=e1.fi)])
    assert r["anotacions"][0]["explicacio"] == "absent" and r["trobats"] == 1
