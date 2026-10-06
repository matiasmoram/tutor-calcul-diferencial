import time
from abc import ABC, abstractmethod


class Clock(ABC):
    @abstractmethod
    def now(self) -> float:
        """Seconds since the epoch."""

    @abstractmethod
    def monotonic(self) -> float:
        """Seconds on a monotonic clock, for measuring latencies."""


class SystemClock(Clock):
    def now(self) -> float:
        return time.time()

    def monotonic(self) -> float:
        return time.perf_counter()
