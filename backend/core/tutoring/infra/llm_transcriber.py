from core.course.domain.entities.exercise import Exercise
from core.shared.llm.client import Image, LLMClient, LLMRequest, Stage
from core.tutoring.domain.ports import Transcriber
from core.tutoring.domain.values.photo import Photo
from core.tutoring.domain.values.transcription import Transcription
from core.tutoring.domain.values.turn_trace import ModelCall
from core.tutoring.infra.llm_schemas import transcription_schema
from core.tutoring.infra.llm_stage import call_stage, validate_output
from core.tutoring.infra.prompts import TRANSCRIPTION_SYSTEM, transcription_user

STAGE_NAME = "La transcripció"


class LLMTranscriber(Transcriber):
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    async def transcribe(self, ex: Exercise, photo: Photo) -> tuple[Transcription, ModelCall]:
        request = LLMRequest(
            system=TRANSCRIPTION_SYSTEM,
            user=transcription_user(ex),
            schema=transcription_schema(),
            image=Image(data=photo.data, media_type=photo.media_type),
        )
        data, call = await call_stage(self._llm, Stage.TRANSCRIPTION, request, STAGE_NAME)
        transcription = validate_output(Transcription, data, call, STAGE_NAME)
        return transcription.model_copy(update={"text": transcription.text.strip()}), call
