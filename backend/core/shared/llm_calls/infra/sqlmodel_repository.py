from sqlalchemy import Column, Index
from sqlmodel import Field, SQLModel, col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.shared.llm_calls.domain.llm_call import LLMCall
from core.shared.llm_calls.domain.repository import LLMCallRepository
from core.shared.storage.session_provider import BaseSQLModelRepository, JsonColumn, with_session


class LLMCallRecord(SQLModel, table=True):
    __tablename__ = "llm_calls"  # type: ignore[assignment]
    __table_args__ = (Index("ix_llm_calls_session_id", "session_id"), Index("ix_llm_calls_created_at", "created_at"))

    id: int | None = Field(default=None, primary_key=True)
    session_id: str | None = Field(default=None, max_length=64)
    turn: int | None = None
    created_at: float
    stage: str = Field(max_length=32)
    model: str = Field(max_length=96)
    ok: bool
    latency_ms: int | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    cached_tokens: int | None = None
    error: str | None = None
    response: dict[str, object] | None = Field(default=None, sa_column=Column(JsonColumn))
    system: str | None = None
    prompt: str | None = None


class SQLModelLLMCallRepository(LLMCallRepository, BaseSQLModelRepository):
    @with_session
    async def add(self, session: AsyncSession, call: LLMCall) -> None:
        session.add(LLMCallRecord(**call.model_dump()))

    @with_session
    async def of_session(self, session: AsyncSession, session_id: str, limit: int = 500) -> list[LLMCall]:
        rows = await session.exec(
            select(LLMCallRecord)
            .where(LLMCallRecord.session_id == session_id)
            .order_by(col(LLMCallRecord.id).desc())
            .limit(limit)
        )
        return [LLMCall.model_validate(r.model_dump(exclude={"id"})) for r in rows]
