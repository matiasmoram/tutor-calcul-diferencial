from core.mistakes.domain.ports import MistakeGenerator
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.llm_outputs import GenerationDraft
from core.mistakes.domain.values.mistake_source import MistakeSource, TheorySource
from core.mistakes.infra import prompts
from core.mistakes.infra.llm_schemas import generation_schema
from core.shared.domain.model_usage import ModelUsage
from core.shared.llm.client import LLMClient, LLMRequest, Stage


class LLMMistakeGenerator(MistakeGenerator):
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
