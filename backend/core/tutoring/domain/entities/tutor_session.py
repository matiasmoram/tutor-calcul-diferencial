from pydantic import BaseModel, Field

from core.shared.domain.ids import ExerciseId, SessionId
from core.tutoring.domain.values.chat_message import ChatMessage
from core.tutoring.domain.values.session_state import SessionState


class TutorSession(BaseModel):
    """A student working on one exercise with the tutor: the conversation and the policy's state.

    The database holds the only copy. ``version`` is the stored version this object was read at: saving a turn on
    a stale version fails (optimistic concurrency), so two turns of one session never interleave."""

    id: SessionId
    exercise_id: ExerciseId
    history: list[ChatMessage] = Field(default_factory=list)
    state: SessionState = Field(default_factory=SessionState)
    version: int = 0
    created_at: float
    updated_at: float

    @classmethod
    def start(cls, exercise_id: ExerciseId, now: float) -> "TutorSession":
        return cls(id=SessionId.generate(), exercise_id=exercise_id, created_at=now, updated_at=now)

    @property
    def closed(self) -> bool:
        return self.state.closed

    @property
    def next_turn(self) -> int:
        return self.state.turns + 1

    def history_with(self, student_text: str) -> list[ChatMessage]:
        """The conversation as the stages of a turn see it: with the student's new message."""
        return [*self.history, ChatMessage.from_student(student_text)]

    def record_turn(self, student_text: str, tutor_text: str, state: SessionState, now: float) -> None:
        self.history = [*self.history_with(student_text), ChatMessage.from_tutor(tutor_text)]
        self.state = state
        self.updated_at = now
