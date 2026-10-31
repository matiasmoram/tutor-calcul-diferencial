"""The authoring validator (scripts/check_fitxes.py) over the authored sheets."""

from tests.fixtures.course import authored_course
from tests.scripts.loader import load_script

check_fitxes = load_script("check_fitxes")


def test_every_sheet_passes_the_authoring_checks() -> None:
    course = authored_course()
    bad = {ex.id: check_fitxes.problems_of(ex, course) for ex in course.exercises.values()}
    assert not {k: v for k, v in bad.items() if v}


def test_a_sheet_breaking_the_rules_is_reported() -> None:
    course = authored_course()
    ex = course.exercise("t2-4c")
    step = ex.steps[0]
    broken = ex.model_copy(
        update={
            "steps": [step.model_copy(update={"idea": step.detail, "leak_patterns": ["$^"]})],
            "statement": "$x",
        }
    )
    problems = check_fitxes.problems_of(broken, course)
    assert "needs at least 2 steps" in problems
    assert "enunciat: unbalanced $" in problems
    assert f"step {step.id}: no leak regex matches its own detall" in problems
