from pydantic import BaseModel, Field

from core.quizzes.domain.entities.grading import Answer, StudentCheck
from core.quizzes.domain.entities.statement import Statement
from core.shared.domain.contract import catalan_alias
from core.shared.domain.model_usage import ModelUsage


class AnsweredStatement(BaseModel):
    statement: Statement
    answer: Answer


class IdeaCitation(BaseModel):
    """The grader's claim that the answer contains key idea ``num`` (1-based), with the student's words."""

    num: int
    quote: str = Field(default="", validation_alias=catalan_alias("cita", "quote"))


class GraderEvaluation(BaseModel):
    statement_id: str = Field(validation_alias=catalan_alias("id", "statement_id"))
    ideas: list[IdeaCitation] = Field(default_factory=list, validation_alias=catalan_alias("idees", "ideas"))
    justification: str | None = Field(default=None, validation_alias=catalan_alias("justificacio", "justification"))
    feedback: str = ""


class GraderVerdict(BaseModel):
    evaluations: list[GraderEvaluation]
    summary: str
    call: ModelUsage


class StudentClaims(BaseModel):
    """The concrete computations of one answer, as the transcriber wrote them for sympy."""

    statement_id: str
    checks: list[StudentCheck]
