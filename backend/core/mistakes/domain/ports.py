from typing import Protocol

from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.llm_outputs import GenerationDraft, GraderReport, VerificationReport
from core.mistakes.domain.values.located_annotation import LocatedAnnotation
from core.mistakes.domain.values.mistake_source import MistakeSource
from core.shared.domain.model_usage import ModelUsage


class MistakeGenerator(Protocol):
    async def generate(
        self, source: MistakeSource, difficulty: Difficulty, rejections: list[str]
    ) -> tuple[GenerationDraft, ModelUsage]:
        """A document with the difficulty's number of errors. `rejections`: why the previous attempt was refused."""
        ...


class MistakeVerifier(Protocol):
    async def verify(
        self, source: MistakeSource, fragments: list[str], statement_fragments: int
    ) -> tuple[VerificationReport, ModelUsage]:
        """Every problem found in the fragments. Never sees the declared errors."""
        ...


class AnnotationGrader(Protocol):
    async def grade(
        self, source: MistakeSource, exercise: MistakeExercise, annotations: list[LocatedAnnotation]
    ) -> tuple[GraderReport, ModelUsage]:
        """Which candidate error each annotation describes and how good the student's reason is."""
        ...


class PregeneratedMistakeSource(Protocol):
    """Documents generated and verified offline (the JSON files in the repository): the seed of the database."""

    def load(self) -> list[MistakeExercise]: ...
