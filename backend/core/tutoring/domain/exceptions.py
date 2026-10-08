from core.shared.domain.exceptions import DomainException
from core.tutoring.domain.values.turn_trace import ModelCall


class TutoringException(DomainException):
    pass


class TutorSessionNotFoundException(TutoringException):
    def __init__(self, session_id: str) -> None:
        super().__init__("Sessió desconeguda", 404)
        self.session_id = session_id


class ConcurrentTurnException(TutoringException):
    """Another turn of the same session was saved first (two tabs, or a resend while the reply was pending)."""

    def __init__(self, session_id: str) -> None:
        super().__init__("Encara s'està responent el missatge anterior.", 409)
        self.session_id = session_id


class TurnTimeoutException(TutoringException):
    """The turn did not finish within its deadline; nothing was stored, the student can resend."""

    def __init__(self, session_id: str) -> None:
        super().__init__("La resposta ha trigat massa. Torna-ho a provar.", 504)
        self.session_id = session_id


class InvalidPhotoException(TutoringException):
    def __init__(self, message: str) -> None:
        super().__init__(message, 400)


class ModelOutputException(TutoringException):
    """A stage's model answered, but not with something usable (invalid JSON or schema, empty text, refusal).

    ``call`` is the call that produced it, when there was one, so the turn trace still accounts for it."""

    def __init__(self, stage_name: str, detail: str, call: ModelCall | None = None) -> None:
        super().__init__(f"{stage_name} ha fallat: {detail}", 502)
        self.detail = detail
        self.call = call
