from collections.abc import Sequence

from core.course.domain.entities.course import Course
from core.course.domain.entities.exercise import Exercise
from core.course.domain.entities.theory_item import TheoryItem
from core.shared.domain.ids import TheoryItemId
from core.shared.llm.client import LLMClient, LLMRequest, Stage
from core.tutoring.domain.ports import ReplyJudge
from core.tutoring.domain.values.chat_message import ChatMessage
from core.tutoring.domain.values.guard_verdict import GuardVerdict
from core.tutoring.domain.values.plan import Plan
from core.tutoring.domain.values.turn_trace import ModelCall
from core.tutoring.infra.llm_schemas import guard_schema
from core.tutoring.infra.llm_stage import call_stage, validate_output
from core.tutoring.infra.prompts import GUARD_SYSTEM, guard_context, guard_user

STAGE_NAME = "El guardià"


class LLMReplyJudge(ReplyJudge):
    def __init__(self, llm: LLMClient, course: Course) -> None:
        self._llm = llm
        self._course = course

    async def judge(
        self,
        ex: Exercise,
        plan: Plan,
        allowed_content: str,
        theory: Sequence[TheoryItem],
        history: Sequence[ChatMessage],
        message: str,
        references: Sequence[TheoryItemId],
    ) -> tuple[GuardVerdict, ModelCall]:
        request = LLMRequest(
            system=GUARD_SYSTEM,
            user=guard_user(plan, allowed_content, history, message, theory, references),
            schema=guard_schema(),
            context=guard_context(self._course, ex),
        )
        data, call = await call_stage(self._llm, Stage.GUARD, request, STAGE_NAME)
        return validate_output(GuardVerdict, data, call, STAGE_NAME), call
