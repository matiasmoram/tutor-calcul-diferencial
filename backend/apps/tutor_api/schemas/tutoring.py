from pydantic import BaseModel, Field

from apps.tutor_api.schemas.course import ExerciseResponse, SheetSummaryResponse, TheoryItemResponse
from apps.tutor_api.schemas.student_text import StudentText
from core.tutoring.application.photo_transcriber import TranscriptionResult
from core.tutoring.application.session_starter import StartedSession
from core.tutoring.domain.entities.tutor_turn import TutorTurn
from core.tutoring.domain.values.chat_message import TurnOrigin
from core.tutoring.domain.values.transcription import Transcription
from core.tutoring.domain.values.turn_trace import ModelCall


class NewSessionRequest(BaseModel):
    exercici_id: StudentText = Field(max_length=20)


class MessageRequest(BaseModel):
    text: StudentText = Field(min_length=1, max_length=4000)
    origen: TurnOrigin = "text"


class PhotoRequest(BaseModel):
    # Under the body limit of the photo route (server.py). Base64 has no control characters to check.
    imatge: str = Field(min_length=1, max_length=9_000_000, description="data:image/...;base64,...")


class StepLabelResponse(BaseModel):
    id: str
    titol: str


class SheetTheoryResponse(BaseModel):
    id: str
    etiqueta: str
    nom: str
    on: list[str]
    reservada: bool


class SessionResponse(BaseModel):
    session_id: str
    exercici: ExerciseResponse
    llista: SheetSummaryResponse
    # Background theory the student may read from the start (never the items that solve the exercise).
    teoria: list[TheoryItemResponse]
    # Professors only: the solution sheet's outline and the theory it cites.
    passos: list[StepLabelResponse] | None = None
    nota_professor: str | None = None
    resultat: str | None = None
    teoria_fitxa: list[SheetTheoryResponse] | None = None

    @classmethod
    def from_entity(cls, started: StartedSession, professor: bool) -> "SessionResponse":
        out = cls(
            session_id=started.session.id,
            exercici=ExerciseResponse.from_entity(started.exercise),
            llista=SheetSummaryResponse.from_entity(started.sheet),
            teoria=[TheoryItemResponse.from_entity(it) for it in started.background_theory],
        )
        if professor:
            ex = started.exercise
            out.passos = [StepLabelResponse(id=s.id, titol=s.title) for s in ex.steps]
            out.nota_professor = ex.professor_note
            out.resultat = ex.result.value
            out.teoria_fitxa = [
                SheetTheoryResponse(
                    id=u.item.id, etiqueta=u.item.label, nom=u.item.name, on=u.used_in, reservada=u.reserved
                )
                for u in started.sheet_theory
            ]
        return out


class ProfessorTurnResponse(BaseModel):
    t: float
    exercici: str
    alumne: str
    tutor: str
    trace: dict[str, object]

    @classmethod
    def from_entity(cls, turn: TutorTurn, exercise_id: str) -> "ProfessorTurnResponse":
        return cls(
            t=turn.created_at,
            exercici=exercise_id,
            alumne=turn.student_text,
            tutor=turn.tutor_text,
            trace=turn.trace.model_dump(mode="json"),
        )


class TranscriptionResponse(Transcription):
    """The transcription's own contract keys, plus the call that produced it."""

    crida: ModelCall

    @classmethod
    def from_entity(cls, result: TranscriptionResult) -> "TranscriptionResponse":
        return cls(**dict(result.transcription), crida=result.call)


class TurnResponse(BaseModel):
    missatge: str
    referencies: list[TheoryItemResponse]  # the allowed items the reply cites, for the web to link
    # Professors get the full trace; students only {"fallback": ...} (it holds the allowed content and drafts).
    trace: dict[str, object]
