from pydantic import BaseModel


class LLMCall(BaseModel):
    """One model call, successful or not: the audit log of everything the models were asked and answered."""

    session_id: str | None
    turn: int | None
    created_at: float
    stage: str
    model: str
    ok: bool
    latency_ms: int | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    cached_tokens: int | None = None
    error: str | None = None
    response: dict[str, object] | None = None
    system: str | None = None  # prompts only with TUTOR_LOG_PROMPTS=1 (large)
    prompt: str | None = None
