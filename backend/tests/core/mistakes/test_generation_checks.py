import pytest

from core.mistakes.domain.generation_checks import compare_verification, validate_generation
from core.mistakes.domain.locate import locate
from core.mistakes.domain.values.llm_outputs import VerifierFinding
from core.shared.llm.client import JsonObject
from tests.core.mistakes.builders import FRAGS, draft, err, finding, gen, terr, tgen


def findings(*items: JsonObject) -> list[VerifierFinding]:
    return [VerifierFinding.model_validate(i) for i in items]


def test_locate_tolerates_whitespace_only() -> None:
    assert locate("a  b   c", "a b c") == (0, 8)
    assert locate("abc", "abd") is None


def test_validation_accepts_well_formed_generation() -> None:
    check = validate_generation(draft(gen([err(2, "$x^4 \\ge x^4+y^2$"), err(3, "demostra que el límit existeix")])), 2)
    assert check.problems == [] and check.valid
    first = check.mistakes[0]
    assert first.quote == "$x^4 \\ge x^4+y^2$" and check.fragments[1][first.start : first.end] == first.quote


@pytest.mark.parametrize(
    ("errors", "n", "expected"),
    [
        ([err(2, "$x^4 \\ge x^4+y^2$")], 2, "exactament 2 errors"),
        ([err(2, "$x^4 \\ge x^4+y^2$"), err(2, "fitat")], 2, "dos errors al fragment 2"),
        ([err(9, "x")], 1, "fragment inexistent"),
        ([err(1, "text que no hi és")], 1, "no apareix literalment"),
    ],
)
def test_validation_rejects(errors: list[JsonObject], n: int, expected: str) -> None:
    problems = validate_generation(draft(gen(errors)), n).problems
    assert any(expected in p for p in problems), problems


def test_validation_rejects_unbalanced_math() -> None:
    frags = [*FRAGS[:4], "Per tant el límit és $0."]
    problems = validate_generation(draft(gen([err(2, "fitat")], frags)), 1).problems
    assert any("senar" in p for p in problems)


def test_display_math_is_rejected() -> None:
    frags = [*FRAGS[:4], "Per tant el límit és $$0$$."]
    problems = validate_generation(draft(gen([err(2, "fitat")], frags)), 1).problems
    assert any("$$" in p for p in problems)


def test_a_malformed_fragment_number_is_a_rejection_reason_not_a_crash() -> None:
    problems = validate_generation(draft(gen([err(2, "fitat") | {"fragment": "2"}])), 1).problems
    assert any("fragment inexistent (2)" in p for p in problems)


def test_verification_must_find_all_declared_and_nothing_else() -> None:
    mistakes = validate_generation(draft(gen([err(2, "$x^4 \\ge x^4+y^2$")])), 1).mistakes
    ok = findings(finding(2, "x"), finding(5, "y", "consequencia"), finding(1, "z", "imprecisio"))
    assert compare_verification(mistakes, ok) == []
    missing = compare_verification(mistakes, [])
    assert "no l'ha detectat" in missing[0]
    extra = compare_verification(mistakes, [*ok, *findings(finding(3, "demostra", "error", "salt"))])
    assert "NO intencionat" in extra[0]


def test_a_different_problem_in_the_same_fragment_does_not_confirm_the_declared_one() -> None:
    check = validate_generation(draft(gen([err(2, "$x^4 \\ge x^4+y^2$")])), 1)
    elsewhere = findings(finding(2, "el quocient està fitat per $|x|$"))
    assert "no l'ha detectat" in compare_verification(check.mistakes, elsewhere, check.fragments)[0]
    on_it = findings(finding(2, "x^4 \\ge"))
    assert compare_verification(check.mistakes, on_it, check.fragments) == []


def test_theory_validation_requires_statement_error_and_split() -> None:
    ok = tgen(
        [terr(2, r"de classe $\mathcal{C}^1$", "conclusio"), terr(5, "les parcials són contínues", "pas_injustificat")]
    )
    check = validate_generation(draft(ok), 2, theory=True)
    assert check.problems == [] and len(check.mistakes) == 2 and check.statement_fragments == 2
    # Both errors in the proof: the statement must carry one.
    p = validate_generation(
        draft(tgen([terr(4, "Per la definició", "pas_injustificat"), terr(5, "són contínues", "pas_injustificat")])),
        2,
        theory=True,
    ).problems
    assert any("enunciat" in x for x in p)
    # Two errors, both in the statement: one must be in the proof.
    p = validate_generation(
        draft(tgen([terr(1, "diferenciable"), terr(2, "de classe", "conclusio")])), 2, True
    ).problems
    assert any("demostració" in x for x in p)
    # n_enunciat must leave a proof.
    p = validate_generation(draft(tgen([terr(1, "diferenciable")], n_enunciat=4)), 1, theory=True).problems
    assert any("n_enunciat" in x for x in p)
    # Problem error types are not valid for theory documents and vice versa.
    p = validate_generation(draft(tgen([terr(1, "diferenciable", "teorema_mal_aplicat")])), 1, theory=True).problems
    assert any("tipus no vàlid" in x for x in p)
