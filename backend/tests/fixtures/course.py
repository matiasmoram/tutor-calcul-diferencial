"""The authored course, loaded once per test run (it is read-only)."""

from functools import cache

from core.course.domain.entities.course import Course
from core.course.infra.yaml_course_source import YamlCourseSource
from settings import BACKEND_DIR


def authored_source() -> YamlCourseSource:
    return YamlCourseSource(BACKEND_DIR / "exercicis", BACKEND_DIR / "teoria")


@cache
def authored_course() -> Course:
    return authored_source().load()
