import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from tutor.fitxes import load_exercicis, load_llistes  # noqa: E402
from tutor.guardia import deterministic_check  # noqa: E402
from tutor.llm import CallMeta  # noqa: E402
from tutor.pipeline import Sessio, Tutor  # noqa: E402
from tutor.politica import EstatSessio, allowed_content, decide  # noqa: E402
from tutor.schemas import Diagnosi, diagnosi_schema  # noqa: E402
from tutor.teoria import load_teoria, parse_ref  # noqa: E402

TEORIA = load_teoria()
LLISTES, EX = load_llistes(teoria=TEORIA)


def diag(ex_id="t2-4c", passos=None, **kw):
    ex = EX[ex_id]
    passos = passos or {}
    base = dict(
        evidencia="",
        resum_alumne="",
        estat_passos=[{"pas": s, "estat": passos.get(s, "no_iniciat")} for s in ex.step_ids],
        pas_actual=ex.step_ids[0],
        errors_detectats=[],
        error_altre="",
        resultat_proposat="cap",
        resultat_justificat=False,
        nivell_desorientacio="encallat",
        intencio="mostra_treball",
    )
    base.update(kw)
    return Diagnosi.model_validate(base)


# ---------- sheets ----------

def test_all_sheets_load_and_cite_existing_theory():
    assert {f"t2-4{c}" for c in "abcdefg"} <= set(EX)
    for ex in EX.values():
        assert ex.all_refs(), ex.id
        assert all(parse_ref(r)[0] in TEORIA for r in ex.all_refs()), ex.id


def test_every_sheet_passes_the_authoring_checks():
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
    from check_fitxes import problems_of

    bad = {ex.id: problems_of(ex, TEORIA) for ex in EX.values()}
    assert not {k: v for k, v in bad.items() if v}


@pytest.mark.parametrize("ex_id", sorted(EX))
def test_step_leak_regexes_match_their_own_detail(ex_id):
    """At least one leak regex per step must catch the step's own detail (others cover alternate notations)."""
    for pas in EX[ex_id].passos:
        if pas.fuites:
            assert any(re.search(p, pas.detall, re.IGNORECASE) for p in pas.fuites), (ex_id, pas.id, pas.fuites)


@pytest.mark.parametrize("ex_id", sorted(EX))
def test_hint_texts_do_not_contain_their_own_banned_content(ex_id):
    """Objective (level 1) and idea (level 2) are shown below level 3, where the step's leak regexes apply."""
    for pas in EX[ex_id].passos:
        for pattern in pas.fuites:
            for text in (pas.objectiu, pas.idea):
                assert not re.search(pattern, text, re.IGNORECASE), (ex_id, pas.id, pattern)


@pytest.mark.parametrize("ex_id", sorted(EX))
def test_hint_texts_do_not_reveal_the_final_result(ex_id):
    ex = EX[ex_id]
    for pas in ex.passos:
        for pattern in ex.resultat.fuites:
            for text in (pas.objectiu, pas.idea):
                assert not re.search(pattern, text, re.IGNORECASE), (ex_id, pas.id, pattern)


def test_lists_group_their_exercises_by_problem():
    assert set(LLISTES) <= {f"tema-{n}" for n in range(1, 7)} and "tema-2" in LLISTES
    assert all(EX[e].llista == lid for lid, l in LLISTES.items() for e in l.exercicis)
    p4 = next(p for p in LLISTES["tema-2"].problemes if p.num == 4)
    assert p4.exercicis == [f"t2-4{c}" for c in "abcdefg"]
    ex = EX["t2-4c"]
    assert ex.problema == 4 and ex.apartat == "c" and ex.etiqueta == "4(c)"
    assert ex.enunciat_md().startswith(ex.preambul.strip()) and "(c)" in ex.enunciat_md()


def test_diagnosi_schema_uses_closed_enums():
    schema = diagnosi_schema(EX["t2-4c"])
    assert schema["properties"]["pas_actual"]["enum"] == EX["t2-4c"].step_ids + ["cap"]
    assert "altre" in schema["properties"]["errors_detectats"]["items"]["enum"]


# ---------- policy ----------

def test_paths_as_proof_triggers_socratic_error_question():
    d = diag(passos={"candidat": "completat"}, errors_detectats=["camins_com_a_prova"],
             resultat_proposat="correcte", nivell_desorientacio="en_cami", intencio="proposa_resultat")
    pla, st = decide(EX["t2-4c"], d, EstatSessio(), ["Per camins dona 0, per tant el límit és 0"])
    assert pla.accio == "questionar_error"
    assert pla.error_objectiu == "camins_com_a_prova"
    assert pla.pas_objectiu == "acotar"
    # The reply may repeat the student's own words ("el límit és 0"), but not reveal the bound.
    assert not any("mit" in r for r in pla.regex_prohibides)
    assert any("|x|" in r or "\\|x\\|" in r for r in pla.regex_prohibides)
    # Without those words the result stays protected: the tutor has not confirmed it.
    pla, _ = decide(EX["t2-4c"], d, EstatSessio())
    assert any("mit" in r for r in pla.regex_prohibides)


def test_hint_level_escalates_and_caps_then_shows_step():
    ex = EX["t2-4c"]
    st = EstatSessio()
    levels = []
    for _ in range(3):  # a student who keeps trying (and stays stuck) climbs one level per turn
        pla, st = decide(ex, diag(intencio="mostra_treball", nivell_desorientacio="encallat"), st)
        levels.append(pla.nivell_pista)
    assert levels == [2, 3, 3]
    pla, st = decide(ex, diag(intencio="demana_solucio"), st)
    assert pla.accio == "mostrar_pas" and pla.nivell_pista == 4 and pla.pas_objectiu == "candidat"


def test_asking_for_solution_early_only_raises_hint_level():
    pla, _ = decide(EX["t2-4c"], diag(intencio="demana_solucio", nivell_desorientacio="perdut"), EstatSessio())
    assert pla.accio == "pista" and pla.nivell_pista == 2
    assert not pla.pot_dir_resultat


def test_completed_steps_are_monotonic_unless_marked_wrong():
    ex = EX["t2-4c"]
    _, st = decide(ex, diag(passos={"candidat": "completat"}, nivell_desorientacio="en_cami"), EstatSessio())
    assert st.completats == ["candidat"]
    _, st = decide(ex, diag(nivell_desorientacio="en_cami"), st)
    assert st.completats == ["candidat"]
    _, st = decide(ex, diag(passos={"candidat": "erroni"}), st)
    assert st.completats == []


def test_progress_validates_and_moves_on():
    pla, _ = decide(EX["t2-4c"], diag(passos={"candidat": "completat"}, nivell_desorientacio="en_cami"), EstatSessio())
    assert pla.accio == "validar_i_avancar" and pla.pas_objectiu == "acotar" and pla.nivell_pista == 1


def test_close_only_when_correct_and_justified():
    ex = EX["t2-4c"]
    pla, st = decide(ex, diag(resultat_proposat="correcte", resultat_justificat=True, intencio="proposa_resultat",
                              nivell_desorientacio="en_cami"), EstatSessio())
    assert pla.accio == "tancar" and pla.pot_dir_resultat and st.tancat


def test_wrong_result_after_work_is_questioned_without_revealing():
    d = diag(passos={"candidat": "completat"}, resultat_proposat="incorrecte", intencio="proposa_resultat")
    pla, _ = decide(EX["t2-4c"], d, EstatSessio())
    assert pla.accio == "questionar_resultat"
    content = allowed_content(EX["t2-4c"], pla, ["candidat"])
    assert "RESULTAT" not in content


def test_bare_guesses_are_neither_confirmed_nor_denied():
    """No oracle: "és 1?" then "és 0?" must get the same neutral treatment."""
    ex = EX["t2-4c"]
    for verdict in ("incorrecte", "correcte"):
        pla, st = decide(ex, diag(resultat_proposat=verdict, intencio="proposa_resultat"), EstatSessio())
        assert pla.accio == "demanar_raonament"
        assert not pla.pot_dir_resultat and not pla.resultat_dit_per_alumne and not st.resultat_confirmat
        assert any(re.search(r, "el límit és 0", re.IGNORECASE) for r in pla.regex_prohibides)


def test_allowed_content_hides_later_steps_and_unearned_detail():
    ex = EX["t2-4c"]
    pla, st = decide(ex, diag(passos={"candidat": "completat"}, nivell_desorientacio="en_cami"), EstatSessio())
    content = allowed_content(ex, pla, st.completats)
    assert ex.pas("acotar").objectiu in content
    assert ex.pas("acotar").idea not in content  # level 1: objective only
    assert ex.pas("acotar").detall not in content
    assert ex.pas("concloure").idea not in content


# ---------- deterministic guard ----------

def test_guard_catches_leaked_bound_and_missing_question():
    pla, _ = decide(EX["t2-4c"], diag(passos={"candidat": "completat"}, nivell_desorientacio="en_cami"), EstatSessio())
    problems = deterministic_check(r"Fixa't que $\frac{|x|^5}{x^4+y^2} \le |x|$.", pla)
    assert any("prohibit" in p for p in problems)
    assert any("pregunta" in p for p in problems)
    assert deterministic_check("Molt bé. Què passa si comparaaes el denominador amb un dels seus termes?", pla) == []


# ---------- pipeline with a scripted LLM ----------

class ScriptedLLM:
    def __init__(self, script):
        self.script = {k: list(v) for k, v in script.items()}
        self.seen = []
        self.contexts = []
        self.images = []

    def structured(self, stage, system, user, schema, image=None, context=None):
        self.seen.append((stage, user))
        self.contexts.append((stage, context))
        self.images.append(image)
        return self.script[stage].pop(0), CallMeta(stage=stage, model="fake", latency_ms=1)


def _diag_json(**kw):
    return diag(**kw).model_dump()


def test_pipeline_retries_after_rejection_and_redactor_never_sees_solution():
    ok = {"veredicte": "ok", "infraccions": [], "explicacio": ""}
    llm = ScriptedLLM({
        "diagnosi": [_diag_json(passos={"candidat": "completat"}, nivell_desorientacio="en_cami")],
        "resposta": [
            {"text": r"El límit és 0 perquè $\le |x|$. Ho veus?"},  # leaks, rejected by regex
            {"text": "Bona feina amb els camins. Com podries fitar el quocient per una cosa que tendeixi a 0?"},
        ],
        "guardia": [ok],
    })
    s = Sessio(exercici=EX["t2-4c"])
    out = Tutor(llm, TEORIA).turn(s, "He provat y=kx i y=kx^2 i dona 0")
    assert out["missatge"].startswith("Bona feina")
    assert len(out["trace"]["intents"]) == 2 and out["trace"]["intents"][0]["determinista"]
    assert not out["trace"]["fallback"]
    redactor_inputs = [u for stage, u in llm.seen if stage == "resposta"]
    for u in redactor_inputs:
        assert EX["t2-4c"].pas("acotar").detall not in u
        assert "RESULTAT CORRECTE" not in u
    assert "REBUTJAT" in redactor_inputs[1]
    assert [m["rol"] for m in s.historial] == ["alumne", "tutor"]


def test_pipeline_falls_back_when_every_draft_is_rejected():
    bad = {"veredicte": "rebutjat", "infraccions": ["revela_pas_futur"], "explicacio": "avança la fita"}
    llm = ScriptedLLM({
        "diagnosi": [_diag_json(errors_detectats=["camins_com_a_prova"])],
        "resposta": [{"text": "Pensa-hi, d'acord?"}] * 3,
        "guardia": [bad] * 3,
    })
    out = Tutor(llm, TEORIA).turn(Sessio(exercici=EX["t2-4c"]), "dona 0 per tots els camins, per tant és 0")
    assert out["trace"]["fallback"]
    assert out["missatge"] == EX["t2-4c"].error("camins_com_a_prova").pregunta


def test_guard_verdict_inconsistency_is_fail_closed():
    llm = ScriptedLLM({
        "diagnosi": [_diag_json()],
        "resposta": [{"text": "Què has provat?"}] * 3,
        "guardia": [{"veredicte": "ok", "infraccions": ["revela_resultat"], "explicacio": ""}] * 3,
    })
    out = Tutor(llm, TEORIA).turn(Sessio(exercici=EX["t2-4c"]), "no sé què fer")
    assert out["trace"]["fallback"]


def test_failed_diagnosis_does_not_record_the_turn():
    class Boom:
        def structured(self, *a, **kw):
            raise RuntimeError("api down")

    s = Sessio(exercici=EX["t2-4c"])
    with pytest.raises(RuntimeError):
        Tutor(Boom(), TEORIA).turn(s, "hola")
    assert s.historial == [] and s.estat.torns == 0


# ---------- photo transcription ----------

from tutor.llm import Imatge  # noqa: E402
from tutor.transcripcio import ImatgeInvalida, transcribe, validate_image  # noqa: E402


def test_image_validation():
    assert validate_image(b"x", "image/png").media_type == "image/png"
    with pytest.raises(ImatgeInvalida):
        validate_image(b"x", "application/pdf")
    with pytest.raises(ImatgeInvalida):
        validate_image(b"", "image/jpeg")
    with pytest.raises(ImatgeInvalida):
        validate_image(b"x" * (6 * 1024 * 1024 + 1), "image/jpeg")


def test_transcription_sends_the_image_and_keeps_student_text_verbatim():
    llm = ScriptedLLM({"transcripcio": [{
        "transcripcio": "  $y=kx$ dona 0, per tant el límit és 0  ",
        "llegibilitat": "bona", "contingut": "treball_matematic", "dubtes": [],
    }]})
    img = Imatge(b"PNG", "image/png")
    t, meta = transcribe(llm, EX["t2-4c"], img)
    assert t.transcripcio == "$y=kx$ dona 0, per tant el límit és 0"
    assert llm.images == [img] and meta.stage == "transcripcio"


def test_transcription_endpoint_and_photo_origin_in_trace(monkeypatch, tmp_path):
    import base64 as b64
    import os

    from fastapi.testclient import TestClient

    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    import app as app_module

    ok = {"veredicte": "ok", "infraccions": [], "explicacio": ""}
    llm = ScriptedLLM({
        "transcripcio": [{"transcripcio": "no sé seguir", "llegibilitat": "parcial",
                          "contingut": "treball_matematic", "dubtes": ["línia 2"]}],
        "diagnosi": [_diag_json()],
        "resposta": [{"text": "Què has provat fins ara?"}],
        "guardia": [ok],
    })
    monkeypatch.setattr(app_module, "_tutor", Tutor(llm, TEORIA))
    client = TestClient(app_module.app)
    sid = client.post("/api/sessions", json={"exercici_id": "t2-4c"}).json()["session_id"]

    bad = client.post(f"/api/sessions/{sid}/transcripcio", json={"imatge": "data:application/pdf;base64,AAAA"})
    assert bad.status_code == 400

    data_url = "data:image/png;base64," + b64.b64encode(b"fakepng").decode()
    r = client.post(f"/api/sessions/{sid}/transcripcio", json={"imatge": data_url})
    assert r.status_code == 200 and r.json()["llegibilitat"] == "parcial"

    r = client.post(f"/api/sessions/{sid}/missatges", json={"text": r.json()["transcripcio"], "origen": "foto"})
    assert r.status_code == 200 and r.json()["trace"]["origen"] == "foto"
    assert "no-cache" in client.get("/").headers["cache-control"]


# ---------- course theory ----------

from tutor.politica import allowed_theory  # noqa: E402
from tutor import prompts  # noqa: E402


def _step_with_theory(ex):
    return next(p for p in ex.passos if p.teoria)


def test_step_theory_is_gated_like_the_idea():
    ex = EX["t2-4c"]
    pas = _step_with_theory(ex)
    i = ex.step_ids.index(pas.id)
    done = ex.step_ids[:i]
    st = EstatSessio(completats=done)
    d1 = diag(passos={s: "completat" for s in done}, nivell_desorientacio="en_cami")
    pla, st2 = decide(ex, d1, st)
    pla.pas_objectiu, pla.nivell_pista = pas.id, 1
    ids1 = {it.id for it in allowed_theory(ex, pla, done, TEORIA)}
    pla.nivell_pista = 2
    ids2 = {it.id for it in allowed_theory(ex, pla, done, TEORIA)}
    step_ids = {parse_ref(r)[0] for r in pas.teoria}
    background = {parse_ref(r)[0] for r in ex.teoria}
    assert (step_ids - background) and not ((step_ids - background) & ids1)
    assert step_ids <= ids2


def test_reserved_theory_never_reaches_the_reply_stage():
    ex = EX["t2-4c"].model_copy(deep=True)
    pas = _step_with_theory(ex)
    reserved = pas.teoria[0]
    ex.teoria_reservada = [reserved]
    pla, _ = decide(ex, diag(nivell_desorientacio="encallat", intencio="demana_pista"), EstatSessio())
    pla.pas_objectiu, pla.nivell_pista = pas.id, 3
    assert parse_ref(reserved)[0] not in {it.id for it in allowed_theory(ex, pla, [], TEORIA)}


def test_items_citing_the_problem_are_reserved_automatically():
    ex = EX["t2-4c"]
    fake = TEORIA[parse_ref(ex.all_refs()[0])[0]].model_copy(update={"id": "T2.999", "problemes": ["T2.4"]})
    assert "T2.999" in ex.reserved_ids({**TEORIA, "T2.999": fake})


def test_reply_references_are_the_allowed_items_it_cites():
    ex = EX["t2-4c"]
    background = parse_ref(ex.teoria[0])[0]
    it = TEORIA[background]
    nom = it.etiqueta.split(" (")[0]  # "Definició 6"
    ok = {"veredicte": "ok", "infraccions": [], "explicacio": ""}
    llm = ScriptedLLM({
        "diagnosi": [_diag_json(intencio="pregunta_conceptual", teoria_pregunta=[background])],
        # Cites the allowed item, and an item it was never shown (Teorema 4 del Tema 6): only the first counts.
        "resposta": [{"text": f"Recorda la {nom} del Tema {it.tema} i el Teorema 4 del Tema 6. Com l'aplicaries aquí?"}],
        "guardia": [ok],
    })
    out = Tutor(llm, TEORIA).turn(Sessio(exercici=ex), "Què vol dir exactament que existeixi el límit?")
    assert [r["id"] for r in out["referencies"]] == [background]
    assert out["referencies"][0]["enunciat"] == TEORIA[background].enunciat.strip()
    assert background in out["trace"]["teoria_permesa"]
    redactor = next(u for stage, u in llm.seen if stage == "resposta")
    assert TEORIA[background].enunciat.strip()[:40] in redactor


def test_static_context_is_identical_across_turns_for_caching():
    ex = EX["t2-4c"]
    ok = {"veredicte": "ok", "infraccions": [], "explicacio": ""}
    llm = ScriptedLLM({
        "diagnosi": [_diag_json(), _diag_json()],
        "resposta": [{"text": "Què has provat?"}] * 2,
        "guardia": [ok, ok],
    })
    tutor, s = Tutor(llm, TEORIA), Sessio(exercici=ex)
    tutor.turn(s, "no sé per on començar")
    tutor.turn(s, "he provat rectes")
    diag_ctx = [c for stage, c in llm.contexts if stage == "diagnosi"]
    guard_ctx = [c for stage, c in llm.contexts if stage == "guardia"]
    assert diag_ctx[0] == diag_ctx[1] and guard_ctx[0] == guard_ctx[1]
    assert ex.full_reference() in diag_ctx[0]
    # The conversation is dynamic: it must not be part of the cached prefix.
    assert "he provat rectes" not in diag_ctx[1]


def test_diagnosis_concept_ids_exclude_reserved_items():
    ex = EX["t2-4c"].model_copy(deep=True)
    some = parse_ref(ex.all_refs()[0])[0]
    ex.teoria_reservada = [some]
    assert some not in prompts.diagnosi_teoria_ids(ex, TEORIA)


def test_result_regex_does_not_veto_content_the_reply_may_show():
    """Multi-answer exercises: the result regex also matches a step's own detail."""
    ex = EX["t2-4c"].model_copy(deep=True)
    ex.resultat.fuites = [r"\\delta\s*=\s*\\epsilon"]  # matches the `concloure` detail
    st = EstatSessio(completats=["candidat", "acotar"], nivell_per_pas={"concloure": 2})
    pla, _ = decide(ex, diag(passos={"candidat": "completat", "acotar": "completat"}, intencio="mostra_treball"), st)
    assert pla.pas_objectiu == "concloure" and pla.nivell_pista == 3
    assert ex.resultat.fuites[0] not in pla.regex_prohibides
    pla, _ = decide(ex, diag(passos={"candidat": "completat", "acotar": "completat"}, intencio="demana_pista",
                             nivell_desorientacio="en_cami"), EstatSessio(completats=["candidat", "acotar"]))
    assert pla.nivell_pista < 3 and ex.resultat.fuites[0] in pla.regex_prohibides


def test_repair_latex_undoes_json_escape_damage():
    from tutor.llm import repair_latex

    damaged = {"missatge": "Si $h=f\x0crac{1}{x}\neq g$ i $\x08eta\times y$.\nQuè en penses?", "referencies": ["T2.6"]}
    fixed = repair_latex(damaged)
    assert fixed["missatge"] == r"Si $h=f\frac{1}{x}\neq g$ i $\beta\times y$." + "\nQuè en penses?"
    assert fixed["referencies"] == ["T2.6"]


def test_no_progress_on_the_same_step_escalates_the_hint():
    """An on-track student who keeps proposing without finishing the step must not get the same hint forever."""
    ex = EX["t2-4c"]
    st = EstatSessio()
    levels = []
    for _ in range(3):
        pla, st = decide(ex, diag(intencio="mostra_treball", nivell_desorientacio="en_cami"), st)
        levels.append(pla.nivell_pista)
    assert levels == [1, 2, 3]
