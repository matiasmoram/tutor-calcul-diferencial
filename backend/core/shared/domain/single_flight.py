import asyncio
from collections.abc import Awaitable, Callable, Hashable


class SingleFlight[K: Hashable, V]:
    """At most one run per key at a time: a caller arriving while a run for its key is in flight awaits that run's
    result (or exception) instead of starting another one. In process memory, like the rate limiter.

    The run is a task of its own, so a caller that goes away (a closed connection cancels its request) does not
    cancel the work the other callers are waiting for."""

    def __init__(self) -> None:
        self._running: dict[K, asyncio.Task[V]] = {}

    async def run(self, key: K, work: Callable[[], Awaitable[V]]) -> V:
        task = self._running.get(key)
        if task is None:
            task = asyncio.create_task(self._wrap(work))
            self._running[key] = task
            task.add_done_callback(lambda t: self._forget(key, t))
        return await asyncio.shield(task)

    def in_flight(self, key: K) -> bool:
        return key in self._running

    @staticmethod
    async def _wrap(work: Callable[[], Awaitable[V]]) -> V:
        return await work()

    def _forget(self, key: K, task: asyncio.Task[V]) -> None:
        if self._running.get(key) is task:
            del self._running[key]
        if not task.cancelled():
            task.exception()  # retrieved here, so a run nobody awaits any more is not reported as never retrieved
