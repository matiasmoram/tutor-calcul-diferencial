from pydantic import BaseModel, Field

from core.course.domain.entities.course import Course
from core.quizzes.application.quiz_provider import QuizProvider
from core.quizzes.domain.entities.quiz import Quiz
from core.quizzes.domain.entities.quiz_session import QuizSession
from core.quizzes.domain.repository import QuizSessionRepository
from core.quizzes.domain.services.sources import quiz_source
from core.quizzes.domain.values.difficulty import Difficulty
from core.quizzes.domain.values.quiz_source import QuizSource
from core.shared.domain.clock import Clock
from core.shared.domain.ids import SessionId
from core.shared.llm.call_scope import call_scope


class QuizSessionStarterInput(BaseModel):
    source_id: str = Field(max_length=20)  # "tema-2", or a result of the notes ("T2.12") as the focus
    difficulty: Difficulty = "normal"
    new: bool = False
    except_id: str | None = Field(default=None, max_length=40)  # quiz just seen: prefer another one


class StartedQuizSession(BaseModel):
    session: QuizSession
    quiz: Quiz
    source: QuizSource
    generated_now: bool


class QuizSessionStarter:
    def __init__(self, course: Course, provider: QuizProvider, sessions: QuizSessionRepository, clock: Clock) -> None:
        self._course = course
        self._provider = provider
        self._sessions = sessions
        self._clock = clock

    async def start(self, request: QuizSessionStarterInput) -> StartedQuizSession:
        source = quiz_source(self._course, request.source_id)
        session_id = SessionId.generate()
        with call_scope(session_id):
            provided = await self._provider.get_or_generate(source, request.difficulty, request.new, request.except_id)
        now = self._clock.now()
        session = QuizSession(
            id=session_id,
            source_id=source.id,
            difficulty=request.difficulty,
            quiz_id=provided.quiz.id,
            created_at=now,
            updated_at=now,
        )
        await self._sessions.add(session)
        return StartedQuizSession(
            session=session, quiz=provided.quiz, source=source, generated_now=provided.generated_now
        )
