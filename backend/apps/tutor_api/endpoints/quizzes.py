""" "Cert o fals": quizzes on a topic or a result of the notes, with hints and a graded justification."""

import random

from fastapi import APIRouter, Depends

from apps.tutor_api.dependencies import (
    AppState,
    domain_errors,
    ensure_api_key,
    get_config,
    get_course,
    get_llm,
    get_session_provider,
    get_state,
    get_sympy_pool,
    may_generate,
    model_rate_limited,
)
from apps.tutor_api.schemas.course import TheoryIndexEntryResponse, TheoryItemResponse
from apps.tutor_api.schemas.quizzes import (
    AnswersRequest,
    HintResponse,
    NewQuizRequest,
    PublicQuizResponse,
    QuizSessionResponse,
    QuizSourcesResponse,
)
from core.course.domain.entities.course import Course
from core.quizzes.application.answers_grader import AnswersGrader, AnswersGraderInput
from core.quizzes.application.hint_revealer import HintRevealer
from core.quizzes.application.quiz_generator import QuizGenerator
from core.quizzes.application.quiz_provider import QuizProvider
from core.quizzes.application.quiz_session_starter import QuizSessionStarter, QuizSessionStarterInput
from core.quizzes.application.source_lister import SourceLister
from core.quizzes.domain.exceptions import QuizSessionNotFoundException
from core.quizzes.domain.sources import quiz_source
from core.quizzes.infra.llm_answer_grader import LLMAnswerGrader
from core.quizzes.infra.llm_blind_solver import LLMBlindSolver
from core.quizzes.infra.llm_claim_extractor import LLMClaimExtractor
from core.quizzes.infra.llm_quiz_auditor import LLMQuizAuditor
from core.quizzes.infra.llm_quiz_writer import LLMQuizWriter
from core.quizzes.infra.sqlmodel_repository import SQLModelQuizRepository, SQLModelQuizSessionRepository
from core.quizzes.infra.sympy_check_evaluator import SympyCheckEvaluator
from core.shared.domain.clock import SystemClock
from core.shared.domain.ids import SessionId
from core.shared.llm.client import LLMClient
from core.shared.math.infra.sympy_pool import SympyCheckPool
from core.shared.storage.session_provider import SQLModelSessionProvider
from settings import Config

router = APIRouter()


def _get_provider(
    state: AppState = Depends(get_state),
    sessions: SQLModelSessionProvider = Depends(get_session_provider),
    llm: LLMClient = Depends(get_llm),
    pool: SympyCheckPool = Depends(get_sympy_pool),
    generation_allowed: bool = Depends(may_generate),
) -> QuizProvider:
    rng = random.Random()
    generator = QuizGenerator(
        LLMQuizWriter(llm),
        LLMBlindSolver(llm),
        LLMQuizAuditor(llm),
        SympyCheckEvaluator(pool),
        SystemClock(),
        rng,
        deadline_s=state.config.QUIZ_GENERATION_DEADLINE_S,
    )
    return QuizProvider(
        SQLModelQuizRepository(sessions),
        generator,
        rng,
        generations=state.quiz_generations,
        may_generate=generation_allowed,
    )


def _get_starter(
    course: Course = Depends(get_course),
    sessions: SQLModelSessionProvider = Depends(get_session_provider),
    provider: QuizProvider = Depends(_get_provider),
) -> QuizSessionStarter:
    return QuizSessionStarter(course, provider, SQLModelQuizSessionRepository(sessions), SystemClock())


def _get_hints(sessions: SQLModelSessionProvider = Depends(get_session_provider)) -> HintRevealer:
    return HintRevealer(SQLModelQuizSessionRepository(sessions), SQLModelQuizRepository(sessions), SystemClock())


def _get_grader(
    course: Course = Depends(get_course),
    sessions: SQLModelSessionProvider = Depends(get_session_provider),
    llm: LLMClient = Depends(get_llm),
    pool: SympyCheckPool = Depends(get_sympy_pool),
) -> AnswersGrader:
    return AnswersGrader(
        course,
        SQLModelQuizSessionRepository(sessions),
        SQLModelQuizRepository(sessions),
        LLMAnswerGrader(llm),
        LLMClaimExtractor(llm),
        SympyCheckEvaluator(pool),
        SystemClock(),
    )


def _get_lister(
    course: Course = Depends(get_course), sessions: SQLModelSessionProvider = Depends(get_session_provider)
) -> SourceLister:
    return SourceLister(course, SQLModelQuizRepository(sessions))


@router.get("/api/afirmacions/fonts")
async def quiz_sources(lister: SourceLister = Depends(_get_lister)) -> QuizSourcesResponse:
    """Topics (whole-topic quizzes) and the results of the notes that can be the focus, with ready quizzes."""
    return QuizSourcesResponse.from_entity(await lister.list_sources())


@router.post("/api/afirmacions/sessions", dependencies=[Depends(model_rate_limited)])
async def start_quiz(
    body: NewQuizRequest,
    course: Course = Depends(get_course),
    provider: QuizProvider = Depends(_get_provider),
    starter: QuizSessionStarter = Depends(_get_starter),
    config: Config = Depends(get_config),
) -> QuizSessionResponse:
    with domain_errors("La generació"):
        source = quiz_source(course, body.font)
        if await provider.will_generate(source, body.dificultat, body.nova):
            ensure_api_key(config)
        started = await starter.start(
            QuizSessionStarterInput(
                source_id=body.font, difficulty=body.dificultat, new=body.nova, except_id=body.excepte
            )
        )
    focus = started.source.focus
    return QuizSessionResponse(
        session_id=started.session.id,
        questionari=PublicQuizResponse.from_entity(started.quiz),
        generat_ara=started.generated_now,
        focus=TheoryIndexEntryResponse.from_entity(focus) if focus else None,
    )


@router.post("/api/afirmacions/sessions/{session_id}/pista/{statement_id}")
async def reveal_hint(session_id: str, statement_id: str, hints: HintRevealer = Depends(_get_hints)) -> HintResponse:
    """Hints are served one at a time and recorded: a used hint lowers that statement's score."""
    with domain_errors():
        revealed = await hints.reveal(_session_id(session_id), statement_id)
    return HintResponse(id=revealed.statement_id, pista=revealed.hint)


@router.post("/api/afirmacions/sessions/{session_id}/correccio", dependencies=[Depends(model_rate_limited)])
async def grade_answers(
    session_id: str,
    body: AnswersRequest,
    course: Course = Depends(get_course),
    grader: AnswersGrader = Depends(_get_grader),
    config: Config = Depends(get_config),
) -> dict[str, object]:
    sid = _session_id(session_id)
    if any(a.verdict for a in body.respostes):
        ensure_api_key(config)
    with domain_errors("La correcció"):
        grading = await grader.grade(sid, AnswersGraderInput(answers=body.respostes))
        quiz_items = await grader.cited_theory(sid)
    result: dict[str, object] = grading.model_dump()
    result["teoria"] = {
        i: TheoryItemResponse.from_entity(course.theory[i]).model_dump() for i in quiz_items if i in course.theory
    }
    return result


def _session_id(raw: str) -> SessionId:
    with domain_errors():
        try:
            return SessionId(raw)
        except ValueError:
            raise QuizSessionNotFoundException(raw) from None
