"""Pre-generate verified 'Cert o fals' quizzes with the LLM so the demo doesn't wait on them.

Usage: python scripts/pregenerate_afirmacions.py tema-2:normal T2.12:facil tema-3:dificil ...
A source is a whole tema ("tema-2") or a result of the notes as the focus ("T2.12").
"""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

from tutor import afirmacions  # noqa: E402
from tutor.llm import make_llm  # noqa: E402


def main(specs: list[str]) -> None:
    llm = make_llm()
    for spec in specs:
        font_id, _, dif = spec.partition(":")
        dif = dif or "normal"
        t0 = time.perf_counter()
        print(f"=== {font_id} ({dif})", flush=True)
        try:
            q, log = afirmacions.generate(llm, afirmacions.font_de(font_id), dif)
        except Exception as e:  # report and continue with the next spec
            print(f"  FAILED: {type(e).__name__}: {e}", flush=True)
            continue
        afirmacions.save(q)
        for entry in log:
            print(f"  ronda {entry['ronda']}: demanades {entry['demanades']}, rebudes {entry['rebudes']}, "
                  f"acceptades en total {entry['acceptades_total']}")
            for r in entry["rebutjades"]:
                print(f"    REBUTJADA «{r['enunciat'][:90]}»: {'; '.join(r['motius'])[:300]}")
        for a in q.afirmacions:
            print(f"  [{a.id}] ({a.veredicte}, {a.trampa}, CAS {a.cas_ok}/{len(a.comprovacions)}) {a.enunciat}")
            if a.contraexemple:
                print(f"       contraexemple: {a.contraexemple}")
        print(f"  saved {q.id} in {time.perf_counter() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or ["tema-2:normal"])
