from collections.abc import Sequence

from loguru import logger

from core.quizzes.domain.entities.grading import StudentCheck
from core.quizzes.domain.ports import CheckEvaluator
from core.quizzes.domain.services.scoring import faithful
from core.shared.math.infra.sympy_pool import POOL_UNAVAILABLE, UNAVAILABLE_DETAIL, SympyCheckPool
from core.shared.math.sympy_checks import CheckResult, MathCheck, evaluate


class SympyCheckEvaluator(CheckEvaluator):
    """sympy checks under a deadline. With `pool` (long-lived, owned and closed by the composition root) they run in
    its workers and `timeout_s` is the pool's; without one every call spawns and tears down its own workers (one-off
    scripts). `in_process=True` runs inline (tests: no hang protection).

    A pool that cannot take the checks (workers dying at start-up, closed at shutdown) gives every check the result
    of one that timed out: the paid model work around them still stands, as when a single check fails."""

    def __init__(self, pool: SympyCheckPool | None = None, timeout_s: float = 25.0, in_process: bool = False) -> None:
        self._pool = pool
        self._timeout_s = timeout_s
        self._in_process = in_process

    def evaluate(self, checks: Sequence[MathCheck]) -> list[CheckResult]:
        if self._pool is not None and not self._in_process:
            try:
                return self._pool.evaluate_blocking(checks)
            except POOL_UNAVAILABLE as e:
                logger.error("sympy pool unavailable, {} checks undecided: {!r}", len(checks), e)
                return [CheckResult(status="indeterminat", detail=UNAVAILABLE_DETAIL) for _ in checks]
        return evaluate(checks, timeout_s=self._timeout_s, in_process=self._in_process)

    def faithful(self, claims: Sequence[StudentCheck]) -> list[bool]:
        if self._in_process:
            return [faithful(c) for c in claims]
        if self._pool is not None:
            return _faithful_in(self._pool, claims)
        pool = SympyCheckPool(max_workers=min(4, max(1, len(claims))), timeout_s=self._timeout_s)
        try:
            return _faithful_in(pool, claims)
        finally:
            pool.close()


def _faithful_in(pool: SympyCheckPool, claims: Sequence[StudentCheck]) -> list[bool]:
    try:
        return pool.map_blocking(faithful, claims, _not_faithful)
    except POOL_UNAVAILABLE as e:
        logger.error("sympy pool unavailable, {} claims not run: {!r}", len(claims), e)
        return [False for _ in claims]


def _not_faithful(_claim: StudentCheck, _reason: str) -> bool:
    # Timed out or crashed: the claim is not run, so it can neither lower nor raise the grade.
    return False
