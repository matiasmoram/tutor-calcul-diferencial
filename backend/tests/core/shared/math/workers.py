"""Check workers for the pool tests. Module-level so spawned processes can unpickle them."""

import time

from core.shared.math.sympy_checks import CheckResult, MathCheck, evaluate_one


def hang_on_description(check: MathCheck) -> CheckResult:
    """Stands in for sympy stuck in a hard limit: never returns in test time when the description is "hang"."""
    if check.description == "hang":
        time.sleep(600)
    return evaluate_one(check)


def hang_on_negative(n: int) -> int:
    """A job other than a check, for `SympyCheckPool.map`: never returns in test time on a negative number."""
    if n < 0:
        time.sleep(600)
    return n * n
