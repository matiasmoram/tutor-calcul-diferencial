import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT_DIR / "backend"
GENERATION_POLICIES = ("professor", "tothom")


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
        # The same, all clients together: a second line when many addresses share the budget (or fake one).
        self.MODEL_REQUESTS_PER_MINUTE_GLOBAL: int = int(os.getenv("TUTOR_MODEL_REQUESTS_PER_MINUTE_GLOBAL", "150"))
        # Who may start a live generation of a "Troba l'error" document or a "Cert o fals" quiz (minutes and
        # cents each): "professor" (default; students get the stored ones) or "tothom".
        self.GENERATION_POLICY: str = os.getenv("TUTOR_GENERACIO", "professor").lower()
        if self.GENERATION_POLICY not in GENERATION_POLICIES:
            raise ValueError(f"TUTOR_GENERACIO={self.GENERATION_POLICY!r}: must be one of {GENERATION_POLICIES}")
        # Upper bound of one quiz generation, in seconds.
        self.QUIZ_GENERATION_DEADLINE_S: float = float(os.getenv("TUTOR_QUIZ_GENERATION_DEADLINE_S", "420"))
        # Upper bound of one "Troba l'error" document generation (every attempt and verification), in seconds.
        self.MISTAKES_GENERATION_DEADLINE_S: float = float(os.getenv("TUTOR_MISTAKES_GENERATION_DEADLINE_S", "300"))
        # sympy worker processes (~70 MB each idle, capped by TUTOR_SYMPY_WORKER_MEMORY_MB): 1 fits a 512 MB instance.
        self.SYMPY_WORKERS: int = int(os.getenv("TUTOR_SYMPY_WORKERS", "1"))
        # Decide every authored counterexample at start-up so their verdicts are cached. Off by default: on a 0.1 CPU
        # instance that sleeps when idle it costs minutes of CPU on every wake, competing with the first students.
        self.SYMPY_WARM_CACHE: bool = os.getenv("TUTOR_SYMPY_WARM_CACHE", "0") == "1"

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
