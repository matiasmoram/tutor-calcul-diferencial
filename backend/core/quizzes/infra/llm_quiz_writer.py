from core.quizzes.domain.values.drafts import BatchRequest, StatementDraft, WrittenBatch
from core.quizzes.domain.values.quiz_source import QuizSource
from core.quizzes.infra.llm_outputs import objects, parse_all
from core.quizzes.infra.llm_schemas import generation_schema
from core.quizzes.infra.prompts import GENERATION_SYSTEM, generation_request, source_context
from core.shared.llm.client import LLMClient, LLMRequest, Stage


class LLMQuizWriter:
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    async def write(self, source: QuizSource, request: BatchRequest) -> WrittenBatch:
        data, meta = await self._llm.structured(
            Stage.QUIZ_GENERATION,
            LLMRequest(
                system=GENERATION_SYSTEM,
                user=generation_request(source, request),
                schema=generation_schema(source.allowed_refs),
                context=source_context(source),
            ),
        )
        drafts = parse_all(StatementDraft, objects(data, "afirmacions"), Stage.QUIZ_GENERATION)
        return WrittenBatch(drafts=drafts, call=meta.usage())
