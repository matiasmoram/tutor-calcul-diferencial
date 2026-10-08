from collections.abc import Mapping

from core.shared.llm.client import CallMeta, JsonObject, LLMClient, LLMRequest, Stage


class StageRouter(LLMClient):
    """Sends each stage to its own backend, so stages can mix providers (e.g. a strong diagnosis, a tiny reply)."""

    def __init__(self, routes: Mapping[Stage, LLMClient]) -> None:
        self._routes = routes

    def model_for(self, stage: Stage) -> str:
        return self._routes[stage].model_for(stage)

    async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
        return await self._routes[stage].structured(stage, request)
