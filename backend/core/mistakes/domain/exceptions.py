from core.shared.domain.exceptions import DomainException


class MistakesException(DomainException):
    pass


class MistakeSourceRequiredException(MistakesException):
    def __init__(self) -> None:
        super().__init__("Cal indicar un exercici o un resultat dels apunts (només un).", 422)


class UnknownTheoryResultException(MistakesException):
    """Not an item of the notes, or one without a proof (not eligible for the theory activity)."""

    def __init__(self, item_id: str) -> None:
        super().__init__("Resultat dels apunts desconegut o sense demostració", 404)


class MistakeExerciseNotFoundException(MistakesException):
    def __init__(self, exercise_id: str) -> None:
        super().__init__("Document desconegut", 404)


class MistakeSessionNotFoundException(MistakesException):
    def __init__(self, session_id: str) -> None:
        super().__init__("Sessió desconeguda", 404)


class InvalidAnnotationsException(MistakesException):
    def __init__(self, message: str) -> None:
        super().__init__(message, 422)


class GradingInProgressException(MistakesException):
    def __init__(self) -> None:
        super().__init__("Ja s'està corregint aquest document.", 409)


class MistakeGradingTimeoutException(MistakesException):
    """The grading did not finish within its deadline; nothing was stored, the student can resubmit."""

    def __init__(self, session_id: str) -> None:
        super().__init__("La correcció ha trigat massa. Torna-ho a provar.", 504)
        self.session_id = session_id


class MistakeSessionAlreadyGradedException(MistakesException):
    """Another grading of the session was stored first (a claim that went stale was taken over)."""

    def __init__(self, session_id: str) -> None:
        super().__init__("Aquest document ja s'ha corregit.", 409)
        self.session_id = session_id


class MistakeGenerationTimeoutException(MistakesException):
    """The generation did not finish within its deadline (the attempts paid are in the call log). 502 like a failed
    generation, so the API reports it as "La generació ha fallat: ..."."""

    def __init__(self, deadline_s: float) -> None:
        super().__init__(f"no s'ha pogut generar el document en {deadline_s:.0f} s: torna-ho a provar més tard", 502)


class MistakeGenerationFailedException(MistakesException):
    """Every attempt was rejected by validation or verification. 502 like any failed model stage, so the API
    reports it as "La generació ha fallat: ..."."""

    def __init__(self, attempts: int) -> None:
        super().__init__(f"no s'ha pogut generar un document amb errors verificats després de {attempts} intents", 502)
