from core.tutoring.domain.services.guard import deterministic_check
from core.tutoring.domain.services.policy import allowed_content, decide
from core.tutoring.domain.values.session_state import SessionState
from tests.core.tutoring.builders import EX4C, diagnosis


def test_guard_catches_leaked_bound_and_missing_question() -> None:
    plan, _ = decide(EX4C, diagnosis(steps={"candidat": "completat"}, nivell_desorientacio="en_cami"), SessionState())
    problems = deterministic_check(r"Fixa't que $\frac{|x|^5}{x^4+y^2} \le |x|$.", plan)
    assert any("prohibit" in p for p in problems)
    assert any("pregunta" in p for p in problems)
    assert deterministic_check("Molt bé. Què passa si comparaaes el denominador amb un dels seus termes?", plan) == []


def test_sympy_guard_catches_a_leak_in_another_notation_but_not_allowed_formulas() -> None:
    plan, state = decide(EX4C, diagnosis(intencio="mostra_treball", nivell_desorientacio="en_cami"), SessionState())
    assert plan.target_step == "candidat" and plan.forbidden_texts
    permitted = [allowed_content(EX4C, plan, state.completed), EX4C.statement_md()]
    # The bound of the next step, written differently from the sheet ($|x|^5 x^{-4}$ instead of a fraction).
    leak = deterministic_check("Fixa't que $|x|^{5}x^{-4}$ ho controla tot. Ho veus?", plan, permitted)
    assert any("fórmula" in p for p in leak)
    # The statement's own expression is allowed.
    ok = deterministic_check("Mira el quocient $\\frac{x^5}{x^4+y^2}$ sobre alguna recta. Què obtens?", plan, permitted)
    assert not any("fórmula" in p for p in ok)


def test_empty_and_overlong_messages_are_rejected() -> None:
    plan, _ = decide(EX4C, diagnosis(), SessionState())
    assert deterministic_check("   ", plan) == ["missatge buit"]
    long = " ".join(["Una frase."] * (plan.max_sentences + 2)) + " Ho veus?"
    assert any("massa llarg" in p for p in deterministic_check(long, plan))
