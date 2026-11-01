"""Everything a turn decided and tried, for the professor panel and the evaluation scripts.

Serialized with its Catalan contract keys (``torn``, ``diagnosi``, ``pla``, ``intents``, ``fallback``, ...)."""

from pydantic import BaseModel, ConfigDict, Field

from core.shared.domain.contract import catalan_alias
from core.shared.domain.ids import TheoryItemId
from core.tutoring.domain.values.chat_message import TurnOrigin
from core.tutoring.domain.values.diagnosis import Diagnosis
from core.tutoring.domain.values.guard_verdict import GuardVerdict
from core.tutoring.domain.values.plan import Plan
from core.tutoring.domain.values.session_state import SessionState


class ModelCall(BaseModel):
    """One model call of a stage, as the trace records it (cost and latency accounting). The fields of `ModelUsage`
    with `stage` first: that is the key order of the stored traces and of the API."""

    model_config = ConfigDict(frozen=True)

    stage: str
    model: str
    latency_ms: int
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0


class FailedDraft(BaseModel):
    """The writer produced no usable draft (model error, empty text)."""

    model_config = ConfigDict(serialize_by_alias=True, frozen=True)

    message: None = Field(
        default=None, validation_alias=catalan_alias("missatge", "message"), serialization_alias="missatge"
    )
    error: str


class CheckedDraft(BaseModel):
    """A draft and what the guards said. ``verdict`` is None when the deterministic checks already rejected it."""

    model_config = ConfigDict(serialize_by_alias=True, frozen=True)

    message: str = Field(validation_alias=catalan_alias("missatge", "message"), serialization_alias="missatge")
    references: list[TheoryItemId] = Field(
        validation_alias=catalan_alias("referencies", "references"), serialization_alias="referencies"
    )
    deterministic_problems: list[str] = Field(
        validation_alias=catalan_alias("determinista", "deterministic_problems"), serialization_alias="determinista"
    )
    verdict: GuardVerdict | None = Field(validation_alias=catalan_alias("llm", "verdict"), serialization_alias="llm")

    @property
    def approved(self) -> bool:
        return not self.deterministic_problems and self.verdict is not None and self.verdict.approved

    def rejection_reasons(self) -> list[str]:
        reasons = [*self.deterministic_problems, *(self.verdict.violations if self.verdict else [])]
        if self.verdict and self.verdict.explanation:
            reasons.append(self.verdict.explanation)
        return reasons


type DraftAttempt = CheckedDraft | FailedDraft


class TurnTrace(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True, frozen=True)

    turn: int = Field(validation_alias=catalan_alias("torn", "turn"), serialization_alias="torn")
    origin: TurnOrigin = Field(validation_alias=catalan_alias("origen", "origin"), serialization_alias="origen")
    diagnosis: Diagnosis = Field(
        validation_alias=catalan_alias("diagnosi", "diagnosis"), serialization_alias="diagnosi"
    )
    plan: Plan = Field(validation_alias=catalan_alias("pla", "plan"), serialization_alias="pla")
    allowed_content: str = Field(
        validation_alias=catalan_alias("contingut_permes", "allowed_content"), serialization_alias="contingut_permes"
    )
    allowed_theory: list[TheoryItemId] = Field(
        validation_alias=catalan_alias("teoria_permesa", "allowed_theory"), serialization_alias="teoria_permesa"
    )
    attempts: list[DraftAttempt] = Field(
        validation_alias=catalan_alias("intents", "attempts"), serialization_alias="intents"
    )
    fallback: bool
    previous_state: SessionState = Field(
        validation_alias=catalan_alias("estat_previ", "previous_state"), serialization_alias="estat_previ"
    )
    state: SessionState = Field(validation_alias=catalan_alias("estat", "state"), serialization_alias="estat")
    calls: list[ModelCall] = Field(validation_alias=catalan_alias("crides", "calls"), serialization_alias="crides")
    latency_ms: int = Field(
        validation_alias=catalan_alias("latencia_ms", "latency_ms"), serialization_alias="latencia_ms"
    )
