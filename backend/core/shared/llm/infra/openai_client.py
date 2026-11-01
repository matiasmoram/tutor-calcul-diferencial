from collections.abc import Awaitable, Mapping
from typing import cast

import openai
from loguru import logger
from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat.chat_completion import Choice

from core.shared.domain.clock import Clock, SystemClock
from core.shared.llm.client import (
    CallMeta,
    Image,
    JsonObject,
    LLMClient,
    LLMError,
    LLMQuotaExhaustedError,
    LLMRequest,
    Stage,
    StageConfig,
    TruncatedOutputError,
    billed,
    parse_json,
    plain_text,
)
from core.shared.llm.infra.provider_errors import provider_failure

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class OpenAILLMClient(LLMClient):
    """OpenAI Chat Completions with strict JSON-schema output. Also serves any OpenAI-compatible endpoint."""

    def __init__(
        self,
        stages: Mapping[Stage, StageConfig],
        client: openai.AsyncOpenAI,
        clock: Clock | None = None,
        extra_body: dict[str, object] | None = None,
    ) -> None:
        self._stages = stages
        self._client = client
        self._clock = clock or SystemClock()
        self._extra_body = extra_body

    def model_for(self, stage: Stage) -> str:
        return self._stages[stage].model

    async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
        cfg = self._stages[stage]
        t0 = self._clock.monotonic()
        system = request.system
        if request.schema is not None and "json" not in system.lower():
            # Some providers (e.g. Qwen on OpenRouter) reject JSON mode unless the prompt mentions JSON.
            system += "\n\nRespon només amb un objecte JSON que segueixi l'esquema."
        kwargs: dict[str, object] = {}
        if cfg.effort:  # non-reasoning models reject `reasoning_effort`
            kwargs["reasoning_effort"] = cfg.effort
        if self._extra_body:
            kwargs["extra_body"] = self._extra_body
        if request.schema is not None:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": f"tutor_{stage}", "strict": True, "schema": request.schema},
            }
        user = f"{request.context}\n\n{request.user}" if request.context else request.user  # cached prefix first
        response = await _translated(
            self._client.chat.completions.create(
                model=cfg.model,
                max_completion_tokens=cfg.max_tokens,
                messages=cast(
                    list[ChatCompletionMessageParam],
                    [{"role": "system", "content": system}, {"role": "user", "content": _content(user, request.image)}],
                ),
                **kwargs,  # type: ignore[arg-type]
            )
        )
        usage = response.usage
        details = usage.prompt_tokens_details if usage else None
        meta = CallMeta(
            stage=stage,
            model=cfg.model,
            latency_ms=int((self._clock.monotonic() - t0) * 1000),
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
            cached_tokens=(details.cached_tokens or 0) if details else 0,
        )
        with billed(meta):
            return _output(stage, cfg, request, response.choices[0]), meta


def _output(stage: Stage, cfg: StageConfig, request: LLMRequest, choice: Choice) -> JsonObject:
    if choice.message.refusal:
        raise LLMError(f"{stage}: model refused ({choice.message.refusal})")
    if choice.finish_reason == "length":
        raise TruncatedOutputError(f"{stage}: output truncated at max_tokens={cfg.max_tokens}")
    if not choice.message.content:
        raise LLMError(f"{stage}: empty response (finish_reason={choice.finish_reason})")
    if request.schema is None:
        return plain_text(stage, choice.message.content)
    return parse_json(stage, choice.message.content)


def _content(user: str, image: Image | None) -> str | list[dict[str, object]]:
    if image is None:
        return user
    return [
        {"type": "text", "text": user},
        {"type": "image_url", "image_url": {"url": f"data:{image.media_type};base64,{image.b64()}", "detail": "high"}},
    ]


async def _translated[T](call: Awaitable[T]) -> T:
    try:
        return await call
    except openai.RateLimitError as e:
        if e.code == "insufficient_quota":
            logger.error("LLM quota exhausted, not retrying: {}", e.message)
            raise LLMQuotaExhaustedError(e.message) from e
        raise provider_failure("OpenAI", e.status_code, e.message) from e
    except openai.APIStatusError as e:
        raise provider_failure("OpenAI", e.status_code, e.message) from e
    except openai.APIConnectionError as e:
        raise provider_failure("OpenAI", None, str(e)) from e
