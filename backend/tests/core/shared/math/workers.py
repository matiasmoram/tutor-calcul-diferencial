"""Check workers for the pool tests. Module-level so spawned processes can unpickle them."""

import os
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


def allocate_mb(mb: int) -> int:
    """A runaway check: allocates `mb` MB (a MemoryError under the worker's address-space cap)."""
    return len(bytearray(mb * 1024 * 1024))


def die_on_negative(n: int) -> int:
    """A worker killed mid-check (as by the OOM killer) on a negative number."""
    if n < 0:
        os._exit(1)
    return n * n


def address_space_limit(_: int) -> int:
    """The worker's soft RLIMIT_AS (POSIX only)."""
    import resource

    return resource.getrlimit(resource.RLIMIT_AS)[0]
