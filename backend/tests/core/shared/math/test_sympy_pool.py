import asyncio
from collections.abc import Iterator
from multiprocessing.process import BaseProcess

import pytest

from core.shared.math.infra.sympy_pool import TIMEOUT_DETAIL, SympyCheckPool
from core.shared.math.sympy_checks import MathCheck
from tests.core.shared.math.test_sympy_checks import ITERATED, check
from tests.core.shared.math.workers import hang_on_description

HANG = MathCheck(description="hang", kind="igualtat", expression="x", value="x")
NO_LIMIT = check("no_limit", "sin(1/x)")


@pytest.fixture
def pool() -> Iterator[SympyCheckPool]:
    p = SympyCheckPool(max_workers=1, timeout_s=60, worker=hang_on_description)
    yield p
    p.close()


def workers(p: SympyCheckPool) -> list[BaseProcess]:
    assert p._executor is not None and p._executor._processes is not None
    return list(p._executor._processes.values())


def worker_pids(p: SympyCheckPool) -> set[int | None]:
    return {w.pid for w in workers(p)}


async def test_workers_are_reused_across_calls(pool: SympyCheckPool) -> None:
    assert [r.status for r in await pool.evaluate([ITERATED, NO_LIMIT])] == ["ok", "ok"]
    executor, pids = pool._executor, worker_pids(pool)
    assert [r.status for r in await pool.evaluate([NO_LIMIT])] == ["ok"]
    assert [r.status for r in pool.evaluate_blocking([ITERATED])] == ["ok"]
    assert pool._executor is executor and worker_pids(pool) == pids


async def test_concurrent_calls_share_the_bounded_pool(pool: SympyCheckPool) -> None:
    outs = await asyncio.gather(*(pool.evaluate([ITERATED]) for _ in range(3)))
    assert [[r.status for r in out] for out in outs] == [["ok"]] * 3
    assert len(worker_pids(pool)) == 1


async def test_a_hung_check_times_out_and_the_pool_recovers(pool: SympyCheckPool) -> None:
    await pool.evaluate([ITERATED])  # warm the worker so only HANG can be slow
    stuck = workers(pool)

    out = await pool.evaluate([HANG], timeout_s=1.0)

    assert out[0].status == "indeterminat" and out[0].detail == TIMEOUT_DETAIL
    assert pool._executor is None
    assert not any(p.is_alive() for p in stuck)
    assert [r.status for r in await pool.evaluate([ITERATED])] == ["ok"]
    assert worker_pids(pool).isdisjoint(p.pid for p in stuck)


def test_a_blocking_call_times_out_and_the_pool_recovers(pool: SympyCheckPool) -> None:
    pool.evaluate_blocking([ITERATED])
    out = pool.evaluate_blocking([ITERATED, HANG], timeout_s=1.0)
    assert [r.status for r in out] == ["ok", "indeterminat"]
    assert [r.status for r in pool.evaluate_blocking([NO_LIMIT])] == ["ok"]


async def test_close_stops_the_workers(pool: SympyCheckPool) -> None:
    await pool.evaluate([ITERATED])
    processes = workers(pool)

    pool.close()
    pool.close()

    assert pool._executor is None
    assert not any(p.is_alive() for p in processes)
    with pytest.raises(RuntimeError):
        await pool.evaluate([ITERATED])


async def test_in_process_mode_needs_no_workers() -> None:
    p = SympyCheckPool(in_process=True)
    assert [r.status for r in await p.evaluate([ITERATED])] == ["ok"]
    assert [r.status for r in p.evaluate_blocking([NO_LIMIT])] == ["ok"]
    assert p._executor is None
    assert await p.evaluate([]) == []
