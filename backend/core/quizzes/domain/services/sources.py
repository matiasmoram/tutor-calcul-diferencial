import re

from core.course.domain.entities.course import Course
from core.course.domain.entities.theory_item import TheoryItem
from core.quizzes.domain.exceptions import UnknownQuizSourceException
from core.quizzes.domain.values.quiz_source import QuizSource

# Results that can anchor a focused quiz.
FOCUS_KINDS: tuple[str, ...] = ("teorema", "proposicio", "lema", "corollari", "definicio")
_TOPIC_SOURCE = re.compile(r"tema-([1-6])")


def focus_items(course: Course) -> list[TheoryItem]:
    return [it for it in course.theory.values() if it.kind in FOCUS_KINDS and it.number is not None]


def topic_source(course: Course, topic: int, focus: TheoryItem | None = None) -> QuizSource:
    title = next((t.title for t in course.topics if t.number == topic), "")
    return QuizSource(
        topic=topic,
        topic_title=title,
        notes=tuple(it for it in course.theory.values() if it.topic == topic),
        allowed_refs=tuple(it.id for it in course.theory.values() if it.number is not None and it.topic <= topic),
        focus=focus,
    )


def quiz_source(course: Course, source_id: str) -> QuizSource:
    """``tema-2`` or the id of a focusable result of the notes (``T2.12``)."""
    m = _TOPIC_SOURCE.fullmatch(source_id)
    if m:
        return topic_source(course, int(m.group(1)))
    item = next((it for it in focus_items(course) if it.id == source_id), None)
    if item is None:
        raise UnknownQuizSourceException(source_id)
    return topic_source(course, item.topic, item)
