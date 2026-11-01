from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from core.quizzes.domain.entities.statement import Statement
from core.quizzes.domain.exceptions import StatementNotFoundException
from core.quizzes.domain.values.difficulty import Difficulty
from core.quizzes.domain.values.quiz_id import QuizId
from core.shared.domain.contract import catalan_alias, omit_none
from core.shared.domain.model_usage import ModelUsage


class RejectedStatement(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    statement: str = Field(validation_alias=catalan_alias("enunciat", "statement"), serialization_alias="enunciat")
    reasons: list[str] = Field(validation_alias=catalan_alias("motius", "reasons"), serialization_alias="motius")


class GenerationRound(BaseModel):
    """One batch of the generation: what was asked, what came back, what was rejected and why."""

    model_config = ConfigDict(serialize_by_alias=True)

    round: int = Field(validation_alias=catalan_alias("ronda", "round"), serialization_alias="ronda")
    requested: int = Field(validation_alias=catalan_alias("demanades", "requested"), serialization_alias="demanades")
    received: int = Field(validation_alias=catalan_alias("rebudes", "received"), serialization_alias="rebudes")
    generation: ModelUsage | None = Field(
        default=None, validation_alias=catalan_alias("generacio", "generation"), serialization_alias="generacio"
    )
    rejected: list[RejectedStatement] = Field(
        default_factory=list, validation_alias=catalan_alias("rebutjades", "rejected"), serialization_alias="rebutjades"
    )
    # Absent from the stored document when no statement reached the verification.
    solver: ModelUsage | None = Field(
        default=None,
        validation_alias=catalan_alias("solucionador", "solver"),
        serialization_alias="solucionador",
        exclude_if=omit_none,
    )
    audit: ModelUsage | None = Field(
        default=None,
        validation_alias=catalan_alias("auditoria", "audit"),
        serialization_alias="auditoria",
        exclude_if=omit_none,
    )
    accepted_total: int = Field(
        default=0,
        validation_alias=catalan_alias("acceptades_total", "accepted_total"),
        serialization_alias="acceptades_total",
    )


class QuizVerification(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    rounds: list[GenerationRound] = Field(
        default_factory=list, validation_alias=catalan_alias("rondes", "rounds"), serialization_alias="rondes"
    )


class Quiz(BaseModel):
    """A verified "Cert o fals" quiz. Its serialized form is the stored document (``generats/afirmacions``)."""

    model_config = ConfigDict(serialize_by_alias=True)

    id: QuizId
    source_id: str = Field(validation_alias=catalan_alias("font", "source_id"), serialization_alias="font")
    topic: int = Field(validation_alias=catalan_alias("tema", "topic"), serialization_alias="tema")
    difficulty: Difficulty = Field(
        validation_alias=catalan_alias("dificultat", "difficulty"), serialization_alias="dificultat"
    )
    statements: list[Statement] = Field(
        validation_alias=catalan_alias("afirmacions", "statements"), serialization_alias="afirmacions"
    )
    verification: QuizVerification | None = Field(
        default=None, validation_alias=catalan_alias("verificacio", "verification"), serialization_alias="verificacio"
    )
    created_at: float = Field(validation_alias=catalan_alias("creat", "created_at"), serialization_alias="creat")

    @field_validator("verification", mode="before")
    @classmethod
    def _absent_when_empty(cls, value: object) -> object:
        return None if value == {} else value

    @field_serializer("verification")
    def _empty_when_absent(self, value: QuizVerification | None) -> dict[str, object]:
        return {} if value is None else value.model_dump()

    def statement(self, statement_id: str) -> Statement:
        for s in self.statements:
            if s.id == statement_id:
                return s
        raise StatementNotFoundException(statement_id)

    def has_statement(self, statement_id: str) -> bool:
        return any(s.id == statement_id for s in self.statements)

    def cited_theory(self) -> set[str]:
        """Items of the notes the solutions cite (the API sends them with the grading)."""
        return {str(r) for s in self.statements for r in s.theory}
