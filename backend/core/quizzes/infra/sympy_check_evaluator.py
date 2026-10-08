from collections.abc import Sequence

from core.shared.math.infra.sympy_pool import SympyCheckPool
from core.shared.math.sympy_checks import CheckResult, MathCheck, evaluate


class SympyCheckEvaluator:
    """sympy checks under a deadline. With `pool` (long-lived, owned and closed by the composition root) they run in
    its workers and `timeout_s` is the pool's; without one every call spawns and tears down its own workers (one-off
    scripts). `in_process=True` runs inline (tests: no hang protection)."""

    def __init__(self, pool: SympyCheckPool | None = None, timeout_s: float = 25.0, in_process: bool = False) -> None:
        self._pool = pool
        self._timeout_s = timeout_s
        self._in_process = in_process

    def evaluate(self, checks: Sequence[MathCheck]) -> list[CheckResult]:
        if self._pool is not None and not self._in_process:
            return self._pool.evaluate_blocking(checks)
        return evaluate(checks, timeout_s=self._timeout_s, in_process=self._in_process)
