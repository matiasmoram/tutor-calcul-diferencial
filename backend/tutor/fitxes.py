"""Loading and validation of exercise sheets ("fitxes").

One YAML file per tema (`exercicis/temaN.yaml`): a `llista:` header and a list of `problemes`,
each with its shared statement (`preambul`) and one sheet per sub-part (`exercicis`).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, field_validator

from .teoria import ItemTeoria, parse_ref

EXERCICIS_DIR = Path(__file__).resolve().parent.parent / "exercicis"


def _check_regexes(patterns: list[str]) -> list[str]:
    for p in patterns:
        re.compile(p)
    return patterns


def _check_refs(refs: list[str]) -> list[str]:
    for r in refs:
        parse_ref(r)
    return refs


class Pas(BaseModel):
    id: str
    titol: str
    objectiu: str
    idea: str
    detall: str
    fuites: list[str] = Field(default_factory=list)
    # Course results this step uses. Shown to the reply stage once the strategy may be named (level >= 2).
    teoria: list[str] = Field(default_factory=list)

    @field_validator("fuites")
    @classmethod
    def _valid_regexes(cls, v: list[str]) -> list[str]:
        return _check_regexes(v)

    @field_validator("teoria")
    @classmethod
    def _valid_refs(cls, v: list[str]) -> list[str]:
        return _check_refs(v)


class ErrorComu(BaseModel):
    id: str
    descripcio: str
    pregunta: str


class Resultat(BaseModel):
    valor: str
    fuites: list[str] = Field(default_factory=list)

    @field_validator("fuites")
    @classmethod
    def _valid_regexes(cls, v: list[str]) -> list[str]:
        return _check_regexes(v)


class Exercici(BaseModel):
    id: str
    llista: str = ""
    grup: str = ""
    tema: int | None = None
    problema: int = 0
    apartat: str | None = None
    etiqueta: str = ""
    tipus: Literal["calcul", "teoric"] = "calcul"
    format: Literal["latex", "text"] = "text"
    font: str | None = None
    preambul: str = ""
    indicacio: str = ""
    enunciat: str
    resultat: Resultat
    passos: list[Pas]
    errors_comuns: list[ErrorComu]
    # Background theory (definitions the statement relies on): safe to show from the first turn.
    teoria: list[str] = Field(default_factory=list)
    # Theory that solves this very exercise (e.g. a worked example in the notes): grading stages only.
    teoria_reservada: list[str] = Field(default_factory=list)
    nota_professor: str = ""

    @field_validator("passos")
    @classmethod
    def _unique_steps(cls, v: list[Pas]) -> list[Pas]:
        ids = [p.id for p in v]
        if len(ids) != len(set(ids)) or not ids:
            raise ValueError(f"step ids must be non-empty and unique: {ids}")
        return v

    @field_validator("teoria", "teoria_reservada")
    @classmethod
    def _valid_refs(cls, v: list[str]) -> list[str]:
        return _check_refs(v)

    @property
    def step_ids(self) -> list[str]:
        return [p.id for p in self.passos]

    @property
    def error_ids(self) -> list[str]:
        return [e.id for e in self.errors_comuns]

    def pas(self, step_id: str) -> Pas:
        return next(p for p in self.passos if p.id == step_id)

    def error(self, error_id: str) -> ErrorComu:
        return next(e for e in self.errors_comuns if e.id == error_id)

    def all_refs(self) -> list[str]:
        """Every theory reference of the sheet, in order, without duplicates."""
        refs = self.teoria + [r for p in self.passos for r in p.teoria] + self.teoria_reservada
        return list(dict.fromkeys(refs))

    def reserved_ids(self, teoria: dict[str, ItemTeoria]) -> set[str]:
        """Items the reply stage must never see: declared ones, plus any item of the notes that cites this problem."""
        own = f"T{self.tema}.{self.problema}"
        auto = {it.id for it in teoria.values() if own in it.problemes} if self.tema else set()
        return {parse_ref(r)[0] for r in self.teoria_reservada} | auto

    def full_reference(self) -> str:
        """Full solution sheet as text. Only the diagnosis and guard stages see this."""
        lines = [
            f"ENUNCIAT: {self.enunciat_md()}",
            f"RESULTAT CORRECTE: {self.resultat.valor.strip()}",
            "PASSOS DE LA SOLUCIÓ (en ordre):",
        ]
        for i, p in enumerate(self.passos, 1):
            lines.append(f"  {i}. [{p.id}] {p.titol}" + (f"  (teoria: {', '.join(p.teoria)})" if p.teoria else ""))
            lines.append(f"     objectiu: {p.objectiu.strip()}")
            lines.append(f"     idea: {p.idea.strip()}")
            lines.append(f"     detall: {p.detall.strip()}")
        lines.append("ERRORS COMUNS:")
        for e in self.errors_comuns:
            lines.append(f"  - [{e.id}] {e.descripcio.strip()}")
        return "\n".join(lines)

    def enunciat_md(self) -> str:
        """Statement as prose with $...$ math, whatever the source format; includes the shared preamble."""
        own = f"${self.enunciat}$" if self.format == "latex" else self.enunciat.strip()
        if self.preambul.strip():
            own = f"{self.preambul.strip()}\n\n({self.apartat}) {own}" if self.apartat else f"{self.preambul.strip()}\n\n{own}"
        if self.indicacio.strip() and self.indicacio.strip() not in own:
            own += f"\n\nIndicació: {self.indicacio.strip()}"
        return own

    def public(self) -> dict:
        return {
            "id": self.id,
            "llista": self.llista,
            "grup": self.grup,
            "tema": self.tema,
            "problema": self.problema,
            "apartat": self.apartat,
            "etiqueta": self.etiqueta,
            "tipus": self.tipus,
            "format": self.format,
            "font": self.font,
            "preambul": self.preambul.strip(),
            "indicacio": self.indicacio.strip(),
            "enunciat": self.enunciat.strip(),
        }


class Problema(BaseModel):
    num: int
    font: str | None = None
    preambul: str = ""
    indicacio: str | None = None
    exercicis: list[str] = Field(default_factory=list)


class Llista(BaseModel):
    id: str
    etiqueta: str
    titol: str
    descripcio: str = ""
    tema: int | None = None
    tipus: Literal["calcul", "teoric", "mixt"] = "mixt"
    format: Literal["latex", "text"] = "text"
    exercicis: list[str] = Field(default_factory=list)
    problemes: list[Problema] = Field(default_factory=list)

    def public(self) -> dict:
        return self.model_dump(exclude={"problemes"}) | {
            "n_exercicis": len(self.exercicis),
            "n_problemes": len(self.problemes),
        }


def _exercici(llista: Llista, prob: Problema, raw: dict) -> Exercici:
    apartat = raw.get("apartat")
    defaults = {
        "llista": llista.id,
        "grup": llista.titol,
        "tema": llista.tema,
        "problema": prob.num,
        "format": llista.format,
        "font": prob.font,
        "preambul": prob.preambul,
        "indicacio": prob.indicacio or "",
        "etiqueta": f"{prob.num}({apartat})" if apartat else str(prob.num),
    }
    return Exercici(**(defaults | raw))


def load_llistes(
    directory: Path = EXERCICIS_DIR, teoria: dict[str, ItemTeoria] | None = None
) -> tuple[dict[str, Llista], dict[str, Exercici]]:
    """Load every list. With `teoria`, also check that every cited theory item exists."""
    llistes: dict[str, Llista] = {}
    exercicis: dict[str, Exercici] = {}
    for path in sorted(directory.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        llista = Llista(**data["llista"])
        if llista.id in llistes:
            raise ValueError(f"duplicate list id {llista.id} in {path}")
        for raw_prob in data["problemes"]:
            prob = Problema(**{k: v for k, v in raw_prob.items() if k != "exercicis" and v is not None})
            for raw in raw_prob["exercicis"]:
                ex = _exercici(llista, prob, {k: v for k, v in raw.items() if v is not None})
                if ex.id in exercicis:
                    raise ValueError(f"duplicate exercise id {ex.id} in {path}")
                if teoria is not None:
                    missing = [r for r in ex.all_refs() if parse_ref(r)[0] not in teoria]
                    if missing:
                        raise ValueError(f"{ex.id}: unknown theory references {missing}")
                exercicis[ex.id] = ex
                prob.exercicis.append(ex.id)
                llista.exercicis.append(ex.id)
            llista.problemes.append(prob)
        llistes[llista.id] = llista
    return llistes, exercicis


def load_exercicis(directory: Path = EXERCICIS_DIR) -> dict[str, Exercici]:
    return load_llistes(directory)[1]
