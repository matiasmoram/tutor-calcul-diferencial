import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from core.course.domain.exceptions import UnknownStepException
from core.course.domain.values.theory_ref import TheoryRef
from core.shared.domain.ids import ExerciseId, ProblemSheetId

ExerciseKind = Literal["calcul", "teoric"]
StatementFormat = Literal["latex", "text"]


def _compile_all(patterns: list[str]) -> list[str]:
    for p in patterns:
        re.compile(p)
    return patterns


class Step(BaseModel):
    id: str
    title: str
    objective: str
    idea: str
    detail: str
    # Regexes that must not match a reply before the step's content may be shown (leak detection).
    leak_patterns: list[str] = Field(default_factory=list)
    # Course results this step uses. Shown to the reply stage once the strategy may be named (level >= 2).
    theory: list[TheoryRef] = Field(default_factory=list)

    @field_validator("leak_patterns")
    @classmethod
    def _valid_regexes(cls, v: list[str]) -> list[str]:
        return _compile_all(v)


class CommonMistake(BaseModel):
    id: str
    description: str
    question: str  # what the tutor asks so the student finds the mistake


class ExpectedResult(BaseModel):
    value: str
    leak_patterns: list[str] = Field(default_factory=list)

    @field_validator("leak_patterns")
    @classmethod
    def _valid_regexes(cls, v: list[str]) -> list[str]:
        return _compile_all(v)


class Exercise(BaseModel):
    """One sub-part of a problem of the collection, with its hidden solution sheet (authored offline)."""

    id: ExerciseId
    sheet_id: ProblemSheetId
    group: str = ""  # title of the problem sheet
    topic: int | None = None
    problem: int = 0
    part: str | None = None  # "a", "b", ...
    label: str = ""  # "4(c)"
    kind: ExerciseKind = "calcul"
    format: StatementFormat = "text"
    source: str | None = None
    preamble: str = ""  # statement shared by every part of the problem
    hint: str = ""  # "Indicació" printed with the problem
    statement: str
    result: ExpectedResult
    steps: list[Step]
    common_mistakes: list[CommonMistake]
    # Background theory (definitions the statement relies on): safe to show from the first turn.
    theory: list[TheoryRef] = Field(default_factory=list)
    # Theory that solves this very exercise (e.g. a worked example in the notes): grading stages only.
    reserved_theory: list[TheoryRef] = Field(default_factory=list)
    professor_note: str = ""

    @field_validator("steps")
    @classmethod
    def _unique_steps(cls, v: list[Step]) -> list[Step]:
        ids = [s.id for s in v]
        if not ids or len(ids) != len(set(ids)):
            raise ValueError(f"step ids must be non-empty and unique: {ids}")
        return v

    @property
    def step_ids(self) -> list[str]:
        return [s.id for s in self.steps]

    @property
    def mistake_ids(self) -> list[str]:
        return [m.id for m in self.common_mistakes]

    def step(self, step_id: str) -> Step:
        for s in self.steps:
            if s.id == step_id:
                return s
        raise UnknownStepException(self.id, step_id)

    def mistake(self, mistake_id: str) -> CommonMistake:
        for m in self.common_mistakes:
            if m.id == mistake_id:
                return m
        raise UnknownStepException(self.id, mistake_id)

    def all_refs(self) -> list[TheoryRef]:
        """Every theory reference of the sheet, in order, without duplicates."""
        refs = [*self.theory, *(r for s in self.steps for r in s.theory), *self.reserved_theory]
        return list(dict.fromkeys(refs))

    def statement_md(self) -> str:
        """Statement as prose with $...$ math, whatever the source format; includes the shared preamble."""
        own = f"${self.statement}$" if self.format == "latex" else self.statement.strip()
        if self.preamble.strip():
            prefix = f"{self.preamble.strip()}\n\n"
            own = f"{prefix}({self.part}) {own}" if self.part else f"{prefix}{own}"
        if self.hint.strip() and self.hint.strip() not in own:
            own += f"\n\nIndicació: {self.hint.strip()}"
        return own

    def full_reference(self) -> str:
        """Full solution sheet as text. Only the diagnosis and guard stages see this."""
        lines = [
            f"ENUNCIAT: {self.statement_md()}",
            f"RESULTAT CORRECTE: {self.result.value.strip()}",
            "PASSOS DE LA SOLUCIÓ (en ordre):",
        ]
        for i, s in enumerate(self.steps, 1):
            lines.append(f"  {i}. [{s.id}] {s.title}" + (f"  (teoria: {', '.join(s.theory)})" if s.theory else ""))
            lines.append(f"     objectiu: {s.objective.strip()}")
            lines.append(f"     idea: {s.idea.strip()}")
            lines.append(f"     detall: {s.detail.strip()}")
        lines.append("ERRORS COMUNS:")
        for m in self.common_mistakes:
            lines.append(f"  - [{m.id}] {m.description.strip()}")
        return "\n".join(lines)
