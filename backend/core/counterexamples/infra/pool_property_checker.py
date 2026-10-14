from collections import OrderedDict
from collections.abc import Sequence

from loguru import logger

from core.counterexamples.domain.entities.spec import SpecCatalog
from core.counterexamples.domain.services.property_deciders import check_property, undecided
from core.counterexamples.domain.values.submission import PropertyCheck
from core.counterexamples.domain.values.verdict import PropertyVerdict
from core.shared.math.infra.sympy_pool import POOL_UNAVAILABLE, UNAVAILABLE_DETAIL, SympyCheckPool

CACHE_SIZE = 512


class VerdictCache:
    """The verdicts already decided, by check (LRU). `check_property` is a pure function of the check, so a verdict
    holds for every later identical check: the authored examples and the answers students share cost one decision."""

    def __init__(self, size: int = CACHE_SIZE) -> None:
        self._size = size
        self._verdicts: OrderedDict[str, PropertyVerdict] = OrderedDict()

    def get(self, key: str) -> PropertyVerdict | None:
        verdict = self._verdicts.get(key)
        if verdict is None:
            return None
        self._verdicts.move_to_end(key)
        return verdict.model_copy(deep=True)

    def put(self, key: str, verdict: PropertyVerdict) -> None:
        self._verdicts[key] = verdict.model_copy(deep=True)
        self._verdicts.move_to_end(key)
        while len(self._verdicts) > self._size:
            self._verdicts.popitem(last=False)

    def __len__(self) -> int:
        return len(self._verdicts)


# One per process: the graders are built per request.
_VERDICTS = VerdictCache()


class PoolPropertyChecker:
    """Each property in its own worker under the pool's deadline: one that hangs comes back 'indeterminat' and the
    others still get their verdict. Decided verdicts are cached; a property the pool gave up on (deadline, interrupted
    worker) is not, since another try may decide it."""

    def __init__(self, pool: SympyCheckPool, timeout_s: float | None = None, cache: VerdictCache | None = None) -> None:
        self._pool = pool
        self._timeout_s = timeout_s
        self._cache = _VERDICTS if cache is None else cache

    async def check(self, checks: Sequence[PropertyCheck]) -> list[PropertyVerdict]:
        keys = [c.model_dump_json() for c in checks]
        verdicts = [self._cache.get(k) for k in keys]
        missing = [i for i, v in enumerate(verdicts) if v is None]
        given_up: set[int] = set()

        def gave_up(check: PropertyCheck, reason: str) -> PropertyVerdict:
            verdict = undecided(check, reason)
            given_up.add(id(verdict))
            return verdict

        todo = [checks[i] for i in missing]
        try:
            decided = await self._pool.map(check_property, todo, gave_up, self._timeout_s)
        except POOL_UNAVAILABLE as e:  # workers dying at start-up, or the pool closed at shutdown
            logger.error("sympy pool unavailable, {} properties undecided: {!r}", len(todo), e)
            decided = [gave_up(c, UNAVAILABLE_DETAIL) for c in todo]
        for i, verdict in zip(missing, decided, strict=True):
            verdicts[i] = verdict
            if id(verdict) not in given_up:
                self._cache.put(keys[i], verdict)
        return [v for v in verdicts if v is not None]

    async def warm(self, catalog: SpecCatalog) -> None:
        """Decides every authored example ahead (one challenge at a time, so students' checks interleave)."""
        for spec in catalog.specs.values():
            example = spec.example
            paths = [p for cert in example.certificates.values() for p in cert.paths]
            await self.check(
                [
                    PropertyCheck(
                        kind=kind,
                        function=example.function,
                        origin_value=example.origin_value,
                        certificate=example.certificate(kind),
                        context_paths=paths,
                    )
                    for kind in spec.properties
                ]
            )
