"""Policy invariants fuzzed over a sample of real sheets (scripts/fuzz_politica.py does the full run)."""

import importlib.util
from types import ModuleType

import pytest

from settings import ROOT_DIR
from tests.fixtures.course import authored_course


def _load_script(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, ROOT_DIR / "scripts" / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fuzz_politica = _load_script("fuzz_politica")
COURSE = authored_course()
SAMPLE = sorted(COURSE.exercises)[::11]  # ~30 exercises across all topics


@pytest.mark.parametrize("ex_id", SAMPLE)
def test_policy_invariants_hold_under_random_sessions(ex_id: str) -> None:
    violations: list[str] = []
    for profile, seeds in (("random", 6), ("stuck_trying", 2), ("beggar", 2)):
        for seed in range(seeds):
            violations += fuzz_politica.check(COURSE, COURSE.exercise(ex_id), seed, 16, profile)
    assert not violations, violations[:3]
