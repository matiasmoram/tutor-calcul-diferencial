from typing import Literal

from pydantic import BaseModel, Field

from core.course.domain.entities.exercise import StatementFormat
from core.shared.domain.ids import ExerciseId, ProblemSheetId


class Problem(BaseModel):
    number: int
    source: str | None = None
    preamble: str = ""
    hint: str | None = None
    exercise_ids: list[ExerciseId] = Field(default_factory=list)


class ProblemSheet(BaseModel):
    """One topic's collection of problems ("Tema 2"), each problem with one exercise per sub-part."""

    id: ProblemSheetId
    label: str
    title: str
    description: str = ""
    topic: int | None = None
    kind: Literal["calcul", "teoric", "mixt"] = "mixt"
    format: StatementFormat = "text"
    exercise_ids: list[ExerciseId] = Field(default_factory=list)
    problems: list[Problem] = Field(default_factory=list)
