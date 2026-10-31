from typing import Protocol

from core.mistakes.domain.entities.mistake_exercise import DeclaredMistake


class GradableText(Protocol):
    """What a student annotates and gets graded on: a whole document ("sencer") or the view of one part
    ("per_parts"). Fragments are numbered from 1 across the whole document."""

    @property
    def fragments(self) -> list[str]: ...

    @property
    def statement_fragments(self) -> int: ...

    @property
    def mistakes(self) -> list[DeclaredMistake]:
        """The errors this grading counts."""
        ...

    @property
    def annotatable(self) -> range:
        """The fragment numbers an annotation may land on; annotations elsewhere are dropped."""
        ...
