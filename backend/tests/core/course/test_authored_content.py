"""The authored sheets and notes: they load, cite existing theory, and their leak regexes are consistent."""

import re

import pytest

from core.course.domain.entities.course import Course
from core.course.domain.entities.exercise import Exercise
from core.course.domain.exceptions import ExerciseNotFoundException, InvalidCourseContentException
from core.shared.math.latex_cas import leaked
from tests.fixtures.course import authored_course

COURSE = authored_course()
EXERCISE_IDS = sorted(COURSE.exercises)


def test_all_sheets_load_and_cite_existing_theory() -> None:
    assert {f"t2-4{c}" for c in "abcdefg"} <= set(COURSE.exercises)
    assert len(COURSE.topics) == 6 and len(COURSE.theory) >= 200
    for ex in COURSE.exercises.values():
        assert ex.all_refs(), ex.id
        assert all(r.item_id in COURSE.theory for r in ex.all_refs()), ex.id


def test_an_unknown_theory_reference_is_rejected() -> None:
    ex = COURSE.exercise("t2-4c")
    broken = Exercise.model_validate(ex.model_dump() | {"theory": [*ex.theory, "T2.999"]})
    with pytest.raises(InvalidCourseContentException):
        Course(topics=COURSE.topics, theory=COURSE.theory, sheets=COURSE.sheets, exercises={ex.id: broken})


@pytest.mark.parametrize("ex_id", EXERCISE_IDS)
def test_step_leak_regexes_match_their_own_detail(ex_id: str) -> None:
    """At least one leak regex per step must catch the step's own detail (others cover alternate notations)."""
    for step in COURSE.exercise(ex_id).steps:
        if step.leak_patterns:
            assert any(re.search(p, step.detail, re.IGNORECASE) for p in step.leak_patterns), (ex_id, step.id)


@pytest.mark.parametrize("ex_id", EXERCISE_IDS)
def test_hint_texts_do_not_contain_their_own_banned_content(ex_id: str) -> None:
    """Objective (level 1) and idea (level 2) are shown below level 3, where the step's leak regexes apply."""
    for step in COURSE.exercise(ex_id).steps:
        for pattern in step.leak_patterns:
            for text in (step.objective, step.idea):
                assert not re.search(pattern, text, re.IGNORECASE), (ex_id, step.id, pattern)


@pytest.mark.parametrize("ex_id", EXERCISE_IDS)
def test_hint_texts_do_not_reveal_the_final_result(ex_id: str) -> None:
    ex = COURSE.exercise(ex_id)
    for step in ex.steps:
        for pattern in ex.result.leak_patterns:
            for text in (step.objective, step.idea):
                assert not re.search(pattern, text, re.IGNORECASE), (ex_id, step.id, pattern)


def test_sheets_group_their_exercises_by_problem() -> None:
    assert set(COURSE.sheets) <= {f"tema-{n}" for n in range(1, 7)} and "tema-2" in COURSE.sheets
    assert all(COURSE.exercise(e).sheet_id == sid for sid, s in COURSE.sheets.items() for e in s.exercise_ids)
    p4 = next(p for p in COURSE.sheet("tema-2").problems if p.number == 4)
    assert p4.exercise_ids == [f"t2-4{c}" for c in "abcdefg"]
    ex = COURSE.exercise("t2-4c")
    assert ex.problem == 4 and ex.part == "c" and ex.label == "4(c)"
    assert ex.statement_md().startswith(ex.preamble.strip()) and "(c)" in ex.statement_md()


def test_unknown_ids_raise_not_found() -> None:
    with pytest.raises(ExerciseNotFoundException) as e:
        COURSE.exercise("t9-99")
    assert e.value.error_code == 404


def test_reserved_ids_include_items_of_the_notes_that_cite_the_problem() -> None:
    ex = COURSE.exercise("t2-4c")
    some = COURSE.theory[ex.all_refs()[0].item_id]
    fake = some.model_copy(update={"id": "T2.999", "problems": ["T2.4"]})
    course = COURSE.model_copy(update={"theory": {**COURSE.theory, "T2.999": fake}})
    assert "T2.999" in course.reserved_ids(ex)
    assert {r.item_id for r in ex.reserved_theory} <= COURSE.reserved_ids(ex)


def test_citable_items_are_the_numbered_non_exercise_items_of_a_topic() -> None:
    items = COURSE.citable_items(3)
    assert items and all(it.topic == 3 and it.number is not None and it.kind != "exercici" for it in items)


def test_cas_leak_check_on_a_real_sheet() -> None:
    ex = COURSE.exercise("t3-1a")
    detail_x = ex.step("parcial_x").detail
    draft = r"Si simplifiques el numerador, obtens $\frac{-4\,x\,y^{2}}{\left(x^{2}-y^{2}\right)^{2}}$, veritat?"
    assert leaked(draft, [detail_x, ex.result.value], [ex.statement_md()])
    # The hint texts of the sheet do not leak the step's detail.
    for i, step in enumerate(ex.steps):
        forbidden = [s.detail for s in ex.steps[i:]] + [ex.result.value]
        assert leaked(step.objective + step.idea, forbidden, [ex.statement_md()]) == []
