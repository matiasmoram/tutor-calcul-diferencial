from core.mistakes.domain.ports import MistakeVerifier
from core.mistakes.domain.values.llm_outputs import VerificationReport
from core.mistakes.domain.values.mistake_source import MistakeSource
from core.mistakes.infra import prompts
from core.mistakes.infra.llm_schemas import verification_schema
from core.shared.domain.model_usage import ModelUsage
from core.shared.llm.client import LLMClient, LLMRequest, Stage


class LLMMistakeVerifier(MistakeVerifier):
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
