from concurrent.futures.process import BrokenProcessPool

import pytest

from core.counterexamples.application.submission_grader import SubmissionGrader, SubmissionGraderInput
from core.counterexamples.domain.values.spec_id import SpecId
from core.counterexamples.domain.values.submission import Certificate, Path, PropertyCheck
from core.counterexamples.domain.values.verdict import PropertyVerdict
from core.counterexamples.infra.pool_property_checker import PoolPropertyChecker, VerdictCache
from core.shared.math.infra.sympy_pool import TIMEOUT_DETAIL, UNAVAILABLE_DETAIL, SympyCheckPool
from tests.fixtures.counterexamples import authored_challenges

DISCONTINUOUS = PropertyCheck(
    kind="discontinua",
    function="x*y/(x**2+y**2)",
    origin_value="0",
    certificate=Certificate(paths=[Path(x="t", y="t")]),
)
PARTIALS = PropertyCheck(
    kind="parcials_existeixen", function="x*y/(x**2+y**2)", origin_value="0", certificate=Certificate()
)


def closed_pool() -> SympyCheckPool:
    """Any check that reaches it raises: proves the verdicts came from the cache."""
    pool = SympyCheckPool(max_workers=1)
    pool.close()
    return pool


async def test_a_decided_check_is_answered_from_the_cache() -> None:
    cache = VerdictCache()
    first = await PoolPropertyChecker(SympyCheckPool(in_process=True), cache=cache).check([DISCONTINUOUS, PARTIALS])
    assert [v.status for v in first] == ["ok", "ok"] and len(cache) == 2

    again = await PoolPropertyChecker(closed_pool(), cache=cache).check([PARTIALS, DISCONTINUOUS])
    assert again == [first[1], first[0]]


async def test_only_the_misses_go_to_the_pool() -> None:
    cache = VerdictCache()
    [hit] = await PoolPropertyChecker(SympyCheckPool(in_process=True), cache=cache).check([PARTIALS])
    # DISCONTINUOUS is a miss: it reaches the closed pool, which cannot decide it (and it is not cached).
    again, miss = await PoolPropertyChecker(closed_pool(), cache=cache).check([PARTIALS, DISCONTINUOUS])
    assert again == hit
    assert miss.status == "indeterminat" and miss.detail == UNAVAILABLE_DETAIL and len(cache) == 1


async def test_a_pool_whose_workers_keep_dying_leaves_the_properties_undecided(monkeypatch: pytest.MonkeyPatch) -> None:
    """Not a 500 after the student's submission: the same as a property that timed out."""
    pool = SympyCheckPool(max_workers=1)

    def broken(*_: object) -> None:
        raise BrokenProcessPool("sympy workers keep dying at start-up")

    monkeypatch.setattr(pool, "_submit", broken)
    [verdict] = await PoolPropertyChecker(pool, cache=VerdictCache()).check([DISCONTINUOUS])
    assert verdict.status == "indeterminat" and verdict.detail == UNAVAILABLE_DETAIL


async def test_a_timed_out_check_is_not_cached() -> None:
    cache = VerdictCache()
    pool = SympyCheckPool(max_workers=1, timeout_s=0.001)
    try:
        [verdict] = await PoolPropertyChecker(pool, cache=cache).check([DISCONTINUOUS])
    finally:
        pool.close()
    assert verdict.status == "indeterminat" and verdict.detail == TIMEOUT_DETAIL
    assert len(cache) == 0


def test_the_cache_keeps_the_most_recently_used() -> None:
    cache = VerdictCache(size=2)
    ok = PropertyVerdict(kind="parcials_existeixen", status="ok")
    cache.put("a", ok)
    cache.put("b", ok)
    assert cache.get("a") == ok
    cache.put("c", ok)
    assert cache.get("b") is None and cache.get("a") == ok and cache.get("c") == ok


async def test_warm_decides_every_authored_example_as_the_grader_asks_for_it() -> None:
    catalog = authored_challenges()
    cache = VerdictCache()
    await PoolPropertyChecker(SympyCheckPool(in_process=True), cache=cache).warm(catalog)

    # Every verdict the grader needs for the examples is there: the closed pool would raise on a miss.
    grader = SubmissionGrader(catalog, PoolPropertyChecker(closed_pool(), cache=cache))
    for spec_id, spec in catalog.specs.items():
        result = await grader.grade(SubmissionGraderInput(spec_id=SpecId(spec_id), submission=spec.example))
        assert result.passed, spec_id
