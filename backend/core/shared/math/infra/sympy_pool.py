"""A long-lived, bounded pool of worker processes for sympy checks.

Built once by a composition root and closed on exit: spawning a process and importing sympy in it costs seconds and
~100 MB, too much to pay on every quiz round or grading on a small container.

Every call gets one shared deadline; a check without a result by then is "indeterminat". A check that already reached
a worker cannot be cancelled, and `ProcessPoolExecutor` cannot kill a single worker (Python 3.13 has no
`terminate_workers`). So when a call times out on a running check, or the executor breaks, the whole executor is
retired: shut down without waiting, its live processes terminated (through the private `_processes`), and a fresh one
created lazily by the next call. Checks of concurrent calls still running on the retired executor come back
"indeterminat" too. A check that timed out while still queued is only cancelled; the executor is kept.
"""

import asyncio
import multiprocessing as mp
import threading
from collections.abc import Callable, Sequence
from concurrent.futures import Future, ProcessPoolExecutor, wait
from concurrent.futures.process import BrokenProcessPool
from typing import Any

from core.shared.math.sympy_checks import CheckResult, MathCheck, evaluate_one

TIMEOUT_DETAIL = "temps esgotat (sympy)"
INTERRUPTED_DETAIL = "sympy interromput"
_JOIN_TIMEOUT_S = 1.0

type CheckWorker = Callable[[MathCheck], CheckResult]


class SympyCheckPool:
    """`worker` must be a picklable module-level function (it is the seam tests use to simulate a hung check).
    `in_process=True` runs the checks inline: no processes, no hang protection (tests)."""

    def __init__(
        self,
        max_workers: int = 2,
        timeout_s: float = 25.0,
        in_process: bool = False,
        worker: CheckWorker = evaluate_one,
    ) -> None:
        if max_workers < 1:
            raise ValueError("max_workers must be at least 1")
        self._max_workers = max_workers
        self._timeout_s = timeout_s
        self._in_process = in_process
        self._worker = worker
        self._lock = threading.Lock()
        self._executor: ProcessPoolExecutor | None = None
        self._closed = False

    async def evaluate(self, checks: Sequence[MathCheck], timeout_s: float | None = None) -> list[CheckResult]:
        return await self.map(self._worker, checks, _undecided, timeout_s)

    def evaluate_blocking(self, checks: Sequence[MathCheck], timeout_s: float | None = None) -> list[CheckResult]:
        """Same as `evaluate`, blocking the calling thread (for synchronous callers already off the event loop)."""
        return self.map_blocking(self._worker, checks, _undecided, timeout_s)

    async def map[T, R](
        self,
        worker: Callable[[T], R],
        items: Sequence[T],
        undecided: Callable[[T, str], R],
        timeout_s: float | None = None,
    ) -> list[R]:
        """Any other sympy job on the same workers: `worker` is a picklable module-level function, `undecided(item, reason)`
        builds the result of an item without one by the deadline."""
        if not items:
            return []
        if self._in_process:
            return [worker(i) for i in items]
        executor, futures = self._submit(worker, items)
        waiters = [asyncio.wrap_future(f) for f in futures]
        await asyncio.wait(waiters, timeout=self._timeout_s if timeout_s is None else timeout_s)
        for w in waiters:
            # Results are read from `futures`; settle the wrappers so none reports an unretrieved exception.
            if not w.done():
                w.cancel()
            elif not w.cancelled():
                w.exception()
        results, retire = _collect(items, futures, undecided)
        if retire:
            await asyncio.to_thread(self._retire, executor)
        return results

    def map_blocking[T, R](
        self,
        worker: Callable[[T], R],
        items: Sequence[T],
        undecided: Callable[[T, str], R],
        timeout_s: float | None = None,
    ) -> list[R]:
        if not items:
            return []
        if self._in_process:
            return [worker(i) for i in items]
        executor, futures = self._submit(worker, items)
        wait(futures, timeout=self._timeout_s if timeout_s is None else timeout_s)
        results, retire = _collect(items, futures, undecided)
        if retire:
            self._retire(executor)
        return results

    def close(self) -> None:
        """Stops the workers, killing any still busy. Idempotent; evaluating afterwards raises `RuntimeError`."""
        with self._lock:
            self._closed = True
            executor, self._executor = self._executor, None
        if executor is not None:
            _tear_down(executor)

    def _submit(
        self, worker: Callable[[Any], Any], items: Sequence[Any]
    ) -> tuple[ProcessPoolExecutor, list[Future[Any]]]:
        with self._lock:
            if self._closed:
                raise RuntimeError("SympyCheckPool is closed")
            for _ in range(2):
                if self._executor is None:
                    self._executor = ProcessPoolExecutor(self._max_workers, mp_context=mp.get_context("spawn"))
                executor = self._executor
                try:
                    return executor, [executor.submit(worker, i) for i in items]
                except BrokenProcessPool:  # a worker died (e.g. OOM-killed) since the last call
                    self._executor = None
                    _tear_down(executor)
            raise BrokenProcessPool("sympy workers keep dying at start-up")

    def _retire(self, executor: ProcessPoolExecutor) -> None:
        with self._lock:
            if self._executor is not executor:  # a concurrent call already retired it
                return
            self._executor = None
        _tear_down(executor)


def _undecided(_check: MathCheck, detail: str) -> CheckResult:
    return CheckResult(status="indeterminat", detail=detail)


def _collect[T, R](
    items: Sequence[T], futures: Sequence[Future[R]], undecided: Callable[[T, str], R]
) -> tuple[list[R], bool]:
    """The results in order, and whether the executor must be retired (a worker is stuck or the pool is broken)."""
    results: list[R] = []
    retire = False
    for item, f in zip(items, futures, strict=True):
        if not f.done():
            if not f.cancel():
                retire = True
            results.append(undecided(item, TIMEOUT_DETAIL))
        elif f.cancelled():
            results.append(undecided(item, INTERRUPTED_DETAIL))
        elif (error := f.exception()) is not None:
            retire = retire or isinstance(error, BrokenProcessPool)
            detail = (
                INTERRUPTED_DETAIL
                if isinstance(error, BrokenProcessPool)
                else f"error de sympy ({type(error).__name__})"
            )
            results.append(undecided(item, detail))
        else:
            results.append(f.result())
    return results, retire


def _tear_down(executor: ProcessPoolExecutor) -> None:
    processes = list(executor._processes.values()) if executor._processes else []
    executor.shutdown(wait=False, cancel_futures=True)
    for p in processes:
        if p.is_alive():
            p.terminate()
    for p in processes:
        p.join(_JOIN_TIMEOUT_S)
    # SIGTERM is not guaranteed to be handled within the timeout (a busy or loaded machine): escalate.
    for p in processes:
        if p.is_alive():
            p.kill()
            p.join(_JOIN_TIMEOUT_S)
