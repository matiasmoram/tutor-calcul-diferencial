"""Builds the configured LLM client. Call only from composition roots (apps/, scripts/, test fixtures)."""

import anthropic
import openai
from google import genai

from core.shared.llm.client import LLMClient
from core.shared.llm.infra.anthropic_client import AnthropicLLMClient
from core.shared.llm.infra.gemini_client import GeminiLLMClient
from core.shared.llm.infra.openai_client import OPENROUTER_BASE_URL, OpenAILLMClient
from core.shared.llm.infra.stage_configs import stage_configs
from settings import Config

TIMEOUT_S = 180  # a hung provider must not block a turn forever


def make_llm_client(config: Config) -> LLMClient:
    stages = stage_configs(config)
    match config.LLM_PROVIDER:
        case "openai":
            return OpenAILLMClient(stages, openai.AsyncOpenAI(timeout=TIMEOUT_S, max_retries=2))
        case "openrouter":
            client = openai.AsyncOpenAI(
                base_url=OPENROUTER_BASE_URL,
                api_key=config.api_key("OPENROUTER_API_KEY"),
                timeout=TIMEOUT_S,
                max_retries=2,
            )
            # Only route to providers that honour every parameter sent (the JSON schema, when there is one).
            return OpenAILLMClient(stages, client, extra_body={"provider": {"require_parameters": True}})
        case "gemini":
            return GeminiLLMClient(stages, genai.Client(api_key=config.api_key("GEMINI_API_KEY")))
        case _:
            return AnthropicLLMClient(stages, anthropic.AsyncAnthropic())
