"""One real tutor turn against the configured provider: checks schemas, theory citations and cache metrics.

    python scripts/smoke_turn.py [exercise_id] ["student message"]
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

from tutor.fitxes import load_llistes  # noqa: E402
from tutor.llm import make_llm  # noqa: E402
from tutor.pipeline import Sessio, Tutor  # noqa: E402
from tutor.teoria import load_teoria  # noqa: E402


def main() -> None:
    ex_id = sys.argv[1] if len(sys.argv) > 1 else "t2-4c"
    msgs = sys.argv[2:] or [
        "Què vol dir exactament que el límit existeixi? No entenc la definició.",
        "He provat les rectes y=kx i dona 0, per tant el límit és 0.",
    ]
    teoria = load_teoria()
    _, exercicis = load_llistes(teoria=teoria)
    tutor = Tutor(make_llm(), teoria)
    s = Sessio(exercici=exercicis[ex_id])
    for m in msgs:
        out = tutor.turn(s, m)
        t = out["trace"]
        print(f"\nALUMNE: {m}\nTUTOR: {out['missatge']}")
        print(f"  acció={t['pla']['accio']} teoria_permesa={t['teoria_permesa']} refs={[r['id'] for r in out['referencies']]}")
        print("  " + json.dumps([(c["stage"], c["input_tokens"], c["cached_tokens"], c["output_tokens"]) for c in t["crides"]]))


if __name__ == "__main__":
    main()
