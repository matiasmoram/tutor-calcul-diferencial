from pydantic import BaseModel

from core.mistakes.domain.entities.mistake_exercise import SourceId
from core.mistakes.domain.entities.mistake_grading import MistakeGrading
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.mistake_exercise_id import MistakeExerciseId
from core.mistakes.domain.values.mistake_kind import SourceKind
from core.shared.domain.ids import SessionId


class MistakeSession(BaseModel):
    """One student working on one document. Graded once: the result reveals every error, so a resubmission would
    be free points; later submissions get the stored result."""

    id: SessionId
    source_kind: SourceKind
    source_id: SourceId
    exercise_id: MistakeExerciseId
    difficulty: Difficulty
    created_at: float
    grading: MistakeGrading | None = None
