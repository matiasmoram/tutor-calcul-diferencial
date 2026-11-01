from core.mistakes.domain.ports import PartCorrupter
from core.mistakes.domain.services.corruption_plan import CorruptionPlan
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.llm_outputs import CorruptionDraft
from core.mistakes.domain.values.mistake_source import MistakeSource, TheorySource
from core.mistakes.domain.values.resolution import Resolution
from core.mistakes.infra import prompts
from core.mistakes.infra.llm_schemas import corruption_schema
from core.shared.domain.model_usage import ModelUsage
from core.shared.llm.client import LLMClient, LLMRequest, Stage


class LLMPartCorrupter(PartCorrupter):
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    async def corrupt(
        self,
        source: MistakeSource,
        resolution: Resolution,
        part: int,
        difficulty: Difficulty,
        rejections: list[str],
        plan: CorruptionPlan | None = None,
    ) -> tuple[CorruptionDraft, ModelUsage]:
        request = LLMRequest(
            system=prompts.corruption_system(source),
            user=prompts.corruption_user(resolution, part, difficulty, rejections, plan),
            schema=corruption_schema(len(resolution.parts[part - 1].fragments), isinstance(source, TheorySource)),
            # The same for every part and retry: the clean resolution is cached with the reference.
            context=prompts.corruption_context(source, resolution),
        )
        data, meta = await self._llm.structured(Stage.MISTAKES_GENERATION, request)
        return CorruptionDraft.model_validate(data), meta.usage()
