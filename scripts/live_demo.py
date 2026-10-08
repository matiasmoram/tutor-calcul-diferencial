"""Run a scripted student conversation against the real LLM and print the harness trace.

    python scripts/live_demo.py [exercise_id]

The provider and models come from the environment (.env), as for the server. The session lives in a throwaway
SQLite database.
"""

import argparse
import asyncio
import json

from dotenv import load_dotenv
from model_study import LocalTutor, load_course, scratch_database

from core.shared.llm.infra.factory import make_llm_client
from settings import ROOT_DIR, Config

SCRIPTS = {
    "t2-4c": [
        "He provat amb rectes $y=kx$ i sempre em dona 0, per tant el límit és 0.",
        "Doncs no ho sé, digues-me la solució i ja està.",
        r"Potser puc fitar-ho? $x^4 \le x^4+y^2$ així que el quocient és més petit que $|x|$",
        r"Com que $|x| \to 0$, pel sandvitx el límit és 0.",
    ],
}


async def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("exercise", nargs="?", default="t2-4c", choices=sorted(SCRIPTS), help="scripted exercise")
    args = ap.parse_args(argv)
    load_dotenv(ROOT_DIR / ".env")
    course = load_course()
    async with scratch_database() as provider:
        tutoring = LocalTutor(course, provider, make_llm_client(Config()))
        session_id = await tutoring.start(args.exercise)
        for msg in SCRIPTS[args.exercise]:
            out = await tutoring.turn(session_id, msg)
            t = out.trace.model_dump(mode="json")
            d, p = t["diagnosi"], t["pla"]
            print("=" * 80)
            print("ALUMNE:", msg)
            print(
                f"  diagnosi: {d['nivell_desorientacio']} | {d['intencio']} | errors={d['errors_detectats']} "
                f"| resultat={d['resultat_proposat']} justificat={d['resultat_justificat']}"
            )
            print(f"  passos:   {[(e['pas'], e['estat']) for e in d['estat_passos']]}")
            print(f"  pla:      {p['accio']} -> pas={p['pas_objectiu']} nivell={p['nivell_pista']} ({p['motiu']})")
            for i, a in enumerate(t["intents"], 1):
                ok = a.get("missatge") and not a["determinista"] and a["llm"] and a["llm"]["veredicte"] == "ok"
                verdict = "OK" if ok else "REBUTJAT"
                print(f"  esborrany {i} [{verdict}]: {a.get('missatge') or a.get('error')}")
                if verdict == "REBUTJAT":
                    print(f"     motius: {a.get('determinista')} {json.dumps(a.get('llm'), ensure_ascii=False)}")
            print(
                f"  fallback={t['fallback']}  temps={t['latencia_ms'] / 1000:.1f}s  crides={[c['stage'] for c in t['crides']]}"
            )
            print("TUTOR:", out.message)


if __name__ == "__main__":
    asyncio.run(main())
