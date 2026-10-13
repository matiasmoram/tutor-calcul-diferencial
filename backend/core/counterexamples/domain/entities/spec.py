from collections.abc import Mapping
from typing import Literal

from pydantic import AliasChoices, BaseModel, Field

from core.counterexamples.domain.exceptions import UnknownSpecException
from core.counterexamples.domain.properties import PropertyKind
from core.counterexamples.domain.values.spec_id import SpecId
from core.counterexamples.domain.values.submission import Submission

Difficulty = Literal["facil", "normal", "dificil"]  # same values as the quizzes (contexts do not share domains)


def _ca(catalan: str, english: str) -> AliasChoices:
    return AliasChoices(catalan, english)


class Spec(BaseModel):
    """A challenge: build f with all these properties at the origin. `example` is an authored solution with its
    certificates; tests run it through the checker, and the student sees it only after passing."""

    id: SpecId
    topic: int = Field(validation_alias=_ca("tema", "topic"))
    title: str = Field(validation_alias=_ca("titol", "title"))
    statement: str = Field(validation_alias=_ca("enunciat", "statement"))
    properties: list[PropertyKind] = Field(min_length=1, validation_alias=_ca("propietats", "properties"))
    hint: str = Field(validation_alias=_ca("pista", "hint"))
    difficulty: Difficulty = Field(validation_alias=_ca("dificultat", "difficulty"))
    example: Submission = Field(validation_alias=_ca("exemple", "example"))
    # Why the example works, shown with it.
    explanation: str = Field(validation_alias=_ca("explicacio", "explanation"))


class SpecCatalog(BaseModel):
    specs: Mapping[SpecId, Spec]

    def spec(self, spec_id: SpecId) -> Spec:
        try:
            return self.specs[spec_id]
        except KeyError:
            raise UnknownSpecException(spec_id) from None
