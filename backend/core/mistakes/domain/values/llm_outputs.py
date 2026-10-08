"""What the model stages answer, as typed values. Keys and enum values are Catalan: they are the JSON schema contract
(infra/llm_schemas.py) and, for the verifier's findings, part of the stored documents.

The generator's and verifier's answers are validated by code (domain/generation_checks.py), which reports a malformed
answer as a reason to regenerate; so the fields the checks inspect keep whatever JSON type the model sent
(``fragment: int | float | str | None``) instead of failing on parse."""

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

type JsonScalar = int | float | str | None


def _ca(catalan: str, english: str) -> AliasChoices:
    return AliasChoices(catalan, english)


def _is_none(value: object) -> bool:
    return value is None


class DraftMistake(BaseModel):
    """One error as the generator declared it, before validation."""

    model_config = ConfigDict(serialize_by_alias=True)

    fragment: JsonScalar = None  # 1-based
    quote: str = Field(default="", validation_alias=_ca("cita", "quote"), serialization_alias="cita")
    kind: str | None = Field(default=None, validation_alias=_ca("tipus", "kind"), serialization_alias="tipus")
    explanation: str = Field(
        default="", validation_alias=_ca("explicacio", "explanation"), serialization_alias="explicacio"
    )
    correction: str = Field(
        default="", validation_alias=_ca("correccio", "correction"), serialization_alias="correccio"
    )
    hint: str = Field(default="", validation_alias=_ca("pista", "hint"), serialization_alias="pista")


class GenerationDraft(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    fragments: list[str] = Field(default_factory=list)
    mistakes: list[DraftMistake] = Field(
        default_factory=list, validation_alias=_ca("errors", "mistakes"), serialization_alias="errors"
    )
    # Theory documents: how many leading fragments are the statement.
    statement_fragments: JsonScalar = Field(
        default=0, validation_alias=_ca("n_enunciat", "statement_fragments"), serialization_alias="n_enunciat"
    )


class VerifierFinding(BaseModel):
    """One problem the blind verifier found. Stored verbatim in the document's verification."""

    model_config = ConfigDict(serialize_by_alias=True)

    fragment: JsonScalar = Field(default=None, exclude_if=_is_none)
    quote: str = Field(default="", validation_alias=_ca("cita", "quote"), serialization_alias="cita")
    # "error" | "consequencia" | "imprecisio"
    severity: str = Field(default="", validation_alias=_ca("gravetat", "severity"), serialization_alias="gravetat")
    explanation: str = Field(
        default="", validation_alias=_ca("explicacio", "explanation"), serialization_alias="explicacio"
    )


class VerificationReport(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    findings: list[VerifierFinding] = Field(
        default_factory=list, validation_alias=_ca("problemes", "findings"), serialization_alias="problemes"
    )
    assessment: str = Field(
        default="", validation_alias=_ca("valoracio", "assessment"), serialization_alias="valoracio"
    )


class GraderVerdict(BaseModel):
    """The model's judgement of one annotation: which candidate error it describes and how good the reason is."""

    model_config = ConfigDict(serialize_by_alias=True)

    annotation: str = Field(validation_alias=_ca("anotacio", "annotation"), serialization_alias="anotacio")
    mistake: str = Field(default="cap", validation_alias=_ca("error", "mistake"), serialization_alias="error")
    # "correcta" | "parcial" | "incorrecta" | "absent"; anything else is scored as "absent".
    explanation: str = Field(
        default="absent", validation_alias=_ca("explicacio", "explanation"), serialization_alias="explicacio"
    )
    feedback: str = ""


class GraderReport(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    verdicts: list[GraderVerdict] = Field(
        default_factory=list, validation_alias=_ca("avaluacions", "verdicts"), serialization_alias="avaluacions"
    )
    summary: str = Field(default="", validation_alias=_ca("resum", "summary"), serialization_alias="resum")
