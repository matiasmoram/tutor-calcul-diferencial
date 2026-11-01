import pytest

from core.course.domain.entities.exercise import Exercise
from core.mistakes.domain.exceptions import MistakePartsUnavailableException
from core.mistakes.domain.services.locate import locate_all, occurrences
from core.mistakes.domain.services.part_checks import (
    CorruptionCheck,
    check_corruption,
    check_resolution,
    part_verification_problems,
    require_parts,
    resolution_verification_problems,
)
from core.mistakes.domain.values.llm_outputs import CorruptionDraft, PartReport, ResolutionDraft, ResolutionReport
from core.mistakes.domain.values.mistake_source import ProblemSource
from core.shared.llm.client import JsonObject
from tests.core.mistakes.builders import (
    PART2_ERROR,
    PARTS,
    THEORY_PARTS,
    THEORY_STATEMENT,
    corruption,
    edit,
    finding,
    part_checked,
    parted,
    problem_source,
    resolution,
    resolution_checked,
    theory_source,
    theory_written,
    written,
)

CLEAN = PARTS[1][1]  # part 2 of the test resolution, correct


def resolution_problems(data: JsonObject, theory: bool = False) -> list[str]:
    source = theory_source() if theory else problem_source()
    return check_resolution(ResolutionDraft.model_validate(data), source).problems


def test_a_problem_resolution_follows_the_sheet_steps() -> None:
    check = check_resolution(ResolutionDraft.model_validate(written()), problem_source())
    assert check.valid and check.resolution.statement_fragments == 0
    assert [(p.step, p.title) for p in check.resolution.parts] == [
        ("candidat", "Trobar un candidat"),
        ("acotar", "Acotar el quocient"),
        ("concloure", "Concloure amb el sandvitx"),
    ]
    assert check.resolution.first_fragment(3) == 5 and len(check.resolution.fragments) == 6
    # A long step may take two consecutive parts.
    split = [PARTS[0], ("acotar", CLEAN[:1]), ("acotar", CLEAN[1:]), PARTS[2]]
    assert resolution_problems(written(split)) == []


@pytest.mark.parametrize(
    ("parts", "expected"),
    [
        ([PARTS[1], PARTS[0], PARTS[2]], "seguir els passos de la solució en ordre"),
        ([PARTS[0], PARTS[2]], "seguir els passos"),
        ([PARTS[0], PARTS[1], PARTS[0], PARTS[2]], "seguir els passos"),
        ([PARTS[0], *[("acotar", CLEAN[:1])] * 3, PARTS[2]], "el pas acotar té 3 parts"),
        ([PARTS[0], ("acotar", [*CLEAN, *CLEAN, "Més."]), PARTS[2]], "la part 2 ha de tenir entre 1 i 4 fragments"),
        ([PARTS[0], ("acotar", []), PARTS[2]], "la part 2 ha de tenir entre 1 i 4 fragments (en té 0)"),
        ([PARTS[0], ("acotar", ["Amb $x"]), PARTS[2]], "el fragment 1 de la part 2 té un nombre senar de '$'"),
        ([PARTS[0], ("acotar", ["  "]), PARTS[2]], "el fragment 1 de la part 2 és buit"),
        ([PARTS[0], ("acotar", [r"Amb $\fterm{x}$."]), PARTS[2]], "el fragment 1 de la part 2 fa servir ordres LaTeX"),
        ([], "calen com a mínim 2 parts"),
    ],
)
def test_resolution_gates(parts: list[tuple[str, list[str]]], expected: str) -> None:
    problems = resolution_problems(written(parts))
    assert any(expected in p for p in problems), problems


def test_a_theory_resolution_is_the_statement_then_2_to_5_titled_stages() -> None:
    check = check_resolution(ResolutionDraft.model_validate(theory_written()), theory_source())
    assert check.valid and check.resolution.statement_fragments == 1
    assert [p.title for p in check.resolution.parts] == ["Enunciat", "Derivades direccionals", "Conclusió"]
    assert any("entre 2 i 5 parts" in p for p in resolution_problems(theory_written(parts=THEORY_PARTS[:1]), True))
    assert any(
        "l'enunciat ha de tenir entre 1 i 3" in p
        for p in resolution_problems(theory_written(statement=THEORY_STATEMENT * 4), True)
    )
    untitled = theory_written(parts=[("", THEORY_PARTS[0][1]), THEORY_PARTS[1]])
    assert "la part 1 de la demostració no té títol" in resolution_problems(untitled, True)


def test_the_blind_check_of_the_resolution_finds_nothing_and_reaches_the_result() -> None:
    clean = resolution()
    ok = ResolutionReport.model_validate(resolution_checked(True, finding(2, "candidat", "imprecisio")))
    assert resolution_verification_problems(clean, ok, theory=False) == []
    wrong = ResolutionReport.model_validate(resolution_checked(True, finding(4, "Per tant", "consequencia", "hereta")))
    assert resolution_verification_problems(clean, wrong, theory=False) == [
        "hi ha un error a la part 2, fragment 2: «Per tant» — hereta"
    ]
    short = ResolutionReport.model_validate(resolution_checked(False))
    assert resolution_verification_problems(clean, short, theory=False) == [
        "la resolució no arriba al resultat correcte de la solució de referència"
    ]
    assert "enunciat complet" in resolution_verification_problems(clean, short, theory=True)[0]


def test_a_problem_with_a_single_step_has_no_parts() -> None:
    source = problem_source()
    single = Exercise.model_validate(source.exercise.model_dump() | {"steps": source.exercise.steps[:1]})
    with pytest.raises(MistakePartsUnavailableException) as e:
        require_parts(ProblemSource(exercise=single, theory=[], with_proof=frozenset()))
    assert e.value.error_code == 422
    require_parts(source)
    require_parts(theory_source())


def corrupt(data: JsonObject, clean: list[str] = CLEAN, theory: bool = False) -> CorruptionCheck:
    return check_corruption(clean, CorruptionDraft.model_validate(data), 3, "e1", theory)


def test_a_corruption_is_applied_by_code_and_its_error_numbered_in_the_document() -> None:
    check = corrupt(PART2_ERROR)
    assert check.valid and not check.unfit
    assert check.flawed_fragments == ["Com que $x^4 \\ge x^4+y^2$, el quocient està fitat per $|x|$.", CLEAN[1]]
    m = check.mistake
    assert m is not None and m.fragment == 3 and m.quote == "$x^4 \\ge x^4+y^2$" and m.id == "e1"
    assert check.flawed_fragments[0][m.start : m.end] == m.quote and m.hint == "pista 2"
    # A local consequence later in the part.
    both = corrupt(
        corruption(
            [edit(1, "x^4 \\le", "x^4 \\ge"), edit(2, "|f(x,y)|\\le |x|", "|f(x,y)|\\ge |x|")], "x^4 \\ge x^4+y^2"
        )
    )
    assert both.valid and both.flawed_fragments[1] == "Per tant $|f(x,y)|\\ge |x|$."


def test_a_deletion_is_an_edit_too() -> None:
    check = corrupt(corruption([edit(1, ", el quocient", "")], "y^2$ està fitat"))
    assert check.valid and check.flawed_fragments[0] == "Com que $x^4 \\le x^4+y^2$ està fitat per $|x|$."


def test_an_unfit_part_is_not_a_failed_attempt() -> None:
    check = corrupt(corruption([], "", apte=False))
    assert check.unfit and check.mistake is None and check.problems


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (corruption([], "x"), "calen entre 1 i 3 canvis (n'hi ha 0)"),
        (corruption([edit(1, "Com", "Amb")] * 4, "Amb"), "calen entre 1 i 3 canvis"),
        (corruption([edit(3, "Com", "Amb")], "Amb"), "el canvi 1 apunta a un fragment inexistent (3)"),
        (corruption([edit(1, "x^4", "x^5")], "x^5"), "exactament una vegada"),
        (corruption([edit(1, "no hi és", "x")], "x"), "exactament una vegada"),
        (corruption([edit(1, "Com que", "Com que")], "Com que"), "el canvi 1 no canvia res"),
        (
            corruption([edit(1, "x^4 \\le", "x^4 \\ge"), edit(1, "\\le x^4+y^2", "\\ge x^4")], "x^4 \\ge"),
            "els canvis 1 i 2 se solapen",
        ),
        (
            corruption([edit(2, "Per tant", "Llavors"), edit(1, "x^4 \\le", "x^4 \\ge")], "Llavors"),
            "el primer canvi és l'error i ha de ser el primer de la part",
        ),
        (corruption([edit(1, "Com que $x^4 \\le x^4+y^2$", "Com que " + "a" * 250)], "aaaa"), "massa grans"),
        (corruption([edit(1, "x^4 \\le", "x^4 \\ge$")], "x^4 \\ge"), "el fragment 1 té un nombre senar de '$'"),
        (corruption([edit(1, "x^4 \\le", "x^4 \\ge")], "x^4 \\ge", tipus="quantificador"), "el tipus no és vàlid"),
        (corruption([edit(1, "Com que", "Potser com que")], "Potser com que"), "assenyala l'error"),
        (corruption([edit(1, "x^4 \\le", "x^4 \\ge")], "el quocient està fitat"), "la cita ha de ser el text erroni"),
        (corruption([edit(1, "x^4 \\le", "x^4 \\ge")], "x^4 \\le"), "la cita ha de ser el text erroni"),
        (corruption([edit(1, "x^4 \\le", "x^4 \\ge")], "x^4 \\ge", pista=""), "falta el camp 'pista'"),
        (
            corruption([edit(1, "x^4 \\le", "x^4 \\ge")], "x^4 \\ge", pista=r"i el \freelance?"),
            "el camp 'pista' fa servir ordres LaTeX que no existeixen",
        ),
    ],
)
def test_corruption_gates(data: JsonObject, expected: str) -> None:
    check = corrupt(data)
    assert not check.valid and check.mistake is None
    assert any(expected in p for p in check.problems), check.problems


def test_locate_all_finds_every_occurrence() -> None:
    assert locate_all("aba aba", "aba") == [(0, 3), (4, 7)]
    assert locate_all("ababa", "aba") == [(0, 3), (2, 5)]
    assert locate_all("a  b, a b", "a b") == [(6, 9)]
    assert locate_all("a  b, a\nb", "a b") == [(0, 4), (6, 9)]
    assert locate_all("abc", " ") == [] and occurrences("$+-+-+$", "+-+") == [1, 3]


def test_a_quote_whose_text_also_appears_earlier_is_placed_on_the_edit() -> None:
    clean = ["El valor és $2$ i el doble és $4$."]
    check = check_corruption(
        clean, CorruptionDraft.model_validate(corruption([edit(1, "$4$", "$2$")], "$2$")), 1, "e1", False
    )
    assert check.valid and check.mistake is not None
    assert (check.mistake.start, check.mistake.end) == (30, 33) and check.flawed_fragments[0][30:33] == "$2$"


def test_an_original_that_overlaps_itself_is_not_unique() -> None:
    clean = ["Sumem $a+a+a$ i obtenim $3a$."]
    check = check_corruption(
        clean, CorruptionDraft.model_validate(corruption([edit(1, "a+a", "a-a")], "a-a")), 1, "e1", False
    )
    assert any("hi apareix 2 vegades" in p for p in check.problems), check.problems


def test_edits_that_undo_each_other_are_refused() -> None:
    check = corrupt(corruption([edit(1, "Com", "Com que"), edit(1, " que $x^4", " $x^4")], "Com que $x^4"))
    assert check.flawed_fragments[0] == CLEAN[0] and check.mistake is None
    assert "els canvis es desfan entre ells i el fragment 1 queda igual que el correcte" in check.problems


def test_only_words_that_point_at_the_error_are_markers() -> None:
    ordinary = corrupt(corruption([edit(1, "Com que", "Tenint en compte que")], "Tenint en compte que $x^4 \\le"))
    assert ordinary.valid, ordinary.problems
    for marker in ("Compte: com que", "Crec que com que", "Com que (error)"):
        check = corrupt(corruption([edit(1, "Com que", marker)], marker))
        assert any("assenyala l'error" in p for p in check.problems), marker


def test_an_edit_larger_than_half_the_part_is_refused() -> None:
    short = ["Per tant el límit és $0$."]
    check = check_corruption(
        short,
        CorruptionDraft.model_validate(corruption([edit(1, "Per tant el límit", "Doncs el valor del límit")], "límit")),
        1,
        "e1",
        False,
    )
    assert any("massa grans" in p for p in check.problems)


def checked_part(*findings: JsonObject, alert: str = "") -> list[str]:
    doc = parted()
    part = doc.parts[1]
    assert part.mistake is not None and part.flawed_fragments is not None
    report = PartReport.model_validate(part_checked(*findings, alert=alert))
    return part_verification_problems(part.mistake, 3, part.flawed_fragments, report)


def test_the_blind_part_check_must_find_exactly_the_declared_error() -> None:
    assert checked_part(finding(1, "x^4 \\ge")) == []
    assert checked_part(finding(1, ""), finding(1, "Com que", "imprecisio")) == []
    assert "no l'ha detectat" in checked_part(finding(1, "el quocient està fitat per $|x|$"))[0]
    assert "no l'ha detectat" in checked_part()[0]
    unintended = checked_part(finding(1, "x^4 \\ge"), finding(2, "Per tant", "error", "salt"))
    assert unintended == ["hi ha un error NO intencionat al fragment 2: «Per tant» — salt"]
    assert "més d'un error" in checked_part(finding(1, "x^4 \\ge"), finding(1, "\\ge x^4"))[0]


def test_consequences_come_after_the_error_and_the_context_is_not_questioned() -> None:
    assert checked_part(finding(1, "x^4 \\ge"), finding(2, "|f(x,y)|", "consequencia")) == []
    before = checked_part(finding(1, "x^4 \\ge"), finding(1, "Com que", "consequencia"))
    assert before == [
        "la conseqüència del fragment 1 («Com que») és anterior a l'error: les conseqüències han de venir després de l'error"
    ]
    alert = checked_part(finding(1, "x^4 \\ge"), alert="el candidat de la part 1 és fals")
    assert alert == ["el verificador creu que les parts anteriors tenen un error: el candidat de la part 1 és fals"]
