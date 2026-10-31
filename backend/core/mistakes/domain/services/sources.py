from core.course.domain.entities.course import Course
from core.course.domain.entities.theory_item import TheoryItem
from core.mistakes.domain.exceptions import MistakeSourceRequiredException, UnknownTheoryResultException
from core.mistakes.domain.values.mistake_kind import THEORY_RESULT_KINDS, SourceKind
from core.mistakes.domain.values.mistake_source import MistakeSource, ProblemSource, TheorySource


def _is_result_with_proof(item: TheoryItem) -> bool:
    return item.kind in THEORY_RESULT_KINDS and item.number is not None and bool(item.proof.strip())


def theory_results(course: Course) -> list[TheoryItem]:
    """Theory items eligible for the activity: numbered results that have a proof in the notes."""
    return [it for it in course.theory.values() if _is_result_with_proof(it)]


def theory_result(course: Course, item_id: str) -> TheoryItem:
    item = course.theory.get(item_id)
    if item is None or not _is_result_with_proof(item):
        raise UnknownTheoryResultException(item_id)
    return item


def resolve_source(course: Course, exercise_id: str | None, theory_id: str | None) -> MistakeSource:
    """Exactly one source: an exercise of the collection or a result of the notes."""
    if bool(exercise_id) == bool(theory_id):
        raise MistakeSourceRequiredException()
    if exercise_id:
        return ProblemSource.of(course, course.exercise(exercise_id))
    return TheorySource.of(course, theory_result(course, theory_id or ""))


def source_of(course: Course, kind: SourceKind, source_id: str) -> MistakeSource:
    if kind == "problema":
        return resolve_source(course, source_id, None)
    return resolve_source(course, None, source_id)
