from collections.abc import Sequence

from core.shared.math.sympy_checks import CheckResult, MathCheck, evaluate


class SympyCheckEvaluator:
    """sympy in worker processes under a deadline; `in_process=True` runs inline (tests: no hang protection)."""

    def __init__(self, timeout_s: float = 25.0, in_process: bool = False) -> None:
        self._timeout_s = timeout_s
        self._in_process = in_process

    def evaluate(self, checks: Sequence[MathCheck]) -> list[CheckResult]:
        return evaluate(checks, timeout_s=self._timeout_s, in_process=self._in_process)
