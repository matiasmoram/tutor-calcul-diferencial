from typing import Any

from pydantic import BaseModel, Field, SerializerFunctionWrapHandler, field_validator, model_serializer

from apps.tutor_api.schemas.course import (
    THEORY_PDF,
    ExerciseResponse,
    SheetSummaryResponse,
    TheoryIndexEntryResponse,
    TheoryItemResponse,
    TopicSectionResponse,
    pdf_url,
)
from apps.tutor_api.schemas.student_text import StudentText, check_text
from core.mistakes.application.annotations_grader import AnnotationsGrading
from core.mistakes.application.availability_lister import TopicTheoryResults
from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.entities.mistake_grading import MistakeGrading
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


class MistakeGradingResponse(MistakeGrading):
    """The grading as stored, plus the original item of the notes for a theory document (revealed with the grade)."""

    original: TheoryItemResponse | None = None

    @model_serializer(mode="wrap")
    def _omit_absent_original(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        data: dict[str, Any] = handler(self)
        if data.get("original") is None:
            data.pop("original", None)
        return data

    @classmethod
    def from_entity(cls, graded: AnnotationsGrading) -> "MistakeGradingResponse":
        original = TheoryItemResponse.from_entity(graded.original) if graded.original is not None else None
        fields = {name: getattr(graded.grading, name) for name in MistakeGrading.model_fields}
        return cls(**fields, original=original)


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
