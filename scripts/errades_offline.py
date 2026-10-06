"""'Find the error' documents written offline (by an agent or by hand), gated like the LLM pipeline.

A batch file (JSON) is a list of documents, each in the generator's output format plus its source:
  {"font": "teoria" | "problema", "id": "T3.21" | "t3-5", "dificultat": "facil" | "normal" | "dificil",
   "n_enunciat": 2,            # theory only: statement fragments first
   "fragments": [...], "errors": [{"fragment", "cita", "tipus", "explicacio", "correccio", "pista"}]}

Steps (the same gates as errades.generate):
  validate <batch.json>   code validation (counts, quotes, $ balance, statement/proof split)
  blind <batch.json>      writes <batch>.blind.md: the documents WITHOUT the declared errors, plus the
                          reference (sheet or original item of the notes), for an independent reviewer
  import <batch.json>     needs <batch>.ver.json from the reviewer: {"<id>:<dificultat>": {"problemes": [...],
                          "valoracio": ""}} in the verifier's format. Code compares (every declared error
                          found, nothing else wrong) and saves only the documents that pass.
  check-cache             re-validates every cached document against the current sheets / notes
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from tutor import errades  # noqa: E402
from tutor.fitxes import load_exercicis  # noqa: E402

EXERCICIS = load_exercicis()
ITEMS = {it.id: it for it in errades.items_teoria()}


def font_of(doc: dict):
    if doc.get("font") == "teoria":
        if doc["id"] not in ITEMS:
            raise KeyError(f"{doc['id']}: not a result with proof in the notes")
        return errades.FontTeoria(ITEMS[doc["id"]])
    if doc["id"] not in EXERCICIS:
        raise KeyError(f"{doc['id']}: unknown exercise")
    return errades.FontProblema(EXERCICIS[doc["id"]])


def key(doc: dict) -> str:
    return f"{doc['id']}:{doc['dificultat']}"


def validate(doc: dict) -> tuple[list[str], list[errades.ErrorDeclarat], list[str]]:
    try:
        font_of(doc)
    except KeyError as e:
        return [], [], [str(e)]
    if doc.get("dificultat") not in errades.N_ERRORS:
        return [], [], [f"dificultat invàlida: {doc.get('dificultat')}"]
    return errades.validate_generation(doc, errades.N_ERRORS[doc["dificultat"]], doc.get("font") == "teoria")


def load(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def cmd_validate(path: Path) -> int:
    bad = 0
    for doc in load(path):
        _, _, problems = validate(doc)
        if problems:
            bad += 1
            print(f"{key(doc)}:\n  - " + "\n  - ".join(problems))
    print(f"{len(load(path)) - bad} ok, {bad} with problems")
    return 1 if bad else 0


def cmd_blind(path: Path) -> int:
    out = []
    for doc in load(path):
        font = font_of(doc)
        frags, _, _ = validate(doc)
        n_en = doc.get("n_enunciat", 0) if font.tipus == "teoria" else 0
        out.append(
            f"## {key(doc)}\n\n### Referència\n\n{errades._context(font)}\n\n"
            f"### Document a revisar\n\n{errades._numbered(frags, n_en)}\n"
        )
    dest = path.with_suffix(".blind.md")
    dest.write_text("\n\n".join(out), encoding="utf-8")
    print(f"wrote {dest} ({len(out)} documents)")
    return 0


def cmd_import(path: Path, directory: Path = errades.CACHE_DIR) -> int:
    ver_path = path.with_suffix(".ver.json")
    ver = json.loads(ver_path.read_text(encoding="utf-8"))
    ok = bad = 0
    for doc in load(path):
        frags, errs, problems = validate(doc)
        v = ver.get(key(doc))
        if v is None:
            problems = problems + ["no independent review for this document"]
        else:
            problems = problems + errades.compare_verification(errs, v.get("problemes", []), frags)
        if problems:
            bad += 1
            print(f"REJECTED {key(doc)}:\n  - " + "\n  - ".join(problems))
            continue
        sol = errades.SolucioAmbErrors(
            id=errades.nou_id(frags),
            exercici=doc["id"],
            font=doc.get("font", "problema"),
            dificultat=doc["dificultat"],
            fragments=frags,
            n_enunciat=doc.get("n_enunciat", 0) if doc.get("font") == "teoria" else 0,
            errors=errs,
            verificacio={"origen": "offline", "lot": path.name, "valoracio": v.get("valoracio", ""),
                         "problemes": v.get("problemes", [])},
        )
        errades.save(sol, directory)
        ok += 1
    print(f"imported {ok}, rejected {bad}")
    return 1 if bad else 0


def cmd_check_cache(directory: Path = errades.CACHE_DIR) -> int:
    bad = 0
    for p in sorted(directory.glob("*/*/*.json")):
        sol = errades.SolucioAmbErrors.model_validate_json(p.read_text(encoding="utf-8"))
        doc = {"font": sol.font, "id": sol.exercici, "dificultat": sol.dificultat, "n_enunciat": sol.n_enunciat,
               "fragments": sol.fragments, "errors": [e.model_dump() for e in sol.errors]}
        _, _, problems = validate(doc)
        if problems:
            bad += 1
            print(f"{p.relative_to(directory)}: " + "; ".join(problems))
    print(f"{bad} cached documents with problems")
    return 1 if bad else 0


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:] or ["check-cache"]
    if cmd == "check-cache":
        sys.exit(cmd_check_cache())
    fn = {"validate": cmd_validate, "blind": cmd_blind, "import": cmd_import}[cmd]
    sys.exit(max(fn(Path(a)) for a in rest))
