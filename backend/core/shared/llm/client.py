import base64
import json
import re
from abc import ABC, abstractmethod
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import StrEnum

from core.shared.domain.exceptions import DomainException
from core.shared.domain.model_usage import ModelUsage

type JsonObject = dict[str, object]


class LLMError(DomainException):
    """Any failed model call: transport, refusal, truncation, invalid JSON. Callers fail closed on it."""

    # Set when the provider answered (and billed) before the answer turned out unusable, so the tokens still count.
    meta: "CallMeta | None" = None

    def __init__(self, message: str, error_code: int = 502) -> None:
        super().__init__(message, error_code)


class TruncatedOutputError(LLMError):
    """The model hit the stage's max_tokens before finishing. Asking again for the same output would only be cut
    again: a caller that can split the work asks for less instead."""


class MalformedOutputError(LLMError):
    """The model answered, but the text is unusable: invalid JSON, or characters no text can carry (NUL and other
    control characters, lone surrogates). A sampling glitch, not a provider failure: asking again usually works."""


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

    def usage(self) -> ModelUsage:
        return ModelUsage(
            model=self.model,
            latency_ms=self.latency_ms,
            input_tokens=self.input_tokens,
            output_tokens=self.output_tokens,
            cached_tokens=self.cached_tokens,
        )


@contextmanager
def billed(meta: CallMeta) -> Iterator[None]:
    """Reading an answer the provider already billed: a refused, truncated, empty or malformed answer raises its
    LLMError with ``meta`` attached, so callers still count its tokens."""
    try:
        yield
    except LLMError as e:
        e.meta = meta
        raise


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


# What may remain below U+0020 in model text once repair_latex has run: newlines only. A NUL comes from a corrupted
# escape: the text around it is already broken, and Postgres cannot store it in a text or JSONB column. Lone
# surrogates cannot be encoded as UTF-8 at all.
_UNUSABLE = re.compile("[\x00-\x09\x0b-\x1f\ud800-\udfff]")
# Plain text never went through JSON escaping, so a tab or a carriage return in it is what the model meant (a table,
# a CRLF line end) and Postgres stores both. NUL, the other C0 controls and lone surrogates stay unusable.
_UNUSABLE_PLAIN = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f\ud800-\udfff]")


def _check_text(stage: str, value: object, unusable: re.Pattern[str] = _UNUSABLE) -> None:
    if isinstance(value, str):
        if m := unusable.search(value):
            raise MalformedOutputError(f"{stage}: character U+{ord(m.group()):04X} in the model's output")
    elif isinstance(value, list):
        for v in value:
            _check_text(stage, v, unusable)
    elif isinstance(value, dict):
        for v in value.values():
            _check_text(stage, v, unusable)


def parse_json(stage: str, text: str) -> JsonObject:
    """Invalid JSON from a provider is an LLMError, so every caller's fail-closed path handles it."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise MalformedOutputError(f"{stage}: invalid JSON from the model ({e})") from e
    if not isinstance(data, dict):
        raise MalformedOutputError(f"{stage}: expected a JSON object, got {type(data).__name__}")
    data = repair_latex(data)
    _check_text(stage, data)
    return data


def plain_text(stage: str, text: str) -> JsonObject:
    """A plain-text answer, held to the structured rules except for tab and carriage return: only JSON-escape damage
    makes those suspicious."""
    _check_text(stage, text, _UNUSABLE_PLAIN)
    return {"text": text}
