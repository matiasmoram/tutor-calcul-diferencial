"""'Troba l'error': documents with deliberate errors (a worked solution or a result of the notes) to annotate."""

from fastapi import APIRouter, Depends, HTTPException

from apps.tutor_api.dependencies import (
    AppState,
    domain_errors,
    ensure_api_key,
    get_config,
    get_course,
    get_llm,
    get_session_provider,
    get_state,
    may_generate,
    model_rate_limited,
)
from apps.tutor_api.schemas.course import (
    ExerciseResponse,
    SheetSummaryResponse,
    TheoryIndexEntryResponse,
    TheoryItemResponse,
)
from apps.tutor_api.schemas.mistakes import (
    GradingRequest,
    MistakeDocumentResponse,
    MistakeSessionResponse,
    NewMistakeSessionRequest,
    TheoryResultsResponse,
    TopicTheoryResultsResponse,
)
from core.course.domain.entities.course import Course
from core.mistakes.application.annotations_grader import AnnotationsGrader
from core.mistakes.application.availability_lister import AvailabilityLister
from core.mistakes.application.mistake_exercise_generator import MistakeExerciseGenerator
from core.mistakes.application.mistake_exercise_provider import MistakeExerciseProvider
from core.mistakes.application.mistake_session_starter import MistakeSessionStarter, MistakeSessionStarterInput
from core.mistakes.domain.exceptions import MistakeSessionNotFoundException
from core.mistakes.domain.values.mistake_source import ProblemSource
from core.mistakes.infra.llm_annotation_grader import LLMAnnotationGrader
from core.mistakes.infra.llm_mistake_generator import LLMMistakeGenerator
from core.mistakes.infra.llm_mistake_verifier import LLMMistakeVerifier
from core.mistakes.infra.sqlmodel_repository import SQLModelMistakeExerciseRepository, SQLModelMistakeSessionRepository
from core.shared.domain.clock import SystemClock
from core.shared.domain.ids import SessionId
from core.shared.llm.client import LLMClient
from core.shared.storage.session_provider import SQLModelSessionProvider
from settings import Config

router = APIRouter()


def _get_starter(
    state: AppState = Depends(get_state),
    course: Course = Depends(get_course),
    sessions: SQLModelSessionProvider = Depends(get_session_provider),
    llm: LLMClient = Depends(get_llm),
    generation_allowed: bool = Depends(may_generate),
) -> MistakeSessionStarter:
    clock = SystemClock()
    generator = MistakeExerciseGenerator(
        LLMMistakeGenerator(llm),
        LLMMistakeVerifier(llm),
        clock,
        deadline_s=state.config.MISTAKES_GENERATION_DEADLINE_S,
    )
    provider = MistakeExerciseProvider(
        SQLModelMistakeExerciseRepository(sessions),
        generator,
        generations=state.mistake_generations,
        may_generate=generation_allowed,
    )
    return MistakeSessionStarter(course, provider, SQLModelMistakeSessionRepository(sessions), clock)


def _get_grader(
    course: Course = Depends(get_course),
    sessions: SQLModelSessionProvider = Depends(get_session_provider),
    llm: LLMClient = Depends(get_llm),
) -> AnnotationsGrader:
    return AnnotationsGrader(
        course,
        SQLModelMistakeSessionRepository(sessions),
        SQLModelMistakeExerciseRepository(sessions),
        LLMAnnotationGrader(llm),
        SystemClock(),
    )


def _get_lister(
    course: Course = Depends(get_course), sessions: SQLModelSessionProvider = Depends(get_session_provider)
) -> AvailabilityLister:
    return AvailabilityLister(course, SQLModelMistakeExerciseRepository(sessions))


@router.get("/api/errades/teoria")
async def theory_results(lister: AvailabilityLister = Depends(_get_lister)) -> TheoryResultsResponse:
    """Results of the notes available for the theory activity, by topic, with the ready documents per difficulty."""
    topics = await lister.theory_results()
    return TheoryResultsResponse(temes=[TopicTheoryResultsResponse.from_entity(t) for t in topics])


@router.get("/api/errades/disponibles")
async def ready_documents(lister: AvailabilityLister = Depends(_get_lister)) -> dict[str, dict[str, int]]:
    """{source id: {difficulty: n}} of documents ready without calling the API."""
    return await lister.availability()


@router.post("/api/errades/sessions", response_model_exclude_unset=True, dependencies=[Depends(model_rate_limited)])
async def start_session(
    body: NewMistakeSessionRequest,
    course: Course = Depends(get_course),
    starter: MistakeSessionStarter = Depends(_get_starter),
    config: Config = Depends(get_config),
) -> MistakeSessionResponse:
    """Without the cost policy's permission (`may_generate`, applied by the provider), "nova" picks another ready
    document (`excepte`), and a source and difficulty with none ready is a 409: a student never starts a generation."""
    request = MistakeSessionStarterInput(
        exercise_id=body.exercici_id,
        theory_id=body.teoria_id,
        difficulty=body.dificultat,
        fresh=body.nova,
        avoid_id=body.excepte,
    )
    with domain_errors("La generació"):
        if await starter.needs_generation(request):
            ensure_api_key(config)
        started = await starter.start(request)
    out = MistakeSessionResponse(
        session_id=started.session.id,
        font=started.source.kind,
        solucio=MistakeDocumentResponse.from_entity(started.exercise),
        generada_ara=started.generated_now,
    )
    if isinstance(started.source, ProblemSource):
        ex = started.source.exercise
        out.exercici = ExerciseResponse.from_entity(ex)
        out.llista = SheetSummaryResponse.from_entity(course.sheet(ex.sheet_id))
    else:
        # Only the label: the statement of the notes is the answer key until the correction.
        out.teoria = TheoryIndexEntryResponse.from_entity(started.source.item)
    return out


@router.post("/api/errades/sessions/{session_id}/correccio", dependencies=[Depends(model_rate_limited)])
async def grade_annotations(
    session_id: str,
    body: GradingRequest,
    grader: AnnotationsGrader = Depends(_get_grader),
    config: Config = Depends(get_config),
) -> dict[str, object]:
    ensure_api_key(config)
    sid = _session_id(session_id)
    with domain_errors("La correcció"):
        outcome = await grader.grade(sid, body.anotacions)
    result: dict[str, object] = outcome.grading.model_dump()
    if outcome.original is not None:
        result["original"] = TheoryItemResponse.from_entity(outcome.original).model_dump()
    return result


def _session_id(raw: str) -> SessionId:
    try:
        return SessionId(raw)
    except ValueError:
        raise HTTPException(404, MistakeSessionNotFoundException(raw).message) from None
