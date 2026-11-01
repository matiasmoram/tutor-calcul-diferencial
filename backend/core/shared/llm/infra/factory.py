"""Builds the configured LLM client. Call only from composition roots (apps/, scripts/, test fixtures)."""

import anthropic
import openai
from google import genai
from google.genai import types

from core.shared.llm.client import LLMClient
from core.shared.llm.infra.anthropic_client import AnthropicLLMClient
from core.shared.llm.infra.gemini_client import GeminiLLMClient
from core.shared.llm.infra.openai_client import OPENROUTER_BASE_URL, OpenAILLMClient
from core.shared.llm.infra.stage_configs import stage_configs
from settings import Config

TIMEOUT_S = 180  # per HTTP request: a hung provider must not block a turn forever
# The OpenAI and Anthropic SDKs retry timeouts, connection errors, 429 and 5xx: one call can take up to
# (1 + MAX_RETRIES) * TIMEOUT_S plus backoff. Gemini retries in GeminiLLMClient (rate limits only, see MAX_WAIT_S).
# The use cases bound the whole operation on top (TurnHandler's TURN_DEADLINE_S).
MAX_RETRIES = 2


# Stands in for a missing key when the caller allows it: the SDKs refuse to build a client without one. No call is
# made with it: the endpoints that call a model answer 503 first (`ensure_api_key`).
_PLACEHOLDER_KEY = "missing-api-key"


def make_llm_client(config: Config, *, allow_missing_key: bool = False) -> LLMClient:
    """`allow_missing_key`: build the client anyway when the provider's key is not set (a local server that starts
    with a warning). Scripts leave it off and fail at once."""
    stages = stage_configs(config)

    def key_of(name: str) -> str | None:
        return config.api_key(name) or (_PLACEHOLDER_KEY if allow_missing_key else None)

    match config.LLM_PROVIDER:
        case "openai":
            return OpenAILLMClient(
                stages, openai.AsyncOpenAI(api_key=key_of("OPENAI_API_KEY"), timeout=TIMEOUT_S, max_retries=MAX_RETRIES)
            )
        case "openrouter":
            # Never None: the OpenAI SDK would fall back to OPENAI_API_KEY and send it to openrouter.ai.
            key = key_of("OPENROUTER_API_KEY")
            if key is None:
                raise ValueError("OPENROUTER_API_KEY is not set (LLM_PROVIDER=openrouter)")
            client = openai.AsyncOpenAI(
                base_url=OPENROUTER_BASE_URL, api_key=key, timeout=TIMEOUT_S, max_retries=MAX_RETRIES
            )
            # Only route to providers that honour every parameter sent (the JSON schema, when there is one).
            return OpenAILLMClient(stages, client, extra_body={"provider": {"require_parameters": True}})
        case "gemini":
            http_options = types.HttpOptions(timeout=TIMEOUT_S * 1000)  # milliseconds
            return GeminiLLMClient(stages, genai.Client(api_key=key_of("GEMINI_API_KEY"), http_options=http_options))
        case "anthropic":
            return AnthropicLLMClient(stages, anthropic.AsyncAnthropic(timeout=TIMEOUT_S, max_retries=MAX_RETRIES))
    raise ValueError(f"LLM_PROVIDER={config.LLM_PROVIDER!r}: no client for it")
