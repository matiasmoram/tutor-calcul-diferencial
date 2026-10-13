"""The tutor's HTTP API and static frontend. Composition root: the only place that builds concretes."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from apps.tutor_api.dependencies import AppState
from apps.tutor_api.endpoints import config as config_endpoints
from apps.tutor_api.endpoints import counterexamples as counterexample_endpoints
from apps.tutor_api.endpoints import course as course_endpoints
from apps.tutor_api.endpoints import mistakes as mistakes_endpoints
from apps.tutor_api.endpoints import quizzes as quiz_endpoints
from apps.tutor_api.endpoints import tutoring as tutoring_endpoints
from apps.tutor_api.rate_limiter import RateLimiter
from core.counterexamples.infra.yaml_spec_source import YamlSpecSource
from core.course.infra.yaml_course_source import YamlCourseSource
from core.mistakes.application.pregenerated_importer import PregeneratedImporter
from core.mistakes.infra.json_file_source import JsonFileMistakeSource
from core.mistakes.infra.sqlmodel_repository import SQLModelMistakeExerciseRepository
from core.quizzes.application.pregenerated_importer import PregeneratedImporter as QuizImporter
from core.quizzes.infra.json_quiz_files import JsonQuizFiles
from core.quizzes.infra.sqlmodel_repository import SQLModelQuizRepository
from core.shared.llm.client import LLMClient
from core.shared.llm.infra.factory import make_llm_client
from core.shared.llm.infra.logged_client import LoggedLLMClient
from core.shared.llm_calls.infra.sqlmodel_repository import SQLModelLLMCallRepository
from core.shared.math.infra.sympy_pool import SympyCheckPool
from core.shared.storage.session_provider import SQLModelSessionProvider, create_schema_if_sqlite, make_engine
from core.shared.storage.table_registry import register_all_tables
from settings import BACKEND_DIR, ROOT_DIR, Config

FRONTEND_DIR = ROOT_DIR / "frontend"
SOURCES_DIR = ROOT_DIR / "sources"


async def _seed_generated(sessions: SQLModelSessionProvider) -> None:
    """Pre-generated documents and quizzes (backend/generats) seed the generated-content tables.

    Only when the database has fewer than the files (a first start, or a deploy that added files): the import is
    idempotent but costs a round-trip per document. Assumes one server process (the Dockerfile runs one worker);
    with several, run `scripts/db.py import-generats` as a deploy step instead."""
    generated = BACKEND_DIR / "generats"
    mistakes = SQLModelMistakeExerciseRepository(sessions)
    stored = sum(n for by_difficulty in (await mistakes.ready_counts()).values() for n in by_difficulty.values())
    if stored < len(list((generated / "errades").glob("*/*/*.json"))):
        await PregeneratedImporter(JsonFileMistakeSource(generated / "errades"), mistakes).import_all()
    quizzes = SQLModelQuizRepository(sessions)
    stored = sum(n for by_difficulty in (await quizzes.availability()).values() for n in by_difficulty.values())
    if stored < len(list((generated / "afirmacions").glob("*/*/*.json"))):
        await QuizImporter(JsonQuizFiles(generated / "afirmacions"), quizzes).import_all()


def create_app(config: Config | None = None, llm: LLMClient | None = None) -> FastAPI:
    """`llm` replaces the configured provider (tests pass the scripted fake); every call is still logged."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        cfg = config or Config()
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
        limiter = RateLimiter(cfg.MODEL_REQUESTS_PER_MINUTE)
        sympy = SympyCheckPool(max_workers=2)  # workers start lazily, on the first check
        app.state.tutor = AppState(
            config=cfg,
            sessions=sessions,
            course=course,
            llm=logged,
            limiter=limiter,
            sympy=sympy,
            counterexamples=counterexamples,
        )
        yield
        sympy.close()
        await engine.dispose()

    app = FastAPI(title="Tutor socràtic — Càlcul Diferencial", lifespan=lifespan)
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

    @app.get("/", include_in_schema=False)
    async def index() -> FileResponse:
        # Always revalidate the shell page so new asset versions (?v=N) are picked up.
        return FileResponse(FRONTEND_DIR / "index.html", headers={"Cache-Control": "no-cache"})

    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
    app.mount("/pdf", StaticFiles(directory=SOURCES_DIR), name="pdf")
    return app


load_dotenv(ROOT_DIR / ".env")
app = create_app()
