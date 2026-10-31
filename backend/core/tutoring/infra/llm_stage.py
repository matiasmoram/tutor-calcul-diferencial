"""What every tutoring stage adapter shares: one model call, its output validated, failures typed for the domain."""

from pydantic import BaseModel, ValidationError

from core.shared.llm.client import (
    CallMeta,
    JsonObject,
    LLMClient,
    LLMError,
    LLMProviderError,
    LLMRequest,
    Stage,
    TruncatedOutputError,
)
from core.tutoring.domain.exceptions import ModelOutputException, TruncatedModelOutputException
from core.tutoring.domain.values.turn_trace import ModelCall


def model_call(meta: CallMeta) -> ModelCall:
    return ModelCall(stage=str(meta.stage), **meta.usage().model_dump())


async def call_stage(
    llm: LLMClient, stage: Stage, request: LLMRequest, stage_name: str
) -> tuple[JsonObject, ModelCall]:
    """Provider failures (auth, rate limit, outage) propagate; an unusable answer is a ModelOutputException."""
    try:
        data, meta = await llm.structured(stage, request)
    except LLMProviderError:
        raise
    except LLMError as e:
        # The model answered and its tokens were billed: the client attaches the call's metadata to the error.
        failed = e.meta
        call = model_call(failed) if isinstance(failed, CallMeta) else None
        kind = TruncatedModelOutputException if isinstance(e, TruncatedOutputError) else ModelOutputException
        raise kind(stage_name, e.message, call) from e
    return data, model_call(meta)


def validate_output[M: BaseModel](model: type[M], data: JsonObject, call: ModelCall, stage_name: str) -> M:
    try:
        return model.model_validate(data)
    except ValidationError as e:
        raise ModelOutputException(stage_name, str(e), call) from e
