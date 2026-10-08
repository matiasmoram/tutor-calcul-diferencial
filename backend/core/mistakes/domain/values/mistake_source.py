"""Where a document comes from, with the reference material the model stages compare it against."""

from typing import Literal

from pydantic import BaseModel, ConfigDict

from core.course.domain.citations import cited_items
from core.course.domain.entities.course import Course
from core.course.domain.entities.exercise import Exercise
from core.course.domain.entities.theory_item import TheoryItem
from core.shared.domain.ids import ExerciseId, TheoryItemId


class ProblemSource(BaseModel):
    """A worked solution of one exercise ("resolució dolenta"), checked against its solution sheet."""

    model_config = ConfigDict(frozen=True)

    kind: Literal["problema"] = "problema"
    exercise: Exercise
    # Every item the sheet cites (reserved ones included), in order; the ones cited "+dem" with their proof.
    theory: list[TheoryItem]
    with_proof: frozenset[TheoryItemId]

    @property
    def id(self) -> ExerciseId:
        return self.exercise.id

    @classmethod
    def of(cls, course: Course, exercise: Exercise) -> "ProblemSource":
        refs = exercise.all_refs()
        ids = [i for i in dict.fromkeys(r.item_id for r in refs) if i in course.theory]
        return cls(
            exercise=exercise,
            theory=[course.theory[i] for i in ids],
            with_proof=frozenset(r.item_id for r in refs if r.with_proof),
        )


class TheorySource(BaseModel):
    """A result of the notes (statement + proof), checked against the original item."""

    model_config = ConfigDict(frozen=True)

    kind: Literal["teoria"] = "teoria"
    item: TheoryItem
    cited: list[TheoryItem]  # the numbered items of the notes its statement and proof cite

    @property
    def id(self) -> TheoryItemId:
        return self.item.id

    @classmethod
    def of(cls, course: Course, item: TheoryItem) -> "TheorySource":
        numbered = [x for x in course.theory.values() if x.number is not None and x.id != item.id]
        ids = cited_items(f"{item.statement}\n{item.proof}", numbered, item.topic)
        return cls(item=item, cited=[course.theory[i] for i in ids])


type MistakeSource = ProblemSource | TheorySource
