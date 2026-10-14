import asyncio
import sys
import time
from collections.abc import Iterator
from multiprocessing.process import BaseProcess

import pytest

from core.shared.math.infra.sympy_pool import (
    INTERRUPTED_DETAIL,
    MEMORY_LIMIT_ENV,
    TIMEOUT_DETAIL,
    SympyCheckPool,
    limit_memory,
)
from core.shared.math.sympy_checks import MathCheck
from tests.core.shared.math.test_sympy_checks import ITERATED, check
from tests.core.shared.math.workers import (
    address_space_limit,
    allocate_mb,
    die_on_negative,
    hang_on_description,
    hang_on_negative,
)

HANG = MathCheck(description="hang", kind="igualtat", expression="x", value="x")
NO_LIMIT = check("no_limit", "sin(1/x)")


@pytest.fixture
def pool() -> Iterator[SympyCheckPool]:
    p = SympyCheckPool(max_workers=1, timeout_s=60, worker=hang_on_description)
    yield p
    p.close()


def workers(p: SympyCheckPool) -> list[BaseProcess]:
    assert p._executor is not None and p._executor.pool._processes is not None
    return list(p._executor.pool._processes.values())


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


async def test_map_runs_any_job_and_times_out_per_item() -> None:
    p = SympyCheckPool(max_workers=1, timeout_s=60)
    try:
        assert await p.map(hang_on_negative, [2, 3], lambda n, why: -1) == [4, 9]
        out = await p.map(hang_on_negative, [2, -1], lambda n, why: (n, why), timeout_s=1.0)
        assert out == [4, (-1, TIMEOUT_DETAIL)]
        assert await p.map(hang_on_negative, [5], lambda n, why: -1) == [25]
    finally:
        p.close()


posix_only = pytest.mark.skipif(sys.platform == "win32", reason="RLIMIT_AS is POSIX only")


async def test_a_dead_worker_is_undecided_and_replaced() -> None:
    p = SympyCheckPool(max_workers=1, timeout_s=60)
    try:
        assert await p.map(die_on_negative, [2], lambda n, why: -1) == [4]
        dead = worker_pids(p)
        assert await p.map(die_on_negative, [-1], lambda n, why: why) == [INTERRUPTED_DETAIL]
        assert p._executor is None
        assert p.map_blocking(die_on_negative, [3], lambda n, why: -1) == [9]
        assert worker_pids(p).isdisjoint(dead)
    finally:
        p.close()


@posix_only
async def test_workers_address_space_is_capped(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(MEMORY_LIMIT_ENV, "300")
    p = SympyCheckPool(max_workers=1, timeout_s=60)
    try:
        assert await p.map(address_space_limit, [0], lambda n, why: -1) == [300 * 1024 * 1024]
    finally:
        p.close()


@posix_only
async def test_a_runaway_check_fails_in_its_worker_and_the_pool_goes_on() -> None:
    p = SympyCheckPool(max_workers=1, timeout_s=60, memory_limit_mb=256)
    try:
        assert await p.map(allocate_mb, [10], lambda n, why: why) == [10 * 1024 * 1024]
        pids = worker_pids(p)
        assert await p.map(allocate_mb, [4096], lambda n, why: why) == ["error de sympy (MemoryError)"]
        assert await p.map(allocate_mb, [10], lambda n, why: why) == [10 * 1024 * 1024]
        assert worker_pids(p) == pids  # the worker survived its MemoryError
        assert [r.status for r in await p.evaluate([ITERATED])] == ["ok"]
    finally:
        p.close()


def test_no_cap_leaves_the_limit_alone() -> None:
    limit_memory(0)  # also a no-op on Windows for any value
    if sys.platform == "win32":
        limit_memory(256)


def nap(seconds: float) -> float:
    """A check that takes `seconds` (module-level: the spawned workers unpickle it from this module)."""
    time.sleep(seconds)
    return seconds


def _why(_: float, reason: str) -> str:
    return reason


async def test_start_spawns_every_worker() -> None:
    p = SympyCheckPool(max_workers=2, timeout_s=60)
    try:
        await p.start()
        assert len(workers(p)) == 2 and all(w.is_alive() for w in workers(p))
        pids = worker_pids(p)
        assert await p.map(nap, [0.0], _why) == [0.0]
        assert worker_pids(p) == pids
    finally:
        p.close()


async def test_queue_time_behind_another_call_does_not_count() -> None:
    """Call B waits ~1.6 s behind call A, then each of its items runs 0.5 s: over 2 s in all, but each item is well
    within its own 2 s budget. One deadline over the whole call (from submission) would time B out."""
    p = SympyCheckPool(max_workers=1, timeout_s=2.0)
    try:
        await p.start()
        executor = p._executor
        a = asyncio.create_task(p.map(nap, [1.8], _why))
        await asyncio.sleep(0.2)
        b = await p.map(nap, [0.5, 0.5], _why)
        assert b == [0.5, 0.5]
        assert await a == [1.8]
        assert p._executor is executor
    finally:
        p.close()


async def test_a_stuck_check_does_not_time_out_another_calls_check() -> None:
    """A's check runs past its deadline and retires the executor, killing B's queued check with it: B's check is
    resubmitted to the fresh executor and decided, not reported as a timeout or an interruption."""
    p = SympyCheckPool(max_workers=1, timeout_s=1.0)
    try:
        await p.start()
        a = asyncio.create_task(p.map(nap, [30.0], _why))
        await asyncio.sleep(0.2)
        b = await p.map(nap, [0.1], _why)
        assert b == [0.1]
        assert await a == [TIMEOUT_DETAIL]
    finally:
        p.close()
