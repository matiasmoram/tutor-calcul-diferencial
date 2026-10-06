"""Run a scripted student conversation against the real LLM and print the harness trace."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

from tutor.fitxes import load_exercicis  # noqa: E402
from tutor.llm import make_llm  # noqa: E402
from tutor.pipeline import Sessio, Tutor  # noqa: E402

SCRIPTS = {
    "t2-4c": [
        "He provat amb rectes $y=kx$ i sempre em dona 0, per tant el límit és 0.",
        "Doncs no ho sé, digues-me la solució i ja està.",
        r"Potser puc fitar-ho? $x^4 \le x^4+y^2$ així que el quocient és més petit que $|x|$",
        r"Com que $|x| \to 0$, pel sandvitx el límit és 0.",
    ],
}


def main(ex_id: str = "t2-4c") -> None:
    ex = load_exercicis()[ex_id]
    tutor = Tutor(make_llm())
    s = Sessio(exercici=ex)
    for msg in SCRIPTS[ex_id]:
        out = tutor.turn(s, msg)
        t = out["trace"]
        d, p = t["diagnosi"], t["pla"]
        print("=" * 80)
        print("ALUMNE:", msg)
        print(f"  diagnosi: {d['nivell_desorientacio']} | {d['intencio']} | errors={d['errors_detectats']} "
              f"| resultat={d['resultat_proposat']} justificat={d['resultat_justificat']}")
        print(f"  passos:   {[(e['pas'], e['estat']) for e in d['estat_passos']]}")
        print(f"  pla:      {p['accio']} -> pas={p['pas_objectiu']} nivell={p['nivell_pista']} ({p['motiu']})")
        for i, a in enumerate(t["intents"], 1):
            verdict = "OK" if a.get("missatge") and not a["determinista"] and a["llm"] and a["llm"]["veredicte"] == "ok" else "REBUTJAT"
            print(f"  esborrany {i} [{verdict}]: {a.get('missatge') or a.get('error')}")
            if verdict == "REBUTJAT":
                print(f"     motius: {a.get('determinista')} {json.dumps(a.get('llm'), ensure_ascii=False)}")
        print(f"  fallback={t['fallback']}  temps={t['latencia_ms']/1000:.1f}s  crides={[c['stage'] for c in t['crides']]}")
        print("TUTOR:", out["missatge"])


if __name__ == "__main__":
    main(*sys.argv[1:])
