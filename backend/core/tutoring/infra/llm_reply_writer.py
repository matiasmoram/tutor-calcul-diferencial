from collections.abc import Sequence

from core.course.domain.entities.exercise import Exercise
from core.course.domain.entities.theory_item import TheoryItem
from core.shared.llm.client import LLMClient, LLMRequest, Stage
from core.tutoring.domain.exceptions import ModelOutputException
from core.tutoring.domain.ports import ReplyWriter
from core.tutoring.domain.values.chat_message import ChatMessage
from core.tutoring.domain.values.plan import Plan
from core.tutoring.domain.values.turn_trace import ModelCall
from core.tutoring.infra.llm_stage import call_stage
from core.tutoring.infra.prompts import REPLY_SYSTEM, reply_user

STAGE_NAME = "La resposta"


class LLMReplyWriter(ReplyWriter):
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    async def write(
        self,
        ex: Exercise,
        history: Sequence[ChatMessage],
        plan: Plan,
        allowed_content: str,
        theory: Sequence[TheoryItem],
        feedback: str | None,
    ) -> tuple[str, ModelCall]:
        # Plain text (no schema): LaTeX-heavy prose survives intact, and small models need no JSON.
        request = LLMRequest(
            system=REPLY_SYSTEM, user=reply_user(ex, history, plan, allowed_content, feedback, theory), schema=None
        )
        data, call = await call_stage(self._llm, Stage.REPLY, request, STAGE_NAME)
        text = data.get("text")
        message = text.strip() if isinstance(text, str) else ""
        if not message:
            raise ModelOutputException(STAGE_NAME, f"{Stage.REPLY}: empty response", call)
        return message, call
