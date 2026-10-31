"""The deterministic guard fails closed, whitelists only whole formula pieces, and catches citations of theory and
LaTeX commands the reply may not use."""

import pytest

from core.tutoring.domain.services import guard
from core.tutoring.domain.services.fallback import fallback_message
from core.tutoring.domain.services.guard import CAS_ERROR_PROBLEM, citation_problems, deterministic_check
from core.tutoring.domain.services.policy import allowed_content, allowed_theory, decide
from core.tutoring.domain.values.plan import Plan
from core.tutoring.domain.values.session_state import SessionState
from tests.core.tutoring.builders import COURSE, EX4C, diagnosis


def _plan(forbidden: list[str]) -> Plan:
    return Plan(action="pista", reason="", target_step=None, hint_level=1, forbidden_texts=forbidden)


def test_a_cas_error_rejects_the_draft(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*_: object) -> list[tuple[str, str]]:
        raise MemoryError

    monkeypatch.setattr(guard, "explain", boom)
    assert CAS_ERROR_PROBLEM in deterministic_check(r"Mira $x^2$. Ho veus?", _plan([r"$x^2+1$"]))


def test_a_formula_is_whitelisted_only_as_a_whole_piece_of_allowed_text() -> None:
    plan = _plan([r"$x-2y$"])
    # "x-2y" is a substring of the permitted "x-2y-z", not one of its pieces.
    permitted = [r"Considereu el sistema $\begin{aligned} x-2y-z &= 0 \\ x+yt &= 0 \end{aligned}$"]
    assert any("fórmula" in p for p in deterministic_check(r"Prova $x-2y$. Ho veus?", plan, permitted))
    # The same formula as a whole cell of the statement is a quote, not a leak.
    permitted = [r"Considereu el sistema $\begin{aligned} x-2y &= 0 \\ x+yt &= 0 \end{aligned}$"]
    assert not any("fórmula" in p for p in deterministic_check(r"Prova $x-2y$. Ho veus?", plan, permitted))


def test_undelimited_formulas_are_checked_by_the_guard() -> None:
    ex = COURSE.exercise("t5-3")
    plan, _ = decide(ex, diagnosis("t5-3", intencio="demana_pista", nivell_desorientacio="en_cami"), SessionState())
    permitted = [allowed_content(ex, plan, [], []), ex.statement_md()]
    problems = deterministic_check("Prova: P_2 = x + y + 2 + (x^2+y^2)/2. Ho veus?", plan, permitted)
    assert any("fórmula" in p for p in problems)


def test_ordinary_prose_with_an_equals_sign_is_not_flagged() -> None:
    plan, state = decide(EX4C, diagnosis(intencio="mostra_treball", nivell_desorientacio="en_cami"), SessionState())
    permitted = [allowed_content(EX4C, plan, state.completed), EX4C.statement_md()]
    msg = "Molt bé: si poses y = kx, què passa amb el quocient? I si y = x^2?"
    assert deterministic_check(msg, plan, permitted) == []


def test_unknown_latex_commands_are_a_problem() -> None:
    plan = _plan([])
    problems = deterministic_check(r"Fixa't en $e^{\fterm{0.2}}$ i $\blink x$. Ho veus?", plan)
    assert problems == ["ordres LaTeX que no existeixen (KaTeX les mostraria com a error): \\blink, \\fterm"]
    assert deterministic_check(r"Fixa't en $\frac{x^2}{\sqrt{y}}$. Ho veus?", plan) == []


def test_citing_theory_outside_the_allowed_set_is_a_problem() -> None:
    background = COURSE.theory_item(EX4C.theory[0].item_id)
    name = background.label.split(" (")[0]
    ok = f"Recorda la {name} del Tema {background.topic}. Com l'aplicaries?"
    assert citation_problems(ok, [background], EX4C.topic) == []
    bad = f"{ok} I el Teorema 4 del Tema 6?"
    assert citation_problems(bad, [background], EX4C.topic) == [
        "cita teoria que no és a la llista permesa: «Teorema 4 del Tema 6»"
    ]
    # Unless the allowed content itself cites it.
    assert citation_problems(bad, [background], EX4C.topic, ["pel Teorema 4 del Tema 6"]) == []


def test_concept_fallback_names_the_answering_item_with_its_article() -> None:
    items = [COURSE.theory[i] for i in COURSE.theory if COURSE.theory[i].number is not None]
    feminine = next(it for it in items if it.kind == "definicio")
    masculine = next(it for it in items if it.kind == "teorema")
    plan = Plan(action="explicar_concepte", reason="", target_step=None, hint_level=0, extra_theory=[masculine.id])
    msg = fallback_message(EX4C, plan, [feminine, masculine])
    assert msg.startswith(f"Mira el Teorema {masculine.number} del Tema {masculine.topic} ")
    plan = plan.model_copy(update={"extra_theory": [feminine.id]})
    msg = fallback_message(EX4C, plan, [masculine, feminine])
    assert msg.startswith(f"Mira la Definició {feminine.number} del Tema {feminine.topic} ")
    assert citation_problems(msg, [masculine, feminine], EX4C.topic) == []


def test_concept_fallback_passes_the_guard() -> None:
    background = EX4C.theory[0].item_id
    d = diagnosis(intencio="pregunta_conceptual", teoria_pregunta=[background])
    plan, state = decide(EX4C, d, SessionState())
    theory = allowed_theory(COURSE, EX4C, plan, state.completed)
    msg = fallback_message(EX4C, plan, theory)
    assert COURSE.theory_item(background).label.split(" (")[0] in msg
    permitted = [allowed_content(EX4C, plan, state.completed), EX4C.statement_md()]
    assert deterministic_check(msg, plan, permitted) == []
    assert citation_problems(msg, theory, EX4C.topic, permitted) == []
