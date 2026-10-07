"""The authoring validator (scripts/check_fitxes.py) over the authored sheets."""

import importlib.util
from types import ModuleType

from settings import ROOT_DIR
from tests.fixtures.course import authored_course


def _load_script(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, ROOT_DIR / "scripts" / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_fitxes = _load_script("check_fitxes")


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
