from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from core.quizzes.domain.entities.statement import VerifiedCheck
from core.shared.domain.contract import catalan_alias
from core.shared.domain.ids import TheoryItemId
from core.shared.domain.model_usage import ModelUsage

# Contract values (LLM schema, HTTP): Catalan.
Justification = Literal["correcta", "parcial", "incorrecta", "absent"]
JUSTIFICATIONS: tuple[Justification, ...] = ("correcta", "parcial", "incorrecta", "absent")


class Answer(BaseModel):
    """The student's answer to one statement: a verdict ("" = not answered) and a justification."""

    model_config = ConfigDict(serialize_by_alias=True)

    statement_id: str = Field(
        max_length=10, validation_alias=catalan_alias("id", "statement_id"), serialization_alias="id"
    )
    verdict: Literal["cert", "fals", ""] = Field(
        default="", validation_alias=catalan_alias("veredicte", "verdict"), serialization_alias="veredicte"
    )
    justification: str = Field(
        default="",
        max_length=4000,
        validation_alias=catalan_alias("justificacio", "justification"),
        serialization_alias="justificacio",
    )


class StudentCheck(VerifiedCheck):
    """A computation the student wrote, transcribed for sympy, with the student's literal words."""

    quote: str = Field(
        default="", validation_alias=catalan_alias("cita_alumne", "quote"), serialization_alias="cita_alumne"
    )


class StatementSolution(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    counterexample: str = Field(
        validation_alias=catalan_alias("contraexemple", "counterexample"), serialization_alias="contraexemple"
    )
    solution: str = Field(validation_alias=catalan_alias("resolucio", "solution"), serialization_alias="resolucio")
    key_ideas: list[str] = Field(
        validation_alias=catalan_alias("idees_clau", "key_ideas"), serialization_alias="idees_clau"
    )
    theory: list[TheoryItemId] = Field(validation_alias=catalan_alias("teoria", "theory"), serialization_alias="teoria")
    checks: list[VerifiedCheck] = Field(
        validation_alias=catalan_alias("comprovacions", "checks"), serialization_alias="comprovacions"
    )


class StatementGrading(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    id: str
    answer: str = Field(validation_alias=catalan_alias("resposta", "answer"), serialization_alias="resposta")
    verdict: str = Field(validation_alias=catalan_alias("veredicte", "verdict"), serialization_alias="veredicte")
    correct: bool = Field(validation_alias=catalan_alias("encert", "correct"), serialization_alias="encert")
    justification: Justification = Field(
        validation_alias=catalan_alias("justificacio", "justification"), serialization_alias="justificacio"
    )
    feedback: str
    cas_note: str = Field(validation_alias=catalan_alias("nota_cas", "cas_note"), serialization_alias="nota_cas")
    student_checks: list[StudentCheck] = Field(
        validation_alias=catalan_alias("comprovacions_alumne", "student_checks"),
        serialization_alias="comprovacions_alumne",
    )
    ideas_present: list[int] = Field(
        validation_alias=catalan_alias("idees_presents", "ideas_present"), serialization_alias="idees_presents"
    )
    hint_used: bool = Field(
        validation_alias=catalan_alias("pista_usada", "hint_used"), serialization_alias="pista_usada"
    )
    points: float = Field(validation_alias=catalan_alias("punts", "points"), serialization_alias="punts")
    solution: StatementSolution = Field(
        validation_alias=catalan_alias("solucio", "solution"), serialization_alias="solucio"
    )


class QuizGrading(BaseModel):
    """The graded quiz: every verdict and solution is revealed, so a quiz is graded once."""

    model_config = ConfigDict(serialize_by_alias=True)

    grade: int = Field(validation_alias=catalan_alias("nota", "grade"), serialization_alias="nota")  # 0-100
    correct: int = Field(validation_alias=catalan_alias("encerts", "correct"), serialization_alias="encerts")
    total: int
    statements: list[StatementGrading] = Field(
        validation_alias=catalan_alias("afirmacions", "statements"), serialization_alias="afirmacions"
    )
    summary: str = Field(validation_alias=catalan_alias("resum", "summary"), serialization_alias="resum")
    call: ModelUsage | None = Field(validation_alias=catalan_alias("crida", "call"), serialization_alias="crida")
