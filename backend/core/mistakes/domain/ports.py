from typing import Protocol

from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.grading import LocatedAnnotation
from core.mistakes.domain.values.call_record import CallRecord
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.llm_outputs import GenerationDraft, GraderReport, VerificationReport
from core.mistakes.domain.values.mistake_source import MistakeSource


class MistakeGenerator(Protocol):
    async def generate(
        self, source: MistakeSource, difficulty: Difficulty, rejections: list[str]
    ) -> tuple[GenerationDraft, CallRecord]:
        """A document with the difficulty's number of errors. `rejections`: why the previous attempt was refused."""
        ...


class MistakeVerifier(Protocol):
    async def verify(
        self, source: MistakeSource, fragments: list[str], statement_fragments: int
    ) -> tuple[VerificationReport, CallRecord]:
        """Every problem found in the fragments. Never sees the declared errors."""
        ...


class AnnotationGrader(Protocol):
    async def grade(
        self, source: MistakeSource, exercise: MistakeExercise, annotations: list[LocatedAnnotation]
    ) -> tuple[GraderReport, CallRecord]:
        """Which candidate error each annotation describes and how good the student's reason is."""
        ...


class GeneratedMistakesSource(Protocol):
    """Documents generated and verified offline (the JSON files in the repository): the seed of the database."""

    def load(self) -> list[MistakeExercise]: ...
