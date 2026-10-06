"""Validate solution sheets: structure, theory references, leak regexes, LaTeX delimiters.

    python scripts/check_fitxes.py                      # every list in backend/exercicis/
    python scripts/check_fitxes.py chunk.yaml --tema 3  # a file holding only `problemes:` (authoring chunks)

Exit code 1 if any problem is found.
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from tutor.fitxes import Exercici, load_llistes  # noqa: E402
from tutor.teoria import load_teoria, parse_ref  # noqa: E402

ID = re.compile(r"^t[1-6]-\d+[a-z]?$")


def _dollars_balanced(text: str) -> bool:
    return len(re.findall(r"(?<!\\)\$", text)) % 2 == 0


def problems_of(ex: Exercici, teoria: dict) -> list[str]:
    out: list[str] = []
    if not ID.match(ex.id):
        out.append(f"id must look like t3-5 or t2-4c, got {ex.id!r}")
    if len(ex.passos) < 2:
        out.append("needs at least 2 steps")
    if len(ex.errors_comuns) < 2:
        out.append("needs at least 2 common errors")
    texts = {"enunciat": ex.enunciat, "preambul": ex.preambul, "resultat": ex.resultat.valor}
    for p in ex.passos:
        texts |= {f"{p.id}.{k}": getattr(p, k) for k in ("titol", "objectiu", "idea", "detall")}
        if p.fuites and not any(re.search(r, p.detall, re.IGNORECASE) for r in p.fuites):
            out.append(f"step {p.id}: no leak regex matches its own detall")
        for r in p.fuites + ex.resultat.fuites:
            for field in ("objectiu", "idea"):
                if re.search(r, getattr(p, field), re.IGNORECASE):
                    out.append(f"step {p.id}: {field} matches banned regex {r!r}")
    for e in ex.errors_comuns:
        texts |= {f"error {e.id}": e.descripcio + " " + e.pregunta}
        for r in ex.resultat.fuites:
            if re.search(r, e.pregunta, re.IGNORECASE):
                out.append(f"error {e.id}: Socratic question reveals the result ({r!r})")
        # The question is the fallback reply when every draft is rejected: if it matches a step's
        # banned content, the guard blocks it whenever that step is not yet allowed.
        for p in ex.passos:
            for r in p.fuites:
                if re.search(r, e.pregunta, re.IGNORECASE):
                    out.append(f"error {e.id}: Socratic question matches banned regex of step {p.id} ({r!r})")
    for name, text in texts.items():
        if not _dollars_balanced(text):
            out.append(f"{name}: unbalanced $")
    for r in ex.all_refs():
        if parse_ref(r)[0] not in teoria:
            out.append(f"unknown theory reference {r}")
    if not ex.all_refs():
        out.append("cites no theory at all (add the definitions/results it uses)")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("--tema", type=int)
    args = ap.parse_args()
    teoria = load_teoria()

    if args.file:
        data = yaml.safe_load(Path(args.file).read_text(encoding="utf-8"))
        if "llista" not in data:
            data = {"llista": {"id": f"tema-{args.tema}", "etiqueta": f"Tema {args.tema}", "titol": "chunk",
                               "tema": args.tema}, "problemes": data["problemes"]}
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "chunk.yaml").write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
            _, exercicis = load_llistes(Path(d))
    else:
        _, exercicis = load_llistes()

    bad = 0
    for ex in exercicis.values():
        for p in problems_of(ex, teoria):
            print(f"{ex.id}: {p}")
            bad += 1
    print(f"{len(exercicis)} exercises checked, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
