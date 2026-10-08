import os
from collections.abc import AsyncIterator

import pytest
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from core.shared.storage.session_provider import SQLModelSessionProvider, make_engine
from core.shared.storage.table_registry import register_all_tables

register_all_tables()


# CI also runs the suite against Postgres (the production engine): JSONB, psycopg rowcounts, FK cascades.
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


@pytest.fixture
async def session_provider(tmp_path) -> AsyncIterator[SQLModelSessionProvider]:
    """A real database with every registered table, empty for each test: SQLite, or TEST_DATABASE_URL."""
    engine = make_engine(TEST_DATABASE_URL or f"sqlite+aiosqlite:///{(tmp_path / 'test.db').as_posix()}")
    async with engine.begin() as conn:
        if TEST_DATABASE_URL:
            await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield SQLModelSessionProvider(engine)
    await engine.dispose()


@pytest.fixture
async def db_session(session_provider: SQLModelSessionProvider) -> AsyncIterator[AsyncSession]:
    async with session_provider.begin() as session:
        yield session
