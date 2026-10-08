"""JSON schemas of the model stages. Keys and enum values are Catalan: the contract with the model."""

from core.mistakes.domain.values.mistake_kind import PROBLEM_MISTAKE_KINDS, THEORY_MISTAKE_KINDS
from core.shared.llm.client import JsonObject


def generation_schema(theory: bool = False) -> JsonObject:
    props: JsonObject = {
        "fragments": {"type": "array", "items": {"type": "string"}},
        "errors": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["fragment", "cita", "tipus", "explicacio", "correccio", "pista"],
                "properties": {
                    "fragment": {"type": "integer", "description": "Número del fragment (1 = el primer)."},
                    "cita": {"type": "string"},
                    "tipus": {
                        "type": "string",
                        "enum": list(THEORY_MISTAKE_KINDS if theory else PROBLEM_MISTAKE_KINDS),
                    },
                    "explicacio": {"type": "string"},
                    "correccio": {"type": "string"},
                    "pista": {"type": "string"},
                },
            },
        },
    }
    required = ["fragments", "errors"]
    if theory:
        props["n_enunciat"] = {
            "type": "integer",
            "description": "Quants dels primers fragments són l'enunciat (1 a 3).",
        }
        required = ["n_enunciat", "fragments", "errors"]
    return {"type": "object", "additionalProperties": False, "required": required, "properties": props}


def verification_schema() -> JsonObject:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["problemes", "valoracio"],
        "properties": {
            "problemes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["fragment", "cita", "gravetat", "explicacio"],
                    "properties": {
                        "fragment": {"type": "integer"},
                        "cita": {"type": "string"},
                        "gravetat": {"type": "string", "enum": ["error", "consequencia", "imprecisio"]},
                        "explicacio": {"type": "string"},
                    },
                },
            },
            "valoracio": {"type": "string"},
        },
    }


def grading_schema(annotation_ids: list[str], mistake_ids: list[str]) -> JsonObject:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["avaluacions", "resum"],
        "properties": {
            "avaluacions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["anotacio", "error", "explicacio", "feedback"],
                    "properties": {
                        "anotacio": {"type": "string", "enum": annotation_ids},
                        "error": {"type": "string", "enum": [*mistake_ids, "cap"]},
                        "explicacio": {"type": "string", "enum": ["correcta", "parcial", "incorrecta", "absent"]},
                        "feedback": {"type": "string"},
                    },
                },
            },
            "resum": {"type": "string"},
        },
    }
