"""JSON schemas sent to the model for each structured stage.

Built per exercise so step and mistake ids are closed enums: the model cannot invent a step that the sheet does
not have. Keys, enum values and descriptions are the Catalan prompt contract."""

from collections.abc import Sequence

from core.course.domain.entities.exercise import Exercise
from core.shared.llm.client import JsonObject
from core.tutoring.domain.values.diagnosis import (
    DISORIENTATIONS,
    INTENTS,
    OTHER_MISTAKE,
    PROPOSED_RESULTS,
    STEP_STATES,
    Diagnosis,
)
from core.tutoring.domain.values.guard_verdict import VERDICTS, VIOLATIONS
from core.tutoring.domain.values.transcription import LEGIBILITIES, PHOTO_CONTENTS

NO_STEP = "cap"


def _enum(values: Sequence[str], description: str) -> JsonObject:
    return {"type": "string", "enum": list(values), "description": description}


def _id_list(ids: Sequence[str], description: str) -> JsonObject:
    """Array of ids from a closed set. Length limits are enforced in code: not every provider supports maxItems."""
    if not ids:
        return {
            "type": "array",
            "description": "Sempre buit: no hi ha cap ítem disponible.",
            "items": {"type": "string"},
        }
    return {"type": "array", "description": description, "items": _enum(ids, "Id de l'ítem dels apunts.")}


DIAGNOSIS_KEYS: list[str] = [f.serialization_alias or name for name, f in Diagnosis.model_fields.items()]


def diagnosis_schema(ex: Exercise, theory_ids: Sequence[str] = ()) -> JsonObject:
    """`theory_ids`: theory items the diagnosis may point to when the student asks a conceptual question."""
    return {
        "type": "object",
        "additionalProperties": False,
        "required": DIAGNOSIS_KEYS,
        "properties": {
            "evidencia": {
                "type": "string",
                "description": "Cita literal i breu del que ha escrit l'alumne que justifica la diagnosi. Buit si no ha escrit res rellevant.",
            },
            "resum_alumne": {
                "type": "string",
                "description": "Una frase: què ha fet l'alumne fins ara i on és.",
            },
            "estat_passos": {
                "type": "array",
                "description": "Un element per cada pas de la fitxa, en el mateix ordre.",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["pas", "estat"],
                    "properties": {
                        "pas": _enum(ex.step_ids, "Id del pas."),
                        "estat": _enum(STEP_STATES, "Estat del pas segons el treball ESCRIT per l'alumne."),
                    },
                },
            },
            "pas_actual": _enum(
                [*ex.step_ids, NO_STEP],
                "Primer pas que l'alumne encara no ha completat correctament ('cap' si els ha completat tots).",
            ),
            "errors_detectats": {
                "type": "array",
                "description": "Errors comuns de la fitxa presents a l'ÚLTIM missatge de l'alumne. 'altre' si n'hi ha un que no és a la llista.",
                "items": _enum([*ex.mistake_ids, OTHER_MISTAKE], "Id de l'error."),
            },
            "error_altre": {
                "type": "string",
                "description": "Descripció breu de l'error si errors_detectats conté 'altre'; buit altrament.",
            },
            "resultat_proposat": _enum(
                PROPOSED_RESULTS,
                "Si l'alumne ha afirmat un resultat final, si coincideix amb el de la fitxa.",
            ),
            "resultat_justificat": {
                "type": "boolean",
                "description": "Cert només si l'alumne ha donat una justificació rigorosa i completa del resultat.",
            },
            "nivell_desorientacio": _enum(
                DISORIENTATIONS,
                "en_cami: avança bé. dubte_puntual: sap el camí però dubta en un detall. "
                "encallat: sap on és però no sap com continuar. perdut: no sap per on començar o falla un concepte base.",
            ),
            "intencio": _enum(INTENTS, "Què vol l'alumne amb l'últim missatge."),
            "teoria_pregunta": _id_list(
                theory_ids,
                "Si l'intenció és pregunta_conceptual: els ítems dels apunts (màxim 2) que responen la pregunta. Buit altrament.",
            ),
        },
    }  # fmt: skip


def guard_schema() -> JsonObject:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["veredicte", "infraccions", "explicacio"],
        "properties": {
            "veredicte": _enum(VERDICTS, "rebutjat si hi ha alguna infracció."),
            "infraccions": {
                "type": "array",
                "items": _enum(VIOLATIONS, "Tipus d'infracció."),
            },
            "explicacio": {"type": "string", "description": "Una frase justificant el veredicte."},
        },
    }


def transcription_schema() -> JsonObject:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["transcripcio", "llegibilitat", "contingut", "dubtes"],
        "properties": {
            "transcripcio": {"type": "string", "description": "Transcripció literal, fórmules en $...$."},
            "llegibilitat": {"type": "string", "enum": list(LEGIBILITIES)},
            "contingut": {"type": "string", "enum": list(PHOTO_CONTENTS)},
            "dubtes": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Fragments dubtosos o il·legibles, i com s'han interpretat.",
            },
        },
    }
