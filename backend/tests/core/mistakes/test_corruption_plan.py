import random

import pytest

from core.mistakes.domain.services.corruption_plan import STATEMENT_KINDS, plan_corruptions
from core.mistakes.domain.values.mistake_kind import PROBLEM_MISTAKE_KINDS, THEORY_MISTAKE_KINDS
from core.mistakes.infra import prompts
from tests.core.mistakes.builders import resolution


@pytest.mark.parametrize("theory", [False, True])
def test_each_chosen_part_gets_a_distinct_valid_kind_and_knows_the_others(theory: bool) -> None:
    valid = THEORY_MISTAKE_KINDS if theory else PROBLEM_MISTAKE_KINDS
    for seed in range(30):
        plans = plan_corruptions(random.Random(seed), [4, 1, 2], theory)
        kinds = {p: plan.kind for p, plan in plans.items()}
        assert sorted(kinds) == [1, 2, 4] and len(set(kinds.values())) == 3 and set(kinds.values()) <= set(valid)
        for part, plan in plans.items():
            assert plan.others == tuple((q, k) for q, k in sorted(kinds.items()) if q != part)
        if theory:
            assert kinds[1] in STATEMENT_KINDS


def test_the_plan_is_a_pure_function_of_the_seed() -> None:
    assert plan_corruptions(random.Random(7), [1, 3], False) == plan_corruptions(random.Random(7), [1, 3], False)
    assert any(
        plan_corruptions(random.Random(s), [1, 3], False) != plan_corruptions(random.Random(0), [1, 3], False)
        for s in range(1, 20)
    )


def test_more_parts_than_kinds_repeat_kinds_instead_of_failing() -> None:
    plans = plan_corruptions(random.Random(1), list(range(1, 9)), False)
    assert len(plans) == 8 and {p.kind for p in plans.values()} == set(PROBLEM_MISTAKE_KINDS)


def test_the_corrupter_is_told_the_preferred_kind_and_the_neighbours() -> None:
    plans = plan_corruptions(random.Random(3), [1, 3], False)
    user = prompts.corruption_user(resolution(), 1, "normal", [], plans[1])
    assert f"Tipus d'error preferit: {plans[1].kind}" in user
    assert f"part 3 ({plans[3].kind})" in user and "naturalesa diferent" in user
    assert "preferit" not in prompts.corruption_user(resolution(), 1, "normal", [])


def test_both_corrupters_ask_for_errors_that_matter_and_the_writers_for_a_math_step() -> None:
    for system in (prompts.PART_CORRUPTION_SYSTEM, prompts.THEORY_PART_CORRUPTION_SYSTEM):
        assert "ha de comptar per a l'argument" in system and "Dolent:" in system and "Bo:" in system
    for system in (prompts.RESOLUTION_SYSTEM, prompts.THEORY_RESOLUTION_SYSTEM):
        assert "almenys un pas matemàtic" in system
        assert "f_{xy}" in system and "primer respecte de $x$ i després respecte de $y$" in system
