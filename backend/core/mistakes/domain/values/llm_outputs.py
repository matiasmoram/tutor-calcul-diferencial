"""What the model stages answer, as typed values. Keys and enum values are Catalan: they are the JSON schema contract
(infra/llm_schemas.py) and, for the verifier's findings, part of the stored documents.

The generator's and verifier's answers are validated by code (domain/services/generation_checks.py), which reports a malformed
answer as a reason to regenerate; so the fields the checks inspect keep whatever JSON type the model sent
(``fragment: int | float | str | None``) instead of failing on parse."""

from pydantic import BaseModel, ConfigDict, Field

from core.shared.domain.contract import catalan_alias, omit_none

type JsonScalar = int | float | str | None

# Enum values of the schemas (infra/llm_schemas.py), defined once: the fields below stay plain `str` and code compares
# them against these.
SEVERITY_ERROR = "error"  # the step is wrong
SEVERITY_CONSEQUENCE = "consequencia"  # the step is right, but inherits the wrong result of an earlier error
SEVERITY_IMPRECISION = "imprecisio"  # a minor lack of rigour that leaves the mathematics right
SEVERITIES: tuple[str, ...] = (SEVERITY_ERROR, SEVERITY_CONSEQUENCE, SEVERITY_IMPRECISION)
NO_EXPLANATION = "absent"
EXPLANATION_GRADES: tuple[str, ...] = ("correcta", "parcial", "incorrecta", NO_EXPLANATION)
NO_MISTAKE = "cap"  # the grader's answer for an annotation on no real error


class DraftMistake(BaseModel):
    """One error as the generator declared it, before validation."""

    model_config = ConfigDict(serialize_by_alias=True)

    fragment: JsonScalar = None  # 1-based
    quote: str = Field(default="", validation_alias=catalan_alias("cita", "quote"), serialization_alias="cita")
    kind: str | None = Field(default=None, validation_alias=catalan_alias("tipus", "kind"), serialization_alias="tipus")
    explanation: str = Field(
        default="", validation_alias=catalan_alias("explicacio", "explanation"), serialization_alias="explicacio"
    )
    correction: str = Field(
        default="", validation_alias=catalan_alias("correccio", "correction"), serialization_alias="correccio"
    )
    hint: str = Field(default="", validation_alias=catalan_alias("pista", "hint"), serialization_alias="pista")


class GenerationDraft(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    fragments: list[str] = Field(default_factory=list)
    mistakes: list[DraftMistake] = Field(
        default_factory=list, validation_alias=catalan_alias("errors", "mistakes"), serialization_alias="errors"
    )
    # Theory documents: how many leading fragments are the statement.
    statement_fragments: JsonScalar = Field(
        default=0, validation_alias=catalan_alias("n_enunciat", "statement_fragments"), serialization_alias="n_enunciat"
    )


class VerifierFinding(BaseModel):
    """One problem the blind verifier found. Stored verbatim in the document's verification."""

    model_config = ConfigDict(serialize_by_alias=True)

    fragment: JsonScalar = Field(default=None, exclude_if=omit_none)
    quote: str = Field(default="", validation_alias=catalan_alias("cita", "quote"), serialization_alias="cita")
    # One of SEVERITIES.
    severity: str = Field(
        default="", validation_alias=catalan_alias("gravetat", "severity"), serialization_alias="gravetat"
    )
    explanation: str = Field(
        default="", validation_alias=catalan_alias("explicacio", "explanation"), serialization_alias="explicacio"
    )


class VerificationReport(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    findings: list[VerifierFinding] = Field(
        default_factory=list, validation_alias=catalan_alias("problemes", "findings"), serialization_alias="problemes"
    )
    assessment: str = Field(
        default="", validation_alias=catalan_alias("valoracio", "assessment"), serialization_alias="valoracio"
    )


class GraderVerdict(BaseModel):
    """The model's judgement of one annotation: which candidate error it describes and how good the reason is."""

    model_config = ConfigDict(serialize_by_alias=True)

    annotation: str = Field(validation_alias=catalan_alias("anotacio", "annotation"), serialization_alias="anotacio")
    mistake: str = Field(
        default=NO_MISTAKE, validation_alias=catalan_alias("error", "mistake"), serialization_alias="error"
    )
    # One of EXPLANATION_GRADES; anything else is scored as NO_EXPLANATION.
    explanation: str = Field(
        default=NO_EXPLANATION,
        validation_alias=catalan_alias("explicacio", "explanation"),
        serialization_alias="explicacio",
    )
    feedback: str = ""


class GraderReport(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    verdicts: list[GraderVerdict] = Field(
        default_factory=list,
        validation_alias=catalan_alias("avaluacions", "verdicts"),
        serialization_alias="avaluacions",
    )
    summary: str = Field(default="", validation_alias=catalan_alias("resum", "summary"), serialization_alias="resum")


class DraftPart(BaseModel):
    """One part of the correct resolution as the writer sent it: a sheet step (problems) or a titled proof stage
    (theory)."""

    model_config = ConfigDict(serialize_by_alias=True)

    step: str = Field(default="", validation_alias=catalan_alias("pas", "step"), serialization_alias="pas")
    title: str = Field(default="", validation_alias=catalan_alias("titol", "title"), serialization_alias="titol")
    fragments: list[str] = Field(default_factory=list)


class ResolutionDraft(BaseModel):
    """The correct resolution in parts (stage A), before the code checks."""

    model_config = ConfigDict(serialize_by_alias=True)

    # Theory: the statement, which becomes the first part.
    statement: list[str] = Field(
        default_factory=list, validation_alias=catalan_alias("enunciat", "statement"), serialization_alias="enunciat"
    )
    parts: list[DraftPart] = Field(default_factory=list)


class DraftEdit(BaseModel):
    """One replacement in the correct text of a part: `original`, copied from the fragment, becomes `new`."""

    model_config = ConfigDict(serialize_by_alias=True)

    fragment: JsonScalar = None  # 1-based, inside the part
    original: str = ""
    new: str = Field(default="", validation_alias=catalan_alias("nou", "new"), serialization_alias="nou")


class CorruptionDraft(BaseModel):
    """The error put into one part (stage B): the first edit is the error, the later ones its local consequences."""

    model_config = ConfigDict(serialize_by_alias=True)

    # False: the model found no believable error for this part. `bool` first, so `false` is not read as 0.
    fit: bool | JsonScalar = Field(
        default=True, validation_alias=catalan_alias("apte", "fit"), serialization_alias="apte"
    )
    edits: list[DraftEdit] = Field(
        default_factory=list, validation_alias=catalan_alias("canvis", "edits"), serialization_alias="canvis"
    )
    quote: str = Field(default="", validation_alias=catalan_alias("cita", "quote"), serialization_alias="cita")
    kind: str | None = Field(default=None, validation_alias=catalan_alias("tipus", "kind"), serialization_alias="tipus")
    explanation: str = Field(
        default="", validation_alias=catalan_alias("explicacio", "explanation"), serialization_alias="explicacio"
    )
    correction: str = Field(
        default="", validation_alias=catalan_alias("correccio", "correction"), serialization_alias="correccio"
    )
    hint: str = Field(default="", validation_alias=catalan_alias("pista", "hint"), serialization_alias="pista")


class ResolutionReport(VerificationReport):
    """The blind check of the correct resolution (stage A)."""

    reaches_result: bool | JsonScalar = Field(
        default=False,
        validation_alias=catalan_alias("arriba_al_resultat", "reaches_result"),
        serialization_alias="arriba_al_resultat",
    )


class PartReport(VerificationReport):
    """The blind check of one corrupted part (stage C)."""

    # Non-empty: the verifier thinks the earlier parts, given to it as correct context, are wrong.
    context_alert: str = Field(
        default="",
        validation_alias=catalan_alias("alerta_context", "context_alert"),
        serialization_alias="alerta_context",
    )
