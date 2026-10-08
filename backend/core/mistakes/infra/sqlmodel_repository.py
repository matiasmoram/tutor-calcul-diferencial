from sqlalchemy import Column, Index, func, or_, update
from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, SQLModel, col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.entities.mistake_grading import MistakeGrading
from core.mistakes.domain.entities.mistake_session import MistakeSession
from core.mistakes.domain.exceptions import (
    MistakeExerciseNotFoundException,
    MistakeSessionAlreadyGradedException,
    MistakeSessionNotFoundException,
)
from core.mistakes.domain.repository import MistakeExerciseRepository, MistakeSessionRepository, ReadyCounts
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.mistake_exercise_id import MistakeExerciseId
from core.shared.domain.ids import SessionId
from core.shared.storage.session_provider import BaseSQLModelRepository, JsonColumn, with_session


class MistakeExerciseRecord(SQLModel, table=True):
    __tablename__ = "mistake_exercises"  # type: ignore[assignment]
    __table_args__ = (Index("ix_mistake_exercises_source", "source_id", "difficulty"),)

    id: str = Field(primary_key=True, max_length=16)
    source_kind: str = Field(max_length=16)
    source_id: str = Field(max_length=64)
    difficulty: str = Field(max_length=16)
    created_at: float
    data: dict[str, object] = Field(sa_column=Column(JsonColumn, nullable=False))  # the document, Catalan keys


class MistakeSessionRecord(SQLModel, table=True):
    __tablename__ = "mistake_sessions"  # type: ignore[assignment]
    __table_args__ = (Index("ix_mistake_sessions_source_id", "source_id"),)

    id: str = Field(primary_key=True, max_length=64)
    source_kind: str = Field(max_length=16)
    source_id: str = Field(max_length=64)
    exercise_id: str = Field(max_length=16, foreign_key="mistake_exercises.id")
    difficulty: str = Field(max_length=16)
    created_at: float
    grading_started_at: float | None = None  # claim of a grading in progress


class MistakeGradingRecord(SQLModel, table=True):
    __tablename__ = "mistake_gradings"  # type: ignore[assignment]

    id: int | None = Field(default=None, primary_key=True)
    session_id: str = Field(max_length=64, foreign_key="mistake_sessions.id", ondelete="CASCADE", unique=True)
    created_at: float
    annotations: list[dict[str, object]] = Field(sa_column=Column(JsonColumn, nullable=False))
    result: dict[str, object] = Field(sa_column=Column(JsonColumn, nullable=False))


class SQLModelMistakeExerciseRepository(MistakeExerciseRepository, BaseSQLModelRepository):
    @with_session
    async def save(self, session: AsyncSession, exercise: MistakeExercise) -> None:
        await session.merge(
            MistakeExerciseRecord(
                id=exercise.id,
                source_kind=exercise.source_kind,
                source_id=exercise.source_id,
                difficulty=exercise.difficulty,
                created_at=exercise.created_at,
                data=exercise.model_dump(mode="json"),
            )
        )

    @with_session
    async def get(self, session: AsyncSession, exercise_id: MistakeExerciseId) -> MistakeExercise:
        record = await session.get(MistakeExerciseRecord, exercise_id)
        if record is None:
            raise MistakeExerciseNotFoundException(exercise_id)
        return MistakeExercise.model_validate(record.data)

    @with_session
    async def of_source(self, session: AsyncSession, source_id: str, difficulty: Difficulty) -> list[MistakeExercise]:
        rows = await session.exec(
            select(MistakeExerciseRecord)
            .where(MistakeExerciseRecord.source_id == source_id, MistakeExerciseRecord.difficulty == difficulty)
            .order_by(col(MistakeExerciseRecord.id))
        )
        return [MistakeExercise.model_validate(r.data) for r in rows]

    @with_session
    async def ready_counts(self, session: AsyncSession) -> ReadyCounts:
        rows = await session.exec(
            select(MistakeExerciseRecord.source_id, MistakeExerciseRecord.difficulty, func.count()).group_by(
                col(MistakeExerciseRecord.source_id), col(MistakeExerciseRecord.difficulty)
            )
        )
        out: ReadyCounts = {}
        for source_id, difficulty, n in rows:
            out.setdefault(source_id, {})[difficulty] = n
        return out


class SQLModelMistakeSessionRepository(MistakeSessionRepository, BaseSQLModelRepository):
    @with_session
    async def add(self, session: AsyncSession, mistake_session: MistakeSession) -> None:
        session.add(
            MistakeSessionRecord(
                id=mistake_session.id,
                source_kind=mistake_session.source_kind,
                source_id=mistake_session.source_id,
                exercise_id=mistake_session.exercise_id,
                difficulty=mistake_session.difficulty,
                created_at=mistake_session.created_at,
            )
        )

    @with_session
    async def get(self, session: AsyncSession, session_id: SessionId) -> MistakeSession:
        record = await session.get(MistakeSessionRecord, session_id)
        if record is None:
            raise MistakeSessionNotFoundException(session_id)
        grading = (
            await session.exec(select(MistakeGradingRecord).where(MistakeGradingRecord.session_id == session_id))
        ).first()
        return MistakeSession.model_validate(
            record.model_dump(exclude={"grading_started_at"})
            | {"grading": MistakeGrading.model_validate(grading.result) if grading else None}
        )

    @with_session
    async def claim_grading(
        self, session: AsyncSession, session_id: SessionId, now: float, stale_before: float
    ) -> bool:
        graded = select(MistakeGradingRecord.id).where(MistakeGradingRecord.session_id == session_id).exists()
        result = await session.exec(
            update(MistakeSessionRecord)  # type: ignore[call-overload]
            .where(
                col(MistakeSessionRecord.id) == session_id,
                or_(
                    col(MistakeSessionRecord.grading_started_at).is_(None),
                    col(MistakeSessionRecord.grading_started_at) < stale_before,
                ),
                ~graded,
            )
            .values(grading_started_at=now)
        )
        return result.rowcount == 1

    @with_session
    async def release_grading(self, session: AsyncSession, session_id: SessionId, claimed_at: float) -> None:
        await session.exec(
            update(MistakeSessionRecord)  # type: ignore[call-overload]
            .where(
                col(MistakeSessionRecord.id) == session_id, col(MistakeSessionRecord.grading_started_at) == claimed_at
            )
            .values(grading_started_at=None)
        )

    @with_session
    async def save_grading(
        self,
        session: AsyncSession,
        session_id: SessionId,
        annotations: list[Annotation],
        grading: MistakeGrading,
        now: float,
    ) -> None:
        session.add(
            MistakeGradingRecord(
                session_id=session_id,
                created_at=now,
                annotations=[a.model_dump(mode="json") for a in annotations],
                result=grading.model_dump(mode="json"),
            )
        )
        try:
            await session.flush()
        except IntegrityError as e:
            # The one constraint a grading of an existing session can break: session_id is unique, so another
            # grading of it was stored first. Raising rolls this transaction back.
            raise MistakeSessionAlreadyGradedException(session_id) from e
