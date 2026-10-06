from pydantic import AliasChoices, BaseModel, Field

from core.quizzes.domain.entities.grading import Answer, StudentCheck
from core.quizzes.domain.entities.statement import Statement
from core.quizzes.domain.values.call_summary import CallSummary


class AnsweredStatement(BaseModel):
    statement: Statement
    answer: Answer


class IdeaCitation(BaseModel):
    """The grader's claim that the answer contains key idea ``num`` (1-based), with the student's words."""

    num: int
    quote: str = Field(default="", validation_alias=AliasChoices("cita", "quote"))


class GraderEvaluation(BaseModel):
    statement_id: str = Field(validation_alias=AliasChoices("id", "statement_id"))
    ideas: list[IdeaCitation] = Field(default_factory=list, validation_alias=AliasChoices("idees", "ideas"))
    justification: str | None = Field(default=None, validation_alias=AliasChoices("justificacio", "justification"))
    feedback: str = ""


class GraderVerdict(BaseModel):
    evaluations: list[GraderEvaluation]
    summary: str
    call: CallSummary


class StudentClaims(BaseModel):
    """The concrete computations of one answer, as the transcriber wrote them for sympy."""

    statement_id: str
    checks: list[StudentCheck]
