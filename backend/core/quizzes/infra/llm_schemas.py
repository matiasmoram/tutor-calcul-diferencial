"""JSON schemas of the "Cert o fals" stages. Keys and enum values are part of the contract with the models."""

from collections.abc import Sequence

from core.quizzes.domain.entities.grading import JUSTIFICATIONS
from core.quizzes.domain.entities.statement import TRAPS
from core.shared.llm.client import JsonObject
from core.shared.math.sympy_checks import CHECK_SCHEMA


def _object(required: list[str], properties: JsonObject) -> JsonObject:
    return {"type": "object", "additionalProperties": False, "required": required, "properties": properties}


def _array(items: object) -> JsonObject:
    return {"type": "array", "items": items}


def _strings(value: object) -> list[str]:
    assert isinstance(value, list)
    return [str(v) for v in value]


def _properties(value: object) -> JsonObject:
    assert isinstance(value, dict)
    return {str(k): v for k, v in value.items()}


def generation_schema(refs: Sequence[str]) -> JsonObject:
    statement = _object(
        ["enunciat", "veredicte", "trampa", "concepte", "contraexemple", "resolucio", "idees_clau", "pista", "teoria",
         "comprovacions"],
        {
            "enunciat": {"type": "string"},
            "veredicte": {"type": "string", "enum": ["cert", "fals"]},
            "trampa": {"type": "string", "enum": list(TRAPS)},
            "concepte": {"type": "string"},
            "contraexemple": {"type": "string"},
            "resolucio": {"type": "string"},
            "idees_clau": _array({"type": "string"}),
            "pista": {"type": "string"},
            "teoria": _array({"type": "string", "enum": list(refs)}),
            "comprovacions": _array(dict(CHECK_SCHEMA)),
        },
    )  # fmt: skip
    return _object(["afirmacions"], {"afirmacions": _array(statement)})


def solver_schema() -> JsonObject:
    answer = _object(
        ["num", "justificacio", "veredicte", "confianca", "ben_plantejada"],
        {
            "num": {"type": "integer"},
            "justificacio": {"type": "string"},
            "veredicte": {"type": "string", "enum": ["cert", "fals"]},
            "confianca": {"type": "string", "enum": ["alta", "mitjana", "baixa"]},
            "ben_plantejada": {"type": "boolean"},
        },
    )
    return _object(["respostes"], {"respostes": _array(answer)})


def audit_schema() -> JsonObject:
    review = _object(
        ["num", "problemes", "resolucio_correcta", "teoria_correcta", "pista_neutra"],
        {
            "num": {"type": "integer"},
            "problemes": {"type": "string"},
            "resolucio_correcta": {"type": "boolean"},
            "teoria_correcta": {"type": "boolean"},
            "pista_neutra": {"type": "boolean"},
        },
    )
    return _object(["revisions"], {"revisions": _array(review)})


# A student's claim carries its literal quote, so code can refuse checks the grader made up or "corrected".
STUDENT_CHECK_SCHEMA: JsonObject = {
    **CHECK_SCHEMA,
    "required": ["cita_alumne", *_strings(CHECK_SCHEMA["required"])],
    "properties": {"cita_alumne": {"type": "string"}, **_properties(CHECK_SCHEMA["properties"])},
}


def grading_schema(ids: Sequence[str]) -> JsonObject:
    evaluation = _object(
        ["id", "idees", "justificacio", "feedback"],
        {
            "id": {"type": "string", "enum": list(ids)},
            "idees": _array(
                _object(["num", "cita"], {"num": {"type": "integer"}, "cita": {"type": "string"}}),
            ),
            "justificacio": {"type": "string", "enum": list(JUSTIFICATIONS)},
            "feedback": {"type": "string"},
        },
    )
    return _object(["avaluacions", "resum"], {"avaluacions": _array(evaluation), "resum": {"type": "string"}})


def extraction_schema(ids: Sequence[str]) -> JsonObject:
    answer = _object(
        ["id", "comprovacions"],
        {"id": {"type": "string", "enum": list(ids)}, "comprovacions": _array(STUDENT_CHECK_SCHEMA)},
    )
    return _object(["respostes"], {"respostes": _array(answer)})
