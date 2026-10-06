"""The tutor's HTTP API and static frontend. Composition root: the only place that builds concretes."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from apps.tutor_api.dependencies import AppState
from apps.tutor_api.endpoints import config as config_endpoints
from apps.tutor_api.endpoints import course as course_endpoints
from core.course.application.course_loader import CourseLoader
from core.course.infra.sqlmodel_repository import SQLModelCourseRepository
from core.course.infra.yaml_course_source import YamlCourseSource
from core.shared.llm.client import LLMClient
from core.shared.llm.infra.factory import make_llm_client
from core.shared.llm.infra.logged_client import LoggedLLMClient
from core.shared.llm_calls.infra.sqlmodel_repository import SQLModelLLMCallRepository
from core.shared.storage.session_provider import SQLModelSessionProvider, create_schema_if_sqlite, make_engine
from core.shared.storage.table_registry import register_all_tables
from settings import BACKEND_DIR, ROOT_DIR, Config

FRONTEND_DIR = ROOT_DIR / "frontend"
SOURCES_DIR = ROOT_DIR / "sources"


def create_app(config: Config | None = None, llm: LLMClient | None = None) -> FastAPI:
    """`llm` replaces the configured provider (tests pass the scripted fake); every call is still logged."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        cfg = config or Config()
        engine = make_engine(cfg.async_database_url)
        register_all_tables()
        await create_schema_if_sqlite(engine)
        sessions = SQLModelSessionProvider(engine)
        source = YamlCourseSource(BACKEND_DIR / "exercicis", BACKEND_DIR / "teoria")
        course = await CourseLoader(SQLModelCourseRepository(sessions), source).load()
        inner = llm or make_llm_client(cfg)
        logged = LoggedLLMClient(inner, SQLModelLLMCallRepository(sessions), log_prompts=cfg.LOG_PROMPTS)
        app.state.tutor = AppState(config=cfg, sessions=sessions, course=course, llm=logged)
        yield
        await engine.dispose()

    app = FastAPI(title="Tutor socràtic — Càlcul Diferencial", lifespan=lifespan)
    for module in (config_endpoints, course_endpoints):
        app.include_router(module.router)

    @app.get("/", include_in_schema=False)
    async def index() -> FileResponse:
        # Always revalidate the shell page so new asset versions (?v=N) are picked up.
        return FileResponse(FRONTEND_DIR / "index.html", headers={"Cache-Control": "no-cache"})

    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
    app.mount("/pdf", StaticFiles(directory=SOURCES_DIR), name="pdf")
    return app


load_dotenv(ROOT_DIR / ".env")
app = create_app()
