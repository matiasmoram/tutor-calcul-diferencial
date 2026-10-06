from pydantic import BaseModel

from core.course.domain.ports import CourseSource
from core.course.domain.repository import CourseRepository


class CourseImportSummary(BaseModel):
    topics: int
    theory_items: int
    sheets: int
    exercises: int


class CourseImporter:
    """Replaces the stored course with the authored content (run after sheets or notes change)."""

    def __init__(self, source: CourseSource, repository: CourseRepository) -> None:
        self._source = source
        self._courses = repository

    async def import_course(self) -> CourseImportSummary:
        course = self._source.load()
        await self._courses.replace(course)
        return CourseImportSummary(
            topics=len(course.topics),
            theory_items=len(course.theory),
            sheets=len(course.sheets),
            exercises=len(course.exercises),
        )
