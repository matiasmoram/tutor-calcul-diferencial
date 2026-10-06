"""Invariants of the policy state machine (see the docstring of backend/tutor/politica.py)."""

import re

import pytest

from test_harness import EX, TEORIA, ScriptedLLM, _diag_json, diag  # noqa: F401
from tutor.pipeline import Sessio, Tutor
from tutor.politica import EstatSessio, decide

EX4C = EX["t2-4c"]


def run(seq, ex=EX4C, textos=()):
    st = EstatSessio()
    plans = []
    for kw in seq:
        pla, st = decide(ex, diag(ex_id=ex.id, **kw), st, list(textos))
        plans.append(pla)
    return plans, st


def test_correct_result_with_partial_work_does_not_absorb_later_turns():
    """H1: after the student states the right value, hints, solution requests and concept questions still work."""
    done = {"candidat": "completat"}
    plans, st = run([
        dict(passos=done, resultat_proposat="correcte", intencio="proposa_resultat", nivell_desorientacio="en_cami"),
        dict(passos=done, intencio="demana_pista", nivell_desorientacio="encallat"),
        dict(passos=done, intencio="pregunta_conceptual"),
        dict(passos=done, intencio="demana_solucio", nivell_desorientacio="encallat"),
        dict(passos=done, intencio="demana_solucio", nivell_desorientacio="encallat"),
    ])
    assert [p.accio for p in plans] == ["demanar_justificacio", "pista", "explicar_concepte", "pista", "pista"]
    assert plans[4].nivell_pista > plans[1].nivell_pista


def test_repeated_error_escalates_and_varies():
    """H3: the same error again gets more step content, not the same question at level 0."""
    plans, st = run([dict(errors_detectats=["camins_com_a_prova"], intencio="proposa_resultat")] * 3)
    assert all(p.accio == "questionar_error" for p in plans)
    assert plans[0].pregunta_suggerida and not plans[1].pregunta_suggerida
    assert plans[0].nivell_pista < plans[1].nivell_pista <= plans[2].nivell_pista
    assert st.errors_vistos["camins_com_a_prova"] == 3


def test_closing_is_terminal():
    """H5: after tancar, nothing reopens hints and the result stays sayable."""
    plans, st = run([
        dict(resultat_proposat="correcte", resultat_justificat=True, intencio="proposa_resultat", nivell_desorientacio="en_cami"),
        dict(intencio="mostra_treball"),
        dict(resultat_proposat="correcte", intencio="proposa_resultat"),
    ])
    assert [p.accio for p in plans] == ["tancar", "despres_de_tancar", "despres_de_tancar"]
    assert st.tancat and st.completats == EX4C.step_ids
    assert all(p.pot_dir_resultat and not p.regex_prohibides for p in plans)


def test_error_beats_closing():
    """M4: a detected error means the justification is not accepted."""
    plans, _ = run([dict(resultat_proposat="correcte", resultat_justificat=True, errors_detectats=["camins_com_a_prova"],
                         intencio="proposa_resultat")])
    assert plans[0].accio == "questionar_error"


def test_concept_questions_do_not_move_the_hint_ladder():
    """M1: a question about a definition neither raises the level nor counts as a hint for escalation."""
    plans, st = run([dict(intencio="pregunta_conceptual"), dict(intencio="mostra_treball", nivell_desorientacio="en_cami")])
    assert plans[0].accio == "explicar_concepte" and plans[0].nivell_pista == 0
    assert plans[1].accio == "pista" and plans[1].nivell_pista == 1


def test_stuck_student_gets_the_step_shown_without_the_magic_words():
    """M3: frustration at level 3 eventually shows the step, and the next target is the following step."""
    plans, st = run([dict(intencio="mostra_treball", nivell_desorientacio="perdut")]
                    + [dict(intencio="frustracio", nivell_desorientacio="perdut")] * 5)
    assert "mostrar_pas" in [p.accio for p in plans]
    after = plans[[p.accio for p in plans].index("mostrar_pas") + 1]
    assert after.pas_objectiu != "candidat" and "candidat" in st.mostrats


def test_showing_a_step_is_never_vetoed_by_later_step_regexes():
    """H4: the full detail of the target step passes the deterministic guard when the plan shows it."""
    ex = EX["t6-3a"]
    st = EstatSessio(nivell_per_pas={"existencia": 3}, ultim_pas="existencia", ultima_accio="pista", intents_alumne=1)
    pla, _ = decide(ex, diag(ex_id="t6-3a", intencio="demana_solucio", nivell_desorientacio="encallat"), st)
    assert pla.accio == "mostrar_pas"
    detall = ex.pas("existencia").detall
    assert not [r for r in pla.regex_prohibides if re.search(r, detall, re.IGNORECASE)]


def test_turn_is_atomic_on_any_failure():
    """M6: an exception in any stage leaves history and state exactly as before."""

    class FailingReply(ScriptedLLM):
        def structured(self, stage, *a, **kw):
            if stage == "resposta":
                raise RuntimeError("rate limited")
            return super().structured(stage, *a, **kw)

    s = Sessio(exercici=EX4C)
    with pytest.raises(RuntimeError):
        Tutor(FailingReply({"diagnosi": [_diag_json()]}), TEORIA).turn(s, "hola")
    assert s.historial == [] and s.estat == EstatSessio()


def test_fallback_delivers_the_planned_level():
    """H6: when every draft is rejected, the student still gets the content of the level the state records."""
    bad = {"veredicte": "rebutjat", "infraccions": ["no_segueix_l_accio"], "explicacio": "x"}
    llm = ScriptedLLM({
        "diagnosi": [_diag_json(intencio="demana_pista", nivell_desorientacio="perdut")],
        "resposta": [{"text": "Pensa-hi."}] * 3,
        "guardia": [bad] * 3,
    })
    out = Tutor(llm, TEORIA).turn(Sessio(exercici=EX4C), "no sé res")
    assert out["trace"]["fallback"] and out["trace"]["pla"]["nivell_pista"] == 2
    assert EX4C.pas("candidat").idea.strip()[:30] in out["missatge"]


def test_help_abuse_climbs_at_half_speed_and_never_bottoms_out_without_an_attempt():
    """Anti-gaming: "dona'm la solució" every turn, with no attempt, never gets the full step."""
    plans, st = run([dict(intencio="demana_solucio", nivell_desorientacio="encallat")] * 8)
    assert "mostrar_pas" not in [p.accio for p in plans]
    levels = [p.nivell_pista for p in plans]
    assert levels[:3] == [2, 2, 3] and max(levels) == 3
    # One genuine attempt unlocks the bottom-out hint on the next request.
    plans2, _ = run([dict(intencio="demana_solucio", nivell_desorientacio="encallat")] * 4
                    + [dict(intencio="mostra_treball", nivell_desorientacio="encallat"),
                       dict(intencio="demana_solucio", nivell_desorientacio="encallat")])
    assert "mostrar_pas" in [p.accio for p in plans2[-2:]]


def test_frustration_gets_an_empathetic_tone_and_moves_are_tagged():
    plans, _ = run([dict(intencio="frustracio", nivell_desorientacio="perdut")])
    assert plans[0].to == "empatic" and plans[0].moviment == "Focus"


def test_concept_question_is_answered_even_with_an_error_in_the_same_message():
    plans, _ = run([dict(intencio="pregunta_conceptual", errors_detectats=["camins_com_a_prova"])])
    assert plans[0].accio == "explicar_concepte"


def test_a_step_marked_wrong_earlier_does_not_invent_errors_later():
    """Step states span the conversation; errors are only the last message's."""
    plans, _ = run([dict(passos={"candidat": "erroni"}, intencio="demana_pista", nivell_desorientacio="encallat")])
    assert plans[0].accio == "pista" and plans[0].error_objectiu is None


def test_answer_beggar_at_the_top_alternates_hint_and_a_concrete_attempt_request():
    plans, _ = run([dict(intencio="demana_solucio", nivell_desorientacio="encallat")] * 8)
    acts = [p.accio for p in plans]
    assert "demanar_intent" in acts and "mostrar_pas" not in acts
    assert all(not (a == b == "demanar_intent") for a, b in zip(acts, acts[1:]))


def test_sympy_guard_catches_a_leak_in_another_notation_but_not_allowed_formulas():
    from tutor.guardia import deterministic_check
    from tutor.politica import allowed_content

    pla, st = decide(EX4C, diag(intencio="mostra_treball", nivell_desorientacio="en_cami"), EstatSessio())
    assert pla.pas_objectiu == "candidat" and pla.textos_prohibits
    permeses = [allowed_content(EX4C, pla, st.completats), EX4C.enunciat_md()]
    # The bound of the next step, written differently from the sheet ($|x|^5 x^{-4}$ instead of a fraction).
    leak = deterministic_check("Fixa't que $|x|^{5}x^{-4}$ ho controla tot. Ho veus?", pla, permeses)
    assert any("fórmula" in p for p in leak)
    # The statement's own expression is allowed.
    ok = deterministic_check("Mira el quocient $\frac{x^5}{x^4+y^2}$ sobre alguna recta. Què obtens?", pla, permeses)
    assert not any("fórmula" in p for p in ok)
