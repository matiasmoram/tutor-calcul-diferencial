from typing import Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from core.quizzes.domain.entities.statement import VerifiedCheck
from core.quizzes.domain.values.call_summary import CallSummary
from core.shared.domain.ids import TheoryItemId

# Contract values (LLM schema, HTTP): Catalan.
Justification = Literal["correcta", "parcial", "incorrecta", "absent"]
JUSTIFICATIONS: tuple[Justification, ...] = ("correcta", "parcial", "incorrecta", "absent")


class Answer(BaseModel):
    """The student's answer to one statement: a verdict ("" = not answered) and a justification."""

    model_config = ConfigDict(serialize_by_alias=True)

    statement_id: str = Field(
        max_length=10, validation_alias=AliasChoices("id", "statement_id"), serialization_alias="id"
    )
    verdict: Literal["cert", "fals", ""] = Field(
        default="", validation_alias=AliasChoices("veredicte", "verdict"), serialization_alias="veredicte"
    )
    justification: str = Field(
        default="",
        max_length=4000,
        validation_alias=AliasChoices("justificacio", "justification"),
        serialization_alias="justificacio",
    )


class StudentCheck(VerifiedCheck):
    """A computation the student wrote, transcribed for sympy, with the student's literal words."""

    quote: str = Field(
        default="", validation_alias=AliasChoices("cita_alumne", "quote"), serialization_alias="cita_alumne"
    )


class StatementSolution(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    counterexample: str = Field(
        validation_alias=AliasChoices("contraexemple", "counterexample"), serialization_alias="contraexemple"
    )
    solution: str = Field(validation_alias=AliasChoices("resolucio", "solution"), serialization_alias="resolucio")
    key_ideas: list[str] = Field(
        validation_alias=AliasChoices("idees_clau", "key_ideas"), serialization_alias="idees_clau"
    )
    theory: list[TheoryItemId] = Field(validation_alias=AliasChoices("teoria", "theory"), serialization_alias="teoria")
    checks: list[VerifiedCheck] = Field(
        validation_alias=AliasChoices("comprovacions", "checks"), serialization_alias="comprovacions"
    )


class StatementGrading(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    id: str
    answer: str = Field(validation_alias=AliasChoices("resposta", "answer"), serialization_alias="resposta")
    verdict: str = Field(validation_alias=AliasChoices("veredicte", "verdict"), serialization_alias="veredicte")
    correct: bool = Field(validation_alias=AliasChoices("encert", "correct"), serialization_alias="encert")
    justification: Justification = Field(
        validation_alias=AliasChoices("justificacio", "justification"), serialization_alias="justificacio"
    )
    feedback: str
    cas_note: str = Field(validation_alias=AliasChoices("nota_cas", "cas_note"), serialization_alias="nota_cas")
    student_checks: list[StudentCheck] = Field(
        validation_alias=AliasChoices("comprovacions_alumne", "student_checks"),
        serialization_alias="comprovacions_alumne",
    )
    ideas_present: list[int] = Field(
        validation_alias=AliasChoices("idees_presents", "ideas_present"), serialization_alias="idees_presents"
    )
    hint_used: bool = Field(
        validation_alias=AliasChoices("pista_usada", "hint_used"), serialization_alias="pista_usada"
    )
    points: float = Field(validation_alias=AliasChoices("punts", "points"), serialization_alias="punts")
    solution: StatementSolution = Field(
        validation_alias=AliasChoices("solucio", "solution"), serialization_alias="solucio"
    )


class QuizGrading(BaseModel):
    """The graded quiz: every verdict and solution is revealed, so a quiz is graded once."""

    model_config = ConfigDict(serialize_by_alias=True)

    grade: int = Field(validation_alias=AliasChoices("nota", "grade"), serialization_alias="nota")  # 0-100
    correct: int = Field(validation_alias=AliasChoices("encerts", "correct"), serialization_alias="encerts")
    total: int
    statements: list[StatementGrading] = Field(
        validation_alias=AliasChoices("afirmacions", "statements"), serialization_alias="afirmacions"
    )
    summary: str = Field(validation_alias=AliasChoices("resum", "summary"), serialization_alias="resum")
    call: CallSummary | None = Field(validation_alias=AliasChoices("crida", "call"), serialization_alias="crida")
