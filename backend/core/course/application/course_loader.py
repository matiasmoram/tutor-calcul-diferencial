from core.course.domain.entities.course import Course
from core.course.domain.ports import CourseSource
from core.course.domain.repository import CourseRepository


class CourseLoader:
    """The course the app serves: the stored one, imported from the authored source on first start."""

    def __init__(self, repository: CourseRepository, source: CourseSource) -> None:
        self._courses = repository
        self._source = source

    async def load(self) -> Course:
        course = await self._courses.load()
        if course is None:
            course = self._source.load()
            await self._courses.replace(course)
        return course
