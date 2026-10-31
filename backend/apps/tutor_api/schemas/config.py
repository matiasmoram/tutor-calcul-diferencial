from pydantic import BaseModel


class StageResponse(BaseModel):
    model: str
    effort: str
    max_tokens: int


class ConfigResponse(BaseModel):
    panell_professor: bool
    # Whether this viewer may start a live generation (TUTOR_GENERACIO); otherwise only the ready ones open.
    pot_generar: bool
    # The model setup, for professors and demo mode only: null for students.
    provider: str | None = None
    api_key: bool | None = None
    stages: dict[str, StageResponse] | None = None
