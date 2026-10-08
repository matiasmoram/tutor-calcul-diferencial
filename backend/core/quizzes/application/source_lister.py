from collections.abc import Mapping

from pydantic import BaseModel

from core.course.domain.entities.course import Course
from core.course.domain.entities.theory_item import TheoryItem
from core.course.domain.entities.topic import Topic
from core.quizzes.domain.repository import QuizRepository
from core.quizzes.domain.sources import focus_items
from core.quizzes.domain.values.difficulty import QUIZ_SIZES, Difficulty


class FocusSource(BaseModel):
    item: TheoryItem
    available: dict[Difficulty, int]  # ready quizzes per difficulty (absent = none)


class TopicSources(BaseModel):
    topic: Topic
    source_id: str  # "tema-2"
    available: dict[Difficulty, int]
    focus: list[FocusSource]


class QuizSourceIndex(BaseModel):
    topics: list[TopicSources]
    sizes: Mapping[Difficulty, int]  # statements per quiz


class SourceLister:
    """Topics (whole-topic quizzes) and the results of the notes that can be the focus, with ready quizzes."""

    def __init__(self, course: Course, quizzes: QuizRepository) -> None:
        self._course = course
        self._quizzes = quizzes

    async def list_sources(self) -> QuizSourceIndex:
        ready = await self._quizzes.availability()
        items = [FocusSource(item=it, available=ready.get(it.id, {})) for it in focus_items(self._course)]
        return QuizSourceIndex(
            topics=[
                TopicSources(
                    topic=t,
                    source_id=f"tema-{t.number}",
                    available=ready.get(f"tema-{t.number}", {}),
                    focus=[f for f in items if f.item.topic == t.number],
                )
                for t in self._course.topics
            ],
            sizes=dict(QUIZ_SIZES),
        )
