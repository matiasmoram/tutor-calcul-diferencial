"""An exhausted OpenAI quota is its own error, not a rate limit: no retries, generic message, detail kept apart."""

import httpx
import openai
import pytest

from core.shared.llm.client import (
    CallMeta,
    JsonObject,
    LLMClient,
    LLMProviderError,
    LLMQuotaExhaustedError,
    LLMRequest,
    MalformedOutputError,
    Stage,
    StageConfig,
)
from core.shared.llm.infra.openai_client import OpenAILLMClient
from core.shared.llm.infra.retrying_client import RetryingLLMClient

QUOTA = "You exceeded your current quota, please check your plan and billing details."


def _client(code: str, requests: list[httpx.Request], retries: int = 0) -> OpenAILLMClient:
    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        body = {"error": {"message": QUOTA, "type": "insufficient_quota", "code": code}}
        return httpx.Response(429, json=body, headers={"retry-after-ms": "1"})

    sdk = openai.AsyncOpenAI(
        api_key="k", max_retries=retries, http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler))
    )
    return OpenAILLMClient({Stage.REPLY: StageConfig("m", "")}, sdk)


async def test_insufficient_quota_is_a_named_provider_error_with_a_generic_message() -> None:
    requests: list[httpx.Request] = []
    with pytest.raises(LLMQuotaExhaustedError) as e:
        await _client("insufficient_quota", requests).structured(Stage.REPLY, LLMRequest("sys", "user"))
    assert isinstance(e.value, LLMProviderError) and e.value.error_code == 503
    assert "quota" not in e.value.message.lower() and "billing" not in e.value.message.lower()
    assert QUOTA in e.value.detail


async def test_a_plain_rate_limit_stays_a_429_provider_error() -> None:
    with pytest.raises(LLMProviderError) as e:
        await _client("rate_limit_exceeded", []).structured(Stage.REPLY, LLMRequest("sys", "user"))
    assert not isinstance(e.value, LLMQuotaExhaustedError) and e.value.error_code == 429


async def test_the_retrying_client_does_not_ask_again_after_a_quota_error() -> None:
    class Exhausted(LLMClient):
        calls = 0

        def model_for(self, stage: Stage) -> str:
            return "m"

        async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
            self.calls += 1
            raise LLMQuotaExhaustedError(QUOTA)

    inner = Exhausted()
    with pytest.raises(LLMQuotaExhaustedError):
        await RetryingLLMClient(inner, attempts=3).structured(Stage.REPLY, LLMRequest("sys", "user"))
    assert inner.calls == 1
    assert not issubclass(LLMQuotaExhaustedError, MalformedOutputError)


async def test_the_sdk_retry_budget_applies_before_the_mapping() -> None:
    """The SDK retries every 429 itself, quota ones included; the mapping then names the last one."""
    requests: list[httpx.Request] = []
    with pytest.raises(LLMQuotaExhaustedError):
        await _client("insufficient_quota", requests, retries=2).structured(Stage.REPLY, LLMRequest("sys", "user"))
    assert len(requests) == 3  # 1 + max_retries: the SDK spends them, not our client (rejected calls are not billed)
