"""JSON schemas of the model stages. Keys and enum values are Catalan: the contract with the model."""

from core.mistakes.domain.values.llm_outputs import EXPLANATION_GRADES, NO_MISTAKE, SEVERITIES
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
                        "gravetat": {"type": "string", "enum": list(SEVERITIES)},
                        "explicacio": {"type": "string"},
                    },
                },
            },
            "valoracio": {"type": "string"},
        },
    }


_FRAGMENTS: JsonObject = {"type": "array", "items": {"type": "string"}}


def resolution_schema(step_ids: list[str] | None) -> JsonObject:
    """Stage A. Problems: one part per sheet step (`step_ids`); theory (None): the statement, then titled stages."""
    if step_ids is None:
        part: JsonObject = {
            "type": "object",
            "additionalProperties": False,
            "required": ["titol", "fragments"],
            "properties": {"titol": {"type": "string"}, "fragments": _FRAGMENTS},
        }
        return {
            "type": "object",
            "additionalProperties": False,
            "required": ["enunciat", "parts"],
            "properties": {"enunciat": _FRAGMENTS, "parts": {"type": "array", "items": part}},
        }
    part = {
        "type": "object",
        "additionalProperties": False,
        "required": ["pas", "fragments"],
        "properties": {"pas": {"type": "string", "enum": step_ids}, "fragments": _FRAGMENTS},
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["parts"],
        "properties": {"parts": {"type": "array", "items": part}},
    }


def _findings(n_fragments: int) -> JsonObject:
    return {
        "type": "array",
        "items": {
            "type": "object",
            "additionalProperties": False,
            "required": ["fragment", "cita", "gravetat", "explicacio"],
            "properties": {
                "fragment": {"type": "integer", "enum": list(range(1, n_fragments + 1))},
                "cita": {"type": "string"},
                "gravetat": {"type": "string", "enum": list(SEVERITIES)},
                "explicacio": {"type": "string"},
            },
        },
    }


def resolution_verification_schema(n_fragments: int) -> JsonObject:
    """The blind check of the correct resolution (stage A): the findings, and whether it reaches the result."""
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["problemes", "valoracio", "arriba_al_resultat"],
        "properties": {
            "problemes": _findings(n_fragments),
            "valoracio": {"type": "string"},
            "arriba_al_resultat": {"type": "boolean"},
        },
    }


def corruption_schema(n_fragments: int, theory: bool = False) -> JsonObject:
    """Stage B: the edits of one part (fragments numbered inside the part) and the error they make."""
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["apte", "canvis", "cita", "tipus", "explicacio", "correccio", "pista"],
        "properties": {
            "apte": {"type": "boolean"},
            "canvis": {
                "type": "array",
                "description": "D'1 a 3 canvis; el primer és l'error.",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["fragment", "original", "nou"],
                    "properties": {
                        "fragment": {"type": "integer", "enum": list(range(1, n_fragments + 1))},
                        "original": {"type": "string"},
                        "nou": {"type": "string"},
                    },
                },
            },
            "cita": {"type": "string"},
            "tipus": {"type": "string", "enum": list(THEORY_MISTAKE_KINDS if theory else PROBLEM_MISTAKE_KINDS)},
            "explicacio": {"type": "string"},
            "correccio": {"type": "string"},
            "pista": {"type": "string"},
        },
    }


def part_verification_schema(n_fragments: int) -> JsonObject:
    """The blind check of one corrupted part (stage C), fragments numbered inside the part."""
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["problemes", "valoracio", "alerta_context"],
        "properties": {
            "problemes": _findings(n_fragments),
            "valoracio": {"type": "string"},
            "alerta_context": {"type": "string"},
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
                        "error": {"type": "string", "enum": [*mistake_ids, NO_MISTAKE]},
                        "explicacio": {"type": "string", "enum": list(EXPLANATION_GRADES)},
                        "feedback": {"type": "string"},
                    },
                },
            },
            "resum": {"type": "string"},
        },
    }
