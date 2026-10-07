from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass

from fastapi import Depends, HTTPException, Request

from core.course.domain.entities.course import Course
from core.shared.domain.exceptions import DomainException
from core.shared.llm.client import LLMClient
from core.shared.math.infra.sympy_pool import SympyCheckPool
from core.shared.storage.session_provider import SQLModelSessionProvider
from settings import Config


@dataclass
class AppState:
    """Process-wide objects built once by the server's lifespan (the composition root)."""

    config: Config
    sessions: SQLModelSessionProvider
    course: Course
    llm: LLMClient
    sympy: SympyCheckPool  # one long-lived pool of sympy worker processes for the whole server


def get_state(request: Request) -> AppState:
    return request.app.state.tutor


def get_config(state: AppState = Depends(get_state)) -> Config:
    return state.config


def get_course(state: AppState = Depends(get_state)) -> Course:
    return state.course


def get_session_provider(state: AppState = Depends(get_state)) -> SQLModelSessionProvider:
    return state.sessions


def get_llm(state: AppState = Depends(get_state)) -> LLMClient:
    return state.llm


def get_sympy_pool(state: AppState = Depends(get_state)) -> SympyCheckPool:
    return state.sympy


def is_professor(request: Request, config: Config = Depends(get_config)) -> bool:
    """With a professor key configured, only requests carrying it see solutions and traces.
    Without it the app runs in demo mode (everything visible)."""
    return not config.PROFESSOR_KEY or request.headers.get("X-Clau-Professor") == config.PROFESSOR_KEY


def require_professor(professor: bool = Depends(is_professor)) -> None:
    if not professor:
        raise HTTPException(403, "Només per al professorat.")


KEY_VARIABLES: Mapping[str, str] = {
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "openai": "OPENAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
}


def ensure_api_key(config: Config) -> None:
    """Before an action that calls the model: a missing key is a clear 503, not a provider error mid-way."""
    variable = KEY_VARIABLES.get(config.LLM_PROVIDER, "ANTHROPIC_API_KEY")
    if not config.api_key(variable):
        raise HTTPException(503, f"Falta la clau d'API: posa {variable} al fitxer .env i reinicia el servidor.")


@contextmanager
def domain_errors(action: str | None = None) -> Iterator[None]:
    """Translates a domain exception into its HTTP status. `action` prefixes model failures ("La diagnosi")."""
    try:
        yield
    except DomainException as exc:
        detail = f"{action} ha fallat: {exc.message}" if action and exc.error_code == 502 else exc.message
        raise HTTPException(status_code=exc.error_code, detail=detail) from exc
