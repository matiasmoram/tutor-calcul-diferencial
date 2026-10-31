from pydantic import BaseModel, Field

from core.shared.domain.contract import catalan_alias
from core.shared.domain.model_usage import ModelUsage


class SolverAnswer(BaseModel):
    """The blind solver's own verdict on statement ``num`` (1-based, in the order sent)."""

    num: int | None = None
    justification: str = Field(default="", validation_alias=catalan_alias("justificacio", "justification"))
    verdict: str | None = Field(default=None, validation_alias=catalan_alias("veredicte", "verdict"))
    confidence: str = Field(default="", validation_alias=catalan_alias("confianca", "confidence"))
    well_posed: bool = Field(default=True, validation_alias=catalan_alias("ben_plantejada", "well_posed"))


class AuditReview(BaseModel):
    """The auditor's review of statement ``num``; a missing flag counts as a failed check."""

    num: int | None = None
    problems: str = Field(default="", validation_alias=catalan_alias("problemes", "problems"))
    solution_correct: bool = Field(
        default=False, validation_alias=catalan_alias("resolucio_correcta", "solution_correct")
    )
    theory_correct: bool = Field(default=False, validation_alias=catalan_alias("teoria_correcta", "theory_correct"))
    hint_neutral: bool = Field(default=False, validation_alias=catalan_alias("pista_neutra", "hint_neutral"))


class SolverAnswers(BaseModel):
    answers: list[SolverAnswer]
    call: ModelUsage


class AuditReviews(BaseModel):
    reviews: list[AuditReview]
    call: ModelUsage
