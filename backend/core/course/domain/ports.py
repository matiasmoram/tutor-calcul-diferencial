from typing import Protocol

from core.course.domain.entities.course import Course


class CourseSource(Protocol):
    """Where the authored content comes from (the YAML files in the repository)."""

    def load(self) -> Course: ...
