from pydantic import BaseModel, ConfigDict, Field

from core.quizzes.domain.entities.quiz import RejectedStatement
from core.quizzes.domain.entities.statement import StatementVerification, VerifiedCheck
from core.quizzes.domain.values.difficulty import Difficulty
from core.shared.domain.contract import catalan_alias
from core.shared.domain.model_usage import ModelUsage


class StatementDraft(BaseModel):
    """A statement as the writer proposed it: nothing is trusted until the code validation accepts it."""

    model_config = ConfigDict(serialize_by_alias=True)

    statement: str = Field(
        default="", validation_alias=catalan_alias("enunciat", "statement"), serialization_alias="enunciat"
    )
    verdict: str = Field(
        default="", validation_alias=catalan_alias("veredicte", "verdict"), serialization_alias="veredicte"
    )
    trap: str = Field(default="", validation_alias=catalan_alias("trampa", "trap"), serialization_alias="trampa")
    concept: str = Field(
        default="", validation_alias=catalan_alias("concepte", "concept"), serialization_alias="concepte"
    )
    counterexample: str = Field(
        default="",
        validation_alias=catalan_alias("contraexemple", "counterexample"),
        serialization_alias="contraexemple",
    )
    solution: str = Field(
        default="", validation_alias=catalan_alias("resolucio", "solution"), serialization_alias="resolucio"
    )
    key_ideas: list[str] = Field(
        default_factory=list,
        validation_alias=catalan_alias("idees_clau", "key_ideas"),
        serialization_alias="idees_clau",
    )
    hint: str = Field(default="", validation_alias=catalan_alias("pista", "hint"), serialization_alias="pista")
    theory: list[str] = Field(
        default_factory=list, validation_alias=catalan_alias("teoria", "theory"), serialization_alias="teoria"
    )
    checks: list[VerifiedCheck] = Field(
        default_factory=list,
        validation_alias=catalan_alias("comprovacions", "checks"),
        serialization_alias="comprovacions",
    )
    verification: StatementVerification | None = None


class BatchRequest(BaseModel):
    """What the writer is asked for in one round."""

    difficulty: Difficulty
    count: int
    false_min: int
    false_max: int
    kept: list[StatementDraft]  # already in the quiz: not to be repeated
    rejected: list[RejectedStatement]  # previous round's rejections, with the reasons


class WrittenBatch(BaseModel):
    drafts: list[StatementDraft]
    call: ModelUsage
