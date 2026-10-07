"""A hung provider must fail a call in bounded time: every SDK client gets an HTTP timeout and a retry budget."""

import httpx
import pytest
from google import genai
from google.genai import types

from core.shared.llm.client import LLMProviderError, LLMRequest, Stage, StageConfig
from core.shared.llm.infra.factory import MAX_RETRIES, TIMEOUT_S, make_llm_client
from core.shared.llm.infra.gemini_client import GeminiLLMClient
from settings import Config


@pytest.mark.parametrize("provider", ["anthropic", "openai", "openrouter"])
def test_sdk_clients_get_a_timeout_and_a_bounded_retry_budget(monkeypatch: pytest.MonkeyPatch, provider: str) -> None:
    monkeypatch.setenv("LLM_PROVIDER", provider)
    for key in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "OPENROUTER_API_KEY"):
        monkeypatch.setenv(key, "test-key")
    sdk = make_llm_client(Config())._client  # type: ignore[attr-defined]
    assert sdk.timeout == TIMEOUT_S and sdk.max_retries == MAX_RETRIES


def test_the_gemini_client_gets_a_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    sdk = make_llm_client(Config())._client  # type: ignore[attr-defined]
    assert sdk._api_client._http_options.timeout == TIMEOUT_S * 1000  # milliseconds


async def test_a_timed_out_gemini_request_is_not_retried() -> None:
    """Its retry loop is for rate limits and overload: retrying a request that already spent the whole timeout
    would multiply the wait."""
    requests: list[httpx.Request] = []

    def hung(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        raise httpx.ReadTimeout("timed out", request=request)

    http = httpx.AsyncClient(transport=httpx.MockTransport(hung))
    sdk = genai.Client(api_key="test-key", http_options=types.HttpOptions(timeout=1000, httpx_async_client=http))
    client = GeminiLLMClient({Stage.REPLY: StageConfig("gemini-test", "low")}, sdk)
    with pytest.raises(LLMProviderError):
        await client.structured(Stage.REPLY, LLMRequest("sys", "user"))
    assert len(requests) == 1
