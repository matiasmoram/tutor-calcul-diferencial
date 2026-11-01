from core.mistakes.domain.ports import ResolutionWriter
from core.mistakes.domain.values.llm_outputs import ResolutionDraft
from core.mistakes.domain.values.mistake_source import MistakeSource, ProblemSource
from core.mistakes.infra import prompts
from core.mistakes.infra.llm_schemas import resolution_schema
from core.shared.domain.model_usage import ModelUsage
from core.shared.llm.client import LLMClient, LLMRequest, Stage


class LLMResolutionWriter(ResolutionWriter):
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    async def write(self, source: MistakeSource, rejections: list[str]) -> tuple[ResolutionDraft, ModelUsage]:
        steps = source.exercise.step_ids if isinstance(source, ProblemSource) else None
        request = LLMRequest(
            system=prompts.resolution_system(source),
            user=prompts.resolution_user(source, rejections),
            schema=resolution_schema(steps),
            context=prompts.context(source),
        )
        data, meta = await self._llm.structured(Stage.MISTAKES_GENERATION, request)
        return ResolutionDraft.model_validate(data), meta.usage()
