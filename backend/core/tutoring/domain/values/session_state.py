"""The tutor's memory of a session between turns. Stored as a document with its historical Catalan keys."""

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from core.tutoring.domain.values.diagnosis import StepState
from core.tutoring.domain.values.plan import Action


def _ca(catalan: str, english: str) -> AliasChoices:
    return AliasChoices(catalan, english)


class SessionState(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True, frozen=True)

    completed: list[str] = Field(
        default_factory=list, validation_alias=_ca("completats", "completed"), serialization_alias="completats"
    )
    # Highest hint level delivered per step.
    level_per_step: dict[str, int] = Field(
        default_factory=dict,
        validation_alias=_ca("nivell_per_pas", "level_per_step"),
        serialization_alias="nivell_per_pas",
    )
    turns: int = Field(default=0, validation_alias=_ca("torns", "turns"), serialization_alias="torns")
    # Sticky: once closed, the session stays closed.
    closed: bool = Field(default=False, validation_alias=_ca("tancat", "closed"), serialization_alias="tancat")
    # Target of the last hint action.
    last_step: str | None = Field(
        default=None, validation_alias=_ca("ultim_pas", "last_step"), serialization_alias="ultim_pas"
    )
    last_action: Action | None = Field(
        default=None, validation_alias=_ca("ultima_accio", "last_action"), serialization_alias="ultima_accio"
    )
    # Step states after the last turn (to measure progress).
    step_states: dict[str, StepState] = Field(
        default_factory=dict, validation_alias=_ca("estats", "step_states"), serialization_alias="estats"
    )
    # Steps the tutor has shown in full.
    shown: list[str] = Field(
        default_factory=list, validation_alias=_ca("mostrats", "shown"), serialization_alias="mostrats"
    )
    mistakes_seen: dict[str, int] = Field(
        default_factory=dict,
        validation_alias=_ca("errors_vistos", "mistakes_seen"),
        serialization_alias="errors_vistos",
    )
    # Consecutive hint turns at the same level, per step.
    repetitions: dict[str, int] = Field(
        default_factory=dict, validation_alias=_ca("repeticions", "repetitions"), serialization_alias="repeticions"
    )
    # The tutor has already acknowledged the correct result.
    result_confirmed: bool = Field(
        default=False,
        validation_alias=_ca("resultat_confirmat", "result_confirmed"),
        serialization_alias="resultat_confirmat",
    )
    # Turns in which the student showed work or made progress (anti-gaming).
    student_attempts: int = Field(
        default=0, validation_alias=_ca("intents_alumne", "student_attempts"), serialization_alias="intents_alumne"
    )
