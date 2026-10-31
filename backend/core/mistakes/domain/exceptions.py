from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.layout import Layout
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
        self.item_id = item_id


class MistakeExerciseNotFoundException(MistakesException):
    def __init__(self, exercise_id: str) -> None:
        super().__init__("Document desconegut", 404)
        self.exercise_id = exercise_id


class MistakeExerciseNotReadyException(MistakesException):
    """Nothing ready for the source and difficulty, and this caller may not start a generation."""

    def __init__(self, source_id: str, difficulty: Difficulty) -> None:
        super().__init__(
            "Encara no hi ha cap document preparat per a aquest tema i dificultat. "
            "Prova una altra dificultat o demana-ho al professorat.",
            409,
        )
        self.source_id = source_id
        self.difficulty = difficulty


class MistakeSessionNotFoundException(MistakesException):
    def __init__(self, session_id: str) -> None:
        super().__init__("Sessió desconeguda", 404)
        self.session_id = session_id


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


class MistakeLayoutMismatchException(MistakesException):
    """A session graded through the other layout's use case: per parts on the whole-document grading, or the
    other way round."""

    def __init__(self, session_id: str, layout: Layout) -> None:
        if layout == "per_parts":
            message = "Aquest document es corregeix part per part."
        else:
            message = "Aquest document es corregeix sencer, no per parts."
        super().__init__(message, 409)
        self.session_id = session_id
        self.layout = layout


class UnknownMistakePartException(MistakesException):
    """Not a part of the document, or a part without an error (nothing to grade or hint)."""

    def __init__(self, part: int) -> None:
        super().__init__("Part desconeguda", 404)
        self.part = part


class MistakePartOutOfOrderException(MistakesException):
    def __init__(self, part: int) -> None:
        super().__init__("Primer cal corregir la part anterior.", 409)
        self.part = part


class MistakePartAlreadyGradedException(MistakesException):
    """Another grading of the part was stored first (a claim that went stale was taken over)."""

    def __init__(self, session_id: str, part: int) -> None:
        super().__init__("Aquesta part ja s'ha corregit.", 409)
        self.session_id = session_id
        self.part = part


class MistakePartsUnavailableException(MistakesException):
    """A source that cannot be split into at least 2 parts: only the whole-document layout is offered."""

    def __init__(self, source_id: str) -> None:
        super().__init__("Aquest exercici no es pot fer pas a pas: només té una part. Fes-lo en document sencer.", 422)
        self.source_id = source_id


class MistakeGenerationFailedException(MistakesException):
    """Every attempt was rejected by validation or verification. 502 like any failed model stage, so the API
    reports it as "La generació ha fallat: ..."."""

    def __init__(self, attempts: int) -> None:
        super().__init__(f"no s'ha pogut generar un document amb errors verificats després de {attempts} intents", 502)
