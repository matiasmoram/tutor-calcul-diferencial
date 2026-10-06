from core.shared.domain.exceptions import DomainException


class CourseException(DomainException):
    pass


class ExerciseNotFoundException(CourseException):
    def __init__(self, exercise_id: str) -> None:
        super().__init__(f"Exercici desconegut: {exercise_id}", 404)


class ProblemSheetNotFoundException(CourseException):
    def __init__(self, sheet_id: str) -> None:
        super().__init__(f"Llista desconeguda: {sheet_id}", 404)


class TheoryItemNotFoundException(CourseException):
    def __init__(self, item_id: str) -> None:
        super().__init__(f"Ítem de teoria desconegut: {item_id}", 404)


class UnknownStepException(CourseException):
    """A step or mistake id that the sheet does not define: a programming error, not a user one."""

    def __init__(self, exercise_id: str, step_id: str) -> None:
        super().__init__(f"{exercise_id}: no step or mistake {step_id!r}", 500)


class InvalidCourseContentException(CourseException):
    """The authored content is inconsistent (duplicate ids, unknown theory references)."""

    def __init__(self, message: str) -> None:
        super().__init__(message, 500)
