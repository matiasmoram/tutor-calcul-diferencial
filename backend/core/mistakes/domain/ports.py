from typing import Protocol

from core.mistakes.domain.entities.gradable_text import GradableText
from core.mistakes.domain.entities.parted_mistake_exercise import MistakeDocument
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.llm_outputs import (
    CorruptionDraft,
    GenerationDraft,
    GraderReport,
    PartReport,
    ResolutionDraft,
    ResolutionReport,
    VerificationReport,
)
from core.mistakes.domain.values.located_annotation import LocatedAnnotation
from core.mistakes.domain.values.mistake_source import MistakeSource
from core.mistakes.domain.values.resolution import Resolution, ResolutionPart
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


class ResolutionWriter(Protocol):
    async def write(self, source: MistakeSource, rejections: list[str]) -> tuple[ResolutionDraft, ModelUsage]:
        """The complete, correct resolution in parts (theory: the statement, then the proof stages). `rejections`:
        why the previous attempt was refused."""
        ...


class ResolutionVerifier(Protocol):
    async def verify(self, source: MistakeSource, resolution: Resolution) -> tuple[ResolutionReport, ModelUsage]:
        """Every problem found in the correct resolution, and whether it reaches the result."""
        ...


class PartCorrupter(Protocol):
    async def corrupt(
        self, source: MistakeSource, resolution: Resolution, part: int, difficulty: Difficulty, rejections: list[str]
    ) -> tuple[CorruptionDraft, ModelUsage]:
        """One error put into part `part` of the correct resolution, as small edits of its text."""
        ...


class PartVerifier(Protocol):
    async def verify(
        self, source: MistakeSource, earlier: list[ResolutionPart], part: ResolutionPart
    ) -> tuple[PartReport, ModelUsage]:
        """Every problem found in `part` (its flawed text), with the earlier parts, correct, as context. Never sees
        the declared error, the part's correct text nor the parts after it."""
        ...


class AnnotationGrader(Protocol):
    async def grade(
        self, source: MistakeSource, text: GradableText, annotations: list[LocatedAnnotation]
    ) -> tuple[GraderReport, ModelUsage]:
        """Which candidate error each annotation describes and how good the student's reason is."""
        ...


class PregeneratedMistakeSource(Protocol):
    """Documents generated and verified offline (the JSON files in the repository): the seed of the database."""

    def load_all(self) -> list[MistakeDocument]:
        """The documents of both layouts."""
        ...
