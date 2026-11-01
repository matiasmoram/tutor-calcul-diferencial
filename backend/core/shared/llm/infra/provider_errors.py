"""The only text a provider failure may show a client: neutral, never the provider's own."""

from loguru import logger

from core.shared.llm.client import LLMProviderError

PROVIDER_UNAVAILABLE = "El servei del model no està disponible ara mateix. Torna-ho a provar d'aquí a una estona."
PROVIDER_BUSY = "El model està molt ocupat ara mateix. Espera un moment i torna-ho a provar."
PROVIDER_UNREACHABLE = "No s'ha pogut connectar amb el model. Torna-ho a provar d'aquí a una estona."


def provider_failure(provider: str, status: int | None, detail: str) -> LLMProviderError:
    """The error that reaches the client for a provider failure: a neutral message and a status, never the
    provider's own text (it can carry a key fragment or an endpoint). A rejected key or any other provider-side
    failure is a 503, a rate limit a 429, an unreachable provider a 502. The raw detail goes to the log only."""
    logger.warning("{} call failed (status {}): {}", provider, status, detail)
    if status == 429:
        return LLMProviderError(PROVIDER_BUSY, 429)
    if status is None:
        return LLMProviderError(PROVIDER_UNREACHABLE, 502)
    return LLMProviderError(PROVIDER_UNAVAILABLE, 503)
