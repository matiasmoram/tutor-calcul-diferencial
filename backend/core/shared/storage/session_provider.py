import functools
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from types import CoroutineType
from typing import Any, Concatenate

from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

# JSON documents: JSONB on Postgres, JSON (text) on SQLite.
JsonColumn = JSON().with_variant(JSONB(), "postgresql")


def make_engine(url: str) -> AsyncEngine:
    if url.startswith("sqlite"):
        return create_async_engine(url)
    # Supabase's transaction pooler (port 6543) hands each transaction a different server connection, so
    # psycopg's automatic prepared statements collide ("prepared statement _pg3_0 already exists").
    return create_async_engine(
        url, pool_pre_ping=True, pool_size=5, max_overflow=5, connect_args={"prepare_threshold": None}
    )


class SQLModelSessionProvider:
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    @asynccontextmanager
    async def begin(self) -> AsyncIterator[AsyncSession]:
        """One transaction: committed on success, rolled back on any exception."""
        async with AsyncSession(self.engine, expire_on_commit=False) as session, session.begin():
            yield session


class BoundSQLModelSessionProvider(SQLModelSessionProvider):
    """Every repository built on it joins one already-open session (multi-repository atomicity, test fixtures)."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @asynccontextmanager
    async def begin(self) -> AsyncIterator[AsyncSession]:
        yield self._session


class BaseSQLModelRepository:
    def __init__(self, provider: SQLModelSessionProvider) -> None:
        self._provider = provider


def with_session[R: BaseSQLModelRepository, **P, T](
    method: Callable[Concatenate[R, AsyncSession, P], CoroutineType[Any, Any, T]],
) -> Callable[Concatenate[R, P], CoroutineType[Any, Any, T]]:
    """Runs the repository method inside a session from the repository's provider."""

    @functools.wraps(method)
    async def wrapper(self: R, *args: P.args, **kwargs: P.kwargs) -> T:
        async with self._provider.begin() as session:
            return await method(self, session, *args, **kwargs)

    return wrapper
