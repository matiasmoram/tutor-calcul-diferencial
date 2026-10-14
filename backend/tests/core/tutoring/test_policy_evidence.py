"""Policy invariants that do not trust the diagnosis' word alone (see the docstring of core/tutoring/domain/policy.py):
steps need evidence, closing needs reasoning in the message, no oracle for guesses, the result gate only lifts on
the student's own words, and a repeated mistake has no dead end."""

import re

from core.tutoring.domain.fallback import fallback_message
from core.tutoring.domain.policy import decide
from core.tutoring.domain.values.session_state import SessionState
from tests.core.tutoring.builders import COURSE, EX4C, diagnosis

ALL_DONE = dict.fromkeys(EX4C.step_ids, "completat")
T53 = COURSE.exercise("t5-3")  # result 2.125: P_2(0.2,-0.1) = 2.125


def test_steps_marked_completed_without_work_are_not_completed() -> None:
    """Turn 1, "no sé per on començar", diagnosis marks every step completed: no conclusion, no result."""
    d = diagnosis(steps=ALL_DONE, intencio="demana_pista", nivell_desorientacio="encallat")
    plan, state = decide(EX4C, d, SessionState(), ["no sé per on començar"])
    assert state.completed == []
    assert plan.action == "pista" and plan.target_step == EX4C.step_ids[0]
    assert not plan.may_state_result
    assert EX4C.result.value.strip() not in fallback_message(EX4C, plan)


def test_work_completes_at_most_up_to_the_current_target() -> None:
    d = diagnosis(steps=ALL_DONE, intencio="mostra_treball", nivell_desorientacio="en_cami")
    plan, state = decide(EX4C, d, SessionState(), ["he trobat el candidat"])
    assert state.completed == [EX4C.step_ids[0]]
    assert plan.action == "validar_i_avancar" and plan.target_step == EX4C.step_ids[1]


def test_the_conclusion_is_not_stated_in_the_turn_the_last_step_is_completed() -> None:
    done = EX4C.step_ids[:-1]
    state = SessionState(completed=done, step_states=dict.fromkeys(done, "completat"))
    d = diagnosis(steps=ALL_DONE, intencio="mostra_treball", nivell_desorientacio="encallat")
    plan, state = decide(EX4C, d, state, ["fet"])
    assert state.completed == EX4C.step_ids
    assert plan.action == "demanar_conclusio" and not plan.may_state_result


def test_a_bare_guess_flagged_correct_and_justified_does_not_close() -> None:
    for intent in ("proposa_resultat", "demana_pista"):
        d = diagnosis(resultat_proposat="correcte", resultat_justificat=True, intencio=intent)
        plan, state = decide(EX4C, d, SessionState(), ["0?"])
        assert plan.action != "tancar" and not state.closed and not plan.may_state_result


def test_closing_needs_reasoning_in_the_message() -> None:
    d = diagnosis(
        steps={EX4C.step_ids[0]: "completat"},
        resultat_proposat="correcte",
        resultat_justificat=True,
        intencio="proposa_resultat",
        nivell_desorientacio="en_cami",
    )
    plan, state = decide(EX4C, d, SessionState(), ["Per camins dona 0 i la fita ho demostra: el límit és 0"])
    assert plan.action == "tancar" and state.closed


def test_earlier_work_does_not_make_later_guesses_answerable() -> None:
    """No oracle: after partial work, "és 2.2?", "és 2.1?", "és 2.125?" are neither confirmed nor denied."""
    texts = ["he calculat D1f = e^x"]
    _, state = decide(
        T53, diagnosis("t5-3", steps={"polinomi": "en_curs"}, nivell_desorientacio="en_cami"), SessionState(), texts
    )
    for guess, verdict in (("és 2.2?", "incorrecte"), ("és 2.1?", "incorrecte"), ("és 2.125?", "correcte")):
        texts.append(guess)
        d = diagnosis(
            "t5-3",
            steps={"polinomi": "en_curs"},
            intencio="proposa_resultat",
            nivell_desorientacio="en_cami",
            resultat_proposat=verdict,
        )
        plan, state = decide(T53, d, state, texts)
        assert plan.action not in ("questionar_resultat", "demanar_justificacio", "tancar"), guess
        assert not plan.result_stated_by_student and not state.result_confirmed


def test_the_result_gate_lifts_only_on_the_students_own_words() -> None:
    d = diagnosis(
        "t5-3", steps={"polinomi": "en_curs"}, intencio="mostra_treball", nivell_desorientacio="en_cami"
    ).model_copy(update={"proposed_result": "correcte"})
    help_ = diagnosis("t5-3", steps={"polinomi": "en_curs"}, intencio="demana_pista")
    # The diagnosis says "correct", but the student never wrote the result.
    plan, state = decide(T53, d, SessionState(), ["he començat derivant"])
    assert plan.action == "demanar_justificacio" and not plan.result_stated_by_student and not state.result_confirmed
    plan, _ = decide(T53, help_, state, ["he començat derivant", "ajuda"])
    assert any(re.search(p, "el resultat és 2.125", re.IGNORECASE) for p in plan.forbidden_patterns)
    assert T53.result.value in plan.forbidden_texts
    # The student wrote it: it may be acknowledged from now on.
    plan, state = decide(T53, d, SessionState(), ["P2 = 2+x+y+(x^2+y^2)/2, i en el punt surt 2.125"])
    assert plan.result_stated_by_student and state.result_confirmed
    # In another notation than the regexes know: the CAS recognises it.
    plan, state = decide(T53, d, SessionState(), [r"en el punt surt $\frac{17}{8}$"])
    assert plan.result_stated_by_student and state.result_confirmed


def test_a_repeated_mistake_at_the_top_shows_the_step() -> None:
    mistake = T53.mistake_ids[0]
    state = SessionState()
    actions = []
    for i in range(5):
        d = diagnosis(
            "t5-3",
            steps={"polinomi": "erroni"},
            intencio="mostra_treball",
            nivell_desorientacio="encallat",
            errors_detectats=[mistake],
        )
        plan, state = decide(T53, d, state, [f"intent {i}"])
        actions.append((plan.action, plan.target_step))
    assert ("mostrar_pas", "polinomi") in actions
    assert actions.index(("mostrar_pas", "polinomi")) <= 3


def test_asking_for_the_solution_after_a_mistake_at_the_top_shows_the_step() -> None:
    mistake = T53.mistake_ids[0]
    state = SessionState(
        level_per_step={"polinomi": 3}, last_step="polinomi", last_action="questionar_error", student_attempts=1
    )
    d = diagnosis("t5-3", intencio="demana_solucio", nivell_desorientacio="encallat", errors_detectats=[mistake])
    plan, _ = decide(T53, d, state, ["dona'm la solució"])
    assert plan.action == "mostrar_pas" and plan.hint_level == 4


def test_a_mistake_without_any_attempt_never_bottoms_out() -> None:
    """Anti-gaming still holds: no attempt ever, no full step."""
    mistake = T53.mistake_ids[0]
    state = SessionState(level_per_step={"polinomi": 3}, last_step="polinomi", mistakes_seen={mistake: 3})
    d = diagnosis("t5-3", intencio="demana_solucio", nivell_desorientacio="encallat", errors_detectats=[mistake])
    plan, _ = decide(T53, d, state, ["dona'm la solució"])
    assert plan.action == "questionar_error"


def test_a_mistake_repeated_after_every_step_is_resolved_is_no_dead_end() -> None:
    """Seen live (t2-16c, a seeded misconception): with every step resolved, the same mistake was questioned at
    level 0 until the turn limit. It is questioned twice, then the conclusion is shown and the session closes."""
    mistake = EX4C.mistake_ids[0]
    state = SessionState(completed=EX4C.step_ids, step_states=ALL_DONE, student_attempts=3)
    actions = []
    for i in range(4):
        d = diagnosis(
            steps=ALL_DONE, intencio="mostra_treball", nivell_desorientacio="en_cami", errors_detectats=[mistake]
        )
        plan, state = decide(EX4C, d, state, [f"intent {i}"])
        actions.append(plan.action)
        if state.closed:
            break
    assert actions == ["questionar_error", "questionar_error", "mostrar_conclusio"]
    assert state.closed


def test_a_student_stuck_on_a_mistake_after_every_step_gets_the_conclusion() -> None:
    """Stuck, or asking for the solution, on a mistake already questioned once: the conclusion is shown."""
    mistake = EX4C.mistake_ids[0]
    for intent, disorientation in (("demana_solucio", "encallat"), ("mostra_treball", "perdut")):
        state = SessionState(completed=EX4C.step_ids, step_states=ALL_DONE, student_attempts=3)
        actions = []
        for _ in range(2):
            d = diagnosis(
                steps=ALL_DONE, intencio=intent, nivell_desorientacio=disorientation, errors_detectats=[mistake]
            )
            plan, state = decide(EX4C, d, state, ["no ho veig"])
            actions.append(plan.action)
        assert actions == ["questionar_error", "mostrar_conclusio"] and plan.may_state_result


def test_the_conclusion_is_not_shown_in_the_turn_the_last_step_is_completed_even_with_a_mistake() -> None:
    done = EX4C.step_ids[:-1]
    mistake = EX4C.mistake_ids[0]
    state = SessionState(completed=done, step_states=dict.fromkeys(done, "completat"), mistakes_seen={mistake: 5})
    d = diagnosis(steps=ALL_DONE, intencio="mostra_treball", nivell_desorientacio="perdut", errors_detectats=[mistake])
    plan, state = decide(EX4C, d, state, ["fet"])
    assert plan.action == "questionar_error" and not plan.may_state_result and not state.closed
