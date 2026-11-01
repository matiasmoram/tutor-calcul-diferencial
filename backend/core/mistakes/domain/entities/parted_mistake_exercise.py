"""A "troba l'error" document reviewed one part at a time ("Pas a pas"): the correct resolution split into parts,
some of which carry exactly one local, declared error put into the correct text. The student reviews the flawed
parts in order, with every earlier part shown correct, so errors never compound.

Its JSON (Catalan keys, ``"format": "per_parts"``) is a stored-document contract like ``MistakeExercise``'s; the
two share the files tree and the ``mistake_exercises.data`` column, told apart by ``format`` (see
``MistakeDocument``)."""

from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Discriminator, Field, Tag, TypeAdapter, model_validator

from core.mistakes.domain.entities.mistake_exercise import DeclaredMistake, MistakeExercise, SourceId, Verification
from core.mistakes.domain.exceptions import UnknownMistakePartException
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.mistake_exercise_id import MistakeExerciseId
from core.mistakes.domain.values.mistake_kind import SourceKind
from core.shared.domain.contract import catalan_alias, omit_none

STATEMENT_TITLE = "Enunciat"  # the title of a theory document's first part


class MistakePart(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    title: str = Field(validation_alias=catalan_alias("titol", "title"), serialization_alias="titol")
    # Problems: the sheet step this part writes out; "" for theory.
    step: str = Field(default="", validation_alias=catalan_alias("pas", "step"), serialization_alias="pas")
    fragments: list[str]  # the correct text
    # Flawed parts only: the text with the error, the error (numbered like every fragment of the document) and the
    # blind check of the part.
    flawed_fragments: list[str] | None = Field(
        default=None,
        validation_alias=catalan_alias("fragments_errats", "flawed_fragments"),
        serialization_alias="fragments_errats",
        exclude_if=omit_none,
    )
    mistake: DeclaredMistake | None = Field(
        default=None,
        validation_alias=catalan_alias("error", "mistake"),
        serialization_alias="error",
        exclude_if=omit_none,
    )
    verification: Verification | None = Field(
        default=None,
        validation_alias=catalan_alias("verificacio", "verification"),
        serialization_alias="verificacio",
        exclude_if=omit_none,
    )


class PartText(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    part: int
    fragments: list[str]


class PartOutline(BaseModel):
    """One entry of the roadmap the student sees from the start: titles only, and which parts they will review."""

    model_config = ConfigDict(serialize_by_alias=True)

    part: int
    title: str = Field(validation_alias=catalan_alias("titol", "title"), serialization_alias="titol")
    review: bool = Field(validation_alias=catalan_alias("revisar", "review"), serialization_alias="revisar")


class PartToReview(BaseModel):
    """The next flawed part as the student gets it: its flawed text, and the correct text of the parts between the
    previous review and this one. Never its error, its correct text nor anything after it."""

    model_config = ConfigDict(serialize_by_alias=True)

    part: int
    first_fragment: int = Field(
        validation_alias=catalan_alias("primer_fragment", "first_fragment"), serialization_alias="primer_fragment"
    )
    fragments: list[str]
    earlier: list[PartText] = Field(
        validation_alias=catalan_alias("anteriors", "earlier"), serialization_alias="anteriors"
    )


class PartView(BaseModel):
    """What the student has while reviewing one part, and what that part's grading sees: every earlier part
    correct, this part as shown (flawed if it has an error), nothing after it."""

    part: int
    fragments: list[str]
    mistakes: list[DeclaredMistake]  # this part's error, if any
    statement_fragments: int
    first_fragment: int  # of this part: the earlier fragments are context, not annotatable

    @property
    def annotatable(self) -> range:
        return range(self.first_fragment, len(self.fragments) + 1)


class PartedMistakeExercise(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    id: MistakeExerciseId
    source_id: SourceId = Field(validation_alias=catalan_alias("exercici", "source_id"), serialization_alias="exercici")
    source_kind: SourceKind = Field(
        default="problema", validation_alias=catalan_alias("font", "source_kind"), serialization_alias="font"
    )
    difficulty: Difficulty = Field(
        validation_alias=catalan_alias("dificultat", "difficulty"), serialization_alias="dificultat"
    )
    layout: Literal["per_parts"] = Field(
        default="per_parts", validation_alias=catalan_alias("format", "layout"), serialization_alias="format"
    )
    # Theory: the fragments of part 1, the statement. 0 for problems.
    statement_fragments: int = Field(
        default=0, validation_alias=catalan_alias("n_enunciat", "statement_fragments"), serialization_alias="n_enunciat"
    )
    parts: list[MistakePart]
    # The blind check of the correct resolution; each flawed part carries its own.
    verification: Verification = Field(
        validation_alias=catalan_alias("verificacio", "verification"), serialization_alias="verificacio"
    )
    created_at: float = Field(validation_alias=catalan_alias("creat", "created_at"), serialization_alias="creat")

    @model_validator(mode="after")
    def _consistent(self) -> Self:
        if len(self.parts) < 2:
            raise ValueError("a document in parts has at least 2 parts")
        if not self.flawed_parts:
            raise ValueError("no part has an error")
        if self.source_kind == "teoria":
            if self.statement_fragments < 1 or self.statement_fragments != len(self.parts[0].fragments):
                raise ValueError("theory: part 1 is the statement, n_enunciat is its number of fragments")
            if 1 not in self.flawed_parts:
                raise ValueError("theory: the statement (part 1) always has an error")
        elif self.statement_fragments != 0:
            raise ValueError("problems have no statement fragments")
        ids = [m.id for m in self.mistakes]
        if len(set(ids)) != len(ids):
            raise ValueError(f"error ids repeated: {ids}")
        first = 1
        for i, part in enumerate(self.parts, 1):
            if not part.fragments:
                raise ValueError(f"part {i} has no fragments")
            self._check_flawed(i, part, first)
            first += len(part.fragments)
        return self

    @staticmethod
    def _check_flawed(i: int, part: MistakePart, first: int) -> None:
        flawed, mistake = part.flawed_fragments, part.mistake
        if (flawed is None) != (mistake is None):
            raise ValueError(f"part {i}: the flawed text and the error go together")
        if flawed is None or mistake is None:
            return
        if len(flawed) != len(part.fragments):
            raise ValueError(
                f"part {i}: the flawed text has {len(flawed)} fragments, the correct one {len(part.fragments)}"
            )
        local = mistake.fragment - first + 1
        if not 1 <= local <= len(flawed):
            raise ValueError(f"part {i}: the error's fragment {mistake.fragment} is outside the part")
        text = flawed[local - 1]
        # An empty span is an error no annotation can ever overlap.
        if not 0 <= mistake.start < mistake.end <= len(text):
            raise ValueError(
                f"part {i}: the error's span [{mistake.start}, {mistake.end}) is empty or outside its text"
            )
        if text[mistake.start : mistake.end] != mistake.quote:
            raise ValueError(f"part {i}: the error's quote is not at its offsets")
        if text == part.fragments[local - 1]:
            raise ValueError(f"part {i}: the error's fragment is the correct one")

    @property
    def fragments(self) -> list[str]:
        """The whole correct resolution."""
        return [f for p in self.parts for f in p.fragments]

    @property
    def flawed_parts(self) -> list[int]:
        return [i for i, p in enumerate(self.parts, 1) if p.mistake is not None]

    @property
    def mistakes(self) -> list[DeclaredMistake]:
        return [p.mistake for p in self.parts if p.mistake is not None]

    @property
    def n_mistakes(self) -> int:
        return len(self.flawed_parts)

    def part(self, number: int) -> MistakePart:
        """Parts are numbered from 1. Raises UnknownMistakePartException."""
        if not 1 <= number <= len(self.parts):
            raise UnknownMistakePartException(number)
        return self.parts[number - 1]

    def part_range(self, number: int) -> range:
        """The document-wide fragment numbers of the part."""
        part = self.part(number)
        start = 1 + sum(len(p.fragments) for p in self.parts[: number - 1])
        return range(start, start + len(part.fragments))

    def view(self, number: int) -> PartView:
        part = self.part(number)
        earlier = [f for p in self.parts[: number - 1] for f in p.fragments]
        return PartView(
            part=number,
            fragments=[*earlier, *(part.flawed_fragments if part.flawed_fragments is not None else part.fragments)],
            mistakes=[part.mistake] if part.mistake is not None else [],
            statement_fragments=self.statement_fragments,
            first_fragment=len(earlier) + 1,
        )

    def outline(self) -> list[PartOutline]:
        flawed = set(self.flawed_parts)
        return [PartOutline(part=i, title=p.title, review=i in flawed) for i, p in enumerate(self.parts, 1)]

    def review_after(self, graded: int) -> PartToReview | None:
        """The first flawed part after part `graded` (0: the first of all), with the parts in between, correct."""
        number = next((i for i in self.flawed_parts if i > graded), None)
        if number is None:
            return None
        return PartToReview(
            part=number,
            first_fragment=self.part_range(number).start,
            fragments=self.part(number).flawed_fragments or [],
            earlier=[PartText(part=i, fragments=self.parts[i - 1].fragments) for i in range(graded + 1, number)],
        )

    def resolution(self) -> list[PartText]:
        """Every part, correct: revealed once the last flawed part is graded."""
        return [PartText(part=i, fragments=p.fragments) for i, p in enumerate(self.parts, 1)]


def _layout_of(value: object) -> str:
    if isinstance(value, dict):
        return str(value.get("format", value.get("layout", "sencer")))
    return str(getattr(value, "layout", "sencer"))


# A stored document of either layout. Documents without `format` are "sencer" ones.
type MistakeDocument = Annotated[
    Annotated[MistakeExercise, Tag("sencer")] | Annotated[PartedMistakeExercise, Tag("per_parts")],
    Discriminator(_layout_of),
]
MISTAKE_DOCUMENT_ADAPTER: TypeAdapter[MistakeDocument] = TypeAdapter(MistakeDocument)
