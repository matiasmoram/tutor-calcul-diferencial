from collections.abc import Collection, Mapping
from typing import Literal

from pydantic import BaseModel, Field

from core.counterexamples.domain.exceptions import InvalidSpecContentException, UnknownSpecException
from core.counterexamples.domain.values.properties import PropertyKind
from core.counterexamples.domain.values.spec_id import SpecId
from core.counterexamples.domain.values.submission import Submission
from core.shared.domain.contract import catalan_alias
from core.shared.domain.ids import TheoryItemId

Difficulty = Literal["facil", "normal", "dificil"]  # same values as the quizzes (contexts do not share domains)


class Spec(BaseModel):
    """A challenge: build f with all these properties at the origin. `example` is an authored solution with its
    certificates; tests run it through the checker, and the student sees it only after passing."""

    id: SpecId
    topic: int = Field(validation_alias=catalan_alias("tema", "topic"))
    title: str = Field(validation_alias=catalan_alias("titol", "title"))
    statement: str = Field(validation_alias=catalan_alias("enunciat", "statement"))
    properties: list[PropertyKind] = Field(min_length=1, validation_alias=catalan_alias("propietats", "properties"))
    hint: str = Field(validation_alias=catalan_alias("pista", "hint"))
    difficulty: Difficulty = Field(validation_alias=catalan_alias("dificultat", "difficulty"))
    example: Submission = Field(validation_alias=catalan_alias("exemple", "example"))
    # Why the example works, shown with it.
    explanation: str = Field(validation_alias=catalan_alias("explicacio", "explanation"))
    # Items of the notes the challenge is about (definitions, the theorem whose converse fails): shown from the start.
    theory: list[TheoryItemId] = Field(default_factory=list, validation_alias=catalan_alias("teoria", "theory"))
    # Items of the notes that already contain a counterexample like the one asked for: shown only with the example.
    reserved_theory: list[TheoryItemId] = Field(
        default_factory=list, validation_alias=catalan_alias("teoria_reservada", "reserved_theory")
    )


class SpecCatalog(BaseModel):
    specs: Mapping[SpecId, Spec]
    # The items of the notes that define each property.
    property_theory: Mapping[PropertyKind, list[TheoryItemId]]

    def check_theory(self, known: Collection[str]) -> None:
        """Every cited item exists in the notes, and every property used has its definition."""
        cited = {i for items in self.property_theory.values() for i in items}
        for spec in self.specs.values():
            cited |= {*spec.theory, *spec.reserved_theory}
            for kind in spec.properties:
                if not self.property_theory.get(kind):
                    raise InvalidSpecContentException(f"Propietat «{kind}» sense ítems dels apunts")
        if missing := sorted(cited - set(known)):
            raise InvalidSpecContentException(f"Ítems dels apunts desconeguts: {', '.join(missing)}")

    def spec(self, spec_id: SpecId) -> Spec:
        try:
            return self.specs[spec_id]
        except KeyError:
            raise UnknownSpecException(spec_id) from None
