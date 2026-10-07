import hmac
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass

from fastapi import Depends, HTTPException, Request

from apps.tutor_api.rate_limiter import RateLimiter
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
    limiter: RateLimiter
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
    """Only requests carrying the professor key see solutions and traces. Demo mode (TUTOR_DEMO=1, no key) shows
    everything; with neither, nobody does: a missing setting in production must not expose the answer keys."""
    if config.PROFESSOR_KEY:
        return hmac.compare_digest(request.headers.get("X-Clau-Professor", ""), config.PROFESSOR_KEY)
    return config.DEMO_MODE


def rate_limited(request: Request, state: AppState = Depends(get_state)) -> None:
    """For the endpoints that call a model: a client over its budget gets a 429 before any cost."""
    client = request.client.host if request.client else "?"
    if not state.limiter.allow(client):
        raise HTTPException(429, "Massa peticions seguides. Espera un minut i torna-ho a provar.")


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
