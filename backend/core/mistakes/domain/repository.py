from abc import ABC, abstractmethod

from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.entities.mistake_grading import MistakeGrading
from core.mistakes.domain.entities.mistake_session import MistakeSession
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.mistake_exercise_id import MistakeExerciseId
from core.shared.domain.ids import SessionId

# {source id: {difficulty: number of ready documents}}, only non-zero counts.
type ReadyCounts = dict[str, dict[str, int]]


class MistakeExerciseRepository(ABC):
    @abstractmethod
    async def save(self, exercise: MistakeExercise) -> None:
        """Insert, or replace the document with the same id."""

    @abstractmethod
    async def get(self, exercise_id: MistakeExerciseId) -> MistakeExercise:
        """Raises MistakeExerciseNotFoundException."""

    @abstractmethod
    async def of_source(self, source_id: str, difficulty: Difficulty) -> list[MistakeExercise]:
        """Ready documents of one source and difficulty, ordered by id."""

    @abstractmethod
    async def ready_counts(self) -> ReadyCounts: ...


class MistakeSessionRepository(ABC):
    @abstractmethod
    async def add(self, mistake_session: MistakeSession) -> None: ...

    @abstractmethod
    async def get(self, session_id: SessionId) -> MistakeSession:
        """With its grading, if any. Raises MistakeSessionNotFoundException."""

    @abstractmethod
    async def claim_grading(self, session_id: SessionId, now: float, stale_before: float) -> bool:
        """Marks the session as being graded unless it is graded already or another claim newer than
        `stale_before` holds it. True when this caller got the claim."""

    @abstractmethod
    async def release_grading(self, session_id: SessionId) -> None:
        """Drops a claim whose grading failed, so the student can submit again."""

    @abstractmethod
    async def save_grading(
        self, session_id: SessionId, annotations: list[Annotation], grading: MistakeGrading, now: float
    ) -> None: ...
