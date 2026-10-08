from pydantic import BaseModel, Field

from core.quizzes.domain.entities.grading import Answer, QuizGrading
from core.quizzes.domain.values.difficulty import Difficulty
from core.quizzes.domain.values.quiz_id import QuizId
from core.shared.domain.ids import SessionId


class QuizSubmission(BaseModel):
    """The answers handed in, the hints used by then, and their grading."""

    answers: list[Answer]
    hints: list[str]
    result: QuizGrading
    created_at: float


class QuizSession(BaseModel):
    """One student working on one quiz: the hints they opened and, once handed in, the grading.

    ``version`` is the optimistic-concurrency token the repository checks on save."""

    id: SessionId
    source_id: str
    difficulty: Difficulty
    quiz_id: QuizId
    hints_used: list[str] = Field(default_factory=list)
    submission: QuizSubmission | None = None
    created_at: float
    updated_at: float
    version: int = 0

    @property
    def graded(self) -> bool:
        return self.submission is not None

    def use_hint(self, statement_id: str, now: float) -> bool:
        """Records a hint (it lowers that statement's score). After the grading hints cost nothing.
        Returns whether the session changed."""
        if self.graded or statement_id in self.hints_used:
            return False
        self.hints_used.append(statement_id)
        self.updated_at = now
        return True

    def submit(self, answers: list[Answer], result: QuizGrading, now: float) -> None:
        self.submission = QuizSubmission(answers=answers, hints=sorted(self.hints_used), result=result, created_at=now)
        self.updated_at = now
