from pydantic import BaseModel

from core.shared.domain.ids import ExerciseId, SessionId
from core.tutoring.domain.entities.tutor_turn import TutorTurn
from core.tutoring.domain.exceptions import TutorSessionNotFoundException
from core.tutoring.domain.repository import TutorSessionRepository
from core.tutoring.domain.values.session_summary import SessionSummary

DEFAULT_LIMIT = 200


class SessionTranscript(BaseModel):
    session_id: SessionId
    exercise_id: ExerciseId
    turns: list[TutorTurn]


class SessionBrowser:
    """The professor's review of tutoring sessions."""

    def __init__(self, sessions: TutorSessionRepository) -> None:
        self._sessions = sessions

    async def list_sessions(self, limit: int = DEFAULT_LIMIT) -> list[SessionSummary]:
        """Most recent first, sessions without any turn left out."""
        return [
            SessionSummary.of(session, turns)
            for session, turns in await self._sessions.recent_with_turns(limit)
            if turns
        ]

    async def transcript(self, session_id: SessionId) -> SessionTranscript:
        turns = await self._sessions.turns(session_id)
        if not turns:
            raise TutorSessionNotFoundException(session_id)
        session = await self._sessions.get(session_id)
        return SessionTranscript(session_id=session.id, exercise_id=session.exercise_id, turns=turns)
