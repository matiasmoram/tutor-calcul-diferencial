from collections.abc import AsyncIterator

import pytest
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

import core.shared.llm_calls.infra.sqlmodel_repository  # noqa: F401  (registers its table)
from core.shared.storage.session_provider import SQLModelSessionProvider, make_engine


@pytest.fixture
async def session_provider(tmp_path) -> AsyncIterator[SQLModelSessionProvider]:
    """A real (SQLite) database with every registered table, one per test."""
    engine = make_engine(f"sqlite+aiosqlite:///{(tmp_path / 'test.db').as_posix()}")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield SQLModelSessionProvider(engine)
    await engine.dispose()


@pytest.fixture
async def db_session(session_provider: SQLModelSessionProvider) -> AsyncIterator[AsyncSession]:
    async with session_provider.begin() as session:
        yield session
