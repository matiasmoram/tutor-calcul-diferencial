from loguru import logger

from core.shared.llm.client import CallMeta, JsonObject, LLMClient, LLMRequest, MalformedOutputError, Stage


class RetryingLLMClient(LLMClient):
    """Asks again when the model's text is unusable (MalformedOutputError), up to `attempts` calls in all.

    A malformed answer is a sampling glitch: without a retry, one bad character late in a multi-call pipeline
    (a quiz is ~8 calls) throws away everything paid for before it. Every other error propagates at once: a
    truncation or a provider failure would only fail again. Wrap it around LoggedLLMClient so each attempt is logged.
    """

    def __init__(self, inner: LLMClient, attempts: int = 2) -> None:
        self._inner = inner
        self._attempts = attempts

    def model_for(self, stage: Stage) -> str:
        return self._inner.model_for(stage)

    async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
        for attempt in range(1, self._attempts + 1):
            try:
                return await self._inner.structured(stage, request)
            except MalformedOutputError as e:
                if attempt == self._attempts:
                    raise
                logger.warning(f"{e.message}; asking again ({attempt + 1}/{self._attempts})")
        raise AssertionError("unreachable")
