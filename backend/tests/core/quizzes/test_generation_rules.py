import pytest

from core.quizzes.domain.services.balance import false_range, trim
from core.quizzes.domain.services.judging import judge
from core.quizzes.domain.services.validation import all_checks, check_problems, validate_draft, with_results
from core.quizzes.domain.values.drafts import StatementDraft
from core.quizzes.domain.values.verification import AuditReview, SolverAnswer
from core.quizzes.infra.prompts import GENERATION_SYSTEM
from core.shared.llm.client import JsonObject
from core.shared.math.sympy_checks import evaluate_one
from tests.core.quizzes.builders import ITERATED, check, item, source

REFS = set(source().allowed_refs)


def draft(raw: JsonObject) -> StatementDraft:
    return StatementDraft.model_validate(raw)


def test_valid_item_passes() -> None:
    assert validate_draft(draft(item("Afirmació $a$.")), REFS) == []


@pytest.mark.parametrize(
    ("changes", "expected"),
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
def test_item_validation_rejects(changes: JsonObject, expected: str) -> None:
    problems = validate_draft(draft(item("A.") | changes), REFS)
    assert any(expected in p for p in problems), problems


def test_at_most_four_checks_per_statement_as_the_prompt_asks() -> None:
    assert validate_draft(draft(item("A.", checks=[ITERATED] * 4)), REFS) == []
    assert validate_draft(draft(item("A.", checks=[ITERATED] * 5)), REFS) == ["massa comprovacions (màxim 4)"]
    assert "d'1 a 4;" in GENERATION_SYSTEM


def test_failing_sympy_check_rejects_statement() -> None:
    drafts = [
        draft(item("A.", checks=[ITERATED])),
        draft(item("B.", checks=[check("limit", "x*(m*x)/(x**2+(m*x)**2)", "0")])),
    ]
    checked = with_results(drafts, [evaluate_one(c) for c in all_checks(drafts)])
    assert check_problems(checked[0]) == []
    assert any("FALSA segons sympy" in p and "m/(m**2 + 1)" in p for p in check_problems(checked[1]))


def test_judge_needs_blind_agreement_and_clean_audit() -> None:
    drafts = [draft(item("A.")), draft(item("B.", "cert")), draft(item("C.")), draft(item("D."))]
    solver = [
        SolverAnswer.model_validate(a)
        for a in [
            {"num": 1, "veredicte": "fals", "confianca": "alta", "ben_plantejada": True, "justificacio": ""},
            {
                "num": 2,
                "veredicte": "fals",
                "confianca": "alta",
                "ben_plantejada": True,
                "justificacio": "contraexemple",
            },
            {"num": 3, "veredicte": "fals", "confianca": "baixa", "ben_plantejada": True, "justificacio": ""},
            {"num": 4, "veredicte": "fals", "confianca": "alta", "ben_plantejada": True, "justificacio": ""},
        ]
    ]
    ok = {"resolucio_correcta": True, "teoria_correcta": True, "pista_neutra": True, "problemes": ""}
    audit = [
        AuditReview.model_validate(r)
        for r in [
            ok | {"num": 1},
            ok | {"num": 2},
            ok | {"num": 3},
            ok | {"num": 4, "resolucio_correcta": False, "problemes": "no compleix H"},
        ]
    ]
    verdicts = judge(drafts, solver, audit)
    assert verdicts[0] == []
    assert "diu que és fals, no cert" in verdicts[1][0]
    assert "no n'està segur" in verdicts[2][0]
    assert "no compleix H" in verdicts[3][0]


def test_judge_rejects_what_a_pass_did_not_cover() -> None:
    verdicts = judge([draft(item("A."))], [], [])
    assert verdicts == [["el solucionador independent no l'ha resolta", "l'auditoria no l'ha revisada"]]


def test_balance_range() -> None:
    assert false_range(6) == (3, 4) and false_range(10) == (5, 8)


def test_trim_drops_the_latest_surplus_of_one_verdict() -> None:
    kept = [draft(item(f"F{i}.")) for i in range(5)] + [draft(item("C.", "cert"))]
    assert [d.statement for d in trim(kept, 6)] == ["F0.", "F1.", "F2.", "F3.", "C."]
