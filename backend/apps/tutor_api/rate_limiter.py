import time
from collections import defaultdict, deque


class RateLimiter:
    """Sliding window per client, in process memory: enough for one server process (the Dockerfile runs one)."""

    def __init__(self, per_minute: int, window_s: float = 60.0) -> None:
        self._limit = per_minute
        self._window_s = window_s
        self._hits: defaultdict[str, deque[float]] = defaultdict(deque)

    def allow(self, client: str, now: float | None = None) -> bool:
        now = time.monotonic() if now is None else now
        hits = self._hits[client]
        while hits and hits[0] <= now - self._window_s:
            hits.popleft()
        if len(hits) >= self._limit:
            return False
        hits.append(now)
        if len(self._hits) > 10_000:  # forget idle clients so memory stays bounded
            for key in [k for k, v in self._hits.items() if not v or v[-1] <= now - self._window_s]:
                del self._hits[key]
        return True
