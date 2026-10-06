"""Course theory notes (Temes 1-6), transcribed to Markdown + LaTeX and split into numbered items.

Each sheet cites theory by id ("T3.12"). The pipeline injects only the cited items into each
stage, never the whole notes: a typical exercise needs 2-6 items (~0.3-1.5k tokens) instead of
a whole tema (~15-20k tokens).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal
from urllib.parse import quote

import yaml
from pydantic import BaseModel, Field

TEORIA_DIR = Path(__file__).resolve().parent.parent / "teoria"
# The original PDFs, served by the app under /pdf (see app.py).
SOURCES_DIR = Path(__file__).resolve().parent.parent.parent / "sources"
PDF_TEORIA = "Teoria/Càlcul_Diferencial_FME_Tema{tema}.pdf"
PDF_PROBLEMES = "Problemes/_Problemes Temes_1-6.pdf"


def pdf_url(rel: str, page: int | None = None) -> str:
    """URL of a source PDF, opened at `page` by the browser's viewer (#page=N)."""
    return "/pdf/" + quote(rel) + (f"#page={page}" if page else "")


TipusItem = Literal[
    "definicio", "teorema", "proposicio", "lema", "corollari", "observacio", "exemple", "exercici", "nota", "text"
]
NOMS_TIPUS = {
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
# "T3.12" -> statement only; "T3.12+dem" -> statement and proof.
REF = re.compile(r"^(T[1-6]\.(?:x)?\d+)(\+dem)?$")


class ItemTeoria(BaseModel):
    id: str
    tema: int = 0
    tipus: TipusItem
    num: int | None = None
    resum: int | str | None = None  # margin number(s) linking to the 'Resum de teoria'
    seccio: str = ""
    pagina: int | None = None
    nom: str = ""
    enunciat: str
    demostracio: str = ""
    problemes: list[str] = Field(default_factory=list)

    @property
    def etiqueta(self) -> str:
        """How the notes name it: 'Teorema 12 (Tema 3)'."""
        if self.num is None:
            return f"Apunts del Tema {self.tema}, §{self.seccio}"
        return f"{NOMS_TIPUS[self.tipus]} {self.num} (Tema {self.tema})"

    def render(self, amb_demostracio: bool = False) -> str:
        head = f"[{self.id}] {self.etiqueta}" + (f" — {self.nom}" if self.nom else "")
        text = f"{head}\n{self.enunciat.strip()}"
        if amb_demostracio and self.demostracio:
            text += f"\nDemostració: {self.demostracio.strip()}"
        return text

    def index_line(self) -> str:
        return f"{self.id} {self.etiqueta}: {self.nom}"

    def public(self) -> dict:
        return {
            "id": self.id,
            "tema": self.tema,
            "etiqueta": self.etiqueta,
            "nom": self.nom,
            "enunciat": self.enunciat.strip(),
            "demostracio": self.demostracio.strip(),
            "pagina": self.pagina,
            "resum": self.resum,
            "pdf": pdf_url(PDF_TEORIA.format(tema=self.tema), self.pagina),
        }

    def index_entry(self) -> dict:
        """Lightweight entry for the theory index and for linking citations in the chat."""
        return {"id": self.id, "tema": self.tema, "num": self.num, "tipus": self.tipus, "etiqueta": self.etiqueta,
                "nom": self.nom, "seccio": self.seccio, "pagina": self.pagina,
                "pdf": pdf_url(PDF_TEORIA.format(tema=self.tema), self.pagina)}


class Tema(BaseModel):
    tema: int
    titol: str
    seccions: list[dict] = Field(default_factory=list)
    items: list[ItemTeoria]


def load_teoria(directory: Path = TEORIA_DIR) -> dict[str, ItemTeoria]:
    items: dict[str, ItemTeoria] = {}
    for path in sorted(directory.glob("tema*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        # Transcriptions write `key: null` for absent optional fields: treat as absent.
        data["items"] = [{k: v for k, v in it.items() if v is not None} for it in data["items"]]
        tema = Tema(**data)
        for it in tema.items:
            it.tema = tema.tema
            if it.id in items:
                raise ValueError(f"duplicate theory id {it.id} in {path}")
            items[it.id] = it
    return items


def load_temes(directory: Path = TEORIA_DIR) -> list[dict]:
    """Tema headers (number, title, sections) for the theory section of the web."""
    temes = []
    for path in sorted(directory.glob("tema*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        temes.append({"tema": data["tema"], "titol": data["titol"], "seccions": data.get("seccions") or [],
                      "pdf": pdf_url(PDF_TEORIA.format(tema=data["tema"]))})
    return temes


def parse_ref(ref: str) -> tuple[str, bool]:
    m = REF.match(ref)
    if not m:
        raise ValueError(f"invalid theory reference {ref!r} (expected 'T3.12' or 'T3.12+dem')")
    return m.group(1), bool(m.group(2))


# Same pattern as the web's citation linker (frontend/app.js, CITA): "Teorema 12 del Tema 3", "Definició 6 (Tema 2)".
CITA = re.compile(
    r"\b(Definició|Teorema|Proposició|Lema|Corol·lari|Observació|Exemple|Exercici|Nota)\s+(\d+)(?:\s*\([a-z]\))?"
    r"(?:\s*\((?:del\s+)?[Tt]ema\s+(\d)\)|\s+del\s+[Tt]ema\s+(\d))?"
)


def cited_items(text: str, allowed: list[ItemTeoria], default_tema: int | None) -> list[str]:
    """Ids of the allowed items that `text` cites by name (a citation without tema refers to `default_tema`)."""
    by_key = {(NOMS_TIPUS[it.tipus], it.tema, it.num): it.id for it in allowed if it.num is not None}
    out: list[str] = []
    for m in CITA.finditer(text):
        tema = int(m.group(3) or m.group(4) or (default_tema or 0))
        item = by_key.get((m.group(1), tema, int(m.group(2))))
        if item and item not in out:
            out.append(item)
    return out


def index_tema(items: dict[str, ItemTeoria], tema: int) -> list[ItemTeoria]:
    """Citable items of one tema (numbered ones), for the diagnosis to pick from on concept questions."""
    return [it for it in items.values() if it.tema == tema and it.num is not None and it.tipus != "exercici"]
