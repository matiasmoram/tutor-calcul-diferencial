from abc import ABC, abstractmethod

from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_grading import MistakeGrading, PartGrading
from core.mistakes.domain.entities.mistake_session import MistakeSession
from core.mistakes.domain.entities.parted_mistake_exercise import MistakeDocument
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.layout import Layout
from core.mistakes.domain.values.mistake_exercise_id import MistakeExerciseId
from core.shared.domain.ids import SessionId

# {source id: {difficulty: number of ready documents}}, only non-zero counts.
type Availability = dict[str, dict[str, int]]


class MistakeExerciseRepository(ABC):
    @abstractmethod
    async def save(self, exercise: MistakeDocument) -> None:
        """Insert, or replace the document with the same id."""

    @abstractmethod
    async def get(self, exercise_id: MistakeExerciseId) -> MistakeDocument:
        """Raises MistakeExerciseNotFoundException."""

    @abstractmethod
    async def of_source(
        self, source_id: str, difficulty: Difficulty, layout: Layout = "sencer"
    ) -> list[MistakeDocument]:
        """Ready documents of one source, difficulty and layout, ordered by id."""

    @abstractmethod
    async def availability(self, layout: Layout = "sencer") -> Availability:
        """Ready documents of one layout."""


class MistakeSessionRepository(ABC):
    @abstractmethod
    async def add(self, session: MistakeSession) -> None: ...

    @abstractmethod
    async def get(self, session_id: SessionId) -> MistakeSession:
        """With its grading, its part gradings and hinted parts, if any. Raises MistakeSessionNotFoundException."""

    @abstractmethod
    async def claim_grading(self, session_id: SessionId, now: float, stale_before: float) -> bool:
        """Marks the session as being graded, claimed at `now`, unless it is graded already or another claim newer
        than `stale_before` holds it. True when this caller got the claim."""

    @abstractmethod
    async def claim_part(self, session_id: SessionId, part: int, now: float, stale_before: float) -> bool:
        """The same claim for one part of a per-parts session (its grading, or recording its hint), unless the part
        is graded already or another claim newer than `stale_before` holds the session. True when this caller got
        it; `release_grading` drops it."""

    @abstractmethod
    async def release_grading(self, session_id: SessionId, claimed_at: float) -> None:
        """Drops the claim made at `claimed_at`, only if it is still that one: a claim taken over after it went
        stale belongs to another grading and stays."""

    @abstractmethod
    async def save_grading(
        self, session_id: SessionId, annotations: list[Annotation], grading: MistakeGrading, now: float
    ) -> None:
        """Raises MistakeSessionAlreadyGradedException when the session has a grading already: a session is
        graded once."""

    @abstractmethod
    async def save_part_grading(
        self, session_id: SessionId, annotations: list[Annotation], grading: PartGrading, now: float
    ) -> None:
        """Raises MistakePartAlreadyGradedException when the part has a grading already: a part is graded once."""

    @abstractmethod
    async def add_hint(self, session_id: SessionId, part: int, now: float) -> None:
        """Records that the student asked for the part's hint. Recording it again changes nothing."""
