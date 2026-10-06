"""Pre-generate verified 'find the error' documents with the LLM so the demo doesn't wait on it.

Usage: python scripts/pregenerate_errades.py t3-10:normal t2-4c:facil T3.21:dificil ...
Ids starting with "T" are results of the notes (theory activity); the rest are exercises.
"""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

from tutor import errades  # noqa: E402
from tutor.fitxes import load_exercicis  # noqa: E402
from tutor.llm import make_llm  # noqa: E402


def font(font_id: str):
    if font_id.startswith("T"):
        items = {it.id: it for it in errades.items_teoria()}
        return errades.FontTeoria(items[font_id])
    return errades.FontProblema(load_exercicis()[font_id])


def main(specs: list[str]) -> None:
    llm = make_llm()
    for spec in specs:
        font_id, _, dif = spec.partition(":")
        dif = dif or "normal"
        t0 = time.perf_counter()
        print(f"=== {font_id} ({dif})", flush=True)
        try:
            sol, log = errades.generate(llm, font(font_id), dif)
        except Exception as e:  # report and continue with the next spec
            print(f"  FAILED: {e}", flush=True)
            continue
        errades.save(sol)
        for entry in log:
            print(f"  intent {entry['intent']}: validacio={entry['validacio']} discrepancies={entry.get('discrepancies')}")
        for i, f in enumerate(sol.fragments, 1):
            print(f"  [{i}]{' (enunciat)' if i <= sol.n_enunciat else ''} {f}")
        for e in sol.errors:
            print(f"  ERROR {e.id} @[{e.fragment}] ({e.tipus}) «{e.cita}» — {e.explicacio}")
        print(f"  saved {sol.id} in {time.perf_counter() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or ["t3-6:normal"])
