"""The three model stages of "troba l'error" over the shared LLM client."""

from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.llm_outputs import GenerationDraft, GraderReport, VerificationReport
from core.mistakes.domain.values.located_annotation import LocatedAnnotation
from core.mistakes.domain.values.mistake_source import MistakeSource, TheorySource
from core.mistakes.infra import prompts
from core.mistakes.infra.llm_schemas import generation_schema, grading_schema, verification_schema
from core.shared.domain.model_usage import ModelUsage
from core.shared.llm.client import LLMClient, LLMRequest, Stage


class LLMMistakeGenerator:
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    async def generate(
        self, source: MistakeSource, difficulty: Difficulty, rejections: list[str]
    ) -> tuple[GenerationDraft, ModelUsage]:
        request = LLMRequest(
            system=prompts.generation_system(source),
            user=prompts.generation_user(source, difficulty, rejections),
            schema=generation_schema(isinstance(source, TheorySource)),
            context=prompts.context(source),
        )
        data, meta = await self._llm.structured(Stage.MISTAKES_GENERATION, request)
        return GenerationDraft.model_validate(data), meta.usage()


class LLMMistakeVerifier:
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    async def verify(
        self, source: MistakeSource, fragments: list[str], statement_fragments: int
    ) -> tuple[VerificationReport, ModelUsage]:
        request = LLMRequest(
            system=prompts.verification_system(source),
            user=prompts.verification_user(source, fragments, statement_fragments),
            schema=verification_schema(),
            context=prompts.context(source),
        )
        data, meta = await self._llm.structured(Stage.MISTAKES_VERIFICATION, request)
        return VerificationReport.model_validate(data), meta.usage()


class LLMAnnotationGrader:
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    async def grade(
        self, source: MistakeSource, exercise: MistakeExercise, annotations: list[LocatedAnnotation]
    ) -> tuple[GraderReport, ModelUsage]:
        request = LLMRequest(
            system=prompts.GRADING_SYSTEM,
            user=prompts.grading_user(exercise, annotations),
            schema=grading_schema([a.key for a in annotations], [e.id for e in exercise.mistakes]),
            context=prompts.context(source),
        )
        data, meta = await self._llm.structured(Stage.MISTAKES_GRADING, request)
        raw = data.get("avaluacions", [])
        # Malformed entries are skipped, not fatal: an annotation without a verdict is still placed by code.
        verdicts = [v for v in raw if isinstance(v, dict) and "anotacio" in v] if isinstance(raw, list) else []
        report = GraderReport.model_validate({"avaluacions": verdicts, "resum": data.get("resum", "")})
        return report, meta.usage()
