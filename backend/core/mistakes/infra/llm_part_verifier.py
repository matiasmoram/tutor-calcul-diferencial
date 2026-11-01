from core.mistakes.domain.ports import PartVerifier
from core.mistakes.domain.values.llm_outputs import PartReport
from core.mistakes.domain.values.mistake_source import MistakeSource
from core.mistakes.domain.values.resolution import ResolutionPart
from core.mistakes.infra import prompts
from core.mistakes.infra.llm_schemas import part_verification_schema
from core.shared.domain.model_usage import ModelUsage
from core.shared.llm.client import LLMClient, LLMRequest, Stage


class LLMPartVerifier(PartVerifier):
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    async def verify(
        self, source: MistakeSource, earlier: list[ResolutionPart], part: ResolutionPart
    ) -> tuple[PartReport, ModelUsage]:
        request = LLMRequest(
            system=prompts.PART_VERIFICATION_SYSTEM,
            user=prompts.part_verification_user(earlier, part),
            schema=part_verification_schema(len(part.fragments)),
            context=prompts.context(source),
        )
        data, meta = await self._llm.structured(Stage.MISTAKES_VERIFICATION, request)
        return PartReport.model_validate(data), meta.usage()
