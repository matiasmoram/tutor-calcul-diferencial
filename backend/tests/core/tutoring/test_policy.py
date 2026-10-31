"""Invariants of the policy state machine (see the docstring of core/tutoring/domain/services/policy.py)."""

import re
from itertools import pairwise

from core.tutoring.domain.services.policy import allowed_content, allowed_theory, decide
from core.tutoring.domain.values.session_state import SessionState
from tests.core.tutoring.builders import COURSE, EX4C, diagnosis, run_policy


def test_correct_result_with_partial_work_does_not_absorb_later_turns() -> None:
    """After the student states the right value, hints, solution requests and concept questions still work."""
    done = {"candidat": "completat"}
    plans, _ = run_policy(
        [
            dict(steps=done, resultat_proposat="correcte", intencio="proposa_resultat", nivell_desorientacio="en_cami"),
            dict(steps=done, intencio="demana_pista", nivell_desorientacio="encallat"),
            dict(steps=done, intencio="pregunta_conceptual"),
            dict(steps=done, intencio="demana_solucio", nivell_desorientacio="encallat"),
            dict(steps=done, intencio="demana_solucio", nivell_desorientacio="encallat"),
        ]
    )
    assert [p.action for p in plans] == ["demanar_justificacio", "pista", "explicar_concepte", "pista", "pista"]
    assert plans[4].hint_level > plans[1].hint_level


def test_repeated_mistake_escalates_and_varies() -> None:
    """The same mistake again gets more step content, not the same question at level 0."""
    plans, state = run_policy([dict(errors_detectats=["camins_com_a_prova"], intencio="proposa_resultat")] * 3)
    assert all(p.action == "questionar_error" for p in plans)
    assert plans[0].suggested_question and not plans[1].suggested_question
    assert plans[0].hint_level < plans[1].hint_level <= plans[2].hint_level
    assert state.mistakes_seen["camins_com_a_prova"] == 3


def test_closing_is_terminal() -> None:
    """After tancar, nothing reopens hints and the result stays sayable."""
    plans, state = run_policy(
        [
            dict(
                resultat_proposat="correcte",
                resultat_justificat=True,
                intencio="mostra_treball",
                nivell_desorientacio="en_cami",
            ),
            dict(intencio="mostra_treball"),
            dict(resultat_proposat="correcte", intencio="proposa_resultat"),
        ]
    )
    assert [p.action for p in plans] == ["tancar", "despres_de_tancar", "despres_de_tancar"]
    assert state.closed and state.completed == EX4C.step_ids
    assert all(p.may_state_result and not p.forbidden_patterns for p in plans)


def test_a_mistake_beats_closing() -> None:
    """A detected mistake means the justification is not accepted."""
    plans, _ = run_policy(
        [
            dict(
                resultat_proposat="correcte",
                resultat_justificat=True,
                errors_detectats=["camins_com_a_prova"],
                intencio="proposa_resultat",
            )
        ]
    )
    assert plans[0].action == "questionar_error"


def test_concept_questions_do_not_move_the_hint_ladder() -> None:
    plans, _ = run_policy(
        [dict(intencio="pregunta_conceptual"), dict(intencio="mostra_treball", nivell_desorientacio="en_cami")]
    )
    assert plans[0].action == "explicar_concepte" and plans[0].hint_level == 0
    assert plans[1].action == "pista" and plans[1].hint_level == 1


def test_stuck_student_gets_the_step_shown_without_the_magic_words() -> None:
    """Frustration at level 3 eventually shows the step, and the next target is the following step."""
    plans, state = run_policy(
        [dict(intencio="mostra_treball", nivell_desorientacio="perdut")]
        + [dict(intencio="frustracio", nivell_desorientacio="perdut")] * 5
    )
    actions = [p.action for p in plans]
    assert "mostrar_pas" in actions
    after = plans[actions.index("mostrar_pas") + 1]
    assert after.target_step != "candidat" and "candidat" in state.shown


def test_showing_a_step_is_never_vetoed_by_later_step_regexes() -> None:
    """The full detail of the target step passes the deterministic guard when the plan shows it."""
    ex = COURSE.exercise("t6-3a")
    state = SessionState(
        level_per_step={"existencia": 3}, last_step="existencia", last_action="pista", student_attempts=1
    )
    plan, _ = decide(ex, diagnosis("t6-3a", intencio="demana_solucio", nivell_desorientacio="encallat"), state)
    assert plan.action == "mostrar_pas"
    detail = ex.step("existencia").detail
    assert not [r for r in plan.forbidden_patterns if re.search(r, detail, re.IGNORECASE)]


def test_help_abuse_climbs_at_half_speed_and_never_bottoms_out_without_an_attempt() -> None:
    """Anti-gaming: "dona'm la solució" every turn, with no attempt, never gets the full step."""
    plans, _ = run_policy([dict(intencio="demana_solucio", nivell_desorientacio="encallat")] * 8)
    assert "mostrar_pas" not in [p.action for p in plans]
    levels = [p.hint_level for p in plans]
    assert levels[:3] == [2, 2, 3] and max(levels) == 3
    # One genuine attempt unlocks the bottom-out hint on the next request.
    plans2, _ = run_policy(
        [dict(intencio="demana_solucio", nivell_desorientacio="encallat")] * 4
        + [
            dict(intencio="mostra_treball", nivell_desorientacio="encallat"),
            dict(intencio="demana_solucio", nivell_desorientacio="encallat"),
        ]
    )
    assert "mostrar_pas" in [p.action for p in plans2[-2:]]


def test_frustration_gets_an_empathetic_tone_and_moves_are_tagged() -> None:
    plans, _ = run_policy([dict(intencio="frustracio", nivell_desorientacio="perdut")])
    assert plans[0].tone == "empatic" and plans[0].move == "Focus"


def test_concept_question_is_answered_even_with_a_mistake_in_the_same_message() -> None:
    plans, _ = run_policy([dict(intencio="pregunta_conceptual", errors_detectats=["camins_com_a_prova"])])
    assert plans[0].action == "explicar_concepte"


def test_a_step_marked_wrong_earlier_does_not_invent_mistakes_later() -> None:
    """Step states span the conversation; mistakes are only the last message's."""
    plans, _ = run_policy(
        [dict(steps={"candidat": "erroni"}, intencio="demana_pista", nivell_desorientacio="encallat")]
    )
    assert plans[0].action == "pista" and plans[0].target_mistake is None


def test_answer_beggar_at_the_top_alternates_hint_and_a_concrete_attempt_request() -> None:
    plans, _ = run_policy([dict(intencio="demana_solucio", nivell_desorientacio="encallat")] * 8)
    actions = [p.action for p in plans]
    assert "demanar_intent" in actions and "mostrar_pas" not in actions
    assert all(not (a == b == "demanar_intent") for a, b in pairwise(actions))


def test_paths_as_proof_triggers_socratic_mistake_question() -> None:
    d = diagnosis(
        steps={"candidat": "completat"},
        errors_detectats=["camins_com_a_prova"],
        resultat_proposat="correcte",
        nivell_desorientacio="en_cami",
        intencio="proposa_resultat",
    )
    plan, _ = decide(EX4C, d, SessionState(), ["Per camins dona 0, per tant el límit és 0"])
    assert plan.action == "questionar_error"
    assert plan.target_mistake == "camins_com_a_prova"
    assert plan.target_step == "acotar"
    # The reply may repeat the student's own words ("el límit és 0"), but not reveal the bound.
    assert not any("mit" in r for r in plan.forbidden_patterns)
    assert any("|x|" in r or "\\|x\\|" in r for r in plan.forbidden_patterns)
    # Without those words the result stays protected: the tutor has not confirmed it.
    plan, _ = decide(EX4C, d, SessionState())
    assert any("mit" in r for r in plan.forbidden_patterns)


def test_hint_level_escalates_and_caps_then_shows_step() -> None:
    state = SessionState()
    levels = []
    for _ in range(3):  # a student who keeps trying (and stays stuck) climbs one level per turn
        plan, state = decide(EX4C, diagnosis(intencio="mostra_treball", nivell_desorientacio="encallat"), state)
        levels.append(plan.hint_level)
    assert levels == [2, 3, 3]
    plan, state = decide(EX4C, diagnosis(intencio="demana_solucio"), state)
    assert plan.action == "mostrar_pas" and plan.hint_level == 4 and plan.target_step == "candidat"


def test_asking_for_the_solution_early_only_raises_the_hint_level() -> None:
    plan, _ = decide(EX4C, diagnosis(intencio="demana_solucio", nivell_desorientacio="perdut"), SessionState())
    assert plan.action == "pista" and plan.hint_level == 2
    assert not plan.may_state_result


def test_completed_steps_are_monotonic_unless_marked_wrong() -> None:
    _, state = decide(EX4C, diagnosis(steps={"candidat": "completat"}, nivell_desorientacio="en_cami"), SessionState())
    assert state.completed == ["candidat"]
    _, state = decide(EX4C, diagnosis(nivell_desorientacio="en_cami"), state)
    assert state.completed == ["candidat"]
    _, state = decide(EX4C, diagnosis(steps={"candidat": "erroni"}), state)
    assert state.completed == []


def test_progress_validates_and_moves_on() -> None:
    plan, _ = decide(EX4C, diagnosis(steps={"candidat": "completat"}, nivell_desorientacio="en_cami"), SessionState())
    assert plan.action == "validar_i_avancar" and plan.target_step == "acotar" and plan.hint_level == 1


def test_close_only_when_correct_and_justified() -> None:
    d = diagnosis(
        resultat_proposat="correcte",
        resultat_justificat=True,
        intencio="mostra_treball",
        nivell_desorientacio="en_cami",
    )
    plan, state = decide(EX4C, d, SessionState())
    assert plan.action == "tancar" and plan.may_state_result and state.closed


def test_wrong_result_after_work_is_questioned_without_revealing() -> None:
    d = diagnosis(steps={"candidat": "completat"}, resultat_proposat="incorrecte", intencio="proposa_resultat")
    plan, _ = decide(EX4C, d, SessionState())
    assert plan.action == "questionar_resultat"
    assert "RESULTAT" not in allowed_content(EX4C, plan, ["candidat"])


def test_bare_guesses_are_neither_confirmed_nor_denied() -> None:
    """No oracle: "és 1?" then "és 0?" must get the same neutral treatment."""
    for verdict in ("incorrecte", "correcte"):
        plan, state = decide(EX4C, diagnosis(resultat_proposat=verdict, intencio="proposa_resultat"), SessionState())
        assert plan.action == "demanar_raonament"
        assert not plan.may_state_result and not plan.result_stated_by_student and not state.result_confirmed
        assert any(re.search(r, "el límit és 0", re.IGNORECASE) for r in plan.forbidden_patterns)


def test_allowed_content_hides_later_steps_and_unearned_detail() -> None:
    plan, state = decide(
        EX4C, diagnosis(steps={"candidat": "completat"}, nivell_desorientacio="en_cami"), SessionState()
    )
    content = allowed_content(EX4C, plan, state.completed)
    assert EX4C.step("acotar").objective in content
    assert EX4C.step("acotar").idea not in content  # level 1: objective only
    assert EX4C.step("acotar").detail not in content
    assert EX4C.step("concloure").idea not in content


def test_result_regex_does_not_veto_content_the_reply_may_show() -> None:
    """Multi-answer exercises: the result regex also matches a step's own detail."""
    pattern = r"\\delta\s*=\s*\\epsilon"  # matches the `concloure` detail
    ex = EX4C.model_copy(update={"result": EX4C.result.model_copy(update={"leak_patterns": [pattern]})})
    done = {"candidat": "completat", "acotar": "completat"}
    state = SessionState(completed=["candidat", "acotar"], level_per_step={"concloure": 2})
    plan, _ = decide(ex, diagnosis(steps=done, intencio="mostra_treball"), state)
    assert plan.target_step == "concloure" and plan.hint_level == 3
    assert pattern not in plan.forbidden_patterns
    plan, _ = decide(
        ex,
        diagnosis(steps=done, intencio="demana_pista", nivell_desorientacio="en_cami"),
        SessionState(completed=["candidat", "acotar"]),
    )
    assert plan.hint_level < 3 and pattern in plan.forbidden_patterns


def test_no_progress_on_the_same_step_escalates_the_hint() -> None:
    """An on-track student who keeps proposing without finishing the step must not get the same hint forever."""
    state = SessionState()
    levels = []
    for _ in range(3):
        plan, state = decide(EX4C, diagnosis(intencio="mostra_treball", nivell_desorientacio="en_cami"), state)
        levels.append(plan.hint_level)
    assert levels == [1, 2, 3]


# ---------- theory gate ----------


def _step_with_theory():
    return next(s for s in EX4C.steps if s.theory)


def test_step_theory_is_gated_like_the_idea() -> None:
    step = _step_with_theory()
    done = EX4C.step_ids[: EX4C.step_ids.index(step.id)]
    plan, _ = decide(
        EX4C,
        diagnosis(steps=dict.fromkeys(done, "completat"), nivell_desorientacio="en_cami"),
        SessionState(completed=done),
    )
    plan = plan.model_copy(update={"target_step": step.id, "hint_level": 1})
    ids1 = {it.id for it in allowed_theory(COURSE, EX4C, plan, done)}
    ids2 = {it.id for it in allowed_theory(COURSE, EX4C, plan.model_copy(update={"hint_level": 2}), done)}
    step_ids = {r.item_id for r in step.theory}
    background = {r.item_id for r in EX4C.theory}
    assert (step_ids - background) and not ((step_ids - background) & ids1)
    assert step_ids <= ids2


def test_reserved_theory_never_reaches_the_reply_stage() -> None:
    step = _step_with_theory()
    reserved = step.theory[0]
    ex = EX4C.model_copy(update={"reserved_theory": [reserved]})
    plan, _ = decide(ex, diagnosis(nivell_desorientacio="encallat", intencio="demana_pista"), SessionState())
    plan = plan.model_copy(update={"target_step": step.id, "hint_level": 3})
    assert reserved.item_id not in {it.id for it in allowed_theory(COURSE, ex, plan, [])}
