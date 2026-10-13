from core.shared.domain.exceptions import DomainException


class CounterexampleException(DomainException):
    pass


class UnknownSpecException(CounterexampleException):
    def __init__(self, spec_id: str) -> None:
        super().__init__("Repte desconegut", 404)
        self.spec_id = spec_id


class InvalidSubmissionException(CounterexampleException):
    """The function or a certificate cannot be read; the message tells the student what to fix."""

    def __init__(self, message: str) -> None:
        super().__init__(message, 422)


class InvalidSpecContentException(CounterexampleException):
    """The authored challenges cannot be read (a malformed entry, a repeated id)."""

    def __init__(self, message: str) -> None:
        super().__init__(message, 500)
