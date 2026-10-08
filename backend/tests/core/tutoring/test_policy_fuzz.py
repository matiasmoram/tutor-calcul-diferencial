"""Policy invariants fuzzed over a sample of real sheets (the invariants are listed in policy_fuzzer.py)."""

import pytest

from tests.core.tutoring.builders import COURSE
from tests.core.tutoring.policy_fuzzer import check

SAMPLE = sorted(COURSE.exercises)[::11]  # ~30 exercises across all topics


@pytest.mark.parametrize("ex_id", SAMPLE)
def test_policy_invariants_hold_under_random_sessions(ex_id: str) -> None:
    violations: list[str] = []
    for profile, seeds in (("random", 6), ("stuck_trying", 2), ("beggar", 2)):
        for seed in range(seeds):
            violations += check(COURSE, COURSE.exercise(ex_id), seed, 16, profile)
    assert not violations, violations[:3]
