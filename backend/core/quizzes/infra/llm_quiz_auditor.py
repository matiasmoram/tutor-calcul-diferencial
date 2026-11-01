from collections.abc import Sequence

from core.quizzes.domain.ports import QuizAuditor
from core.quizzes.domain.values.drafts import StatementDraft
from core.quizzes.domain.values.quiz_source import QuizSource
from core.quizzes.domain.values.verification import AuditReview, AuditReviews
from core.quizzes.infra.llm_outputs import objects, parse_all
from core.quizzes.infra.llm_schemas import audit_schema
from core.quizzes.infra.prompts import AUDIT_SYSTEM, audit_request, source_context
from core.shared.llm.client import LLMClient, LLMRequest, Stage


class LLMQuizAuditor(QuizAuditor):
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    async def audit(self, source: QuizSource, drafts: Sequence[StatementDraft]) -> AuditReviews:
        data, meta = await self._llm.structured(
            Stage.QUIZ_AUDIT,
            LLMRequest(
                system=AUDIT_SYSTEM,
                user=audit_request(drafts),
                schema=audit_schema(),
                context=source_context(source),
            ),
        )
        reviews = parse_all(AuditReview, objects(data, "revisions"), Stage.QUIZ_AUDIT)
        return AuditReviews(reviews=reviews, call=meta.usage())
