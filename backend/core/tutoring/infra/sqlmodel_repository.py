from sqlalchemy import Column, Index, or_, update
from sqlalchemy.engine import CursorResult
from sqlmodel import Field, SQLModel, col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.shared.domain.ids import ExerciseId, SessionId
from core.shared.storage.session_provider import BaseSQLModelRepository, JsonColumn, with_session
from core.tutoring.domain.entities.tutor_session import TutorSession
from core.tutoring.domain.entities.tutor_turn import TutorTurn
from core.tutoring.domain.exceptions import ConcurrentTurnException, TutorSessionNotFoundException
from core.tutoring.domain.repository import TutorSessionRepository
from core.tutoring.domain.values.chat_message import ChatMessage
from core.tutoring.domain.values.session_state import SessionState
from core.tutoring.domain.values.transcription import Transcription
from core.tutoring.domain.values.turn_trace import TurnTrace


class TutorSessionRecord(SQLModel, table=True):
    __tablename__ = "tutor_sessions"  # type: ignore[assignment]
    __table_args__ = (
        Index("ix_tutor_sessions_exercise_id", "exercise_id"),
        Index("ix_tutor_sessions_updated_at", "updated_at"),
    )

    id: str = Field(primary_key=True, max_length=64)
    exercise_id: str = Field(max_length=32)
    created_at: float
    updated_at: float
    closed: bool = False
    version: int = 0
    turn_started_at: float | None = None  # a turn in progress (see claim_turn)
    state: dict[str, object] = Field(sa_column=Column(JsonColumn, nullable=False))
    history: list[dict[str, object]] = Field(sa_column=Column(JsonColumn, nullable=False))


class TutorTurnRecord(SQLModel, table=True):
    __tablename__ = "tutor_turns"  # type: ignore[assignment]
    __table_args__ = (Index("ix_tutor_turns_session_id_number", "session_id", "number"),)

    id: int | None = Field(default=None, primary_key=True)
    session_id: str = Field(max_length=64, foreign_key="tutor_sessions.id", ondelete="CASCADE")
    number: int
    created_at: float
    origin: str = Field(default="text", max_length=16)
    student_text: str
    tutor_text: str
    # Copied out of the trace for querying.
    action: str | None = Field(default=None, max_length=32)
    step: str | None = Field(default=None, max_length=64)
    level: int | None = None
    fallback: bool = False
    latency_ms: int | None = None
    trace: dict[str, object] = Field(sa_column=Column(JsonColumn, nullable=False))


class TranscriptionRecord(SQLModel, table=True):
    __tablename__ = "transcriptions"  # type: ignore[assignment]
    __table_args__ = (Index("ix_transcriptions_session_id", "session_id"),)

    id: int | None = Field(default=None, primary_key=True)
    session_id: str | None = Field(default=None, max_length=64, foreign_key="tutor_sessions.id", ondelete="CASCADE")
    created_at: float
    result: dict[str, object] = Field(sa_column=Column(JsonColumn, nullable=False))


def _session(r: TutorSessionRecord) -> TutorSession:
    return TutorSession(
        id=SessionId(r.id),
        exercise_id=ExerciseId(r.exercise_id),
        history=[ChatMessage.model_validate(m) for m in r.history],
        state=SessionState.model_validate(r.state),
        version=r.version,
        created_at=r.created_at,
        updated_at=r.updated_at,
    )


def _turn(r: TutorTurnRecord) -> TutorTurn:
    return TutorTurn(
        session_id=SessionId(r.session_id),
        number=r.number,
        created_at=r.created_at,
        origin="foto" if r.origin == "foto" else "text",
        student_text=r.student_text,
        tutor_text=r.tutor_text,
        trace=TurnTrace.model_validate(r.trace),
    )


def _turn_record(turn: TutorTurn) -> TutorTurnRecord:
    plan = turn.trace.plan
    return TutorTurnRecord(
        session_id=turn.session_id,
        number=turn.number,
        created_at=turn.created_at,
        origin=turn.origin,
        student_text=turn.student_text,
        tutor_text=turn.tutor_text,
        action=plan.action,
        step=plan.target_step,
        level=plan.hint_level,
        fallback=turn.trace.fallback,
        latency_ms=turn.trace.latency_ms,
        trace=turn.trace.model_dump(mode="json"),
    )


class SQLModelTutorSessionRepository(TutorSessionRepository, BaseSQLModelRepository):
    @with_session
    async def add(self, db: AsyncSession, session: TutorSession) -> None:
        db.add(
            TutorSessionRecord(
                id=session.id,
                exercise_id=session.exercise_id,
                created_at=session.created_at,
                updated_at=session.updated_at,
                closed=session.closed,
                version=session.version,
                state=session.state.model_dump(mode="json"),
                history=[m.model_dump(mode="json") for m in session.history],
            )
        )

    @with_session
    async def get(self, session: AsyncSession, session_id: SessionId) -> TutorSession:
        record = await session.get(TutorSessionRecord, session_id)
        if record is None:
            raise TutorSessionNotFoundException(session_id)
        return _session(record)

    @with_session
    async def claim_turn(self, db: AsyncSession, session_id: SessionId, now: float, stale_before: float) -> bool:
        result = await db.exec(
            update(TutorSessionRecord)  # type: ignore[call-overload]
            .where(col(TutorSessionRecord.id) == session_id)
            .where(
                or_(
                    col(TutorSessionRecord.turn_started_at).is_(None),
                    col(TutorSessionRecord.turn_started_at) < stale_before,
                )
            )
            .values(turn_started_at=now)
        )
        return isinstance(result, CursorResult) and result.rowcount == 1

    @with_session
    async def release_turn(self, db: AsyncSession, session_id: SessionId) -> None:
        await db.exec(
            update(TutorSessionRecord)  # type: ignore[call-overload]
            .where(col(TutorSessionRecord.id) == session_id)
            .values(turn_started_at=None)
        )

    @with_session
    async def save_turn(self, db: AsyncSession, session: TutorSession, turn: TutorTurn) -> TutorSession:
        result = await db.exec(
            update(TutorSessionRecord)  # type: ignore[call-overload]
            .where(col(TutorSessionRecord.id) == session.id)
            .where(col(TutorSessionRecord.version) == session.version)
            .values(
                state=session.state.model_dump(mode="json"),
                history=[m.model_dump(mode="json") for m in session.history],
                closed=session.closed,
                updated_at=session.updated_at,
                version=session.version + 1,
                turn_started_at=None,
            )
        )
        if not isinstance(result, CursorResult) or result.rowcount != 1:
            raise ConcurrentTurnException(session.id)
        db.add(_turn_record(turn))
        return session.model_copy(update={"version": session.version + 1})

    @with_session
    async def turns(self, session: AsyncSession, session_id: SessionId) -> list[TutorTurn]:
        rows = await session.exec(
            select(TutorTurnRecord)
            .where(TutorTurnRecord.session_id == session_id)
            .order_by(col(TutorTurnRecord.number), col(TutorTurnRecord.id))
        )
        return [_turn(r) for r in rows]

    @with_session
    async def recent_with_turns(self, session: AsyncSession, limit: int) -> list[tuple[TutorSession, list[TutorTurn]]]:
        sessions = (
            await session.exec(
                select(TutorSessionRecord).order_by(col(TutorSessionRecord.updated_at).desc()).limit(limit)
            )
        ).all()
        by_session: dict[str, list[TutorTurn]] = {s.id: [] for s in sessions}
        if by_session:
            rows = await session.exec(
                select(TutorTurnRecord)
                .where(col(TutorTurnRecord.session_id).in_(list(by_session)))
                .order_by(col(TutorTurnRecord.number), col(TutorTurnRecord.id))
            )
            for r in rows:
                by_session[r.session_id].append(_turn(r))
        return [(_session(s), by_session[s.id]) for s in sessions]

    @with_session
    async def add_transcription(
        self, session: AsyncSession, session_id: SessionId, transcription: Transcription, created_at: float
    ) -> None:
        session.add(
            TranscriptionRecord(
                session_id=session_id, created_at=created_at, result=transcription.model_dump(mode="json")
            )
        )
