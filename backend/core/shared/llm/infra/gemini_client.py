import asyncio
from collections.abc import Mapping

import httpx
from google import genai
from google.genai import errors, types

from core.shared.domain.clock import Clock, SystemClock
from core.shared.llm.client import (
    CallMeta,
    JsonObject,
    LLMClient,
    LLMError,
    LLMRequest,
    Stage,
    StageConfig,
    TruncatedOutputError,
    billed,
    parse_json,
    plain_text,
)
from core.shared.llm.infra.provider_errors import provider_failure

# Anthropic-style effort names mapped onto Gemini thinking levels.
THINKING: Mapping[str, types.ThinkingLevel] = {
    "low": types.ThinkingLevel.LOW,
    "medium": types.ThinkingLevel.MEDIUM,
    "high": types.ThinkingLevel.HIGH,
}
MAX_WAIT_S = 90  # total time spent waiting on rate limits / overload per call


class GeminiLLMClient(LLMClient):
    def __init__(self, stages: Mapping[Stage, StageConfig], client: genai.Client, clock: Clock | None = None) -> None:
        self._stages = stages
        self._client = client
        self._clock = clock or SystemClock()

    def model_for(self, stage: Stage) -> str:
        return self._stages[stage].model

    async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
        cfg = self._stages[stage]
        t0 = self._clock.monotonic()
        text = f"{request.context}\n\n{request.user}" if request.context else request.user  # cached prefix first
        image = request.image
        contents: list[types.Part | str] | str = (
            [types.Part.from_bytes(data=image.data, mime_type=image.media_type), text] if image else text
        )
        schema_args: dict[str, object] = (
            {"response_mime_type": "application/json", "response_json_schema": request.schema}
            if request.schema is not None
            else {}
        )
        config = types.GenerateContentConfig(
            system_instruction=request.system,
            max_output_tokens=cfg.max_tokens,
            thinking_config=types.ThinkingConfig(thinking_level=THINKING.get(cfg.effort, types.ThinkingLevel.LOW)),
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            **schema_args,  # type: ignore[arg-type]
        )
        try:
            response = await self._generate_with_retry(cfg.model, contents, config)
        except errors.APIError as e:
            raise provider_failure("Gemini", e.code, e.message or "") from e
        except httpx.TransportError as e:
            raise provider_failure("Gemini", None, str(e)) from e
        usage = response.usage_metadata
        meta = CallMeta(
            stage=stage,
            model=cfg.model,
            latency_ms=int((self._clock.monotonic() - t0) * 1000),
            input_tokens=(usage.prompt_token_count or 0) if usage else 0,
            output_tokens=((usage.candidates_token_count or 0) + (usage.thoughts_token_count or 0)) if usage else 0,
            cached_tokens=(usage.cached_content_token_count or 0) if usage else 0,
        )
        with billed(meta):
            if not response.candidates:
                raise LLMError(f"{stage}: no candidates (prompt_feedback={response.prompt_feedback})")
            finish = response.candidates[0].finish_reason
            if finish is not None and finish.name == "MAX_TOKENS":
                raise TruncatedOutputError(f"{stage}: output truncated at max_tokens={cfg.max_tokens}")
            if finish is not None and finish.name != "STOP":
                raise LLMError(f"{stage}: generation stopped ({finish.name})")
            if not response.text:
                raise LLMError(f"{stage}: empty response")
            if request.schema is None:
                return plain_text(stage, response.text), meta
            return parse_json(stage, response.text), meta

    async def _generate_with_retry(
        self, model: str, contents: list[types.Part | str] | str, config: types.GenerateContentConfig
    ) -> types.GenerateContentResponse:
        """Free-tier keys hit per-minute quotas (429) and transient overload (503): wait and retry.
        A request that timed out is not retried: it already spent the whole HTTP timeout."""
        waited = 0.0
        while True:
            try:
                return await self._client.aio.models.generate_content(model=model, contents=contents, config=config)  # type: ignore[arg-type]
            except httpx.TimeoutException:
                raise
            except (errors.APIError, httpx.TransportError) as e:
                if isinstance(e, errors.APIError) and (e.code not in (429, 503) or _is_daily_quota(e)):
                    raise
                delay = (_retry_delay(e) if isinstance(e, errors.APIError) else None) or 5.0
                if waited + delay > MAX_WAIT_S:
                    raise
                await asyncio.sleep(delay)
                waited += delay


def _error_details(err: errors.APIError) -> list[dict[str, object]]:
    details = err.details
    if not isinstance(details, dict):
        return []
    found = details.get("error", {}).get("details", [])
    return found if isinstance(found, list) else []


def _retry_delay(err: errors.APIError) -> float | None:
    """Read google.rpc.RetryInfo.retryDelay (e.g. '11s', '0.95s') from a Gemini error."""
    for d in _error_details(err):
        delay = d.get("retryDelay")
        if str(d.get("@type", "")).endswith("RetryInfo") and isinstance(delay, str):
            return float(delay.rstrip("s")) + 1.0
    return None


def _is_daily_quota(err: errors.APIError) -> bool:
    """Per-day quotas reset tomorrow: waiting a few seconds won't help."""
    for d in _error_details(err):
        violations = d.get("violations", [])
        if isinstance(violations, list) and any("PerDay" in str(v.get("quotaId", "")) for v in violations):
            return True
    return False
