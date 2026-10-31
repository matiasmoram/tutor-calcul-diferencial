"""The diagnosis stage's reading of the student's last message. Its keys and enum values are the LLM contract
(Catalan): they are what the model is asked for, and what the stored traces contain."""

from collections.abc import Sequence
from typing import Literal, get_args

from pydantic import BaseModel, ConfigDict, Field

from core.shared.domain.contract import catalan_alias

StepState = Literal["no_iniciat", "en_curs", "completat", "erroni"]
Disorientation = Literal["en_cami", "dubte_puntual", "encallat", "perdut"]
Intent = Literal[
    "mostra_treball",
    "demana_pista",
    "demana_solucio",
    "pregunta_conceptual",
    "proposa_resultat",
    "fora_de_tema",
    "frustracio",
]
ProposedResult = Literal["cap", "correcte", "incorrecte"]

STEP_STATES: tuple[StepState, ...] = get_args(StepState)
DISORIENTATIONS: tuple[Disorientation, ...] = get_args(Disorientation)  # in increasing order
INTENTS: tuple[Intent, ...] = get_args(Intent)
PROPOSED_RESULTS: tuple[ProposedResult, ...] = get_args(ProposedResult)
OTHER_MISTAKE = "altre"  # a mistake that is not in the sheet's catalogue


class StepStatus(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True, frozen=True)

    step_id: str = Field(validation_alias=catalan_alias("pas", "step_id"), serialization_alias="pas")
    state: StepState = Field(validation_alias=catalan_alias("estat", "state"), serialization_alias="estat")


class Diagnosis(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True, frozen=True)

    evidence: str = Field(validation_alias=catalan_alias("evidencia", "evidence"), serialization_alias="evidencia")
    student_summary: str = Field(
        validation_alias=catalan_alias("resum_alumne", "student_summary"), serialization_alias="resum_alumne"
    )
    step_states: list[StepStatus] = Field(
        validation_alias=catalan_alias("estat_passos", "step_states"), serialization_alias="estat_passos"
    )
    current_step: str = Field(
        validation_alias=catalan_alias("pas_actual", "current_step"), serialization_alias="pas_actual"
    )
    detected_mistakes: list[str] = Field(
        validation_alias=catalan_alias("errors_detectats", "detected_mistakes"), serialization_alias="errors_detectats"
    )
    other_mistake: str = Field(
        validation_alias=catalan_alias("error_altre", "other_mistake"), serialization_alias="error_altre"
    )
    proposed_result: ProposedResult = Field(
        validation_alias=catalan_alias("resultat_proposat", "proposed_result"), serialization_alias="resultat_proposat"
    )
    result_justified: bool = Field(
        validation_alias=catalan_alias("resultat_justificat", "result_justified"),
        serialization_alias="resultat_justificat",
    )
    disorientation: Disorientation = Field(
        validation_alias=catalan_alias("nivell_desorientacio", "disorientation"),
        serialization_alias="nivell_desorientacio",
    )
    intent: Intent = Field(validation_alias=catalan_alias("intencio", "intent"), serialization_alias="intencio")
    question_theory: list[str] = Field(
        default_factory=list,
        validation_alias=catalan_alias("teoria_pregunta", "question_theory"),
        serialization_alias="teoria_pregunta",
    )

    def step_state_map(self) -> dict[str, StepState]:
        return {s.step_id: s.state for s in self.step_states}

    def normalized(self, step_ids: Sequence[str], theory_ids: Sequence[str]) -> "Diagnosis":
        """The step list complete and ordered, whatever the model returned; theory limited to `theory_ids`."""
        by_id: dict[str, StepState] = {s.step_id: s.state for s in self.step_states if s.step_id in step_ids}
        mistakes = list(dict.fromkeys(self.detected_mistakes))
        # An uncatalogued mistake needs a description to be questioned. (Step states describe the whole
        # conversation and mistakes only the last message, so a step marked wrong is NOT turned into a mistake.)
        if OTHER_MISTAKE in mistakes and not self.other_mistake.strip():
            mistakes = [m for m in mistakes if m != OTHER_MISTAKE]
        allowed = set(theory_ids)
        return self.model_copy(
            update={
                "step_states": [StepStatus(step_id=s, state=by_id.get(s) or "no_iniciat") for s in step_ids],
                "detected_mistakes": mistakes,
                "question_theory": [t for t in dict.fromkeys(self.question_theory) if t in allowed][:2],
            }
        )
