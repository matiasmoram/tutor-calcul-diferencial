"""The result of grading a student's annotations. Its JSON (Catalan keys) is what the frontend reads after
submitting (``frontend/errades.js``): ``nota``, ``trobats``, ``total``, ``falsos_positius``, ``anotacions``,
``errors``, ``resum``, ``crida``."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from core.mistakes.domain.entities.mistake_exercise import DeclaredMistake
from core.shared.domain.contract import catalan_alias
from core.shared.domain.model_usage import ModelUsage

Location = Literal["exacta", "aproximada"]


class AnnotationResult(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    id: str
    # A declared mistake's id, or NO_MISTAKE.
    mistake_id: str = Field(validation_alias=catalan_alias("error", "mistake_id"), serialization_alias="error")
    location: Location | None = Field(
        validation_alias=catalan_alias("localitzacio", "location"), serialization_alias="localitzacio"
    )
    explanation: str = Field(
        validation_alias=catalan_alias("explicacio", "explanation"), serialization_alias="explicacio"
    )
    feedback: str
    points: float = Field(validation_alias=catalan_alias("punts", "points"), serialization_alias="punts")


class MistakeGrading(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    score: int = Field(validation_alias=catalan_alias("nota", "score"), serialization_alias="nota")  # 0..100
    found: int = Field(validation_alias=catalan_alias("trobats", "found"), serialization_alias="trobats")
    total: int
    false_positives: int = Field(
        validation_alias=catalan_alias("falsos_positius", "false_positives"), serialization_alias="falsos_positius"
    )
    annotations: list[AnnotationResult] = Field(
        validation_alias=catalan_alias("anotacions", "annotations"), serialization_alias="anotacions"
    )
    mistakes: list[DeclaredMistake] = Field(
        validation_alias=catalan_alias("errors", "mistakes"), serialization_alias="errors"
    )
    summary: str = Field(validation_alias=catalan_alias("resum", "summary"), serialization_alias="resum")
    call: ModelUsage | None = Field(validation_alias=catalan_alias("crida", "call"), serialization_alias="crida")


class PartGrading(BaseModel):
    """The grading of one flawed part of a per-parts session, stored once. Its score already carries the hint
    factor when the student asked for the part's hint."""

    part: int
    hint_used: bool
    grading: MistakeGrading


class PartScore(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    part: int
    score: int = Field(validation_alias=catalan_alias("nota", "score"), serialization_alias="nota")
    hint_used: bool = Field(validation_alias=catalan_alias("pista", "hint_used"), serialization_alias="pista")


class PartedMistakeGrading(BaseModel):
    """A per-parts session once every flawed part is graded: the mean of the part scores."""

    model_config = ConfigDict(serialize_by_alias=True)

    score: int = Field(validation_alias=catalan_alias("nota", "score"), serialization_alias="nota")  # 0..100
    found: int = Field(validation_alias=catalan_alias("trobats", "found"), serialization_alias="trobats")
    total: int
    false_positives: int = Field(
        validation_alias=catalan_alias("falsos_positius", "false_positives"), serialization_alias="falsos_positius"
    )
    parts: list[PartScore]
