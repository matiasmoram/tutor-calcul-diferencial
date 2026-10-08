from pydantic import BaseModel

from core.quizzes.domain.repository import QuizRepository, QuizSessionRepository
from core.shared.domain.clock import Clock


class RevealedHint(BaseModel):
    statement_id: str
    hint: str


class HintRevealer:
    """Hints are served one at a time and recorded: a used hint lowers that statement's score."""

    def __init__(self, sessions: QuizSessionRepository, quizzes: QuizRepository, clock: Clock) -> None:
        self._sessions = sessions
        self._quizzes = quizzes
        self._clock = clock

    async def reveal(self, session_id: str, statement_id: str) -> RevealedHint:
        session = await self._sessions.get(session_id)
        statement = (await self._quizzes.get(session.quiz_id)).statement(statement_id)
        if session.use_hint(statement.id, self._clock.now()):
            await self._sessions.save(session)
        return RevealedHint(statement_id=statement.id, hint=statement.hint)
