"""The result of grading a student's annotations. Its JSON (Catalan keys) is what the frontend reads after
submitting (``frontend/errades.js``): ``nota``, ``trobats``, ``total``, ``falsos_positius``, ``anotacions``,
``errors``, ``resum``, ``crida``."""

from typing import Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from core.mistakes.domain.entities.mistake_exercise import DeclaredMistake
from core.mistakes.domain.values.call_record import CallRecord

Location = Literal["exacta", "aproximada"]


def _ca(catalan: str, english: str) -> AliasChoices:
    return AliasChoices(catalan, english)


class AnnotationResult(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    id: str
    mistake_id: str = Field(validation_alias=_ca("error", "mistake_id"), serialization_alias="error")  # or "cap"
    location: Location | None = Field(
        validation_alias=_ca("localitzacio", "location"), serialization_alias="localitzacio"
    )
    explanation: str = Field(validation_alias=_ca("explicacio", "explanation"), serialization_alias="explicacio")
    feedback: str
    points: float = Field(validation_alias=_ca("punts", "points"), serialization_alias="punts")


class MistakeGrading(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    score: int = Field(validation_alias=_ca("nota", "score"), serialization_alias="nota")  # 0..100
    found: int = Field(validation_alias=_ca("trobats", "found"), serialization_alias="trobats")
    total: int
    false_positives: int = Field(
        validation_alias=_ca("falsos_positius", "false_positives"), serialization_alias="falsos_positius"
    )
    annotations: list[AnnotationResult] = Field(
        validation_alias=_ca("anotacions", "annotations"), serialization_alias="anotacions"
    )
    mistakes: list[DeclaredMistake] = Field(validation_alias=_ca("errors", "mistakes"), serialization_alias="errors")
    summary: str = Field(validation_alias=_ca("resum", "summary"), serialization_alias="resum")
    call: CallRecord | None = Field(validation_alias=_ca("crida", "call"), serialization_alias="crida")
