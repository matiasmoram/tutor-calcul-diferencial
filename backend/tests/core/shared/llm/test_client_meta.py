"""A billed but unusable answer (refused, truncated, empty, malformed) carries its call metadata on every provider,
so the call log and the tutor's cost accounting still count its tokens."""

from types import SimpleNamespace
from typing import cast

import anthropic
import openai
import pytest
from anthropic.types import Message
from google import genai
from google.genai import types
from openai.types.chat import ChatCompletion

from core.shared.llm.client import (
    CallMeta,
    LLMError,
    LLMRequest,
    MalformedOutputError,
    Stage,
    StageConfig,
    TruncatedOutputError,
)
from core.shared.llm.infra.anthropic_client import AnthropicLLMClient
from core.shared.llm.infra.gemini_client import GeminiLLMClient
from core.shared.llm.infra.openai_client import OpenAILLMClient
from core.shared.llm.infra.stage_configs import MAX_TOKENS

STAGES = {Stage.DIAGNOSIS: StageConfig(model="m", effort="", max_tokens=3000)}


def _openai(content: str | None, finish_reason: str) -> OpenAILLMClient:
    completion = ChatCompletion.model_validate(
        {
            "id": "c",
            "object": "chat.completion",
            "created": 0,
            "model": "m",
            "choices": [
                {"index": 0, "finish_reason": finish_reason, "message": {"role": "assistant", "content": content}}
            ],
            "usage": {"prompt_tokens": 900, "completion_tokens": 3000, "total_tokens": 3900},
        }
    )

    async def create(**_: object) -> ChatCompletion:
        return completion

    fake = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
    return OpenAILLMClient(STAGES, cast(openai.AsyncOpenAI, fake))


def _anthropic(content: str | None, stop_reason: str) -> AnthropicLLMClient:
    message = Message.model_validate(
        {
            "id": "msg",
            "type": "message",
            "role": "assistant",
            "model": "m",
            "content": [] if content is None else [{"type": "text", "text": content}],
            "stop_reason": stop_reason,
            "stop_sequence": None,
            "usage": {"input_tokens": 400, "output_tokens": 3000, "cache_read_input_tokens": 500},
        }
    )

    async def create(**_: object) -> Message:
        return message

    fake = SimpleNamespace(messages=SimpleNamespace(create=create))
    return AnthropicLLMClient(STAGES, cast(anthropic.AsyncAnthropic, fake))


def _gemini(content: str | None, finish_reason: str) -> GeminiLLMClient:
    response = types.GenerateContentResponse.model_validate(
        {
            "candidates": [
                {
                    "finish_reason": finish_reason,
                    "content": {"role": "model", "parts": [] if content is None else [{"text": content}]},
                }
            ],
            "usage_metadata": {"prompt_token_count": 900, "candidates_token_count": 2000, "thoughts_token_count": 1000},
        }
    )

    async def generate_content(**_: object) -> types.GenerateContentResponse:
        return response

    fake = SimpleNamespace(aio=SimpleNamespace(models=SimpleNamespace(generate_content=generate_content)))
    return GeminiLLMClient(STAGES, cast(genai.Client, fake))


_CASES = {
    "openai": (_openai, {"truncated": "length", "ok": "stop", "refused": "content_filter"}),
    "anthropic": (_anthropic, {"truncated": "max_tokens", "ok": "end_turn", "refused": "refusal"}),
    "gemini": (_gemini, {"truncated": "MAX_TOKENS", "ok": "STOP", "refused": "SAFETY"}),
}


@pytest.mark.parametrize("provider", list(_CASES))
@pytest.mark.parametrize(
    ("content", "finish", "kind"),
    [
        ('{"a":', "truncated", TruncatedOutputError),
        (None, "ok", LLMError),
        ("{not json", "ok", MalformedOutputError),
        ('{"a": "x\\u0000y"}', "ok", MalformedOutputError),
    ],
)
async def test_unusable_answers_carry_their_call_meta(
    provider: str, content: str | None, finish: str, kind: type[LLMError]
) -> None:
    make, finishes = _CASES[provider]
    client = make(content, finishes[finish])
    with pytest.raises(kind) as e:
        await client.structured(Stage.DIAGNOSIS, LLMRequest(system="s", user="u", schema={}))
    meta = e.value.meta
    assert isinstance(meta, CallMeta) and meta.output_tokens == 3000 and meta.input_tokens == 900


@pytest.mark.parametrize("provider", ["anthropic", "gemini"])
async def test_a_refusal_carries_its_call_meta(provider: str) -> None:
    make, finishes = _CASES[provider]
    with pytest.raises(LLMError) as e:
        await make("no", finishes["refused"]).structured(Stage.DIAGNOSIS, LLMRequest(system="s", user="u"))
    assert e.value.meta is not None and e.value.meta.output_tokens == 3000


def test_tutor_stages_are_capped_well_below_the_default() -> None:
    assert MAX_TOKENS[Stage.DIAGNOSIS] <= 3000 and MAX_TOKENS[Stage.REPLY] <= 1500 and MAX_TOKENS[Stage.GUARD] <= 1500
