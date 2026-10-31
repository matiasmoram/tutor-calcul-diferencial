from core.mistakes.domain.ports import ResolutionVerifier
from core.mistakes.domain.values.llm_outputs import ResolutionReport
from core.mistakes.domain.values.mistake_source import MistakeSource
from core.mistakes.domain.values.resolution import Resolution
from core.mistakes.infra import prompts
from core.mistakes.infra.llm_schemas import resolution_verification_schema
from core.shared.domain.model_usage import ModelUsage
from core.shared.llm.client import LLMClient, LLMRequest, Stage


class LLMResolutionVerifier(ResolutionVerifier):
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    async def verify(self, source: MistakeSource, resolution: Resolution) -> tuple[ResolutionReport, ModelUsage]:
        fragments = resolution.fragments
        request = LLMRequest(
            system=prompts.resolution_check_system(source),
            user=prompts.verification_user(source, fragments, resolution.statement_fragments),
            schema=resolution_verification_schema(len(fragments)),
            context=prompts.context(source),
        )
        data, meta = await self._llm.structured(Stage.MISTAKES_VERIFICATION, request)
        return ResolutionReport.model_validate(data), meta.usage()
