from core.quizzes.domain.values.difficulty import Difficulty
from core.shared.domain.exceptions import DomainException

# Messages are shown to the student.


class QuizException(DomainException):
    pass


class UnknownQuizSourceException(QuizException):
    def __init__(self, source_id: str) -> None:
        super().__init__("Tema o resultat dels apunts desconegut", 404)
        self.source_id = source_id


class QuizNotFoundException(QuizException):
    def __init__(self, quiz_id: str) -> None:
        super().__init__("Qüestionari desconegut", 404)
        self.quiz_id = quiz_id


class QuizSessionNotFoundException(QuizException):
    def __init__(self, session_id: str) -> None:
        super().__init__("Sessió desconeguda", 404)
        self.session_id = session_id


class StatementNotFoundException(QuizException):
    def __init__(self, statement_id: str) -> None:
        super().__init__("Afirmació desconeguda", 404)
        self.statement_id = statement_id


class QuizNotReadyException(QuizException):
    """Nothing stored for the source and difficulty, and this caller may not start a generation."""

    def __init__(self, source_id: str, difficulty: Difficulty) -> None:
        super().__init__(
            "Encara no hi ha cap qüestionari preparat per a aquest tema i dificultat. "
            "Prova una altra dificultat o demana-ho al professorat.",
            409,
        )
        self.source_id = source_id
        self.difficulty = difficulty


class QuizGenerationTimeoutException(QuizException):
    """The generation did not finish within its deadline (the rounds paid are in the call log). 502 like a failed
    generation, so the API reports it as "La generació ha fallat: ..."."""

    def __init__(self, deadline_s: float) -> None:
        super().__init__(f"no s'ha pogut generar el qüestionari en {deadline_s:.0f} s: torna-ho a provar més tard", 502)
        self.deadline_s = deadline_s


class QuizGenerationFailedException(QuizException):
    """Validation and verification left the quiz short of statements after every round. 502 like any failed model
    stage, so the API reports it as "La generació ha fallat: ..."."""

    def __init__(self, size: int, rounds: int) -> None:
        super().__init__(
            f"no s'ha pogut generar un qüestionari verificat de {size} afirmacions després de {rounds} rondes", 502
        )
        self.size = size
        self.rounds = rounds


class QuizGradingTimeoutException(QuizException):
    """The grading did not finish within its deadline; nothing was stored, the student can resubmit."""

    def __init__(self, session_id: str) -> None:
        super().__init__("La correcció ha trigat massa. Torna-ho a provar.", 504)
        self.session_id = session_id


class ConcurrentQuizGradingException(QuizException):
    """The session changed while it was being graded (a second submission of the same quiz)."""

    def __init__(self, session_id: str) -> None:
        super().__init__("Ja s'està corregint aquest qüestionari.", 409)
        self.session_id = session_id
