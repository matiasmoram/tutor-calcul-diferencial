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


class QuizGenerationException(QuizException):
    """The model could not produce a verified quiz within the allowed rounds."""

    def __init__(self, message: str) -> None:
        super().__init__(message, 502)


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
