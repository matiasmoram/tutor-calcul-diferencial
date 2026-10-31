from pydantic import BaseModel

from core.mistakes.application.part_annotations_grader import GRADING_CLAIM_TIMEOUT_S, parted_session
from core.mistakes.domain.exceptions import GradingInProgressException, MistakePartOutOfOrderException
from core.mistakes.domain.repository import MistakeExerciseRepository, MistakeSessionRepository
from core.shared.domain.clock import Clock
from core.shared.domain.ids import SessionId


class RevealedPartHint(BaseModel):
    part: int
    hint: str


class PartHintRevealer:
    """The hint of a flawed part, recorded: a hinted part scores x HINT_FACTOR. Only for the part under review (or
    a graded one, where it costs nothing).

    The hint is recorded under the session's claim: while the part's grading holds it the reveal is refused, so a
    hint never lands under a running grading."""

    def __init__(self, sessions: MistakeSessionRepository, exercises: MistakeExerciseRepository, clock: Clock) -> None:
        self._sessions = sessions
        self._exercises = exercises
        self._clock = clock

    async def reveal(self, session_id: SessionId, part: int) -> RevealedPartHint:
        session, document = await parted_session(self._sessions, self._exercises, session_id, part)
        mistake = document.part(part).mistake
        revealed = RevealedPartHint(part=part, hint=mistake.hint if mistake is not None else "")
        if session.part_grading(part) is not None or part in session.hinted_parts:
            return revealed  # nothing to record
        if session.next_part(document.flawed_parts) != part:
            raise MistakePartOutOfOrderException(part)
        claimed_at = self._clock.now()
        if not await self._sessions.claim_part(session_id, part, claimed_at, claimed_at - GRADING_CLAIM_TIMEOUT_S):
            if (await self._sessions.get(session_id)).part_grading(part) is not None:
                return revealed  # graded meanwhile: after the grading the hint costs nothing
            raise GradingInProgressException()
        try:
            await self._sessions.add_hint(session_id, part, claimed_at)
        finally:
            await self._sessions.release_grading(session_id, claimed_at)
        return revealed
