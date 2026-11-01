import pytest

from core.mistakes.domain.services.generation_checks import compare_verification, validate_generation
from core.mistakes.domain.services.locate import locate
from core.mistakes.domain.values.llm_outputs import VerifierFinding
from core.mistakes.infra import prompts
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


def test_with_two_errors_a_consequence_before_the_last_one_means_they_compound() -> None:
    check = validate_generation(draft(gen([err(2, "$x^4 \\ge x^4+y^2$"), err(3, "demostra que el límit existeix")])), 2)
    both = findings(finding(2, "x^4 \\ge"), finding(3, "demostra que"))

    def issues(*extra: JsonObject) -> list[str]:
        return compare_verification(check.mistakes, [*both, *findings(*extra)], check.fragments)

    assert issues() == []
    assert issues(finding(4, "sandvitx", "consequencia"), finding(5, "és $0$", "consequencia")) == []
    # By fragment: the first error's wrong bound reaches the fragment of the second one.
    (issue,) = issues(finding(2, "fitat per $|x|$", "consequencia"))
    assert issue.startswith("un error es propaga fins a un altre error: la conseqüència del fragment 2")
    # Same fragment as the last error: by offset.
    assert len(issues(finding(3, "Això", "consequencia"))) == 1
    assert issues(finding(3, "existeix", "consequencia")) == []
    # One error may change later values: its consequences are not compounding.
    one = validate_generation(draft(gen([err(2, "$x^4 \\ge x^4+y^2$")])), 1)
    assert compare_verification(one.mistakes, findings(finding(2, "x^4"), finding(1, "Provem", "consequencia"))) == []


def test_a_declared_error_the_verifier_only_sees_as_a_consequence_is_not_found() -> None:
    check = validate_generation(draft(gen([err(2, "$x^4 \\ge x^4+y^2$"), err(3, "demostra que el límit existeix")])), 2)
    (issue,) = compare_verification(
        check.mistakes, findings(finding(2, "x^4 \\ge"), finding(3, "demostra que", "consequencia")), check.fragments
    )
    assert issue == (
        "l'error declarat al fragment 3 («demostra que el límit existeix») només hereta un error anterior "
        "(el verificador el veu com una conseqüència): els errors no es poden encadenar"
    )
    one = validate_generation(draft(gen([err(2, "$x^4 \\ge x^4+y^2$")])), 1)
    assert "només hereta" in compare_verification(one.mistakes, findings(finding(2, "x^4", "consequencia")))[0]


def test_a_stored_document_whose_last_error_inherits_the_first_is_rejected() -> None:
    """t3-5/normal/803c38a241d4: the conclusion (fragment 8) restates the wrong continuity at the origin (fragment 3)."""
    origin = (
        "3. A l'origen, sobre qualsevol recta $y=mx$ amb $m\\neq 0$ s'obté $f(x,mx)=x/m\\to 0$, i sobre l'eix $y=0$ "
        "també val $0$. Així, el límit a $(0,0)$ és $0=f(0,0)$ i $f$ és contínua a l'origen."
    )
    conclusion = (
        "8. En conclusió, $f$ és contínua a $\\{y\\neq0\\}\\cup\\{(0,0)\\}$ i és discontínua a la resta de l'eix $y=0$."
    )
    frags = ["1. Pas.", "2. Pas.", origin, "4. Pas.", "5. Pas.", "6. Pas.", "7. Pas.", conclusion]
    stored = [err(3, "el límit a $(0,0)$ és $0=f(0,0)$"), err(8, "$f$ és contínua a $\\{y\\neq0\\}\\cup\\{(0,0)\\}$")]
    check = validate_generation(draft(gen(stored, frags)), 2)
    assert check.valid, check.problems
    verified = findings(
        finding(
            3,
            "el límit a $(0,0)$ és $0=f(0,0)$ i $f$ és contínua a l'origen",
            "error",
            "les rectes no decideixen el límit",
        ),
        finding(8, "$f$ és contínua a $\\{y\\neq0\\}\\cup\\{(0,0)\\}$", "consequencia", "hereta el pas 3"),
    )
    (issue,) = compare_verification(check.mistakes, verified, check.fragments)
    assert issue.startswith("l'error declarat al fragment 8") and "només hereta un error anterior" in issue


def test_the_sencer_prompts_forbid_compounding_errors() -> None:
    for system in (prompts.GENERATION_SYSTEM, prompts.THEORY_GENERATION_SYSTEM):
        assert "Els errors no es poden encadenar" in system and "situat més avall al document" in system
    assert "una afirmació certa amb una justificació falsa o insuficient" in prompts.GENERATION_SYSTEM


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


def test_a_second_error_inside_a_declared_fragment_is_unintended() -> None:
    check = validate_generation(draft(gen([err(2, "$x^4 \\ge x^4+y^2$")])), 1)
    other = findings(finding(2, "x^4 \\ge"), finding(2, "el quocient està fitat per $|x|$", "error", "fita falsa"))
    issues = compare_verification(check.mistakes, other, check.fragments)
    assert issues == ["hi ha un error NO intencionat al fragment 2: «el quocient està fitat per $|x|$» — fita falsa"]
    # A consequence of the declared error in its own fragment is not a new error.
    consequence = findings(finding(2, "x^4 \\ge"), finding(2, "fitat per $|x|$", "consequencia"))
    assert compare_verification(check.mistakes, consequence, check.fragments) == []


def test_an_empty_fragment_is_rejected_and_never_renumbers_the_errors() -> None:
    frags = [FRAGS[0], "   ", *FRAGS[1:]]
    check = validate_generation(draft(gen([err(3, "$x^4 \\ge x^4+y^2$")], frags)), 1)
    assert check.problems == ["el fragment 2 és buit"]
    assert len(check.fragments) == 6 and check.mistakes[0].fragment == 3
    assert check.fragments[2][check.mistakes[0].start : check.mistakes[0].end] == "$x^4 \\ge x^4+y^2$"


def test_invented_latex_commands_are_rejected_wherever_they_appear() -> None:
    """What gpt-5.6-luna produced and both the old validation and the verifier let through."""
    frags = [*FRAGS[:4], r"Per tant el límit és $e^{\fterm{0.2}}\blink$."]
    bad = err(5, r"$e^{\fterm{0.2}}\blink$") | {"explicacio": r"cal $\term{x}$", "pista": r"i el \freelance?"}
    problems = validate_generation(draft(gen([bad], frags)), 1).problems
    assert problems == [
        "el fragment 5 fa servir ordres LaTeX que no existeixen (\\blink, \\fterm); "
        "fes servir només ordres estàndard de LaTeX/KaTeX",
        "el camp 'cita' de l'error 1 fa servir ordres LaTeX que no existeixen (\\blink, \\fterm); "
        "fes servir només ordres estàndard de LaTeX/KaTeX",
        "el camp 'explicacio' de l'error 1 fa servir ordres LaTeX que no existeixen (\\term); "
        "fes servir només ordres estàndard de LaTeX/KaTeX",
        "el camp 'pista' de l'error 1 fa servir ordres LaTeX que no existeixen (\\freelance); "
        "fes servir només ordres estàndard de LaTeX/KaTeX",
    ]
    ok = err(2, "$x^4 \\ge x^4+y^2$") | {"correccio": r"$x^4 \le x^4+y^2$, amb $\frac{x^4}{x^4+y^2}\le 1$"}
    assert validate_generation(draft(gen([ok])), 1).valid


def test_the_fragment_count_message_states_the_accepted_range() -> None:
    problems = validate_generation(draft(gen([err(2, "fitat")], FRAGS[:3])), 1).problems
    assert "el nombre de fragments ha de ser entre 4 i 14 (n'hi ha 3)" in problems
    assert validate_generation(draft(gen([err(2, "fitat")], FRAGS[:4])), 1).valid
