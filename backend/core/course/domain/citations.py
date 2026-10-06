import re

from core.course.domain.entities.theory_item import KIND_NAMES, TheoryItem
from core.shared.domain.ids import TheoryItemId

# Same pattern as the web's citation linker (frontend/app.js, CITA): "Teorema 12 del Tema 3", "Definició 6 (Tema 2)".
CITATION = re.compile(
    r"\b(Definició|Teorema|Proposició|Lema|Corol·lari|Observació|Exemple|Exercici|Nota)\s+(\d+)(?:\s*\([a-z]\))?"
    r"(?:\s*\((?:del\s+)?[Tt]ema\s+(\d)\)|\s+del\s+[Tt]ema\s+(\d))?"
)


def cited_items(text: str, allowed: list[TheoryItem], default_topic: int | None) -> list[TheoryItemId]:
    """Ids of the allowed items that `text` cites by name (a citation without topic refers to `default_topic`)."""
    by_key = {(KIND_NAMES[it.kind], it.topic, it.number): it.id for it in allowed if it.number is not None}
    out: list[TheoryItemId] = []
    for m in CITATION.finditer(text):
        topic = int(m.group(3) or m.group(4) or (default_topic or 0))
        item = by_key.get((m.group(1), topic, int(m.group(2))))
        if item and item not in out:
            out.append(item)
    return out
