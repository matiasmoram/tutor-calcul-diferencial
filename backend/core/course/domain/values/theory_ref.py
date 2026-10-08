import re

from core.shared.domain.checked_value import CheckedStr
from core.shared.domain.ids import TheoryItemId


class TheoryRef(CheckedStr):
    """A citation of the notes in a sheet: ``T3.12`` (statement only) or ``T3.12+dem`` (statement and proof)."""

    PATTERN = re.compile(r"(T[1-9]\.x?\d+)(\+dem)?")

    @property
    def item_id(self) -> TheoryItemId:
        return TheoryItemId(self.removesuffix("+dem"))

    @property
    def with_proof(self) -> bool:
        return self.endswith("+dem")
