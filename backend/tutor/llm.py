"""Thin wrappers over the LLM providers: every call returns schema-valid JSON, optionally reading one image."""

from __future__ import annotations

import base64
import json
import os
import re
import time
from dataclasses import dataclass, field
from typing import Protocol

import anthropic
import httpx


class LLMError(RuntimeError):
    pass


@dataclass
class CallMeta:
    stage: str
    model: str
    latency_ms: int
    input_tokens: int = 0  # total prompt tokens, cached ones included
    output_tokens: int = 0
    cached_tokens: int = 0  # prompt tokens served from the provider's prompt cache
    extra: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Imatge:
    data: bytes
    media_type: str  # image/jpeg, image/png, image/webp

    def b64(self) -> str:
        return base64.b64encode(self.data).decode("ascii")


# A model that writes "\\frac" unescaped inside a JSON string gets "\f" (form feed) + "rac" back; the same
# happens with \b, \t, \r, and \n before a letter ("\\neq" -> newline + "eq"). These characters never appear
# in legitimate tutor text, so they are mapped back to the LaTeX backslash.
_JSON_ESCAPES = {"\b": "\\b", "\f": "\\f", "\t": "\\t", "\r": "\\r"}


def repair_latex(value):
    """Undo JSON-escape damage to LaTeX in every string of a structured output."""
    if isinstance(value, str):
        for ch, rep in _JSON_ESCAPES.items():
            value = value.replace(ch, rep)
        # newline directly followed by a LaTeX command name inside $...$, e.g. "\nabla", "\neq", "\nu"
        parts = value.split("$")
        for i in range(1, len(parts), 2):
            parts[i] = re.sub(r"\n(?=[a-zA-Z])", r"\\n", parts[i])
        return "$".join(parts)
    if isinstance(value, list):
        return [repair_latex(v) for v in value]
    if isinstance(value, dict):
        return {k: repair_latex(v) for k, v in value.items()}
    return value


def _parse(stage: str, text: str) -> dict:
    """Invalid JSON from a provider is an LLMError, so every caller's fail-closed path handles it."""
    try:
        return repair_latex(json.loads(text))
    except json.JSONDecodeError as e:
        raise LLMError(f"{stage}: invalid JSON from the model ({e})") from e


class StructuredLLM(Protocol):
    def structured(
        self, stage: str, system: str, user: str, schema: dict, image: Imatge | None = None, context: str | None = None
    ) -> tuple[dict, CallMeta]:
        """`schema=None` asks for plain text and returns {"text": ...}: prose full of LaTeX is not forced through
        JSON escaping, which small models get wrong (\\delta -> \\r + "elta").
        `context` is the static per-exercise prefix (sheet, theory). It goes before `user` so that
        providers can serve it from their prompt cache on every later turn of the session."""
        ...


@dataclass
class StageConfig:
    model: str
    effort: str
    max_tokens: int = 16000


DEFAULT_MODELS = {
    "anthropic": "claude-opus-5-5",
    "gemini": "gemini-3.5-flash",
    "openai": "gpt-5.5",
    "openrouter": "openai/gpt-oss-20b",
}
# Free-tier Gemini quotas are per model: spreading stages over models triples throughput.
GEMINI_STAGE_MODELS = {
    "diagnosi": "gemini-3.5-flash",
    "resposta": "gemini-3.5-flash-lite",
    "guardia": "gemini-3-flash-preview",
    "transcripcio": "gemini-3.5-flash",
    "afirmacions_generacio": "gemini-3.5-flash",
    "afirmacions_verificacio": "gemini-3-flash-preview",
    "afirmacions_auditoria": "gemini-3.5-flash-lite",
    "afirmacions_correccio": "gemini-3-flash-preview",
}
# Diagnosis needs the strongest judgment; phrasing and checking run on a faster model.
OPENAI_STAGE_MODELS = {
    "diagnosi": "gpt-5.5",
    "resposta": "gpt-5.4-mini",
    "guardia": "gpt-5.4-mini",
    "transcripcio": "gpt-5.5",
    "errades_generacio": "gpt-5.5",
    "errades_verificacio": "gpt-5.5",
    "errades_correccio": "gpt-5.5",
    "afirmacions_generacio": "gpt-5.5",
    "afirmacions_verificacio": "gpt-5.5",
    "afirmacions_auditoria": "gpt-5.5",
    "afirmacions_correccio": "gpt-5.5",
}
STAGE_MODELS = {"gemini": GEMINI_STAGE_MODELS, "openai": OPENAI_STAGE_MODELS}


def provider() -> str:
    return os.getenv("LLM_PROVIDER", "anthropic").lower()


def default_stage_configs() -> dict[str, StageConfig]:
    base = os.getenv("TUTOR_MODEL")

    def model(stage: str) -> str:
        default = base or STAGE_MODELS.get(provider(), {}).get(stage, DEFAULT_MODELS[provider()])
        return os.getenv(f"TUTOR_MODEL_{stage.upper()}", default)

    return {
        "diagnosi": StageConfig(model("diagnosi"), os.getenv("TUTOR_EFFORT_DIAGNOSI", "medium")),
        "resposta": StageConfig(model("resposta"), os.getenv("TUTOR_EFFORT_RESPOSTA", "low")),
        "guardia": StageConfig(model("guardia"), os.getenv("TUTOR_EFFORT_GUARDIA", "low")),
        # Handwriting OCR: reading maths reliably needs a strong vision model, not deep reasoning.
        "transcripcio": StageConfig(model("transcripcio"), os.getenv("TUTOR_EFFORT_TRANSCRIPCIO", "low")),
        # "Find the error" mode: writing plausible, subtle errors and checking them both need real reasoning.
        "errades_generacio": StageConfig(model("errades_generacio"), os.getenv("TUTOR_EFFORT_ERRADES_GENERACIO", "medium")),
        "errades_verificacio": StageConfig(model("errades_verificacio"), os.getenv("TUTOR_EFFORT_ERRADES_VERIFICACIO", "medium")),
        "errades_correccio": StageConfig(model("errades_correccio"), os.getenv("TUTOR_EFFORT_ERRADES_CORRECCIO", "low")),
        # "Cert o fals" mode: generated in batches of a few statements; the blind solver must really reason.
        # 20000 is the most Anthropic accepts without streaming.
        "afirmacions_generacio": StageConfig(
            model("afirmacions_generacio"), os.getenv("TUTOR_EFFORT_AFIRMACIONS_GENERACIO", "medium"), max_tokens=20000
        ),
        "afirmacions_verificacio": StageConfig(
            model("afirmacions_verificacio"), os.getenv("TUTOR_EFFORT_AFIRMACIONS_VERIFICACIO", "medium"), max_tokens=20000
        ),
        "afirmacions_auditoria": StageConfig(
            model("afirmacions_auditoria"), os.getenv("TUTOR_EFFORT_AFIRMACIONS_AUDITORIA", "medium"), max_tokens=20000
        ),
        "afirmacions_correccio": StageConfig(
            model("afirmacions_correccio"), os.getenv("TUTOR_EFFORT_AFIRMACIONS_CORRECCIO", "low"), max_tokens=20000
        ),
    }


class AnthropicLLM:
    def __init__(self, stages: dict[str, StageConfig] | None = None, client: anthropic.Anthropic | None = None):
        self.client = client or anthropic.Anthropic()
        self.stages = stages or default_stage_configs()

    def structured(
        self, stage: str, system: str, user: str, schema: dict, image: Imatge | None = None, context: str | None = None
    ) -> tuple[dict, CallMeta]:
        cfg = self.stages[stage]
        t0 = time.perf_counter()
        response = self.client.messages.create(
            model=cfg.model,
            max_tokens=cfg.max_tokens,
            system=system,
            messages=[{"role": "user", "content": _anthropic_content(user, image, context)}],
            output_config={"effort": cfg.effort}
            | ({"format": {"type": "json_schema", "schema": schema}} if schema is not None else {}),
        )
        meta = CallMeta(
            stage=stage,
            model=cfg.model,
            latency_ms=int((time.perf_counter() - t0) * 1000),
            input_tokens=response.usage.input_tokens
            + (response.usage.cache_read_input_tokens or 0)
            + (response.usage.cache_creation_input_tokens or 0),
            output_tokens=response.usage.output_tokens,
            cached_tokens=response.usage.cache_read_input_tokens or 0,
        )
        if response.stop_reason == "refusal":
            details = getattr(response, "stop_details", None)
            raise LLMError(f"{stage}: model refused ({getattr(details, 'category', None)})")
        if response.stop_reason == "max_tokens":
            raise LLMError(f"{stage}: output truncated at max_tokens={cfg.max_tokens}")
        text = next((b.text for b in response.content if b.type == "text"), None)
        if text is None:
            raise LLMError(f"{stage}: no text block in response (stop_reason={response.stop_reason})")
        if schema is None:
            return {"text": text}, meta
        return _parse(stage, text), meta


class GeminiLLM:
    """Same contract as AnthropicLLM, over the Gemini API (google-genai SDK)."""

    # Anthropic-style effort names mapped onto Gemini thinking levels.
    THINKING = {"low": "low", "medium": "medium", "high": "high"}

    def __init__(self, stages: dict[str, StageConfig] | None = None, client=None):
        from google import genai

        self.client = client or genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.stages = stages or default_stage_configs()

    MAX_WAIT_S = 90  # total time spent waiting on rate limits / overload per call

    def _generate_with_retry(self, model: str, contents, config):
        """Free-tier keys hit per-minute quotas (429) and transient overload (503): wait and retry."""
        from google.genai import errors

        waited = 0.0
        while True:
            try:
                return self.client.models.generate_content(model=model, contents=contents, config=config)
            except (errors.APIError, httpx.TransportError) as e:
                if isinstance(e, errors.APIError) and (e.code not in (429, 503) or _is_daily_quota(e)):
                    raise
                delay = (_retry_delay(e) if isinstance(e, errors.APIError) else None) or 5.0
                if waited + delay > self.MAX_WAIT_S:
                    raise
                time.sleep(delay)
                waited += delay

    def structured(
        self, stage: str, system: str, user: str, schema: dict, image: Imatge | None = None, context: str | None = None
    ) -> tuple[dict, CallMeta]:
        from google.genai import types

        cfg = self.stages[stage]
        t0 = time.perf_counter()
        text = _with_context(user, context)
        contents = [types.Part.from_bytes(data=image.data, mime_type=image.media_type), text] if image else text
        response = self._generate_with_retry(
            cfg.model,
            contents,
            types.GenerateContentConfig(
                system_instruction=system,
                max_output_tokens=cfg.max_tokens,
                **({"response_mime_type": "application/json", "response_json_schema": schema} if schema is not None else {}),
                thinking_config=types.ThinkingConfig(thinking_level=self.THINKING.get(cfg.effort, "low")),
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            ),
        )
        usage = response.usage_metadata
        meta = CallMeta(
            stage=stage,
            model=cfg.model,
            latency_ms=int((time.perf_counter() - t0) * 1000),
            input_tokens=(usage.prompt_token_count or 0) if usage else 0,
            output_tokens=((usage.candidates_token_count or 0) + (usage.thoughts_token_count or 0)) if usage else 0,
            cached_tokens=(usage.cached_content_token_count or 0) if usage else 0,
        )
        if not response.candidates:
            raise LLMError(f"{stage}: no candidates (prompt_feedback={response.prompt_feedback})")
        finish = response.candidates[0].finish_reason
        if finish is not None and finish.name == "MAX_TOKENS":
            raise LLMError(f"{stage}: output truncated at max_tokens={cfg.max_tokens}")
        if finish is not None and finish.name != "STOP":
            raise LLMError(f"{stage}: generation stopped ({finish.name})")
        if not response.text:
            raise LLMError(f"{stage}: empty response")
        if schema is None:
            return {"text": response.text}, meta
        return _parse(stage, response.text), meta


def _retry_delay(err) -> float | None:
    """Read google.rpc.RetryInfo.retryDelay (e.g. '11s', '0.95s') from a Gemini error."""
    details = (err.details or {}).get("error", {}).get("details", []) if isinstance(err.details, dict) else []
    for d in details:
        if d.get("@type", "").endswith("RetryInfo") and d.get("retryDelay"):
            return float(d["retryDelay"].rstrip("s")) + 1.0
    return None


def _is_daily_quota(err) -> bool:
    """Per-day quotas reset tomorrow: waiting a few seconds won't help."""
    details = (err.details or {}).get("error", {}).get("details", []) if isinstance(err.details, dict) else []
    return any("PerDay" in v.get("quotaId", "") for d in details for v in d.get("violations", []))


class OpenAILLM:
    """Same contract, over the OpenAI Chat Completions API with strict JSON-schema output."""

    def __init__(self, stages: dict[str, StageConfig] | None = None, client=None):
        import openai

        self.client = client or openai.OpenAI(timeout=180, max_retries=2)  # a hung provider must not block a turn forever
        self.stages = stages or default_stage_configs()

    def extra_args(self) -> dict:
        return {}

    def structured(
        self, stage: str, system: str, user: str, schema: dict, image: Imatge | None = None, context: str | None = None
    ) -> tuple[dict, CallMeta]:
        cfg = self.stages[stage]
        t0 = time.perf_counter()
        # Non-reasoning models reject `reasoning_effort`: an empty effort leaves it out.
        effort = {"reasoning_effort": cfg.effort} if cfg.effort else {}
        if schema is not None and "json" not in system.lower():
            # Some providers (e.g. Qwen on OpenRouter) reject JSON mode unless the prompt mentions JSON.
            system += "\n\nRespon només amb un objecte JSON que segueixi l'esquema."
        response = self.client.chat.completions.create(
            model=cfg.model,
            max_completion_tokens=cfg.max_tokens,
            **effort,
            **self.extra_args(),
            messages=[{"role": "system", "content": system}, {"role": "user", "content": _openai_content(_with_context(user, context), image)}],
            **(
                {"response_format": {
                    "type": "json_schema",
                    "json_schema": {"name": f"tutor_{stage}", "strict": True, "schema": schema},
                }}
                if schema is not None
                else {}
            ),
        )
        usage = response.usage
        meta = CallMeta(
            stage=stage,
            model=cfg.model,
            latency_ms=int((time.perf_counter() - t0) * 1000),
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
            cached_tokens=(getattr(usage.prompt_tokens_details, "cached_tokens", 0) or 0) if usage else 0,
        )
        choice = response.choices[0]
        if choice.message.refusal:
            raise LLMError(f"{stage}: model refused ({choice.message.refusal})")
        if choice.finish_reason == "length":
            raise LLMError(f"{stage}: output truncated at max_tokens={cfg.max_tokens}")
        if not choice.message.content:
            raise LLMError(f"{stage}: empty response (finish_reason={choice.finish_reason})")
        if schema is None:
            return {"text": choice.message.content}, meta
        return _parse(stage, choice.message.content), meta


def _with_context(user: str, context: str | None) -> str:
    """OpenAI and Gemini cache identical prompt prefixes automatically: the static context goes first."""
    return f"{context}\n\n{user}" if context else user


def _anthropic_content(user: str, image: Imatge | None, context: str | None = None):
    blocks: list[dict] = []
    if image is not None:
        blocks.append({"type": "image", "source": {"type": "base64", "media_type": image.media_type, "data": image.b64()}})
    if context:
        # Explicit breakpoint: system prompt + per-exercise context are cached across the session's turns.
        blocks.append({"type": "text", "text": context, "cache_control": {"type": "ephemeral"}})
    if not blocks:
        return user
    return blocks + [{"type": "text", "text": user}]


def _openai_content(user: str, image: Imatge | None):
    if image is None:
        return user
    return [
        {"type": "text", "text": user},
        {"type": "image_url", "image_url": {"url": f"data:{image.media_type};base64,{image.b64()}", "detail": "high"}},
    ]


class OpenRouterLLM(OpenAILLM):
    """Any OpenRouter model through its OpenAI-compatible API (OPENROUTER_API_KEY). Model ids like 'openai/gpt-oss-20b'."""

    def __init__(self, stages: dict[str, StageConfig] | None = None, client=None, api_key: str | None = None):
        import openai

        client = client or openai.OpenAI(
            base_url="https://openrouter.ai/api/v1", api_key=api_key or os.getenv("OPENROUTER_API_KEY"),
            timeout=180, max_retries=2,
        )
        super().__init__(stages, client)

    def extra_args(self) -> dict:
        # Only route to providers that honour every parameter sent (the JSON schema, when there is one).
        return {"extra_body": {"provider": {"require_parameters": True}}}


class StageRouter:
    """Sends each stage to its own backend, so stages can mix providers (e.g. a strong diagnosis, a tiny reply)."""

    def __init__(self, routes: dict[str, StructuredLLM]):
        self.routes = routes

    def structured(self, stage: str, *args, **kwargs) -> tuple[dict, CallMeta]:
        return self.routes[stage].structured(stage, *args, **kwargs)


def make_llm() -> StructuredLLM:
    return {"gemini": GeminiLLM, "openai": OpenAILLM, "openrouter": OpenRouterLLM}.get(provider(), AnthropicLLM)()
