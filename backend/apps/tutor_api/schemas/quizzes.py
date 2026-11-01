from collections.abc import Iterable

from pydantic import BaseModel, Field, field_validator

from apps.tutor_api.schemas.course import (
    THEORY_PDF,
    TheoryIndexEntryResponse,
    TheoryItemResponse,
    TopicSectionResponse,
    pdf_url,
)
from apps.tutor_api.schemas.student_text import StudentText, check_text
from core.course.domain.entities.theory_item import TheoryItem
from core.quizzes.application.source_lister import QuizSourceIndex, TopicSources
from core.quizzes.domain.entities.grading import Answer, QuizGrading
from core.quizzes.domain.entities.quiz import Quiz
from core.quizzes.domain.values.difficulty import Difficulty


class NewQuizRequest(BaseModel):
    font: StudentText = Field(max_length=20)  # "tema-2" or a result of the notes ("T2.12") as the focus
    dificultat: Difficulty = "normal"
    nova: bool = False
    excepte: StudentText | None = Field(default=None, max_length=40)


class AnswersRequest(BaseModel):
    respostes: list[Answer] = Field(max_length=20)

    @field_validator("respostes")
    @classmethod
    def _student_text(cls, answers: list[Answer]) -> list[Answer]:
        for a in answers:
            check_text(a.statement_id)
            check_text(a.justification)
        return answers


class QuizGradingResponse(QuizGrading):
    """The grading's own contract keys, plus the items of the notes its solutions cite."""

    teoria: dict[str, TheoryItemResponse]

    @classmethod
    def from_entity(cls, grading: QuizGrading, cited: Iterable[TheoryItem]) -> "QuizGradingResponse":
        return cls(**dict(grading), teoria={it.id: TheoryItemResponse.from_entity(it) for it in cited})


class PublicStatementResponse(BaseModel):
    id: str
    enunciat: str
    concepte: str


class PublicQuizResponse(BaseModel):
    """What the student sees before answering: statements and topic labels, never verdicts or hints."""

    id: str
    font: str
    tema: int
    dificultat: str
    afirmacions: list[PublicStatementResponse]

    @classmethod
    def from_entity(cls, quiz: Quiz) -> "PublicQuizResponse":
        return cls(
            id=quiz.id,
            font=quiz.source_id,
            tema=quiz.topic,
            dificultat=quiz.difficulty,
            afirmacions=[
                PublicStatementResponse(id=s.id, enunciat=s.statement, concepte=s.concept) for s in quiz.statements
            ],
        )


class QuizSessionResponse(BaseModel):
    session_id: str
    questionari: PublicQuizResponse
    generat_ara: bool
    focus: TheoryIndexEntryResponse | None


class HintResponse(BaseModel):
    id: str
    pista: str


class FocusSourceResponse(TheoryIndexEntryResponse):
    disponibles: dict[Difficulty, int]


class TopicSourcesResponse(BaseModel):
    tema: int
    titol: str
    seccions: list[TopicSectionResponse]
    pdf: str
    id: str
    disponibles: dict[Difficulty, int]
    items: list[FocusSourceResponse]

    @classmethod
    def from_entity(cls, t: TopicSources) -> "TopicSourcesResponse":
        return cls(
            tema=t.topic.number,
            titol=t.topic.title,
            seccions=[TopicSectionResponse(id=s.id, titol=s.title) for s in t.topic.sections],
            pdf=pdf_url(THEORY_PDF.format(topic=t.topic.number)),
            id=t.source_id,
            disponibles=dict(t.available),
            items=[
                FocusSourceResponse(
                    **TheoryIndexEntryResponse.from_entity(f.item).model_dump(), disponibles=dict(f.available)
                )
                for f in t.focus
            ],
        )


class QuizSourcesResponse(BaseModel):
    temes: list[TopicSourcesResponse]
    mida: dict[Difficulty, int]

    @classmethod
    def from_entity(cls, index: QuizSourceIndex) -> "QuizSourcesResponse":
        return cls(temes=[TopicSourcesResponse.from_entity(t) for t in index.topics], mida=dict(index.sizes))
