from pydantic import BaseModel

from core.quizzes.domain.exceptions import ConcurrentQuizGradingException
from core.quizzes.domain.repository import QuizRepository, QuizSessionRepository
from core.quizzes.domain.values.grading_claim import GRADING_CLAIM_TIMEOUT_S
from core.shared.domain.clock import Clock


class RevealedHint(BaseModel):
    statement_id: str
    hint: str


class HintRevealer:
    """Hints are served one at a time and recorded: a used hint lowers that statement's score.

    A hint is recorded under the grading claim: while a grading holds it the reveal is refused, so a hint can never
    change the session under a running grading and make its save fail after the grader was paid for."""

    def __init__(self, sessions: QuizSessionRepository, quizzes: QuizRepository, clock: Clock) -> None:
        self._sessions = sessions
        self._quizzes = quizzes
        self._clock = clock

    async def reveal(self, session_id: str, statement_id: str) -> RevealedHint:
        session = await self._sessions.get(session_id)
        statement = (await self._quizzes.get(session.quiz_id)).statement(statement_id)
        revealed = RevealedHint(statement_id=statement.id, hint=statement.hint)
        if session.graded or statement.id in session.hints_used:
            return revealed  # nothing to record
        claimed_at = self._clock.now()
        if not await self._sessions.claim_grading(session_id, claimed_at, claimed_at - GRADING_CLAIM_TIMEOUT_S):
            if (await self._sessions.get(session_id)).graded:
                return revealed  # graded meanwhile: after the grading hints cost nothing
            raise ConcurrentQuizGradingException(session_id)
        try:
            session = await self._sessions.get(session_id)
            if session.use_hint(statement.id, claimed_at):
                await self._sessions.save(session)
        finally:
            await self._sessions.release_grading(session_id, claimed_at)
        return revealed
