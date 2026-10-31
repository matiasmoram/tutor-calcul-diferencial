"""Which items of the notes each audience of a tutoring session may see (beyond the per-turn gate in policy.py)."""

from pydantic import BaseModel

from core.course.domain.entities.course import Course
from core.course.domain.entities.exercise import Exercise
from core.course.domain.entities.theory_item import TheoryItem
from core.shared.domain.ids import TheoryItemId


class SheetTheoryUse(BaseModel):
    """For the professor panel: an item the sheet cites, where it is used, and whether the reply stage may see it."""

    item: TheoryItem
    used_in: list[str]  # "enunciat" (the statement's background theory) or step ids
    reserved: bool


def background_theory(course: Course, ex: Exercise) -> list[TheoryItem]:
    """Theory the student may read from the start (never the items that solve the exercise)."""
    reserved = course.reserved_ids(ex)
    ids = [i for i in dict.fromkeys(r.item_id for r in ex.theory) if i in course.theory and i not in reserved]
    return [course.theory[i] for i in ids]


def concept_question_ids(course: Course, ex: Exercise) -> list[TheoryItemId]:
    """What the diagnosis may point to for a conceptual question: the sheet's items and the topic's index."""
    reserved = course.reserved_ids(ex)
    ids = [r.item_id for r in ex.all_refs()] + [it.id for it in course.citable_items(ex.topic or 0)]
    return [i for i in dict.fromkeys(ids) if i in course.theory and i not in reserved]


def sheet_theory(course: Course, ex: Exercise) -> list[SheetTheoryUse]:
    reserved = course.reserved_ids(ex)
    used: dict[TheoryItemId, list[str]] = {}
    for r in ex.theory:
        used.setdefault(r.item_id, []).append("enunciat")
    for step in ex.steps:
        for r in step.theory:
            used.setdefault(r.item_id, []).append(step.id)
    for r in ex.reserved_theory:
        used.setdefault(r.item_id, [])
    for i in sorted(reserved):
        used.setdefault(i, [])
    return [
        SheetTheoryUse(item=course.theory[i], used_in=on, reserved=i in reserved)
        for i, on in used.items()
        if i in course.theory
    ]
