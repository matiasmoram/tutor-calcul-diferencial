"""What the tutor may do this turn, decided by the policy. The action names and keys are Catalan: they are part
of the reply prompt and of the stored traces the professor panel reads."""

from collections.abc import Mapping
from typing import Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

Action = Literal[
    "redirigir",
    "tancar",
    "despres_de_tancar",
    "demanar_raonament",
    "demanar_intent",
    "demanar_justificacio",
    "demanar_conclusio",
    "mostrar_conclusio",
    "questionar_error",
    "questionar_resultat",
    "explicar_concepte",
    "validar_i_avancar",
    "pista",
    "mostrar_pas",
]
Tone = Literal["normal", "empatic"]
# Teacher move of an action (MathDial taxonomy), for logs and the professor panel.
TeacherMove = Literal["Generic", "Probing", "Focus", "Telling"]

TEACHER_MOVES: Mapping[Action, TeacherMove] = {
    "redirigir": "Generic",
    "tancar": "Generic",
    "despres_de_tancar": "Generic",
    "demanar_raonament": "Probing",
    "demanar_intent": "Probing",
    "demanar_justificacio": "Probing",
    "mostrar_conclusio": "Telling",
    "demanar_conclusio": "Focus",
    "questionar_error": "Probing",
    "questionar_resultat": "Focus",
    "explicar_concepte": "Telling",
    "validar_i_avancar": "Focus",
    "pista": "Focus",
    "mostrar_pas": "Telling",
}


def _ca(catalan: str, english: str) -> AliasChoices:
    return AliasChoices(catalan, english)


class Plan(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True, frozen=True)

    action: Action = Field(validation_alias=_ca("accio", "action"), serialization_alias="accio")
    reason: str = Field(validation_alias=_ca("motiu", "reason"), serialization_alias="motiu")
    target_step: str | None = Field(
        validation_alias=_ca("pas_objectiu", "target_step"), serialization_alias="pas_objectiu"
    )
    hint_level: int = Field(validation_alias=_ca("nivell_pista", "hint_level"), serialization_alias="nivell_pista")
    target_mistake: str | None = Field(
        default=None, validation_alias=_ca("error_objectiu", "target_mistake"), serialization_alias="error_objectiu"
    )
    mistake_text: str | None = Field(
        default=None, validation_alias=_ca("error_text", "mistake_text"), serialization_alias="error_text"
    )
    suggested_question: str | None = Field(
        default=None,
        validation_alias=_ca("pregunta_suggerida", "suggested_question"),
        serialization_alias="pregunta_suggerida",
    )
    may_state_result: bool = Field(
        default=False,
        validation_alias=_ca("pot_dir_resultat", "may_state_result"),
        serialization_alias="pot_dir_resultat",
    )
    # The student stated the correct result: it may be acknowledged.
    result_stated_by_student: bool = Field(
        default=False,
        validation_alias=_ca("resultat_dit_per_alumne", "result_stated_by_student"),
        serialization_alias="resultat_dit_per_alumne",
    )
    requires_question: bool = Field(
        default=True,
        validation_alias=_ca("requereix_pregunta", "requires_question"),
        serialization_alias="requereix_pregunta",
    )
    max_sentences: int = Field(
        default=4, validation_alias=_ca("max_frases", "max_sentences"), serialization_alias="max_frases"
    )
    forbidden_patterns: list[str] = Field(
        default_factory=list,
        validation_alias=_ca("regex_prohibides", "forbidden_patterns"),
        serialization_alias="regex_prohibides",
    )
    # Texts whose formulas the reply must not reproduce in any equivalent form (sympy check in the guard):
    # the result until it may be said, and the details of steps the plan does not open.
    forbidden_texts: list[str] = Field(
        default_factory=list,
        validation_alias=_ca("textos_prohibits", "forbidden_texts"),
        serialization_alias="textos_prohibits",
    )
    # Items answering a conceptual question.
    extra_theory: list[str] = Field(
        default_factory=list, validation_alias=_ca("teoria_extra", "extra_theory"), serialization_alias="teoria_extra"
    )
    # Empathetic opener for frustrated or lost students.
    tone: Tone = Field(default="normal", validation_alias=_ca("to", "tone"), serialization_alias="to")
    move: TeacherMove = Field(
        default="Generic", validation_alias=_ca("moviment", "move"), serialization_alias="moviment"
    )
