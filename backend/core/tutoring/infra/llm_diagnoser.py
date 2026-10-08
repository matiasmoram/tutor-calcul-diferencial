from collections.abc import Sequence

from core.course.domain.entities.course import Course
from core.course.domain.entities.exercise import Exercise
from core.shared.domain.ids import TheoryItemId
from core.shared.llm.client import LLMClient, LLMRequest, Stage
from core.tutoring.domain.ports import Diagnoser
from core.tutoring.domain.values.chat_message import ChatMessage
from core.tutoring.domain.values.diagnosis import Diagnosis
from core.tutoring.domain.values.session_state import SessionState
from core.tutoring.domain.values.turn_trace import ModelCall
from core.tutoring.infra.llm_schemas import diagnosis_schema
from core.tutoring.infra.llm_stage import call_stage, validate_output
from core.tutoring.infra.prompts import DIAGNOSIS_SYSTEM, diagnosis_context, diagnosis_user

STAGE_NAME = "La diagnosi"


class LLMDiagnoser(Diagnoser):
    def __init__(self, llm: LLMClient, course: Course) -> None:
        self._llm = llm
        self._course = course

    async def diagnose(
        self, ex: Exercise, state: SessionState, history: Sequence[ChatMessage], concept_ids: Sequence[TheoryItemId]
    ) -> tuple[Diagnosis, ModelCall]:
        request = LLMRequest(
            system=DIAGNOSIS_SYSTEM,
            user=diagnosis_user(state, history),
            schema=diagnosis_schema(ex, concept_ids),
            context=diagnosis_context(self._course, ex),
        )
        data, call = await call_stage(self._llm, Stage.DIAGNOSIS, request, STAGE_NAME)
        return validate_output(Diagnosis, data, call, STAGE_NAME), call
