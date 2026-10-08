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
    async def claim_turn(self, session_id: SessionId, now: float, stale_before: float) -> bool:
        """Marks a turn as in progress, claimed at `now`, unless another one is (a claim older than `stale_before`
        is taken over). False when another turn holds it: a second message must be refused before any model is
        called. Raises TutorSessionNotFoundException for an unknown session."""

    @abstractmethod
    async def release_turn(self, session_id: SessionId, claimed_at: float) -> None:
        """Drops the claim made at `claimed_at`, only if it is still that one: a claim taken over after it went
        stale belongs to another turn and stays."""

    @abstractmethod
    async def save_turn(self, session: TutorSession, turn: TutorTurn, claimed_at: float) -> TutorSession:
        """Stores the session after `turn` together with the turn, in one transaction, and releases the turn
        claim, if the stored session is still at ``session.version`` and the claim is still the one made at
        `claimed_at`; raises ConcurrentTurnException otherwise (a turn whose claim was taken over never stores).
        Returns the session at its new version."""

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
