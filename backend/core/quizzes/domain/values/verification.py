from pydantic import AliasChoices, BaseModel, Field

from core.quizzes.domain.values.call_summary import CallSummary


class SolverAnswer(BaseModel):
    """The blind solver's own verdict on statement ``num`` (1-based, in the order sent)."""

    num: int | None = None
    justification: str = Field(default="", validation_alias=AliasChoices("justificacio", "justification"))
    verdict: str | None = Field(default=None, validation_alias=AliasChoices("veredicte", "verdict"))
    confidence: str = Field(default="", validation_alias=AliasChoices("confianca", "confidence"))
    well_posed: bool = Field(default=True, validation_alias=AliasChoices("ben_plantejada", "well_posed"))


class AuditReview(BaseModel):
    """The auditor's review of statement ``num``; a missing flag counts as a failed check."""

    num: int | None = None
    problems: str = Field(default="", validation_alias=AliasChoices("problemes", "problems"))
    solution_correct: bool = Field(
        default=False, validation_alias=AliasChoices("resolucio_correcta", "solution_correct")
    )
    theory_correct: bool = Field(default=False, validation_alias=AliasChoices("teoria_correcta", "theory_correct"))
    hint_neutral: bool = Field(default=False, validation_alias=AliasChoices("pista_neutra", "hint_neutral"))


class SolverAnswers(BaseModel):
    answers: list[SolverAnswer]
    call: CallSummary


class AuditReviews(BaseModel):
    reviews: list[AuditReview]
    call: CallSummary
