"""The Socratic tutor: sessions on an exercise, turns, notebook photos, and the professor's review."""

from fastapi import APIRouter, Depends

from apps.tutor_api.dependencies import (
    ensure_api_key,
    get_config,
    get_course,
    get_llm,
    get_session_provider,
    is_professor,
    model_rate_limited,
    rate_limited,
    require_professor,
)
from apps.tutor_api.schemas.course import TheoryItemResponse
from apps.tutor_api.schemas.tutoring import (
    MessageRequest,
    NewSessionRequest,
    PhotoRequest,
    ProfessorTurnResponse,
    SessionResponse,
    TranscriptionResponse,
    TurnResponse,
)
from core.course.domain.entities.course import Course
from core.course.domain.exceptions import ExerciseNotFoundException
from core.shared.domain.clock import SystemClock
from core.shared.domain.ids import ExerciseId, SessionId
from core.shared.llm.client import LLMClient
from core.shared.storage.session_provider import SQLModelSessionProvider
from core.tutoring.application.photo_transcriber import PhotoTranscriber, PhotoTranscriberInput
from core.tutoring.application.session_browser import SessionBrowser
from core.tutoring.application.session_starter import SessionStarter
from core.tutoring.application.turn_handler import TurnHandler, TurnHandlerInput
from core.tutoring.domain.exceptions import TutorSessionNotFoundException
from core.tutoring.domain.values.photo import Photo
from core.tutoring.domain.values.session_summary import SessionSummary
from core.tutoring.infra.llm_diagnoser import LLMDiagnoser
from core.tutoring.infra.llm_reply_judge import LLMReplyJudge
from core.tutoring.infra.llm_reply_writer import LLMReplyWriter
from core.tutoring.infra.llm_transcriber import LLMTranscriber
from core.tutoring.infra.sqlmodel_repository import SQLModelTutorSessionRepository
from settings import Config

router = APIRouter()


def _get_starter(
    course: Course = Depends(get_course), sessions: SQLModelSessionProvider = Depends(get_session_provider)
) -> SessionStarter:
    return SessionStarter(course, SQLModelTutorSessionRepository(sessions), SystemClock())


def _get_turn_handler(
    course: Course = Depends(get_course),
    sessions: SQLModelSessionProvider = Depends(get_session_provider),
    llm: LLMClient = Depends(get_llm),
) -> TurnHandler:
    return TurnHandler(
        course,
        SQLModelTutorSessionRepository(sessions),
        LLMDiagnoser(llm, course),
        LLMReplyWriter(llm),
        LLMReplyJudge(llm, course),
        SystemClock(),
    )


def _get_transcriber(
    course: Course = Depends(get_course),
    sessions: SQLModelSessionProvider = Depends(get_session_provider),
    llm: LLMClient = Depends(get_llm),
) -> PhotoTranscriber:
    return PhotoTranscriber(course, SQLModelTutorSessionRepository(sessions), LLMTranscriber(llm), SystemClock())


def _get_browser(sessions: SQLModelSessionProvider = Depends(get_session_provider)) -> SessionBrowser:
    return SessionBrowser(SQLModelTutorSessionRepository(sessions))


@router.post("/api/sessions", response_model_exclude_unset=True, dependencies=[Depends(rate_limited)])
async def start_session(
    body: NewSessionRequest,
    starter: SessionStarter = Depends(_get_starter),
    professor: bool = Depends(is_professor),
) -> SessionResponse:
    started = await starter.start(_exercise_id(body.exercici_id))
    return SessionResponse.from_entity(started, professor)


@router.post("/api/sessions/{session_id}/missatges", dependencies=[Depends(model_rate_limited)])
async def send_message(
    session_id: str,
    body: MessageRequest,
    handler: TurnHandler = Depends(_get_turn_handler),
    config: Config = Depends(get_config),
    professor: bool = Depends(is_professor),
) -> TurnResponse:
    sid = _session_id(session_id)
    ensure_api_key(config)
    result = await handler.handle(TurnHandlerInput(session_id=sid, text=body.text, origin=body.origen))
    trace: dict[str, object] = (
        result.trace.model_dump(mode="json") if professor else {"fallback": result.trace.fallback}
    )
    references = [TheoryItemResponse.from_entity(it) for it in result.references]
    return TurnResponse(missatge=result.message, referencies=references, trace=trace)


@router.post("/api/sessions/{session_id}/transcripcio", dependencies=[Depends(model_rate_limited)])
async def transcribe_photo(
    session_id: str,
    body: PhotoRequest,
    transcriber: PhotoTranscriber = Depends(_get_transcriber),
    config: Config = Depends(get_config),
) -> TranscriptionResponse:
    sid = _session_id(session_id)
    ensure_api_key(config)
    result = await transcriber.transcribe(PhotoTranscriberInput(session_id=sid, photo=Photo.from_data_url(body.imatge)))
    return TranscriptionResponse.from_entity(result)


@router.get("/api/professor/sessions", dependencies=[Depends(require_professor)])
async def professor_sessions(browser: SessionBrowser = Depends(_get_browser)) -> list[SessionSummary]:
    return await browser.list_sessions()


@router.get("/api/professor/sessions/{session_id}", dependencies=[Depends(require_professor)])
async def professor_session(
    session_id: str, browser: SessionBrowser = Depends(_get_browser)
) -> list[ProfessorTurnResponse]:
    transcript = await browser.transcript(_session_id(session_id))
    return [ProfessorTurnResponse.from_entity(t, transcript.exercise_id) for t in transcript.turns]


def _session_id(raw: str) -> SessionId:
    try:
        return SessionId(raw)
    except ValueError:
        raise TutorSessionNotFoundException(raw) from None


def _exercise_id(raw: str) -> ExerciseId:
    try:
        return ExerciseId(raw)
    except ValueError:
        raise ExerciseNotFoundException(raw) from None
