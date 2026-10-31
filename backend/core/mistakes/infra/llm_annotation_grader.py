from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.ports import AnnotationGrader
from core.mistakes.domain.values.llm_outputs import GraderReport
from core.mistakes.domain.values.located_annotation import LocatedAnnotation
from core.mistakes.domain.values.mistake_source import MistakeSource
from core.mistakes.infra import prompts
from core.mistakes.infra.llm_schemas import grading_schema
from core.shared.domain.model_usage import ModelUsage
from core.shared.llm.client import LLMClient, LLMRequest, Stage


class LLMAnnotationGrader(AnnotationGrader):
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
