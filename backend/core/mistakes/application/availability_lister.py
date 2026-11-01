from pydantic import BaseModel

from core.course.domain.entities.course import Course
from core.course.domain.entities.theory_item import TheoryItem
from core.course.domain.entities.topic import Topic
from core.mistakes.domain.repository import Availability, MistakeExerciseRepository
from core.mistakes.domain.services.sources import theory_results
from core.mistakes.domain.values.layout import Layout


class AvailableTheoryResult(BaseModel):
    item: TheoryItem
    ready: dict[str, int]  # {difficulty: number of ready documents}


class TopicTheoryResults(BaseModel):
    topic: Topic
    items: list[AvailableTheoryResult]


class AvailabilityLister:
    """What the UI can open without calling the model."""

    def __init__(self, course: Course, exercises: MistakeExerciseRepository) -> None:
        self._course = course
        self._exercises = exercises

    async def availability(self, layout: Layout = "sencer") -> Availability:
        """{source id: {difficulty: n}} of ready documents of the layout (exercises and theory results alike)."""
        return await self._exercises.availability(layout)

    async def theory_results(self, layout: Layout = "sencer") -> list[TopicTheoryResults]:
        """Every topic, with its results of the notes eligible for the theory activity and their ready documents of
        the layout."""
        ready = await self._exercises.availability(layout)
        items = [AvailableTheoryResult(item=it, ready=ready.get(it.id, {})) for it in theory_results(self._course)]
        return [
            TopicTheoryResults(topic=t, items=[i for i in items if i.item.topic == t.number])
            for t in self._course.topics
        ]
