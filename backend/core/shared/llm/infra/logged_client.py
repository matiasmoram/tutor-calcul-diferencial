from loguru import logger

from core.shared.domain.clock import Clock, SystemClock
from core.shared.llm.call_scope import current_scope
from core.shared.llm.client import CallMeta, JsonObject, LLMClient, LLMError, LLMRequest, Stage
from core.shared.llm_calls.domain.llm_call import LLMCall
from core.shared.llm_calls.domain.repository import LLMCallRepository


class LoggedLLMClient(LLMClient):
    """Records every call (failures included) in the call log, attributed to the current call scope.

    A failure to write the log is logged and swallowed: the audit trail must never break a student's turn."""

    def __init__(
        self, inner: LLMClient, calls: LLMCallRepository, log_prompts: bool = False, clock: Clock | None = None
    ) -> None:
        self._inner = inner
        self._calls = calls
        self._log_prompts = log_prompts
        self._clock = clock or SystemClock()

    def model_for(self, stage: Stage) -> str:
        return self._inner.model_for(stage)

    async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
        try:
            data, meta = await self._inner.structured(stage, request)
        except Exception as e:
            # A truncated or malformed answer was billed all the same: its tokens belong in the log.
            failed = e.meta if isinstance(e, LLMError) else None
            await self._record(stage, request, ok=False, meta=failed, error=f"{type(e).__name__}: {e}")
            raise
        await self._record(stage, request, ok=True, meta=meta, response=data)
        return data, meta

    async def _record(
        self,
        stage: Stage,
        request: LLMRequest,
        *,
        ok: bool,
        meta: CallMeta | None = None,
        response: JsonObject | None = None,
        error: str | None = None,
    ) -> None:
        scope = current_scope()
        call = LLMCall(
            session_id=scope.session_id,
            turn=scope.turn,
            created_at=self._clock.now(),
            stage=stage,
            model=meta.model if meta else self._inner.model_for(stage),
            ok=ok,
            latency_ms=meta.latency_ms if meta else None,
            input_tokens=meta.input_tokens if meta else None,
            output_tokens=meta.output_tokens if meta else None,
            cached_tokens=meta.cached_tokens if meta else None,
            error=error,
            response=response,
            system=request.system if self._log_prompts else None,
            prompt=f"{request.context or ''}\n\n{request.user}".strip() if self._log_prompts else None,
        )
        try:
            await self._calls.add(call)
        except Exception as e:  # best effort by design (see class docstring)
            logger.error(f"LLM call log write failed: {e}")
