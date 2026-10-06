from collections.abc import Mapping

import anthropic

from core.shared.domain.clock import Clock, SystemClock
from core.shared.llm.client import (
    CallMeta,
    Image,
    JsonObject,
    LLMClient,
    LLMError,
    LLMRequest,
    Stage,
    StageConfig,
    parse_json,
)


class AnthropicLLMClient(LLMClient):
    def __init__(
        self, stages: Mapping[Stage, StageConfig], client: anthropic.AsyncAnthropic, clock: Clock | None = None
    ) -> None:
        self._stages = stages
        self._client = client
        self._clock = clock or SystemClock()

    def model_for(self, stage: Stage) -> str:
        return self._stages[stage].model

    async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
        cfg = self._stages[stage]
        t0 = self._clock.monotonic()
        output_config: dict[str, object] = {"effort": cfg.effort}
        if request.schema is not None:
            output_config["format"] = {"type": "json_schema", "schema": request.schema}
        response = await self._client.messages.create(
            model=cfg.model,
            max_tokens=cfg.max_tokens,
            system=request.system,
            messages=[{"role": "user", "content": _content(request.user, request.image, request.context)}],  # type: ignore[arg-type]
            output_config=output_config,  # type: ignore[arg-type]
        )
        usage = response.usage
        meta = CallMeta(
            stage=stage,
            model=cfg.model,
            latency_ms=int((self._clock.monotonic() - t0) * 1000),
            input_tokens=usage.input_tokens
            + (usage.cache_read_input_tokens or 0)
            + (usage.cache_creation_input_tokens or 0),
            output_tokens=usage.output_tokens,
            cached_tokens=usage.cache_read_input_tokens or 0,
        )
        if response.stop_reason == "refusal":
            raise LLMError(f"{stage}: model refused")
        if response.stop_reason == "max_tokens":
            raise LLMError(f"{stage}: output truncated at max_tokens={cfg.max_tokens}")
        text = next((b.text for b in response.content if b.type == "text"), None)
        if text is None:
            raise LLMError(f"{stage}: no text block in response (stop_reason={response.stop_reason})")
        if request.schema is None:
            return {"text": text}, meta
        return parse_json(stage, text), meta


def _content(user: str, image: Image | None, context: str | None) -> str | list[dict[str, object]]:
    blocks: list[dict[str, object]] = []
    if image is not None:
        blocks.append(
            {"type": "image", "source": {"type": "base64", "media_type": image.media_type, "data": image.b64()}}
        )
    if context:
        # Explicit breakpoint: system prompt + per-exercise context are cached across the session's turns.
        blocks.append({"type": "text", "text": context, "cache_control": {"type": "ephemeral"}})
    if not blocks:
        return user
    return [*blocks, {"type": "text", "text": user}]
