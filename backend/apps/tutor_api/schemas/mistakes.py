from typing import Any, Literal

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
from core.mistakes.application.part_annotations_grader import PartGradingOutcome
from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_exercise import DeclaredMistake, MistakeExercise
from core.mistakes.domain.entities.mistake_grading import AnnotationResult, MistakeGrading, PartScore
from core.mistakes.domain.entities.parted_mistake_exercise import (
    PartedMistakeExercise,
    PartOutline,
    PartText,
    PartToReview,
)
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.layout import Layout
from core.shared.domain.contract import omit_none
from core.shared.domain.model_usage import ModelUsage


class NewMistakeSessionRequest(BaseModel):
    # Exactly one source: an exercise of the collection ("resolució dolenta") or a result of the notes.
    exercici_id: StudentText | None = Field(default=None, max_length=20)
    teoria_id: StudentText | None = Field(default=None, max_length=20)
    dificultat: Difficulty = "normal"
    nova: bool = False
    excepte: StudentText | None = Field(default=None, max_length=40)  # document just seen: prefer another one
    format: Layout = "sencer"


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


class PartOutlineResponse(BaseModel):
    part: int
    titol: str
    revisar: bool

    @classmethod
    def from_entity(cls, p: PartOutline) -> "PartOutlineResponse":
        return cls(part=p.part, titol=p.title, revisar=p.review)


class PartTextResponse(BaseModel):
    part: int
    fragments: list[str]

    @classmethod
    def from_entity(cls, p: PartText) -> "PartTextResponse":
        return cls(part=p.part, fragments=p.fragments)


class PartToReviewResponse(BaseModel):
    """The flawed part to review next: its text with the error, and the correct text of the clean parts since the
    previous review."""

    part: int
    primer_fragment: int
    fragments: list[str]
    anteriors: list[PartTextResponse]

    @classmethod
    def from_entity(cls, p: PartToReview) -> "PartToReviewResponse":
        return cls(
            part=p.part,
            primer_fragment=p.first_fragment,
            fragments=p.fragments,
            anteriors=[PartTextResponse.from_entity(t) for t in p.earlier],
        )


class PartedMistakeDocumentResponse(BaseModel):
    """What the student sees before reviewing a per-parts document: every part's title and the first flawed part.
    Never the errors, the correct text of the part under review nor the parts after it."""

    id: str
    font: str
    dificultat: str
    format: Literal["per_parts"]
    n_enunciat: int
    n_errors: int
    parts: list[PartOutlineResponse]
    actual: PartToReviewResponse

    @classmethod
    def from_entity(cls, doc: PartedMistakeExercise) -> "PartedMistakeDocumentResponse":
        first = doc.review_after(0)
        assert first is not None, "a document in parts has at least one flawed part"
        return cls(
            id=doc.id,
            font=doc.source_kind,
            dificultat=doc.difficulty,
            format=doc.layout,
            n_enunciat=doc.statement_fragments,
            n_errors=doc.n_mistakes,
            parts=[PartOutlineResponse.from_entity(p) for p in doc.outline()],
            actual=PartToReviewResponse.from_entity(first),
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
    solucio: MistakeDocumentResponse | PartedMistakeDocumentResponse
    generada_ara: bool
    exercici: ExerciseResponse | None = None
    llista: SheetSummaryResponse | None = None
    teoria: TheoryIndexEntryResponse | None = None


class PartHintResponse(BaseModel):
    pista: str


class PartScoreResponse(BaseModel):
    part: int
    nota: int
    pista: bool  # the student asked for the part's hint: its nota carries the hint factor

    @classmethod
    def from_entity(cls, p: PartScore) -> "PartScoreResponse":
        return cls(part=p.part, nota=p.score, pista=p.hint_used)


class PartedGradingResponse(BaseModel):
    """A per-parts session once its last flawed part is graded: the mean of the part scores, the whole correct
    resolution and, for theory, the original item of the notes."""

    nota: int
    trobats: int
    total: int
    falsos_positius: int
    parts: list[PartScoreResponse]
    resolucio: list[PartTextResponse]
    original: TheoryItemResponse | None = Field(default=None, exclude_if=omit_none)


class PartGradingResponse(BaseModel):
    """One graded part: the same grading JSON as a whole document's, restricted to the part (its error only), then
    the part's correct text and what comes next, the next flawed part or the final result."""

    nota: int
    trobats: int
    total: int
    falsos_positius: int
    anotacions: list[AnnotationResult]
    errors: list[DeclaredMistake]
    resum: str
    crida: ModelUsage | None
    part: int
    correcte: list[str]
    seguent: PartToReviewResponse | None
    final: PartedGradingResponse | None

    @classmethod
    def from_entity(cls, outcome: PartGradingOutcome) -> "PartGradingResponse":
        g = outcome.graded.grading
        final = None
        if outcome.final is not None:
            final = PartedGradingResponse(
                nota=outcome.final.score,
                trobats=outcome.final.found,
                total=outcome.final.total,
                falsos_positius=outcome.final.false_positives,
                parts=[PartScoreResponse.from_entity(p) for p in outcome.final.parts],
                resolucio=[PartTextResponse.from_entity(p) for p in outcome.resolution or []],
                original=TheoryItemResponse.from_entity(outcome.original) if outcome.original else None,
            )
        return cls(
            nota=g.score,
            trobats=g.found,
            total=g.total,
            falsos_positius=g.false_positives,
            anotacions=g.annotations,
            errors=g.mistakes,
            resum=g.summary,
            crida=g.call,
            part=outcome.graded.part,
            correcte=outcome.correct,
            seguent=PartToReviewResponse.from_entity(outcome.next) if outcome.next else None,
            final=final,
        )


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
