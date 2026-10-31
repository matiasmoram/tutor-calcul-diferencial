import hmac
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from fastapi import Depends, HTTPException, Request

from apps.tutor_api.rate_limiter import RateLimiter
from core.counterexamples.domain.entities.spec import SpecCatalog
from core.course.domain.entities.course import Course
from core.mistakes.application.mistake_exercise_provider import MistakeGenerations
from core.quizzes.application.quiz_provider import QuizGenerations
from core.shared.domain.exceptions import DomainException
from core.shared.llm.client import LLMClient
from core.shared.math.infra.sympy_pool import SympyCheckPool
from core.shared.storage.session_provider import SQLModelSessionProvider
from settings import Config, api_key_variable


@dataclass
class AppState:
    """Process-wide objects built once by the server's lifespan (the composition root)."""

    config: Config
    sessions: SQLModelSessionProvider
    course: Course
    llm: LLMClient
    limiter: RateLimiter  # per client
    global_limiter: RateLimiter  # all clients together, for the endpoints that pay a model
    sympy: SympyCheckPool  # one long-lived pool of sympy worker processes for the whole server
    counterexamples: SpecCatalog
    quiz_generations: QuizGenerations  # one generation per source and difficulty at a time, process-wide
    mistake_generations: MistakeGenerations  # the same for "Troba l'error" documents


def get_state(request: Request) -> AppState:
    return request.app.state.tutor


def get_config(state: AppState = Depends(get_state)) -> Config:
    return state.config


def get_course(state: AppState = Depends(get_state)) -> Course:
    return state.course


def get_counterexamples(state: AppState = Depends(get_state)) -> SpecCatalog:
    return state.counterexamples


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
        # Bytes, not str: compare_digest rejects a str with non-ASCII characters (a TypeError, a 500 on every route).
        # Starlette decodes headers as latin-1, so encoding back gives the bytes the client sent.
        sent = request.headers.get("X-Clau-Professor", "").encode("latin-1")
        return hmac.compare_digest(sent, config.PROFESSOR_KEY.encode("utf-8"))
    return config.DEMO_MODE


def may_generate(professor: bool = Depends(is_professor), config: Config = Depends(get_config)) -> bool:
    """Whether this request may start a live generation (a document or a quiz): the cost policy TUTOR_GENERACIO."""
    return professor or config.GENERATION_POLICY == "tothom"


def client_key(request: Request) -> str:
    """The address the rate limits count. Behind the platform's proxy, the rightmost X-Forwarded-For hop: the proxy
    appends the address that connected to it, while everything to its left is whatever the client wrote. Read here
    rather than from `request.client`, which is right only if the proxy's own address is in FORWARDED_ALLOW_IPS
    (Dockerfile); otherwise every student would share the proxy's single budget. Without a proxy in front (local
    development), the header is the client's to forge."""
    forwarded = request.headers.get("X-Forwarded-For", "")
    hops = [h.strip() for h in forwarded.split(",") if h.strip()]
    if hops:
        return hops[-1]
    return request.client.host if request.client else "?"


def rate_limited(request: Request, state: AppState = Depends(get_state)) -> None:
    """Per client, for the endpoints that cost something (a model call, sympy workers, a stored row): a client over
    its budget gets a 429 before any cost."""
    if not state.limiter.allow(client_key(request)):
        raise HTTPException(429, "Massa peticions seguides. Espera un minut i torna-ho a provar.")


def model_rate_limited(request: Request, state: AppState = Depends(get_state)) -> None:
    """For the endpoints that call a model: the per-client budget, then the budget of all clients together."""
    rate_limited(request, state)
    if not state.global_limiter.allow("*"):
        raise HTTPException(429, "El tutor està molt ocupat ara mateix. Espera un minut i torna-ho a provar.")


def require_professor(professor: bool = Depends(is_professor)) -> None:
    if not professor:
        raise HTTPException(403, "Només per al professorat.")


def ensure_api_key(config: Config) -> None:
    """Before an action that calls the model: a missing key is a clear 503, not a provider error mid-way. Only a
    local server gets here without one: production refuses to start without it."""
    variable = api_key_variable(config)
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
