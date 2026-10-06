"""Which session and turn the model calls in progress belong to.

A ContextVar on purpose: the scope is set once by a use case around its unit of work, and read only by the
call-logging decorator. Threading it through every port (diagnoser, writer, judge, generators) would add a
parameter to a dozen signatures that none of them uses.
"""

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass


@dataclass(frozen=True)
class CallScope:
    session_id: str | None = None
    turn: int | None = None


_SCOPE: ContextVar[CallScope] = ContextVar("llm_call_scope", default=CallScope())  # noqa: B039


def current_scope() -> CallScope:
    return _SCOPE.get()


@contextmanager
def call_scope(session_id: str | None, turn: int | None = None) -> Iterator[None]:
    token = _SCOPE.set(CallScope(session_id, turn))
    try:
        yield
    finally:
        _SCOPE.reset(token)
