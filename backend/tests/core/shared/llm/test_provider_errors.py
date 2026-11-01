"""A provider failure reaches the client as a neutral message: never the provider's text (key fragments, URLs)."""

import httpx
import openai
import pytest

from core.shared.llm.client import PROVIDER_BUSY, PROVIDER_UNAVAILABLE, PROVIDER_UNREACHABLE, LLMProviderError
from core.shared.llm.infra.openai_client import _translated

SECRET = "sk-place**lder"


def _status_error(status: int) -> openai.APIStatusError:
    request = httpx.Request("POST", "https://api.openai.com/v1/chat/completions")
    response = httpx.Response(status, request=request, json={"error": {"message": f"Incorrect API key: {SECRET}"}})
    return openai.APIStatusError(f"Incorrect API key provided: {SECRET}", response=response, body=None)


@pytest.mark.parametrize(
    ("status", "message", "code"),
    [(401, PROVIDER_UNAVAILABLE, 503), (500, PROVIDER_UNAVAILABLE, 503), (429, PROVIDER_BUSY, 429)],
)
async def test_provider_status_errors_are_neutral(status: int, message: str, code: int) -> None:
    async def call() -> None:
        raise _status_error(status)

    with pytest.raises(LLMProviderError) as caught:
        await _translated(call())
    assert caught.value.message == message
    assert caught.value.error_code == code
    assert SECRET not in caught.value.message


async def test_an_unreachable_provider_is_a_neutral_502() -> None:
    async def call() -> None:
        raise openai.APIConnectionError(request=httpx.Request("POST", "https://x.invalid"))

    with pytest.raises(LLMProviderError) as caught:
        await _translated(call())
    assert (caught.value.message, caught.value.error_code) == (PROVIDER_UNREACHABLE, 502)
