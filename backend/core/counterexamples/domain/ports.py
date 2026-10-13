from collections.abc import Sequence
from typing import Protocol

from core.counterexamples.domain.entities.spec import SpecCatalog
from core.counterexamples.domain.values.submission import PropertyCheck
from core.counterexamples.domain.values.verdict import PropertyVerdict


class PropertyChecker(Protocol):
    """Decides each property for a submission, in order. Never raises on bad maths: undecidable is 'indeterminat'."""

    async def check(self, checks: Sequence[PropertyCheck]) -> list[PropertyVerdict]: ...


class SpecSource(Protocol):
    def load(self) -> SpecCatalog: ...
