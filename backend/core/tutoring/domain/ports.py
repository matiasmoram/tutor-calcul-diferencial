"""The model stages of a turn. Each returns its output and the call that produced it (for the turn trace).

Implementations raise ``ModelOutputException`` when the model answered with something unusable; provider failures
(auth, rate limit, outage) propagate as they are."""

from collections.abc import Sequence
from typing import Protocol

from core.course.domain.entities.exercise import Exercise
from core.course.domain.entities.theory_item import TheoryItem
from core.shared.domain.ids import TheoryItemId
from core.tutoring.domain.values.chat_message import ChatMessage
from core.tutoring.domain.values.diagnosis import Diagnosis
from core.tutoring.domain.values.guard_verdict import GuardVerdict
from core.tutoring.domain.values.photo import Photo
from core.tutoring.domain.values.plan import Plan
from core.tutoring.domain.values.session_state import SessionState
from core.tutoring.domain.values.transcription import Transcription
from core.tutoring.domain.values.turn_trace import ModelCall


class Diagnoser(Protocol):
    async def diagnose(
        self, ex: Exercise, state: SessionState, history: Sequence[ChatMessage], concept_ids: Sequence[TheoryItemId]
    ) -> tuple[Diagnosis, ModelCall]:
        """The student's last message classified against the full solution. ``concept_ids``: the items it may
        point to for a conceptual question."""
        ...


class ReplyWriter(Protocol):
    async def write(
        self,
        ex: Exercise,
        history: Sequence[ChatMessage],
        plan: Plan,
        allowed_content: str,
        theory: Sequence[TheoryItem],
        feedback: str | None,
    ) -> tuple[str, ModelCall]:
        """A non-empty draft of the tutor's message. Sees only the plan and the content it allows; ``feedback``
        is why the previous draft was rejected."""
        ...


class ReplyJudge(Protocol):
    async def judge(
        self,
        ex: Exercise,
        plan: Plan,
        allowed_content: str,
        theory: Sequence[TheoryItem],
        history: Sequence[ChatMessage],
        message: str,
        references: Sequence[TheoryItemId],
    ) -> tuple[GuardVerdict, ModelCall]:
        """Whether a draft follows the plan, judged with the full solution."""
        ...


class Transcriber(Protocol):
    async def transcribe(self, ex: Exercise, photo: Photo) -> tuple[Transcription, ModelCall]: ...
