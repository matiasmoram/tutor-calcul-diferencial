"""The tutor's HTTP API and static frontend. Composition root: the only place that builds concretes."""

import asyncio
from collections import defaultdict
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from apps.tutor_api.body_limit import BodySizeLimit
from apps.tutor_api.dependencies import AppState
from apps.tutor_api.endpoints import config as config_endpoints
from apps.tutor_api.endpoints import counterexamples as counterexample_endpoints
from apps.tutor_api.endpoints import course as course_endpoints
from apps.tutor_api.endpoints import mistakes as mistakes_endpoints
from apps.tutor_api.endpoints import quizzes as quiz_endpoints
from apps.tutor_api.endpoints import tutoring as tutoring_endpoints
from apps.tutor_api.rate_limiter import RateLimiter
from core.counterexamples.domain.entities.spec import SpecCatalog
from core.counterexamples.infra.pool_property_checker import PoolPropertyChecker
from core.counterexamples.infra.yaml_spec_source import YamlSpecSource
from core.course.infra.yaml_course_source import YamlCourseSource
from core.mistakes.infra.json_file_source import JsonFileMistakeSource
from core.mistakes.infra.sqlmodel_repository import SQLModelMistakeExerciseRepository
from core.quizzes.infra.json_quiz_files import JsonQuizFiles
from core.quizzes.infra.sqlmodel_repository import SQLModelQuizRepository
from core.shared.domain.single_flight import SingleFlight
from core.shared.llm.client import LLMClient
from core.shared.llm.infra.factory import make_llm_client
from core.shared.llm.infra.logged_client import LoggedLLMClient
from core.shared.llm.infra.retrying_client import RetryingLLMClient
from core.shared.llm_calls.infra.sqlmodel_repository import SQLModelLLMCallRepository
from core.shared.math.infra.sympy_pool import SympyCheckPool
from core.shared.storage.session_provider import SQLModelSessionProvider, create_schema_if_sqlite, make_engine
from core.shared.storage.table_registry import register_all_tables
from settings import BACKEND_DIR, ROOT_DIR, Config

FRONTEND_DIR = ROOT_DIR / "frontend"
SOURCES_DIR = ROOT_DIR / "sources"
# Request bodies: a notebook photo (base64, PhotoRequest) is the only large one.
MAX_BODY = 256 * 1024
MAX_PHOTO_BODY = 10 * 1024 * 1024
PHOTO_ROUTE = r"/api/sessions/[^/]+/transcripcio"


async def _seed_generated(sessions: SQLModelSessionProvider) -> None:
    """Pre-generated documents and quizzes (backend/generats) seed the generated-content tables.

    Every start imports the files whose id the database lacks (a first start, or a deploy that added files): one
    query per source and difficulty (and layout, for documents), one write per missing document. Counting rows instead
    would let the documents generated at run time hide new files forever. Assumes one server process (the Dockerfile
    runs one worker); with several, run `scripts/db.py import-generats` as a deploy step instead."""
    generated = BACKEND_DIR / "generats"
    mistakes = SQLModelMistakeExerciseRepository(sessions)
    documents_by_group = _grouped(
        JsonFileMistakeSource(generated / "errades").load_all(), lambda d: (d.source_id, d.difficulty, d.layout)
    )
    for (source_id, difficulty, layout), documents in documents_by_group.items():
        stored = {e.id for e in await mistakes.of_source(source_id, difficulty, layout)}
        for document in documents:
            if document.id not in stored:
                await mistakes.save(document)
    quizzes = SQLModelQuizRepository(sessions)
    quizzes_by_group = _grouped(
        JsonQuizFiles(generated / "afirmacions").load_all(), lambda q: (q.source_id, q.difficulty)
    )
    for (source_id, difficulty), group in quizzes_by_group.items():
        stored = {q.id for q in await quizzes.of_source(source_id, difficulty)}
        for quiz in group:
            if quiz.id not in stored:
                await quizzes.add(quiz)


async def _warm_sympy(pool: SympyCheckPool, catalog: SpecCatalog, warm_cache: bool) -> None:
    try:
        await pool.start()
        if warm_cache:
            await PoolPropertyChecker(pool).warm(catalog)
    except Exception:  # best effort: the checks still run, only colder
        logger.exception("sympy warm-up failed")
    else:
        logger.info("sympy warm-up done")


def _grouped[K, T](items: list[T], key: Callable[[T], K]) -> dict[K, list[T]]:
    out: dict[K, list[T]] = defaultdict(list)
    for item in items:
        out[key(item)].append(item)
    return out


def _validation_error(request: Request, exc: Exception) -> JSONResponse:
    """FastAPI's default 422 echoes the invalid input, and a lone surrogate in it cannot be encoded: the 422 became
    a 500. Location and message only (both ASCII-safe once a surrogate in a dict key is replaced)."""
    assert isinstance(exc, RequestValidationError)
    errors = [
        {"loc": [_printable(part) for part in e.get("loc", ())], "msg": _printable(e.get("msg", "")), "type": e["type"]}
        for e in exc.errors()
    ]
    return JSONResponse({"detail": errors}, status_code=422)


def _printable(value: object) -> object:
    if isinstance(value, str):
        return value.encode("utf-8", "replace").decode("utf-8")
    return value


def create_app(config: Config | None = None, llm: LLMClient | None = None) -> FastAPI:
    """`llm` replaces the configured provider (tests pass the scripted fake); every call is still logged."""

    cfg = config or Config()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine = make_engine(cfg.async_database_url)
        register_all_tables()
        await create_schema_if_sqlite(engine)
        sessions = SQLModelSessionProvider(engine)
        # The course is read-only authored content shipped in the image: loaded from the YAML on every start, so a
        # deploy with edited sheets serves them at once (the database holds only what the app produces).
        course = YamlCourseSource(BACKEND_DIR / "exercicis", BACKEND_DIR / "teoria").load()
        counterexamples = YamlSpecSource(BACKEND_DIR / "contraexemples" / "reptes.yaml").load()
        counterexamples.check_theory(course.theory)  # a challenge citing a missing item fails the start-up
        await _seed_generated(sessions)
        inner = llm or make_llm_client(cfg)
        logged = LoggedLLMClient(inner, SQLModelLLMCallRepository(sessions), log_prompts=cfg.LOG_PROMPTS)
        if not cfg.PROFESSOR_KEY and not cfg.DEMO_MODE:
            logger.warning(
                "No TUTOR_CLAU_PROFESSOR and no TUTOR_DEMO=1: solutions and traces are hidden from everyone."
            )
        sympy = SympyCheckPool(max_workers=cfg.SYMPY_WORKERS)
        # Spawns the workers and decides the authored examples in the background: /health answers meanwhile.
        warm_up = asyncio.create_task(_warm_sympy(sympy, counterexamples, cfg.SYMPY_WARM_CACHE))
        app.state.tutor = AppState(
            config=cfg,
            sessions=sessions,
            course=course,
            llm=RetryingLLMClient(logged),
            limiter=RateLimiter(cfg.MODEL_REQUESTS_PER_MINUTE),
            global_limiter=RateLimiter(cfg.MODEL_REQUESTS_PER_MINUTE_GLOBAL),
            sympy=sympy,
            counterexamples=counterexamples,
            quiz_generations=SingleFlight(),
            mistake_generations=SingleFlight(),
        )
        yield
        warm_up.cancel()
        await asyncio.gather(warm_up, return_exceptions=True)
        sympy.close()
        await engine.dispose()

    # The API schema and its explorer only in demo mode: in production they would map every route for anyone.
    docs = cfg.DEMO_MODE
    app = FastAPI(
        title="Tutor socràtic — Càlcul Diferencial",
        lifespan=lifespan,
        docs_url="/docs" if docs else None,
        redoc_url="/redoc" if docs else None,
        openapi_url="/openapi.json" if docs else None,
    )
    app.add_exception_handler(RequestValidationError, _validation_error)
    app.add_middleware(BodySizeLimit, default=MAX_BODY, by_path=[(PHOTO_ROUTE, MAX_PHOTO_BODY)])
    for module in (
        config_endpoints,
        course_endpoints,
        tutoring_endpoints,
        mistakes_endpoints,
        quiz_endpoints,
        counterexample_endpoints,
    ):
        app.include_router(module.router)

    @app.get("/health", include_in_schema=False)
    async def health() -> dict[str, str]:
        """Liveness for the platform's health check: answers once startup (course, database) has finished."""
        return {"status": "ok"}

    @app.api_route("/", methods=["GET", "HEAD"], include_in_schema=False)  # HEAD: uptime monitors
    async def index() -> FileResponse:
        # Always revalidate the shell page so new asset versions (?v=N) are picked up.
        return FileResponse(FRONTEND_DIR / "index.html", headers={"Cache-Control": "no-cache"})

    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
    app.mount("/pdf", StaticFiles(directory=SOURCES_DIR), name="pdf")
    return app


load_dotenv(ROOT_DIR / ".env")
app = create_app()
