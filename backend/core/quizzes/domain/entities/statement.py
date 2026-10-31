from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from core.shared.domain.contract import catalan_alias
from core.shared.domain.ids import TheoryItemId
from core.shared.math.sympy_checks import CheckResult, MathCheck

# Contract values (LLM schemas, stored quizzes, HTTP): Catalan.
Verdict = Literal["cert", "fals"]
TRAPS: tuple[str, ...] = (
    "reciproc",  # the converse of a theorem
    "hipotesi_eliminada",  # a theorem without one of its hypotheses
    "conclusio_mes_forta",  # a stronger conclusion than what holds
    "quantificadors",  # order or kind of quantifiers changed
    "informacio_parcial",  # partial information (paths, iterated limits, partial derivatives) taken as enough
    "generalitzacio",  # a 1-variable fact that fails in several variables, or a special case generalised
    "cert_resultat",  # true: a result (or a direct consequence) of the notes
    "cert_demostracio",  # true: needs a short proof of its own
)


class VerifiedCheck(MathCheck):
    """A sympy check with the result code computed for it (empty until it is evaluated)."""

    status: str = Field(default="", validation_alias=catalan_alias("estat", "status"), serialization_alias="estat")
    computed: str = Field(
        default="", validation_alias=catalan_alias("calculat", "computed"), serialization_alias="calculat"
    )
    detail: str = Field(default="", validation_alias=catalan_alias("detall", "detail"), serialization_alias="detall")

    @property
    def failed(self) -> bool:
        return self.status == "falla"

    def with_result(self, result: CheckResult) -> Self:
        return self.model_copy(update={"status": result.status, "computed": result.computed, "detail": result.detail})


class StatementVerification(BaseModel):
    """What the blind solver said about an accepted statement."""

    model_config = ConfigDict(serialize_by_alias=True)

    solver_justification: str = Field(
        validation_alias=catalan_alias("solucionador", "solver_justification"), serialization_alias="solucionador"
    )
    confidence: str = Field(validation_alias=catalan_alias("confianca", "confidence"), serialization_alias="confianca")
    round: int = Field(validation_alias=catalan_alias("ronda", "round"), serialization_alias="ronda")


class Statement(BaseModel):
    """One statement of a quiz, with its verdict and the model answer the grading compares against."""

    model_config = ConfigDict(serialize_by_alias=True)

    id: str  # "a1", "a2", ... in the order shown
    statement: str = Field(validation_alias=catalan_alias("enunciat", "statement"), serialization_alias="enunciat")
    verdict: Verdict = Field(validation_alias=catalan_alias("veredicte", "verdict"), serialization_alias="veredicte")
    concept: str = Field(validation_alias=catalan_alias("concepte", "concept"), serialization_alias="concepte")
    trap: str = Field(validation_alias=catalan_alias("trampa", "trap"), serialization_alias="trampa")
    counterexample: str = Field(
        default="",
        validation_alias=catalan_alias("contraexemple", "counterexample"),
        serialization_alias="contraexemple",
    )
    solution: str = Field(validation_alias=catalan_alias("resolucio", "solution"), serialization_alias="resolucio")
    key_ideas: list[str] = Field(
        validation_alias=catalan_alias("idees_clau", "key_ideas"), serialization_alias="idees_clau"
    )
    hint: str = Field(validation_alias=catalan_alias("pista", "hint"), serialization_alias="pista")
    theory: list[TheoryItemId] = Field(
        default_factory=list, validation_alias=catalan_alias("teoria", "theory"), serialization_alias="teoria"
    )
    checks: list[VerifiedCheck] = Field(
        default_factory=list,
        validation_alias=catalan_alias("comprovacions", "checks"),
        serialization_alias="comprovacions",
    )
    verification: StatementVerification | None = Field(
        default=None, validation_alias=catalan_alias("verificacio", "verification"), serialization_alias="verificacio"
    )

    @field_validator("verification", mode="before")
    @classmethod
    def _absent_when_empty(cls, value: object) -> object:
        return None if value == {} else value

    @field_serializer("verification")
    def _empty_when_absent(self, value: StatementVerification | None) -> dict[str, object]:
        return {} if value is None else value.model_dump()

    @property
    def checks_passed(self) -> int:
        return sum(c.status == "ok" for c in self.checks)
