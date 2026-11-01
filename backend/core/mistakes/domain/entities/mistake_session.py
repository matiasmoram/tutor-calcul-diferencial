from pydantic import BaseModel, Field

from core.mistakes.domain.entities.mistake_exercise import SourceId
from core.mistakes.domain.entities.mistake_grading import MistakeGrading, PartGrading
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.layout import Layout
from core.mistakes.domain.values.mistake_exercise_id import MistakeExerciseId
from core.mistakes.domain.values.mistake_kind import SourceKind
from core.shared.domain.ids import SessionId


class MistakeSession(BaseModel):
    """One student working on one document. Graded once: the result reveals every error, so a resubmission would
    be free points; later submissions get the stored result. A per-parts session is graded part by part, in order,
    each flawed part once."""

    id: SessionId
    source_kind: SourceKind
    source_id: SourceId
    exercise_id: MistakeExerciseId
    difficulty: Difficulty
    created_at: float
    layout: Layout = "sencer"
    grading: MistakeGrading | None = None
    part_gradings: list[PartGrading] = Field(default_factory=list)  # by part
    hinted_parts: list[int] = Field(default_factory=list)

    def part_grading(self, part: int) -> PartGrading | None:
        return next((g for g in self.part_gradings if g.part == part), None)

    def next_part(self, flawed_parts: list[int]) -> int | None:
        """The first flawed part not graded yet; None once every one is."""
        graded = {g.part for g in self.part_gradings}
        return next((p for p in flawed_parts if p not in graded), None)
