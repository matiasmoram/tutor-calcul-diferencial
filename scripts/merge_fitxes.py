"""Merge authoring chunks (work/fitxes/temaN_pK.yaml) into one list per tema (backend/exercicis/temaN.yaml).

    python scripts/merge_fitxes.py            # every tema with at least one chunk
    python scripts/merge_fitxes.py 2 3        # only these temes

The list header comes from the transcribed statements (work/enunciats/temaN.yaml). Problems are sorted by number;
a problem present in two chunks is an error.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CHUNKS = ROOT / "work" / "fitxes"
ENUNCIATS = ROOT / "work" / "enunciats"
OUT = ROOT / "backend" / "exercicis"


def _str_repr(dumper: yaml.Dumper, data: str):
    # Multi-line prose as block scalars, so the merged file stays as readable as the chunks.
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


yaml.add_representer(str, _str_repr, Dumper=yaml.SafeDumper)


def merge(tema: int) -> Path | None:
    chunks = sorted(CHUNKS.glob(f"tema{tema}_p*.yaml"))
    if not chunks:
        return None
    problemes: dict[int, dict] = {}
    for c in chunks:
        for p in yaml.safe_load(c.read_text(encoding="utf-8"))["problemes"]:
            if p["num"] in problemes:
                raise ValueError(f"problem {p['num']} of tema {tema} appears in two chunks ({c.name})")
            problemes[p["num"]] = p
    enunciats = yaml.safe_load((ENUNCIATS / f"tema{tema}.yaml").read_text(encoding="utf-8"))
    missing = sorted({p["num"] for p in enunciats["problemes"]} - set(problemes))
    data = {
        "llista": {
            "id": f"tema-{tema}",
            "etiqueta": f"Tema {tema}",
            "titol": re.sub(r"^Tema\s*\d+\s*[:.]\s*", "", enunciats["titol"]),
            "descripcio": f"Problemes del Tema {tema} de la col·lecció de Càlcul Diferencial (FME-UPC).",
            "tema": tema,
            "tipus": "mixt",
            "format": "text",
        },
        "problemes": [problemes[n] for n in sorted(problemes)],
    }
    out = OUT / f"tema{tema}.yaml"
    header = f"# Tema {tema}: generat per scripts/merge_fitxes.py a partir de work/fitxes/tema{tema}_p*.yaml\n"
    out.write_text(header + yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    n_ex = sum(len(p["exercicis"]) for p in data["problemes"])
    print(f"tema {tema}: {len(problemes)} problems, {n_ex} exercises -> {out.name}"
          + (f"  (missing problems: {missing})" if missing else ""))
    return out


def main() -> None:
    temes = [int(a) for a in sys.argv[1:]] or range(1, 7)
    for t in temes:
        merge(t)


if __name__ == "__main__":
    main()
