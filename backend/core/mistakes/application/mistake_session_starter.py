from pydantic import BaseModel, Field

from core.course.domain.entities.course import Course
from core.mistakes.application.mistake_exercise_provider import MistakeExerciseProvider
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.entities.mistake_session import MistakeSession
from core.mistakes.domain.repository import MistakeSessionRepository
from core.mistakes.domain.sources import resolve_source
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.mistake_source import MistakeSource
from core.shared.domain.clock import Clock
from core.shared.domain.ids import SessionId
from core.shared.llm.call_scope import call_scope


class MistakeSessionStarterInput(BaseModel):
    # Exactly one source. Plain strings: an id that is malformed or unknown is the same 404 for the student.
    exercise_id: str | None = None
    theory_id: str | None = None
    difficulty: Difficulty = "normal"
    fresh: bool = False  # generate a new document even if some are ready
    avoid: str | None = Field(default=None, max_length=40)  # document just seen: prefer another one


class StartedMistakeSession(BaseModel):
    session: MistakeSession
    source: MistakeSource
    exercise: MistakeExercise
    freshly_generated: bool


class MistakeSessionStarter:
    def __init__(
        self, course: Course, provider: MistakeExerciseProvider, sessions: MistakeSessionRepository, clock: Clock
    ) -> None:
        self._course = course
        self._provider = provider
        self._sessions = sessions
        self._clock = clock

    async def needs_generation(self, data: MistakeSessionStarterInput) -> bool:
        """Whether `start(data)` will call the model (the API checks the provider key first)."""
        source = resolve_source(self._course, data.exercise_id, data.theory_id)
        return data.fresh or not await self._provider.has_ready(source, data.difficulty)

    async def start(self, data: MistakeSessionStarterInput) -> StartedMistakeSession:
        source = resolve_source(self._course, data.exercise_id, data.theory_id)
        session_id = SessionId.generate()
        with call_scope(session_id):
            provided = await self._provider.get_or_generate(source, data.difficulty, data.fresh, data.avoid)
        session = MistakeSession(
            id=session_id,
            source_kind=source.kind,
            source_id=source.id,
            exercise_id=provided.exercise.id,
            difficulty=data.difficulty,
            created_at=self._clock.now(),
        )
        await self._sessions.add(session)
        return StartedMistakeSession(
            session=session, source=source, exercise=provided.exercise, freshly_generated=provided.freshly_generated
        )
