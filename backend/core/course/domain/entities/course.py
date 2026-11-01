from pydantic import BaseModel

from core.course.domain.entities.exercise import Exercise
from core.course.domain.entities.problem_sheet import ProblemSheet
from core.course.domain.entities.theory_item import TheoryItem
from core.course.domain.entities.topic import Topic
from core.course.domain.exceptions import (
    ExerciseNotFoundException,
    InvalidCourseContentException,
    ProblemSheetNotFoundException,
    TheoryItemNotFoundException,
)
from core.course.domain.values.theory_ref import TheoryRef
from core.shared.domain.ids import TheoryItemId


class Course(BaseModel):
    """The whole authored content: topics, theory notes, problem sheets and their exercises.

    Read-only at run time and small (a few hundred exercises), so it is loaded whole and queried in memory."""

    topics: list[Topic]
    theory: dict[str, TheoryItem]
    sheets: dict[str, ProblemSheet]
    exercises: dict[str, Exercise]

    def model_post_init(self, context: object, /) -> None:
        missing = {
            ex.id: [r for r in ex.all_refs() if r.item_id not in self.theory]
            for ex in self.exercises.values()
            if any(r.item_id not in self.theory for r in ex.all_refs())
        }
        if missing:
            raise InvalidCourseContentException(f"unknown theory references: {missing}")

    def exercise(self, exercise_id: str) -> Exercise:
        ex = self.exercises.get(exercise_id)
        if ex is None:
            raise ExerciseNotFoundException(exercise_id)
        return ex

    def sheet(self, sheet_id: str) -> ProblemSheet:
        sheet = self.sheets.get(sheet_id)
        if sheet is None:
            raise ProblemSheetNotFoundException(sheet_id)
        return sheet

    def theory_item(self, item_id: str) -> TheoryItem:
        item = self.theory.get(item_id)
        if item is None:
            raise TheoryItemNotFoundException(item_id)
        return item

    def items(self, refs: list[TheoryRef]) -> list[TheoryItem]:
        return [self.theory[r.item_id] for r in refs]

    def cited_theory(self, ex: Exercise) -> tuple[list[TheoryItem], frozenset[TheoryItemId]]:
        """Every item the sheet cites (reserved ones included), in order, and the ids of those cited with their proof
        ("+dem"): for the stages that see the full solution."""
        refs = ex.all_refs()
        ids = dict.fromkeys(r.item_id for r in refs)
        return [self.theory[i] for i in ids], frozenset(r.item_id for r in refs if r.with_proof)

    def citable_items(self, topic: int) -> list[TheoryItem]:
        """Citable items of one topic, for the diagnosis to pick from on concept questions."""
        return [it for it in self.theory.values() if it.topic == topic and it.citable]

    def reserved_ids(self, ex: Exercise) -> set[TheoryItemId]:
        """Items the reply stage must never see: declared ones, plus any item of the notes citing this problem."""
        own = f"T{ex.topic}.{ex.problem}"
        auto = {it.id for it in self.theory.values() if own in it.problems} if ex.topic else set()
        return {r.item_id for r in ex.reserved_theory} | auto
