from collections.abc import Sequence

from core.counterexamples.domain.services.property_deciders import check_property, undecided
from core.counterexamples.domain.values.submission import PropertyCheck
from core.counterexamples.domain.values.verdict import PropertyVerdict
from core.shared.math.infra.sympy_pool import SympyCheckPool


class PoolPropertyChecker:
    """Each property in its own worker under the pool's deadline: one that hangs comes back 'indeterminat' and the
    others still get their verdict."""

    def __init__(self, pool: SympyCheckPool, timeout_s: float | None = None) -> None:
        self._pool = pool
        self._timeout_s = timeout_s

    async def check(self, checks: Sequence[PropertyCheck]) -> list[PropertyVerdict]:
        return await self._pool.map(check_property, checks, undecided, self._timeout_s)
