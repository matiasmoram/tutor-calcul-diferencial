import base64
import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum

from core.shared.domain.exceptions import DomainException

type JsonObject = dict[str, object]


class LLMError(DomainException):
    """Any failed model call: transport, refusal, truncation, invalid JSON. Callers fail closed on it."""

    def __init__(self, message: str, error_code: int = 502) -> None:
        super().__init__(message, error_code)


class LLMProviderError(LLMError):
    """The provider rejected or could not serve the call (bad key 401, rate limit 429, outage 502).
    Clients translate their SDK's exceptions into this, so no other layer depends on an SDK."""


class Stage(StrEnum):
    DIAGNOSIS = "diagnosis"
    REPLY = "reply"
    GUARD = "guard"
    TRANSCRIPTION = "transcription"
    MISTAKES_GENERATION = "mistakes_generation"
    MISTAKES_VERIFICATION = "mistakes_verification"
    MISTAKES_GRADING = "mistakes_grading"
    QUIZ_GENERATION = "quiz_generation"
    QUIZ_VERIFICATION = "quiz_verification"
    QUIZ_AUDIT = "quiz_audit"
    QUIZ_GRADING = "quiz_grading"
    QUIZ_EXTRACTION = "quiz_extraction"


@dataclass
class CallMeta:
    stage: str
    model: str
    latency_ms: int
    input_tokens: int = 0  # total prompt tokens, cached ones included
    output_tokens: int = 0
    cached_tokens: int = 0  # prompt tokens served from the provider's prompt cache


@dataclass(frozen=True)
class Image:
    data: bytes
    media_type: str  # image/jpeg, image/png, image/webp

    def b64(self) -> str:
        return base64.b64encode(self.data).decode("ascii")


@dataclass(frozen=True)
class StageConfig:
    model: str
    effort: str
    max_tokens: int = 16000


@dataclass
class LLMRequest:
    system: str
    user: str
    schema: JsonObject | None = None  # None: plain text, returned as {"text": ...}
    image: Image | None = None
    # Static per-exercise prefix (sheet, theory). Sent before `user` so providers serve it from their prompt cache.
    context: str | None = None
    extra: dict[str, str] = field(default_factory=dict)


class LLMClient(ABC):
    @abstractmethod
    async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
        """Schema-valid JSON for ``request.schema``; with no schema, ``{"text": <prose>}``.

        Prose full of LaTeX is asked for as plain text: forcing it through JSON escaping breaks it on small
        models (``\\delta`` -> carriage return + ``elta``)."""

    @abstractmethod
    def model_for(self, stage: Stage) -> str: ...


# A model that writes "\\frac" unescaped inside a JSON string gets "\f" (form feed) + "rac" back; the same
# happens with \b, \t, \r, and \n before a letter ("\\neq" -> newline + "eq"). These characters never appear
# in legitimate tutor text, so they are mapped back to the LaTeX backslash.
_JSON_ESCAPES = {"\b": "\\b", "\f": "\\f", "\t": "\\t", "\r": "\\r"}


def repair_latex[T](value: T) -> T:
    """Undo JSON-escape damage to LaTeX in every string of a structured output."""
    if isinstance(value, str):
        repaired = value
        for ch, rep in _JSON_ESCAPES.items():
            repaired = repaired.replace(ch, rep)
        # newline directly followed by a LaTeX command name inside $...$, e.g. "\nabla", "\neq", "\nu"
        parts = repaired.split("$")
        for i in range(1, len(parts), 2):
            parts[i] = re.sub(r"\n(?=[a-zA-Z])", r"\\n", parts[i])
        return "$".join(parts)  # type: ignore[return-value]
    if isinstance(value, list):
        return [repair_latex(v) for v in value]  # type: ignore[return-value]
    if isinstance(value, dict):
        return {k: repair_latex(v) for k, v in value.items()}  # type: ignore[return-value]
    return value


def parse_json(stage: str, text: str) -> JsonObject:
    """Invalid JSON from a provider is an LLMError, so every caller's fail-closed path handles it."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise LLMError(f"{stage}: invalid JSON from the model ({e})") from e
    if not isinstance(data, dict):
        raise LLMError(f"{stage}: expected a JSON object, got {type(data).__name__}")
    return repair_latex(data)
