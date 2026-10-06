from fastapi import APIRouter, Depends

from apps.tutor_api.dependencies import domain_errors, get_course
from apps.tutor_api.schemas.course import (
    PROBLEMS_PDF,
    SheetResponse,
    SheetSummaryResponse,
    TheoryIndexResponse,
    TheoryItemResponse,
    TopicIndexResponse,
    pdf_url,
)
from core.course.domain.entities.course import Course

router = APIRouter()


@router.get("/api/llistes")
async def list_sheets(course: Course = Depends(get_course)) -> list[SheetSummaryResponse]:
    return [SheetSummaryResponse.from_entity(s) for s in course.sheets.values()]


@router.get("/api/llistes/{sheet_id}")
async def get_sheet(sheet_id: str, course: Course = Depends(get_course)) -> SheetResponse:
    with domain_errors():
        sheet = course.sheet(sheet_id)
    return SheetResponse.from_entity(sheet, [course.exercise(e) for e in sheet.exercise_ids])


@router.get("/api/teoria")
async def theory_index(course: Course = Depends(get_course)) -> TheoryIndexResponse:
    """Every item of the notes, grouped by topic, with a link to its page in the PDF."""
    topics = [
        TopicIndexResponse.from_entity(t, [it for it in course.theory.values() if it.topic == t.number])
        for t in course.topics
    ]
    return TheoryIndexResponse(temes=topics, problemes_pdf=pdf_url(PROBLEMS_PDF))


@router.get("/api/teoria/{item_id}")
async def get_theory_item(item_id: str, course: Course = Depends(get_course)) -> TheoryItemResponse:
    with domain_errors():
        return TheoryItemResponse.from_entity(course.theory_item(item_id))
