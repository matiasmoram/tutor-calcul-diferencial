from abc import ABC, abstractmethod

from core.shared.domain.ids import SessionId
from core.tutoring.domain.entities.tutor_session import TutorSession
from core.tutoring.domain.entities.tutor_turn import TutorTurn
from core.tutoring.domain.values.transcription import Transcription


class TutorSessionRepository(ABC):
    @abstractmethod
    async def add(self, session: TutorSession) -> None: ...

    @abstractmethod
    async def get(self, session_id: SessionId) -> TutorSession:
        """Raises TutorSessionNotFoundException."""

    @abstractmethod
    async def save_turn(self, session: TutorSession, turn: TutorTurn) -> TutorSession:
        """Stores the session after `turn` together with the turn, in one transaction, if the stored session is
        still at ``session.version``; raises ConcurrentTurnException otherwise. Returns it at its new version."""

    @abstractmethod
    async def turns(self, session_id: SessionId) -> list[TutorTurn]:
        """In order."""

    @abstractmethod
    async def recent_with_turns(self, limit: int) -> list[tuple[TutorSession, list[TutorTurn]]]:
        """The `limit` most recently active sessions, most recent first, each with its turns in order."""

    @abstractmethod
    async def add_transcription(
        self, session_id: SessionId, transcription: Transcription, created_at: float
    ) -> None: ...
