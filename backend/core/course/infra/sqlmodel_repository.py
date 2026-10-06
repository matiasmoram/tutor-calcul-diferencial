from sqlalchemy import Column, Index, delete, func
from sqlmodel import Field, SQLModel, col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.course.domain.entities.course import Course
from core.course.domain.entities.exercise import Exercise
from core.course.domain.entities.problem_sheet import ProblemSheet
from core.course.domain.entities.theory_item import TheoryItem
from core.course.domain.entities.topic import Topic
from core.course.domain.repository import CourseRepository
from core.shared.storage.session_provider import BaseSQLModelRepository, JsonColumn, with_session


class TopicRecord(SQLModel, table=True):
    __tablename__ = "topics"  # type: ignore[assignment]

    number: int = Field(primary_key=True)
    title: str
    data: dict[str, object] = Field(sa_column=Column(JsonColumn, nullable=False))


class TheoryItemRecord(SQLModel, table=True):
    __tablename__ = "theory_items"  # type: ignore[assignment]
    __table_args__ = (Index("ix_theory_items_topic", "topic"),)

    id: str = Field(primary_key=True, max_length=32)
    topic: int
    kind: str = Field(max_length=24)
    number: int | None = None
    position: int  # order of the notes
    data: dict[str, object] = Field(sa_column=Column(JsonColumn, nullable=False))


class ProblemSheetRecord(SQLModel, table=True):
    __tablename__ = "problem_sheets"  # type: ignore[assignment]

    id: str = Field(primary_key=True, max_length=64)
    position: int
    data: dict[str, object] = Field(sa_column=Column(JsonColumn, nullable=False))


class ExerciseRecord(SQLModel, table=True):
    __tablename__ = "exercises"  # type: ignore[assignment]
    __table_args__ = (Index("ix_exercises_sheet_id", "sheet_id"),)

    id: str = Field(primary_key=True, max_length=32)
    sheet_id: str = Field(max_length=64, foreign_key="problem_sheets.id", ondelete="CASCADE")
    problem: int
    part: str | None = Field(default=None, max_length=8)
    position: int
    data: dict[str, object] = Field(sa_column=Column(JsonColumn, nullable=False))


class SQLModelCourseRepository(CourseRepository, BaseSQLModelRepository):
    """Each entity is stored whole as a JSON document, with its key columns alongside for querying."""

    @with_session
    async def load(self, session: AsyncSession) -> Course | None:
        exercises = (await session.exec(select(ExerciseRecord).order_by(col(ExerciseRecord.position)))).all()
        if not exercises:
            return None
        topics = (await session.exec(select(TopicRecord).order_by(col(TopicRecord.number)))).all()
        items = (await session.exec(select(TheoryItemRecord).order_by(col(TheoryItemRecord.position)))).all()
        sheets = (await session.exec(select(ProblemSheetRecord).order_by(col(ProblemSheetRecord.position)))).all()
        return Course(
            topics=[Topic.model_validate(r.data) for r in topics],
            theory={r.id: TheoryItem.model_validate(r.data) for r in items},
            sheets={r.id: ProblemSheet.model_validate(r.data) for r in sheets},
            exercises={r.id: Exercise.model_validate(r.data) for r in exercises},
        )

    @with_session
    async def replace(self, session: AsyncSession, course: Course) -> None:
        for table in (ExerciseRecord, ProblemSheetRecord, TheoryItemRecord, TopicRecord):
            await session.exec(delete(table))  # type: ignore[call-overload]
        session.add_all(
            [TopicRecord(number=t.number, title=t.title, data=t.model_dump(mode="json")) for t in course.topics]
        )
        session.add_all(
            TheoryItemRecord(
                id=it.id, topic=it.topic, kind=it.kind, number=it.number, position=i, data=it.model_dump(mode="json")
            )
            for i, it in enumerate(course.theory.values())
        )
        session.add_all(
            ProblemSheetRecord(id=s.id, position=i, data=s.model_dump(mode="json"))
            for i, s in enumerate(course.sheets.values())
        )
        await session.flush()  # sheets before the exercises that reference them
        session.add_all(
            ExerciseRecord(
                id=ex.id,
                sheet_id=ex.sheet_id,
                problem=ex.problem,
                part=ex.part,
                position=i,
                data=ex.model_dump(mode="json"),
            )
            for i, ex in enumerate(course.exercises.values())
        )

    @with_session
    async def count_exercises(self, session: AsyncSession) -> int:
        return (await session.exec(select(func.count()).select_from(ExerciseRecord))).one()
