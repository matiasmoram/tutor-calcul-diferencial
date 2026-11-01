from collections.abc import Collection, Mapping, Sequence
from typing import Literal

from pydantic import BaseModel, Field

from core.shared.domain.ids import TheoryItemId

# Item kinds as the notes name them (authored data, Catalan).
TheoryItemKind = Literal[
    "definicio", "teorema", "proposicio", "lema", "corollari", "observacio", "exemple", "exercici", "nota", "text"
]
KIND_NAMES: Mapping[str, str] = {
    "definicio": "Definició",
    "teorema": "Teorema",
    "proposicio": "Proposició",
    "lema": "Lema",
    "corollari": "Corol·lari",
    "observacio": "Observació",
    "exemple": "Exemple",
    "exercici": "Exercici",
    "nota": "Nota",
    "text": "Text",
}


class TheoryItem(BaseModel):
    """One item of the course notes (Temes 1-6), transcribed to Markdown + LaTeX.

    Sheets cite items by id ("T3.12"); each stage receives only the cited items, never the whole notes."""

    id: TheoryItemId
    topic: int
    kind: TheoryItemKind
    number: int | None = None
    summary_ref: int | str | None = None  # margin number(s) linking to the "Resum de teoria"
    section: str = ""
    page: int | None = None
    name: str = ""
    statement: str
    proof: str = ""
    problems: list[str] = Field(default_factory=list)  # problems of the collection this item cites ("T2.4")

    @property
    def label(self) -> str:
        """How the notes name it: 'Teorema 12 (Tema 3)'."""
        if self.number is None:
            return f"Apunts del Tema {self.topic}, §{self.section}"
        return f"{KIND_NAMES[self.kind]} {self.number} (Tema {self.topic})"

    @property
    def citable(self) -> bool:
        """Numbered items other than exercises: the ones a reply can cite by name."""
        return self.number is not None and self.kind != "exercici"

    def render(self, with_proof: bool = False) -> str:
        head = f"[{self.id}] {self.label}" + (f" — {self.name}" if self.name else "")
        text = f"{head}\n{self.statement.strip()}"
        if with_proof and self.proof:
            text += f"\nDemostració: {self.proof.strip()}"
        return text

    def index_line(self) -> str:
        return f"{self.id} {self.label}: {self.name}"


def render_items(items: Sequence[TheoryItem], with_proof: Collection[TheoryItemId] = frozenset()) -> str:
    """The items as the prompts show them, the ones in `with_proof` with their proof; "(cap)" when there are none."""
    return "\n\n".join(it.render(with_proof=it.id in with_proof) for it in items) or "(cap)"
