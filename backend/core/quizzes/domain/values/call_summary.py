from pydantic import BaseModel


class CallSummary(BaseModel):
    """What a model call cost, as stored in the quiz's verification log and returned with a grading."""

    model: str
    latency_ms: int
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
