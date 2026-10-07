from collections.abc import Iterator

import pytest

from core.quizzes.infra.sympy_check_evaluator import SympyCheckEvaluator
from core.shared.math.infra.sympy_pool import SympyCheckPool
from tests.core.shared.math.test_sympy_checks import ITERATED, check


@pytest.fixture
def pool() -> Iterator[SympyCheckPool]:
    p = SympyCheckPool(max_workers=1)
    yield p
    p.close()


def test_evaluators_share_the_composition_roots_pool(pool: SympyCheckPool) -> None:
    first, second = SympyCheckEvaluator(pool), SympyCheckEvaluator(pool)
    assert [r.status for r in first.evaluate([ITERATED])] == ["ok"]
    executor = pool._executor
    assert [r.status for r in second.evaluate([check("no_limit", "sin(1/x)")])] == ["ok"]
    assert executor is not None and pool._executor is executor


def test_in_process_evaluator_runs_inline() -> None:
    assert [r.status for r in SympyCheckEvaluator(in_process=True).evaluate([ITERATED])] == ["ok"]
