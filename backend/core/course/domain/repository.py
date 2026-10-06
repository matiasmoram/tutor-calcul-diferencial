from abc import ABC, abstractmethod

from core.course.domain.entities.course import Course


class CourseRepository(ABC):
    @abstractmethod
    async def load(self) -> Course | None:
        """The stored course, or None when nothing has been imported yet."""

    @abstractmethod
    async def replace(self, course: Course) -> None:
        """Stores `course` as the whole content (topics, theory, sheets, exercises), replacing what was there."""

    @abstractmethod
    async def count_exercises(self) -> int: ...
