"""A long-lived, bounded pool of worker processes for sympy checks.

Built once by a composition root and closed on exit: spawning a process and importing sympy in it costs seconds and
~100 MB, too much to pay on every quiz round or grading on a small container. `start` pays it ahead (at server
start-up) instead of on the first student's check.

Each item of a call gets its own deadline, counted from the moment a worker picks it up (the worker reports it): time
spent queued behind other calls or waiting for a worker to spawn does not count, so one slow check cannot time out
another student's. A hard stop per call (budget x (1 + items / workers) + a spawn grace) bounds the queue wait too.

A check that already reached a worker cannot be cancelled, and `ProcessPoolExecutor` cannot kill a single worker
(Python 3.13 has no `terminate_workers`). So when a call has a check running past its deadline, or the executor
breaks, the whole executor is retired: shut down without waiting, its live processes terminated (through the private
`_processes`), and a fresh one created lazily by the next submission. Items of any call that were interrupted that
way, or never started, are resubmitted once to the fresh executor; a second interruption comes back "indeterminat".
A check still queued when its call gives up is only cancelled; the executor is kept.

On POSIX each worker's address space is capped (`memory_limit_mb`; 0 = no cap): on a small container a runaway check
must fail inside its worker (a MemoryError, which `evaluate_one` turns into "indeterminat", or a dead worker, which
breaks and retires the executor) instead of growing until the OOM killer takes the server.
"""

import asyncio
import itertools
import multiprocessing as mp
import os
import threading
import time
from collections.abc import Callable, Iterable, Sequence
from concurrent.futures import FIRST_COMPLETED, Future, ProcessPoolExecutor, wait
from concurrent.futures.process import BrokenProcessPool
from typing import Any

from loguru import logger

from core.shared.math.sympy_checks import CheckResult, MathCheck, evaluate_one

TIMEOUT_DETAIL = "temps esgotat (sympy)"
INTERRUPTED_DETAIL = "sympy interromput"
UNAVAILABLE_DETAIL = "sympy no disponible"
# What a submission can raise: the workers died at start-up twice in a row, or the pool was already closed (shutdown).
POOL_UNAVAILABLE: tuple[type[Exception], ...] = (BrokenProcessPool, RuntimeError)
_JOIN_TIMEOUT_S = 1.0
_POLL_S = 0.1
# Spawning a worker and importing sympy in it, on a slow (0.1 CPU) instance.
_SPAWN_GRACE_S = 10.0
_START_TIMEOUT_S = 120.0
# Address space, not resident memory: an idle worker with sympy imported maps about 80 MB of it, so a check gets the
# rest. With the server itself, one capped worker fits a 512 MB instance.
DEFAULT_MEMORY_LIMIT_MB = 256

type CheckWorker = Callable[[MathCheck], CheckResult]


class SympyCheckPool:
    """`worker` must be a picklable module-level function (it is the seam tests use to simulate a hung check).
    `in_process=True` runs the checks inline: no processes, no hang protection (tests).
    `memory_limit_mb` caps each worker's address space on POSIX (0: no cap)."""

    def __init__(
        self,
        max_workers: int = 2,
        timeout_s: float = 25.0,
        in_process: bool = False,
        worker: CheckWorker = evaluate_one,
        memory_limit_mb: int = DEFAULT_MEMORY_LIMIT_MB,
    ) -> None:
        if max_workers < 1:
            raise ValueError("max_workers must be at least 1")
        self._memory_limit_mb = memory_limit_mb
        self._max_workers = max_workers
        self._timeout_s = timeout_s
        self._in_process = in_process
        self._worker = worker
        self._lock = threading.Lock()
        self._executor: _Executor | None = None
        self._closed = False

    async def start(self) -> None:
        """Spawns every worker and imports sympy in it, so the first check does not pay for it."""
        ready = await self.map(_ready, range(self._max_workers), _not_ready, _START_TIMEOUT_S)
        if None in ready:
            logger.warning("sympy pool: {} of {} workers not ready at start-up", ready.count(None), len(ready))

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
        builds the result of an item without one by its deadline. `timeout_s` is each item's budget once running."""
        if not items:
            return []
        if self._in_process:
            return [worker(i) for i in items]
        results: list[R | _Retry] = [_RETRY] * len(items)
        todo = list(range(len(items)))
        for final in (False, True):
            batch = _Batch(self._submit(worker, [items[i] for i in todo]), self._budget(timeout_s), self._max_workers)
            waiters = [asyncio.wrap_future(f) for f in batch.futures]
            try:
                while not batch.over():
                    pending = [w for w in waiters if not w.done()]
                    await asyncio.wait(pending, timeout=_POLL_S, return_when=asyncio.FIRST_COMPLETED)
            finally:
                _settle(waiters)
            outcome, retire = batch.collect([items[i] for i in todo], undecided, final)
            if retire:
                await asyncio.to_thread(self._retire, batch.executor)
            todo = _merge(results, todo, outcome)
            if not todo:
                break
        return _done(results)

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
        results: list[R | _Retry] = [_RETRY] * len(items)
        todo = list(range(len(items)))
        for final in (False, True):
            batch = _Batch(self._submit(worker, [items[i] for i in todo]), self._budget(timeout_s), self._max_workers)
            while not batch.over():
                wait([f for f in batch.futures if not f.done()], timeout=_POLL_S, return_when=FIRST_COMPLETED)
            outcome, retire = batch.collect([items[i] for i in todo], undecided, final)
            if retire:
                self._retire(batch.executor)
            todo = _merge(results, todo, outcome)
            if not todo:
                break
        return _done(results)

    def close(self) -> None:
        """Stops the workers, killing any still busy. Idempotent; evaluating afterwards raises `RuntimeError`."""
        with self._lock:
            self._closed = True
            executor, self._executor = self._executor, None
        if executor is not None:
            executor.tear_down()

    def _budget(self, timeout_s: float | None) -> float:
        return self._timeout_s if timeout_s is None else timeout_s

    def _submit(self, worker: Callable[[Any], Any], items: Sequence[Any]) -> "_Submitted":
        with self._lock:
            if self._closed:
                raise RuntimeError("SympyCheckPool is closed")
            for _ in range(2):
                if self._executor is None:
                    self._executor = _Executor(self._max_workers, self._memory_limit_mb)
                executor = self._executor
                try:
                    return executor.submit_all(worker, items)
                except BrokenProcessPool:  # a worker died (e.g. OOM-killed) since the last call
                    self._executor = None
                    executor.tear_down()
            raise BrokenProcessPool("sympy workers keep dying at start-up")

    def _retire(self, executor: "_Executor") -> None:
        with self._lock:
            if self._executor is not executor:  # a concurrent call already retired it
                return
            self._executor = None
        executor.tear_down()


class _Retry:
    """An item to resubmit: interrupted by a retirement, or never started."""


_RETRY = _Retry()


class _Submitted:
    def __init__(self, executor: "_Executor", tokens: list[int], futures: list[Future[Any]]) -> None:
        self.executor = executor
        self.tokens = tokens
        self.futures = futures


class _Executor:
    """A `ProcessPoolExecutor` and the moments its workers pick items up. The executor marks an item running when it
    moves it to its call queue, which holds one item more than there are workers: not when a worker starts it."""

    def __init__(self, max_workers: int, memory_limit_mb: int) -> None:
        ctx = mp.get_context("spawn")
        # Written synchronously by the worker before it runs the item: an `mp.Queue` writes from a feeder thread,
        # which a check holding the GIL (a huge integer power) starves, so the item would look never started.
        # One pipe per executor: a worker terminated while writing to it could leave it unusable.
        self._reports, self._writer = ctx.Pipe(duplex=False)
        self.pool = ProcessPoolExecutor(
            max_workers,
            mp_context=ctx,
            initializer=_init_worker,
            initargs=(memory_limit_mb, self._writer, ctx.Lock()),
        )
        self._tokens = itertools.count()
        self._lock = threading.Lock()
        self._started: dict[int, float | None] = {}  # in flight -> when a worker picked it up
        self._stop = threading.Event()
        self._reader = threading.Thread(target=self._read_starts, name="sympy-pool-starts", daemon=True)
        self._reader.start()

    def submit_all(self, worker: Callable[[Any], Any], items: Sequence[Any]) -> _Submitted:
        tokens = [next(self._tokens) for _ in items]
        with self._lock:
            self._started.update(dict.fromkeys(tokens))
        try:
            futures = [self.pool.submit(_run, t, worker, i) for t, i in zip(tokens, items, strict=True)]
        except BaseException:
            self.forget(tokens)
            raise
        return _Submitted(self, tokens, futures)

    def started_at(self, token: int) -> float | None:
        with self._lock:
            return self._started.get(token)

    def forget(self, tokens: Iterable[int]) -> None:
        with self._lock:
            for t in tokens:
                self._started.pop(t, None)

    def tear_down(self) -> None:
        self._stop.set()
        _tear_down(self.pool)
        self._reader.join(_JOIN_TIMEOUT_S)
        self._writer.close()
        self._reports.close()

    def _read_starts(self) -> None:
        while not self._stop.is_set():
            try:
                if not self._reports.poll(_POLL_S):
                    continue
                token = self._reports.recv()
            except (EOFError, OSError):  # every writer is gone, or the pipe was closed under us
                return
            now = time.monotonic()
            with self._lock:
                if token in self._started:  # a report arriving after its call ended is dropped
                    self._started[token] = now


class _Batch:
    """One submission of a call's items and the deadline rules over it."""

    def __init__(self, submitted: _Submitted, budget: float, workers: int) -> None:
        self.executor = submitted.executor
        self.futures = submitted.futures
        self._tokens = submitted.tokens
        self._budget = budget
        self._hard_stop = time.monotonic() + budget * (1 + len(self.futures) / workers) + _SPAWN_GRACE_S
        self._stopped = False

    def over(self) -> bool:
        """No item left; or the hard stop; or an item is past its deadline and none still runs within its own (the
        stuck one holds its worker until the executor is retired, so waiting longer only delays the others)."""
        now = time.monotonic()
        if now >= self._hard_stop:
            self._stopped = True
            return True
        pending = expired = running = False
        for token, f in zip(self._tokens, self.futures, strict=True):
            if f.done():
                continue
            pending = True
            started = self.executor.started_at(token)
            if started is None:
                continue
            if now - started >= self._budget:
                expired = True
            else:
                running = True
        return not pending or (expired and not running)

    def collect[T, R](
        self, items: Sequence[T], undecided: Callable[[T, str], R], final: bool
    ) -> tuple[list[R | _Retry], bool]:
        """The outcome of each item (`_RETRY` to resubmit, never when `final`), and whether the executor must be
        retired (a worker is stuck or the pool is broken)."""
        results: list[R | _Retry] = []
        retire = False
        for item, token, f in zip(items, self._tokens, self.futures, strict=True):
            if not f.done():
                never_ran = self.executor.started_at(token) is None and not self._stopped
                if not f.cancel():
                    retire = True
                results.append(_RETRY if never_ran and not final else undecided(item, TIMEOUT_DETAIL))
            elif f.cancelled():  # by a retirement
                results.append(undecided(item, INTERRUPTED_DETAIL) if final else _RETRY)
            elif isinstance(error := f.exception(), BrokenProcessPool):
                retire = True
                results.append(undecided(item, INTERRUPTED_DETAIL) if final else _RETRY)
            elif error is not None:
                results.append(undecided(item, f"error de sympy ({type(error).__name__})"))
            else:
                results.append(f.result())
        self.executor.forget(self._tokens)
        return results, retire


def _merge[R](results: list[R | _Retry], todo: list[int], outcome: list[R | _Retry]) -> list[int]:
    """Stores the outcome of the `todo` items; returns the ones to resubmit."""
    for i, r in zip(todo, outcome, strict=True):
        results[i] = r
    return [i for i, r in zip(todo, outcome, strict=True) if isinstance(r, _Retry)]


def _done[R](results: list[R | _Retry]) -> list[R]:
    out = [r for r in results if not isinstance(r, _Retry)]
    assert len(out) == len(results), "the final round resubmits nothing"
    return out


def _settle(waiters: Iterable[asyncio.Future[Any]]) -> None:
    """Results are read from the concurrent futures; settle the wrappers so none reports an unretrieved exception."""
    for w in waiters:
        if not w.done():
            w.cancel()
        elif not w.cancelled():
            w.exception()


_start_reports: Any = None  # in a worker: (pipe end, lock) it reports each pick-up on


def _init_worker(memory_limit_mb: int, writer: Any, lock: Any) -> None:
    global _start_reports
    limit_memory(memory_limit_mb)
    _start_reports = (writer, lock)


def _run(token: int, worker: Callable[[Any], Any], item: Any) -> Any:
    if _start_reports is not None:
        writer, lock = _start_reports
        with lock:
            writer.send(token)
    return worker(item)


def _ready(_: int) -> int:
    """Start-up job. Unpickling it in a worker imports this module and, through `sympy_checks`, sympy."""
    return os.getpid()


def _not_ready(_: int, _reason: str) -> None:
    return None


def limit_memory(limit_mb: int) -> None:
    """Worker initializer: caps this process's address space at `limit_mb` MB (never above the hard limit).
    No-op when `limit_mb` is 0 or on Windows, which has no `resource` module."""
    if limit_mb <= 0:
        return
    try:
        import resource
    except ImportError:
        return
    _soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    limit = limit_mb * 1024 * 1024
    if hard != resource.RLIM_INFINITY:
        limit = min(limit, hard)
    resource.setrlimit(resource.RLIMIT_AS, (limit, hard))


def _undecided(_check: MathCheck, detail: str) -> CheckResult:
    return CheckResult(status="indeterminat", detail=detail)


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
