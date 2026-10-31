from sqlalchemy import Column, Index, func, or_, update
from sqlalchemy.engine import CursorResult
from sqlmodel import Field, SQLModel, col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.quizzes.domain.entities.grading import Answer, QuizGrading
from core.quizzes.domain.entities.quiz import Quiz
from core.quizzes.domain.entities.quiz_session import QuizSession, QuizSubmission
from core.quizzes.domain.exceptions import (
    ConcurrentQuizGradingException,
    QuizNotFoundException,
    QuizSessionNotFoundException,
)
from core.quizzes.domain.repository import Availability, QuizRepository, QuizSessionRepository
from core.quizzes.domain.values.difficulty import Difficulty, difficulty_of
from core.quizzes.domain.values.quiz_id import QuizId
from core.shared.domain.ids import SessionId
from core.shared.storage.session_provider import BaseSQLModelRepository, JsonColumn, with_session


class QuizRecord(SQLModel, table=True):
    """The quiz document as stored in ``generats/afirmacions`` (Catalan keys), with its key columns alongside."""

    __tablename__ = "quizzes"  # type: ignore[assignment]
    __table_args__ = (Index("ix_quizzes_source_difficulty", "source_id", "difficulty"),)

    id: str = Field(primary_key=True, max_length=32)
    source_id: str = Field(max_length=64)
    difficulty: str = Field(max_length=16)
    topic: int
    created_at: float
    data: dict[str, object] = Field(sa_column=Column(JsonColumn, nullable=False))


class QuizSessionRecord(SQLModel, table=True):
    __tablename__ = "quiz_sessions"  # type: ignore[assignment]

    id: str = Field(primary_key=True, max_length=64)
    source_id: str = Field(max_length=64)
    difficulty: str = Field(max_length=16)
    quiz_id: str = Field(max_length=32, foreign_key="quizzes.id")
    hints_used: list[str] = Field(sa_column=Column(JsonColumn, nullable=False))
    created_at: float
    updated_at: float
    version: int = 0
    grading_started_at: float | None = None  # claim of a grading in progress (see claim_grading)


class QuizGradingRecord(SQLModel, table=True):
    """The one grading of a session: the answers handed in, the hints used, and the result shown."""

    __tablename__ = "quiz_gradings"  # type: ignore[assignment]

    session_id: str = Field(primary_key=True, max_length=64, foreign_key="quiz_sessions.id", ondelete="CASCADE")
    created_at: float
    answers: list[dict[str, object]] = Field(sa_column=Column(JsonColumn, nullable=False))
    hints: list[str] = Field(sa_column=Column(JsonColumn, nullable=False))
    result: dict[str, object] = Field(sa_column=Column(JsonColumn, nullable=False))


class SQLModelQuizRepository(QuizRepository, BaseSQLModelRepository):
    @with_session
    async def add(self, db: AsyncSession, quiz: Quiz) -> None:
        await db.merge(
            QuizRecord(
                id=quiz.id,
                source_id=quiz.source_id,
                difficulty=quiz.difficulty,
                topic=quiz.topic,
                created_at=quiz.created,
                data=quiz.model_dump(mode="json"),
            )
        )

    @with_session
    async def get(self, db: AsyncSession, quiz_id: QuizId) -> Quiz:
        record = await db.get(QuizRecord, quiz_id)
        if record is None:
            raise QuizNotFoundException(quiz_id)
        return Quiz.model_validate(record.data)

    @with_session
    async def of_source(self, db: AsyncSession, source_id: str, difficulty: Difficulty) -> list[Quiz]:
        rows = await db.exec(
            select(QuizRecord)
            .where(QuizRecord.source_id == source_id, QuizRecord.difficulty == difficulty)
            .order_by(col(QuizRecord.created_at), col(QuizRecord.id))
        )
        return [Quiz.model_validate(r.data) for r in rows]

    @with_session
    async def availability(self, db: AsyncSession) -> Availability:
        rows = await db.exec(
            select(QuizRecord.source_id, QuizRecord.difficulty, func.count()).group_by(
                col(QuizRecord.source_id), col(QuizRecord.difficulty)
            )
        )
        out: Availability = {}
        for source_id, name, n in rows:
            difficulty = difficulty_of(name)
            if difficulty is not None and n:
                out.setdefault(source_id, {})[difficulty] = n
        return out


class SQLModelQuizSessionRepository(QuizSessionRepository, BaseSQLModelRepository):
    @with_session
    async def add(self, db: AsyncSession, session: QuizSession) -> None:
        db.add(
            QuizSessionRecord(
                id=session.id,
                source_id=session.source_id,
                difficulty=session.difficulty,
                quiz_id=session.quiz_id,
                hints_used=list(session.hints_used),
                created_at=session.created_at,
                updated_at=session.updated_at,
                version=session.version,
            )
        )

    @with_session
    async def get(self, db: AsyncSession, session_id: SessionId) -> QuizSession:
        record = await db.get(QuizSessionRecord, session_id)
        if record is None:
            raise QuizSessionNotFoundException(session_id)
        grading = await db.get(QuizGradingRecord, session_id)
        difficulty = difficulty_of(record.difficulty)
        return QuizSession.model_validate(
            {
                "id": SessionId(record.id),
                "source_id": record.source_id,
                "difficulty": difficulty,
                "quiz_id": record.quiz_id,
                "hints_used": record.hints_used,
                "submission": _submission(grading) if grading else None,
                "created_at": record.created_at,
                "updated_at": record.updated_at,
                "version": record.version,
            }
        )

    @with_session
    async def claim_grading(self, db: AsyncSession, session_id: SessionId, now: float, stale_before: float) -> bool:
        graded = select(QuizGradingRecord.session_id).where(QuizGradingRecord.session_id == session_id).exists()
        result = await db.exec(
            update(QuizSessionRecord)  # type: ignore[call-overload]
            .where(
                col(QuizSessionRecord.id) == session_id,
                or_(
                    col(QuizSessionRecord.grading_started_at).is_(None),
                    col(QuizSessionRecord.grading_started_at) < stale_before,
                ),
                ~graded,
            )
            .values(grading_started_at=now)
        )
        return isinstance(result, CursorResult) and result.rowcount == 1

    @with_session
    async def release_grading(self, db: AsyncSession, session_id: SessionId, claimed_at: float) -> None:
        await db.exec(
            update(QuizSessionRecord)  # type: ignore[call-overload]
            .where(col(QuizSessionRecord.id) == session_id, col(QuizSessionRecord.grading_started_at) == claimed_at)
            .values(grading_started_at=None)
        )

    @with_session
    async def save(self, db: AsyncSession, session: QuizSession) -> None:
        result = await db.exec(
            update(QuizSessionRecord)  # type: ignore[call-overload]
            .where(col(QuizSessionRecord.id) == session.id, col(QuizSessionRecord.version) == session.version)
            .values(
                hints_used=list(session.hints_used),
                updated_at=session.updated_at,
                version=session.version + 1,
            )
        )
        if not isinstance(result, CursorResult) or result.rowcount != 1:
            raise ConcurrentQuizGradingException(session.id)
        submission = session.submission
        if submission is not None and await db.get(QuizGradingRecord, session.id) is None:
            db.add(
                QuizGradingRecord(
                    session_id=session.id,
                    created_at=submission.created_at,
                    answers=[a.model_dump(mode="json") for a in submission.answers],
                    hints=list(submission.hints),
                    result=submission.result.model_dump(mode="json"),
                )
            )
        session.version += 1


def _submission(record: QuizGradingRecord) -> QuizSubmission:
    return QuizSubmission(
        answers=[Answer.model_validate(a) for a in record.answers],
        hints=record.hints,
        result=QuizGrading.model_validate(record.result),
        created_at=record.created_at,
    )
