"""The LLM boundary fake: replays scripted JSON outputs per stage. The model is the one thing we mock."""

from collections import defaultdict
from collections.abc import Mapping, Sequence

from core.shared.llm.client import CallMeta, JsonObject, LLMClient, LLMError, LLMRequest, Stage


class ScriptedLLMClient(LLMClient):
    def __init__(self, script: Mapping[Stage, Sequence[JsonObject | Exception]]) -> None:
        self._script = {stage: list(outputs) for stage, outputs in script.items()}
        self.requests: dict[Stage, list[LLMRequest]] = defaultdict(list)

    def model_for(self, stage: Stage) -> str:
        return "scripted"

    async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
        self.requests[stage].append(request)
        outputs = self._script.get(stage)
        if not outputs:
            raise LLMError(f"{stage}: script exhausted")
        out = outputs.pop(0)
        if isinstance(out, Exception):
            raise out
        return out, CallMeta(stage=stage, model="scripted", latency_ms=1, input_tokens=10, output_tokens=2)

    def calls(self, stage: Stage) -> int:
        return len(self.requests[stage])
