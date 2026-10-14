from collections.abc import Iterator
from concurrent.futures.process import BrokenProcessPool

import pytest

from core.quizzes.domain.entities.grading import StudentCheck
from core.quizzes.infra.sympy_check_evaluator import SympyCheckEvaluator
from core.shared.math.infra.sympy_pool import UNAVAILABLE_DETAIL, SympyCheckPool
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


def test_a_closed_pool_leaves_the_checks_undecided() -> None:
    """At shutdown the pool is closed under a running grading: its checks are undecided, not a 500 after paid work."""
    pool = SympyCheckPool(max_workers=1)
    pool.close()
    evaluator = SympyCheckEvaluator(pool)
    [result] = evaluator.evaluate([ITERATED])
    assert result.status == "indeterminat" and result.detail == UNAVAILABLE_DETAIL
    claim = StudentCheck.model_validate(
        check("igualtat", "1", "1", variable="", point="").model_dump() | {"quote": "1"}
    )
    assert evaluator.faithful([claim]) == [False]


def test_workers_that_keep_dying_leave_the_checks_undecided(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = SympyCheckPool(max_workers=1)

    def broken(*_: object) -> None:
        raise BrokenProcessPool("sympy workers keep dying at start-up")

    monkeypatch.setattr(pool, "_submit", broken)
    assert [r.status for r in SympyCheckEvaluator(pool).evaluate([ITERATED, ITERATED])] == ["indeterminat"] * 2
