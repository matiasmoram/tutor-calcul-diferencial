from pydantic import BaseModel, ConfigDict

from core.course.domain.entities.course import Course
from core.shared.domain.clock import Clock
from core.shared.domain.ids import SessionId
from core.shared.llm.call_scope import call_scope
from core.tutoring.domain.ports import Transcriber
from core.tutoring.domain.repository import TutorSessionRepository
from core.tutoring.domain.values.photo import Photo
from core.tutoring.domain.values.transcription import Transcription
from core.tutoring.domain.values.turn_trace import ModelCall


class PhotoTranscriberInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    session_id: SessionId
    photo: Photo


class TranscriptionResult(BaseModel):
    transcription: Transcription
    call: ModelCall


class PhotoTranscriber:
    """Photo of the student's notebook -> text for the student to review before sending it as a message.

    The transcriber must not fix mistakes, or the diagnosis would never see them."""

    def __init__(
        self,
        course: Course,
        sessions: TutorSessionRepository,
        transcriber: Transcriber,
        clock: Clock,
    ) -> None:
        self._course = course
        self._sessions = sessions
        self._transcriber = transcriber
        self._clock = clock

    async def transcribe(self, request: PhotoTranscriberInput) -> TranscriptionResult:
        session = await self._sessions.get(request.session_id)
        ex = self._course.exercise(session.exercise_id)
        with call_scope(session.id):
            transcription, call = await self._transcriber.transcribe(ex, request.photo)
        await self._sessions.add_transcription(session.id, transcription, self._clock.now())
        return TranscriptionResult(transcription=transcription, call=call)
