from collections.abc import Sequence
from typing import Protocol

from core.quizzes.domain.entities.quiz import Quiz
from core.quizzes.domain.sources import QuizSource
from core.quizzes.domain.values.drafts import BatchRequest, StatementDraft, WrittenBatch
from core.quizzes.domain.values.grading_inputs import AnsweredStatement, GraderVerdict, StudentClaims
from core.quizzes.domain.values.verification import AuditReviews, SolverAnswers
from core.shared.math.sympy_checks import CheckResult, MathCheck


class QuizWriter(Protocol):
    """Proposes a batch of statements about the source, each with verdict, model solution, hint and checks."""

    async def write(self, source: QuizSource, request: BatchRequest) -> WrittenBatch: ...


class BlindSolver(Protocol):
    """Decides each statement true or false on its own: it never sees the declared verdicts or solutions."""

    async def solve(self, source: QuizSource, drafts: Sequence[StatementDraft]) -> SolverAnswers: ...


class QuizAuditor(Protocol):
    """Reviews the model solutions, the cited theory and the hints of each statement."""

    async def audit(self, source: QuizSource, drafts: Sequence[StatementDraft]) -> AuditReviews: ...


class AnswerGrader(Protocol):
    """Judges each justification against the model solution and quotes the key ideas it contains."""

    async def grade(self, source: QuizSource, answered: Sequence[AnsweredStatement]) -> GraderVerdict: ...


class ClaimExtractor(Protocol):
    """Transcribes the student's concrete computations as sympy checks. Never sees verdicts or solutions."""

    async def extract(self, answered: Sequence[AnsweredStatement]) -> list[StudentClaims]: ...


class CheckEvaluator(Protocol):
    """Runs sympy checks. Synchronous and CPU-bound: callers run it in a worker thread."""

    def evaluate(self, checks: Sequence[MathCheck]) -> list[CheckResult]: ...


class PregeneratedQuizSource(Protocol):
    """Quizzes generated offline (the seed of the quiz store)."""

    def load_all(self) -> list[Quiz]: ...
