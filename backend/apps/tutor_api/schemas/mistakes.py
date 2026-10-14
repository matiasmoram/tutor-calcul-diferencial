from pydantic import BaseModel, Field, field_validator

from apps.tutor_api.schemas.course import (
    THEORY_PDF,
    ExerciseResponse,
    SheetSummaryResponse,
    TheoryIndexEntryResponse,
    TopicSectionResponse,
    pdf_url,
)
from apps.tutor_api.schemas.student_text import StudentText, check_text
from core.mistakes.application.availability_lister import TopicTheoryResults
from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.values.difficulty import Difficulty


class NewMistakeSessionRequest(BaseModel):
    # Exactly one source: an exercise of the collection ("resolució dolenta") or a result of the notes.
    exercici_id: StudentText | None = Field(default=None, max_length=20)
    teoria_id: StudentText | None = Field(default=None, max_length=20)
    dificultat: Difficulty = "normal"
    nova: bool = False
    excepte: StudentText | None = Field(default=None, max_length=40)  # document just seen: prefer another one


class GradingRequest(BaseModel):
    anotacions: list[Annotation] = Field(max_length=40)

    @field_validator("anotacions")
    @classmethod
    def _student_text(cls, annotations: list[Annotation]) -> list[Annotation]:
        for a in annotations:
            check_text(a.id)
            check_text(a.comment)
        return annotations


class MistakeDocumentResponse(BaseModel):
    """What the student sees before submitting: the text, never the errors."""

    id: str
    font: str
    dificultat: str
    fragments: list[str]
    n_enunciat: int
    n_errors: int

    @classmethod
    def from_entity(cls, ex: MistakeExercise) -> "MistakeDocumentResponse":
        return cls(
            id=ex.id,
            font=ex.source_kind,
            dificultat=ex.difficulty,
            fragments=ex.fragments,
            n_enunciat=ex.statement_fragments,
            n_errors=ex.n_mistakes,
        )


class MistakeSessionResponse(BaseModel):
    session_id: str
    font: str
    solucio: MistakeDocumentResponse
    generada_ara: bool
    exercici: ExerciseResponse | None = None
    llista: SheetSummaryResponse | None = None
    teoria: TheoryIndexEntryResponse | None = None


class TheoryResultResponse(TheoryIndexEntryResponse):
    disponibles: dict[str, int]


class TopicTheoryResultsResponse(BaseModel):
    tema: int
    titol: str
    seccions: list[TopicSectionResponse]
    pdf: str
    items: list[TheoryResultResponse]

    @classmethod
    def from_entity(cls, t: TopicTheoryResults) -> "TopicTheoryResultsResponse":
        return cls(
            tema=t.topic.number,
            titol=t.topic.title,
            seccions=[TopicSectionResponse(id=s.id, titol=s.title) for s in t.topic.sections],
            pdf=pdf_url(THEORY_PDF.format(topic=t.topic.number)),
            items=[
                TheoryResultResponse(**TheoryIndexEntryResponse.from_entity(i.item).model_dump(), disponibles=i.ready)
                for i in t.items
            ],
        )


class TheoryResultsResponse(BaseModel):
    temes: list[TopicTheoryResultsResponse]
