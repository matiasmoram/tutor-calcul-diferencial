import re
from collections.abc import Iterable

from core.course.domain.entities.theory_item import KIND_NAMES, TheoryItem
from core.shared.domain.ids import TheoryItemId

# Same pattern as the web's citation linker (frontend/app.js, CITA): "Teorema 12 del Tema 3", "Definició 6 (Tema 2)".
CITATION = re.compile(
    r"\b(Definició|Teorema|Proposició|Lema|Corol·lari|Observació|Exemple|Exercici|Nota)\s+(\d+)(?:\s*\([a-z]\))?"
    r"(?:\s*\((?:del\s+)?[Tt]ema\s+(\d)\)|\s+del\s+[Tt]ema\s+(\d))?"
)


type CitationKey = tuple[str, int, int]  # kind name as the notes write it, topic, number


def citation_key(match: re.Match[str], default_topic: int | None) -> CitationKey:
    """What a CITATION match names; a citation without topic refers to `default_topic`."""
    return match.group(1), int(match.group(3) or match.group(4) or (default_topic or 0)), int(match.group(2))


def citation_keys(items: Iterable[TheoryItem]) -> dict[CitationKey, TheoryItemId]:
    """How a text cites each numbered item."""
    return {(KIND_NAMES[it.kind], it.topic, it.number): it.id for it in items if it.number is not None}


def cited_items(text: str, allowed: list[TheoryItem], default_topic: int | None) -> list[TheoryItemId]:
    """Ids of the allowed items that `text` cites by name (a citation without topic refers to `default_topic`)."""
    by_key = citation_keys(allowed)
    out: list[TheoryItemId] = []
    for m in CITATION.finditer(text):
        item = by_key.get(citation_key(m, default_topic))
        if item and item not in out:
            out.append(item)
    return out
