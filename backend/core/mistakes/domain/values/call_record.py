from pydantic import BaseModel


class CallRecord(BaseModel):
    """Usage of one model call, as kept in a document's generation log and in a grading result ("crida")."""

    model: str
    latency_ms: int
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
