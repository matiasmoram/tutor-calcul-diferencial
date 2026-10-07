import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT_DIR / "backend"


class Config:
    """Process configuration from environment variables. Read only in composition roots (apps/, scripts/, fixtures)."""

    def __init__(self) -> None:
        self.DATABASE_URL: str = (
            os.getenv("DATABASE_URL") or f"sqlite+aiosqlite:///{(ROOT_DIR / 'data' / 'tutor.db').as_posix()}"
        )
        self.LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "anthropic").lower()
        self.TUTOR_MODEL: str | None = os.getenv("TUTOR_MODEL") or None
        self.PROFESSOR_KEY: str | None = os.getenv("TUTOR_CLAU_PROFESSOR") or None
        self.LOG_PROMPTS: bool = os.getenv("TUTOR_LOG_PROMPTS") == "1"
        # Without a professor key, solutions and traces are hidden from everyone unless demo mode is explicit.
        self.DEMO_MODE: bool = os.getenv("TUTOR_DEMO") == "1"
        # Requests per client and minute to the endpoints that call a model (each one costs money).
        self.MODEL_REQUESTS_PER_MINUTE: int = int(os.getenv("TUTOR_MODEL_REQUESTS_PER_MINUTE", "20"))

    def stage_model(self, stage: str) -> str | None:
        return os.getenv(f"TUTOR_MODEL_{stage.upper()}") or None

    def stage_effort(self, stage: str) -> str | None:
        return os.getenv(f"TUTOR_EFFORT_{stage.upper()}") or None

    def api_key(self, name: str) -> str | None:
        return os.getenv(name) or None

    @property
    def async_database_url(self) -> str:
        """The configured URL with an async driver: psycopg serves both modes, plain SQLite gets aiosqlite."""
        url = self.DATABASE_URL
        if url.startswith("sqlite:///"):
            return "sqlite+aiosqlite:///" + url.removeprefix("sqlite:///")
        if url.startswith("postgresql://") or url.startswith("postgres://"):
            return "postgresql+psycopg://" + url.split("://", 1)[1]
        return url
