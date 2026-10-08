from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from core.quizzes.domain.entities.quiz import RejectedStatement
from core.quizzes.domain.entities.statement import StatementVerification, VerifiedCheck
from core.quizzes.domain.values.call_summary import CallSummary
from core.quizzes.domain.values.difficulty import Difficulty


class StatementDraft(BaseModel):
    """A statement as the writer proposed it: nothing is trusted until the code validation accepts it."""

    model_config = ConfigDict(serialize_by_alias=True)

    statement: str = Field(
        default="", validation_alias=AliasChoices("enunciat", "statement"), serialization_alias="enunciat"
    )
    verdict: str = Field(
        default="", validation_alias=AliasChoices("veredicte", "verdict"), serialization_alias="veredicte"
    )
    trap: str = Field(default="", validation_alias=AliasChoices("trampa", "trap"), serialization_alias="trampa")
    concept: str = Field(
        default="", validation_alias=AliasChoices("concepte", "concept"), serialization_alias="concepte"
    )
    counterexample: str = Field(
        default="",
        validation_alias=AliasChoices("contraexemple", "counterexample"),
        serialization_alias="contraexemple",
    )
    solution: str = Field(
        default="", validation_alias=AliasChoices("resolucio", "solution"), serialization_alias="resolucio"
    )
    key_ideas: list[str] = Field(
        default_factory=list, validation_alias=AliasChoices("idees_clau", "key_ideas"), serialization_alias="idees_clau"
    )
    hint: str = Field(default="", validation_alias=AliasChoices("pista", "hint"), serialization_alias="pista")
    theory: list[str] = Field(
        default_factory=list, validation_alias=AliasChoices("teoria", "theory"), serialization_alias="teoria"
    )
    checks: list[VerifiedCheck] = Field(
        default_factory=list,
        validation_alias=AliasChoices("comprovacions", "checks"),
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
    call: CallSummary
