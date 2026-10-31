"""A "troba l'error" document: a text split into numbered fragments with deliberate, declared errors.

Its JSON (Catalan keys) is a stored-document contract: the pre-generated files in ``backend/generats/errades`` and
the ``mistake_exercises.data`` column both hold ``MistakeExercise.model_dump(mode="json")``."""

from pydantic import BaseModel, ConfigDict, Field

from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.llm_outputs import VerifierFinding
from core.mistakes.domain.values.mistake_exercise_id import MistakeExerciseId
from core.mistakes.domain.values.mistake_kind import SourceKind
from core.shared.domain.contract import catalan_alias, omit_none
from core.shared.domain.ids import ExerciseId, TheoryItemId
from core.shared.domain.model_usage import ModelUsage

type SourceId = ExerciseId | TheoryItemId


class DeclaredMistake(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    id: str  # "e1", "e2", ...
    fragment: int  # 1-based
    quote: str = Field(validation_alias=catalan_alias("cita", "quote"), serialization_alias="cita")
    # Character offsets of the quote inside the fragment text.
    start: int = Field(validation_alias=catalan_alias("inici", "start"), serialization_alias="inici")
    end: int = Field(validation_alias=catalan_alias("fi", "end"), serialization_alias="fi")
    kind: str = Field(validation_alias=catalan_alias("tipus", "kind"), serialization_alias="tipus")
    explanation: str = Field(
        validation_alias=catalan_alias("explicacio", "explanation"), serialization_alias="explicacio"
    )
    correction: str = Field(validation_alias=catalan_alias("correccio", "correction"), serialization_alias="correccio")
    hint: str = Field(validation_alias=catalan_alias("pista", "hint"), serialization_alias="pista")


class GenerationAttempt(BaseModel):
    """One round of generate → validate → (verify). Absent keys stay absent: attempts rejected by validation never
    reached the verifier."""

    model_config = ConfigDict(serialize_by_alias=True)

    attempt: int = Field(validation_alias=catalan_alias("intent", "attempt"), serialization_alias="intent")
    generation: ModelUsage = Field(
        validation_alias=catalan_alias("generacio", "generation"), serialization_alias="generacio"
    )
    validation: list[str] = Field(
        validation_alias=catalan_alias("validacio", "validation"), serialization_alias="validacio"
    )
    verification: ModelUsage | None = Field(
        default=None,
        validation_alias=catalan_alias("verificacio", "verification"),
        serialization_alias="verificacio",
        exclude_if=omit_none,
    )
    verifier_findings: list[VerifierFinding] | None = Field(
        default=None,
        validation_alias=catalan_alias("problemes_verificador", "verifier_findings"),
        serialization_alias="problemes_verificador",
        exclude_if=omit_none,
    )
    discrepancies: list[str] | None = Field(default=None, exclude_if=omit_none)


class Verification(BaseModel):
    """How the document was checked: by the model pipeline ("llm", with its attempts) or offline (with its batch)."""

    model_config = ConfigDict(serialize_by_alias=True)

    origin: str = Field(validation_alias=catalan_alias("origen", "origin"), serialization_alias="origen")
    batch: str | None = Field(
        default=None, validation_alias=catalan_alias("lot", "batch"), serialization_alias="lot", exclude_if=omit_none
    )
    assessment: str = Field(
        default="", validation_alias=catalan_alias("valoracio", "assessment"), serialization_alias="valoracio"
    )
    findings: list[VerifierFinding] = Field(
        default_factory=list, validation_alias=catalan_alias("problemes", "findings"), serialization_alias="problemes"
    )
    attempts: list[GenerationAttempt] | None = Field(
        default=None,
        validation_alias=catalan_alias("intents", "attempts"),
        serialization_alias="intents",
        exclude_if=omit_none,
    )
    # sha256 of the reference text (sheet or notes) the document was checked against; None when the document was not
    # checked against a hashed reference.
    reference_hash: str | None = Field(
        default=None,
        validation_alias=catalan_alias("hash_referencia", "reference_hash"),
        serialization_alias="hash_referencia",
        exclude_if=omit_none,
    )


class MistakeExercise(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    id: MistakeExerciseId
    source_id: SourceId = Field(validation_alias=catalan_alias("exercici", "source_id"), serialization_alias="exercici")
    source_kind: SourceKind = Field(
        default="problema", validation_alias=catalan_alias("font", "source_kind"), serialization_alias="font"
    )
    difficulty: Difficulty = Field(
        validation_alias=catalan_alias("dificultat", "difficulty"), serialization_alias="dificultat"
    )
    fragments: list[str]
    # Theory: the first `statement_fragments` fragments are the statement, the rest the proof. 0 for problems.
    statement_fragments: int = Field(
        default=0, validation_alias=catalan_alias("n_enunciat", "statement_fragments"), serialization_alias="n_enunciat"
    )
    mistakes: list[DeclaredMistake] = Field(
        validation_alias=catalan_alias("errors", "mistakes"), serialization_alias="errors"
    )
    verification: Verification = Field(
        validation_alias=catalan_alias("verificacio", "verification"), serialization_alias="verificacio"
    )
    created_at: float = Field(validation_alias=catalan_alias("creat", "created_at"), serialization_alias="creat")

    @property
    def n_mistakes(self) -> int:
        return len(self.mistakes)

    def mistakes_in(self, fragment: int) -> list[DeclaredMistake]:
        return [m for m in self.mistakes if m.fragment == fragment]
