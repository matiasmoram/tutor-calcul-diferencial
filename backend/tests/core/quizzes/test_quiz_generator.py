import pytest

from core.quizzes.domain.exceptions import QuizGenerationException
from core.shared.llm.client import Stage
from tests.core.quizzes.builders import ITERATED, check, generator, item, ok_audit, ok_solver, source
from tests.fakes.llm import ScriptedLLMClient


async def test_generation_replaces_only_rejected_statements() -> None:
    bad_check = check("limit", "x*(m*x)/(x**2+(m*x)**2)", "0")
    round1 = [
        item("F1 $a$.", checks=[ITERATED]),
        item("F2."),
        item("F3.", checks=[bad_check]),  # rejected by sympy
        item("C1.", "cert"),
        item("C2.", "cert"),  # rejected: the blind solver disagrees
    ]
    round2 = [item("F4."), item("C3.", "cert"), item("C4.", "cert")]
    llm = ScriptedLLMClient(
        {
            Stage.QUIZ_GENERATION: [{"afirmacions": round1}, {"afirmacions": round2}],
            # Round 1 candidates after sympy: F1, F2, C1, C2.
            Stage.QUIZ_VERIFICATION: [ok_solver(["fals", "fals", "cert", "fals"]), ok_solver(["fals", "cert", "cert"])],
            Stage.QUIZ_AUDIT: [ok_audit(4), ok_audit(3)],
        }
    )
    q = await generator(llm).generate(source(), "facil")
    assert len(q.statements) == 6 and [s.id for s in q.statements] == [f"a{i}" for i in range(1, 7)]
    assert sorted(s.statement for s in q.statements) == sorted(["F1 $a$.", "F2.", "C1.", "F4.", "C3.", "C4."])
    assert q.verification is not None
    rounds = q.verification.rounds
    assert len(rounds) == 2 and rounds[0].requested == 5 and rounds[1].requested == 3
    assert [r.accepted_total for r in rounds] == [3, 6] and len(rounds[0].rejected) == 2
    f1 = next(s for s in q.statements if s.statement.startswith("F1"))
    assert f1.checks_passed == 1 and f1.checks[0].computed == "m/(m**2 + 1)"
    assert f1.verification is not None and f1.verification.round == 1
    # The second request carries the reasons and the statements already kept.
    req2 = llm.requests[Stage.QUIZ_GENERATION][1].user
    assert "FALSA segons sympy" in req2 and "diu que és fals, no cert" in req2 and "F1 $a$." in req2
    # The blind solver never sees verdicts or solutions; the audit does.
    blind = llm.requests[Stage.QUIZ_VERIFICATION][0].user
    assert "veredicte" not in blind and "Resolució" not in blind
    assert "veredicte declarat: fals" in llm.requests[Stage.QUIZ_AUDIT][0].user
    # The whole topic's notes are the cached context of every call.
    assert all('<apunts tema="2"' in (r.context or "") for rs in llm.requests.values() for r in rs)


async def test_the_stored_document_keeps_its_catalan_shape() -> None:
    llm = ScriptedLLMClient(
        {
            Stage.QUIZ_GENERATION: [{"afirmacions": [item(f"F{i}.") for i in range(3)] + [item("C1.", "cert")]},
                                    {"afirmacions": [item("C2.", "cert"), item("F9.")]}],
            Stage.QUIZ_VERIFICATION: [ok_solver(["fals"] * 3 + ["cert"]), ok_solver(["cert", "fals"])],
            Stage.QUIZ_AUDIT: [ok_audit(4), ok_audit(2)],
        }
    )  # fmt: skip
    doc = (await generator(llm).generate(source(), "facil")).model_dump(mode="json")
    assert list(doc) == ["id", "font", "tema", "dificultat", "afirmacions", "verificacio", "creat"]
    assert list(doc["afirmacions"][0]) == [
        "id", "enunciat", "veredicte", "concepte", "trampa", "contraexemple", "resolucio", "idees_clau", "pista",
        "teoria", "comprovacions", "verificacio",
    ]  # fmt: skip
    assert set(doc["afirmacions"][0]["verificacio"]) == {"solucionador", "confianca", "ronda"}
    assert list(doc["verificacio"]["rondes"][0]) == [
        "ronda", "demanades", "rebudes", "generacio", "rebutjades", "solucionador", "auditoria", "acceptades_total",
    ]  # fmt: skip


async def test_generation_gives_up_after_too_many_rounds() -> None:
    bad = {"afirmacions": [item(f"X{i}.", contraexemple="") for i in range(5)]}
    llm = ScriptedLLMClient({Stage.QUIZ_GENERATION: [bad] * 10})
    with pytest.raises(QuizGenerationException) as e:
        await generator(llm).generate(source(), "facil")
    assert e.value.error_code == 502 and llm.calls(Stage.QUIZ_GENERATION) == 5
    assert llm.calls(Stage.QUIZ_VERIFICATION) == 0  # nothing reached the verification
