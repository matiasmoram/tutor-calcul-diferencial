from core.shared.domain.exceptions import DomainException


class CourseException(DomainException):
    pass


class ExerciseNotFoundException(CourseException):
    def __init__(self, exercise_id: str) -> None:
        super().__init__("Exercici desconegut", 404)
        self.exercise_id = exercise_id


class ProblemSheetNotFoundException(CourseException):
    def __init__(self, sheet_id: str) -> None:
        super().__init__("Llista desconeguda", 404)
        self.sheet_id = sheet_id


class TheoryItemNotFoundException(CourseException):
    def __init__(self, item_id: str) -> None:
        super().__init__("Ítem de teoria desconegut", 404)
        self.item_id = item_id


class UnknownStepException(CourseException):
    """A step or mistake id that the sheet does not define: a programming error, not a user one."""

    def __init__(self, exercise_id: str, step_id: str) -> None:
        super().__init__(f"{exercise_id}: no step or mistake {step_id!r}", 500)
        self.exercise_id = exercise_id
        self.step_id = step_id


class InvalidCourseContentException(CourseException):
    """The authored content is inconsistent (duplicate ids, unknown theory references)."""

    def __init__(self, message: str) -> None:
        super().__init__(message, 500)
