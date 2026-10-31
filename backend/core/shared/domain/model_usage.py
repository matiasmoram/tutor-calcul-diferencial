from pydantic import BaseModel, ConfigDict


class ModelUsage(BaseModel):
    """What one model call cost, as kept in generation and verification logs, grading results and turn traces."""

    model_config = ConfigDict(frozen=True)

    model: str
    latency_ms: int
    input_tokens: int = 0  # total prompt tokens, cached ones included
    output_tokens: int = 0
    cached_tokens: int = 0  # prompt tokens served from the provider's prompt cache
