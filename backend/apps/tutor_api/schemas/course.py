"""Response models of the course endpoints. Field names are the JSON keys the frontend reads (Catalan)."""

from urllib.parse import quote

from pydantic import BaseModel

from core.course.domain.entities.exercise import Exercise
from core.course.domain.entities.problem_sheet import Problem, ProblemSheet
from core.course.domain.entities.theory_item import TheoryItem
from core.course.domain.entities.topic import Topic

# The course PDFs, served under /pdf: citations open them at the cited page.
THEORY_PDF = "Teoria/Càlcul_Diferencial_FME_Tema{topic}.pdf"
PROBLEMS_PDF = "Problemes/_Problemes Temes_1-6.pdf"


def pdf_url(relative_path: str, page: int | None = None) -> str:
    """URL of a source PDF, opened at `page` by the browser's viewer (#page=N)."""
    return "/pdf/" + quote(relative_path) + (f"#page={page}" if page else "")


class ExerciseResponse(BaseModel):
    id: str
    llista: str
    grup: str
    tema: int | None
    problema: int
    apartat: str | None
    etiqueta: str
    tipus: str
    format: str
    font: str | None
    preambul: str
    indicacio: str
    enunciat: str

    @classmethod
    def from_entity(cls, ex: Exercise) -> "ExerciseResponse":
        return cls(
            id=ex.id,
            llista=ex.sheet_id,
            grup=ex.group,
            tema=ex.topic,
            problema=ex.problem,
            apartat=ex.part,
            etiqueta=ex.label,
            tipus=ex.kind,
            format=ex.format,
            font=ex.source,
            preambul=ex.preamble.strip(),
            indicacio=ex.hint.strip(),
            enunciat=ex.statement.strip(),
        )


class ProblemResponse(BaseModel):
    num: int
    font: str | None
    preambul: str
    indicacio: str | None
    exercicis: list[str]

    @classmethod
    def from_entity(cls, p: Problem) -> "ProblemResponse":
        return cls(num=p.number, font=p.source, preambul=p.preamble, indicacio=p.hint, exercicis=list(p.exercise_ids))


class SheetSummaryResponse(BaseModel):
    id: str
    etiqueta: str
    titol: str
    descripcio: str
    tema: int | None
    tipus: str
    format: str
    exercicis: list[str]
    n_exercicis: int
    n_problemes: int

    @classmethod
    def from_entity(cls, s: ProblemSheet) -> "SheetSummaryResponse":
        return cls(
            id=s.id,
            etiqueta=s.label,
            titol=s.title,
            descripcio=s.description,
            tema=s.topic,
            tipus=s.kind,
            format=s.format,
            exercicis=list(s.exercise_ids),
            n_exercicis=len(s.exercise_ids),
            n_problemes=len(s.problems),
        )


class SheetResponse(BaseModel):
    id: str
    etiqueta: str
    titol: str
    descripcio: str
    tema: int | None
    tipus: str
    format: str
    n_exercicis: int
    n_problemes: int
    exercicis: list[ExerciseResponse]
    problemes: list[ProblemResponse]

    @classmethod
    def from_entity(cls, s: ProblemSheet, exercises: list[Exercise]) -> "SheetResponse":
        summary = SheetSummaryResponse.from_entity(s).model_dump(exclude={"exercicis"})
        return cls(
            **summary,
            exercicis=[ExerciseResponse.from_entity(ex) for ex in exercises],
            problemes=[ProblemResponse.from_entity(p) for p in s.problems],
        )


class TheoryItemResponse(BaseModel):
    """An item with its full text (the theory popups in the chat and the theory section)."""

    id: str
    tema: int
    etiqueta: str
    nom: str
    enunciat: str
    demostracio: str
    pagina: int | None
    resum: int | str | None
    pdf: str

    @classmethod
    def from_entity(cls, it: TheoryItem) -> "TheoryItemResponse":
        return cls(
            id=it.id,
            tema=it.topic,
            etiqueta=it.label,
            nom=it.name,
            enunciat=it.statement.strip(),
            demostracio=it.proof.strip(),
            pagina=it.page,
            resum=it.summary_ref,
            pdf=pdf_url(THEORY_PDF.format(topic=it.topic), it.page),
        )


class TheoryIndexEntryResponse(BaseModel):
    """Lightweight entry for the theory index and for linking citations in the chat."""

    id: str
    tema: int
    num: int | None
    tipus: str
    etiqueta: str
    nom: str
    seccio: str
    pagina: int | None
    pdf: str

    @classmethod
    def from_entity(cls, it: TheoryItem) -> "TheoryIndexEntryResponse":
        return cls(
            id=it.id,
            tema=it.topic,
            num=it.number,
            tipus=it.kind,
            etiqueta=it.label,
            nom=it.name,
            seccio=it.section,
            pagina=it.page,
            pdf=pdf_url(THEORY_PDF.format(topic=it.topic), it.page),
        )


class TopicSectionResponse(BaseModel):
    id: str
    titol: str


class TopicIndexResponse(BaseModel):
    tema: int
    titol: str
    seccions: list[TopicSectionResponse]
    pdf: str
    items: list[TheoryIndexEntryResponse]

    @classmethod
    def from_entity(cls, topic: Topic, items: list[TheoryItem]) -> "TopicIndexResponse":
        return cls(
            tema=topic.number,
            titol=topic.title,
            seccions=[TopicSectionResponse(id=s.id, titol=s.title) for s in topic.sections],
            pdf=pdf_url(THEORY_PDF.format(topic=topic.number)),
            items=[TheoryIndexEntryResponse.from_entity(it) for it in items],
        )


class TheoryIndexResponse(BaseModel):
    temes: list[TopicIndexResponse]
    problemes_pdf: str
