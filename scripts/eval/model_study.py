"""Pilot study: can much smaller models run the tutor? Same scripted students, several model configurations.

    uv run python scripts/eval/model_study.py [config ...]

Each configuration plays the same 4 exercises x 4 scripted student turns (fixed messages, so every config
sees the same input). Per config it writes data/eval/study/<config>.json (traces, metrics) and
data/eval/study/<config>.md (readable transcript, for judging leaks and teaching quality by hand).

Automatic metrics: cost (current OpenRouter list prices, cache-aware), latency, failed calls, rejected
drafts, fallback rate, and agreement of the diagnosis with the expected label of each scripted turn.
API keys come from the environment (.env): OPENAI_API_KEY, OPENROUTER_API_KEY, GEMINI_API_KEY, as each config needs.

The tutor runs through the real use cases (SessionStarter + TurnHandler) over a throwaway SQLite database.
The "stages" of each config in the JSON output are keyed by `core.shared.llm.client.Stage` values.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import time

from dotenv import load_dotenv
from harness import CONFIGS, Json, LocalTutor, build, cost, load_course, scratch_database, stages_json

from core.course.domain.entities.course import Course
from core.shared.storage.session_provider import SQLModelSessionProvider
from settings import ROOT_DIR

OUT = ROOT_DIR / "data" / "eval" / "study"

# Scripted students. Each turn: (message, expected intent, expected common-error id or None).
SCRIPTS = {
    "t2-4c": [
        (
            "He provat les rectes $y=kx$ i sempre dona $0$, per tant el límit és $0$.",
            "proposa_resultat",
            "camins_com_a_prova",
        ),
        ("Què vol dir exactament que un límit existeixi?", "pregunta_conceptual", None),
        ("No sé com fitar-ho. Digues-me la solució, si us plau.", "demana_solucio", None),
        (
            "Com que $x^4\\le x^4+y^2$, tinc $|f|\\le\\frac{|x|^5}{x^4}=|x|\\to0$, i pel sandvitx el límit és $0$.",
            "proposa_resultat",
            None,
        ),
    ],
    "t4-8": [
        ("Calculo el jacobià: $\\det JG=3+6z$, que a $(1,-1,2)$ val $15$.", "mostra_treball", None),
        (
            "Llavors $DG^{-1}(4,4,-1)$ és la jacobiana de $G$ al punt $(4,4,-1)$ invertida, no?",
            "mostra_treball",
            "punt_equivocat",
        ),
        ("Què diu exactament el teorema de la funció inversa?", "pregunta_conceptual", None),
        (
            "Com que té inversa local a tot arreu on $3+6z\\neq0$, $G$ té inversa global.",
            "proposa_resultat",
            "local_implica_global",
        ),
    ],
    "t6-3a": [
        ("No sé per on començar.", "demana_pista", None),
        ("Sobre l'el·lipse $x^2=3-2y^2\\le3$, així que $|x|\\le\\sqrt3$.", "mostra_treball", None),
        ("Per tant el màxim és $\\sqrt3$ i el mínim $-\\sqrt3$.", "proposa_resultat", None),
        (
            "S'assoleixen a $(\\sqrt3,0)$ i $(-\\sqrt3,0)$, perquè quan $y=0$ tenim $x^2=3$, i l'el·lipse és compacta.",
            "proposa_resultat",
            None,
        ),
    ],
    "t3-5": [
        (
            "Sobre les rectes $y=mx$ el límit a l'origen és $0$, per tant $f$ és contínua a l'origen.",
            "proposa_resultat",
            "nomes_rectes",
        ),
        (
            "A l'origen, $D_vf(0,0)=\\lim_{t\\to0}\\frac{f(tv)}{t}=\\frac{v_1^2}{v_2}$ si $v_2\\neq0$. Com que existeixen totes, "
            "$f$ és contínua a l'origen.",
            "mostra_treball",
            "direccionals_implica_continuitat",
        ),
        ("Dona'm una pista per estudiar la continuïtat a l'origen.", "demana_pista", None),
        (
            "Fora de l'eix $y=0$ és un quocient de polinomis amb denominador no nul, així que és contínua.",
            "mostra_treball",
            None,
        ),
    ],
}


async def run_config(name: str, course: Course, provider: SQLModelSessionProvider) -> Json:
    tutoring = LocalTutor(course, provider, build(CONFIGS[name]))
    sessions = []
    for ex_id, script in SCRIPTS.items():
        session_id = await tutoring.start(ex_id)
        turns = []
        for msg, want_intent, want_error in script:
            t0 = time.perf_counter()
            try:
                out = await tutoring.turn(session_id, msg)
                tr = out.trace.model_dump(mode="json")
                turns.append(
                    {
                        "alumne": msg,
                        "tutor": out.message,
                        "referencies": [r.id for r in out.references],
                        "accio": tr["pla"]["accio"],
                        "nivell": tr["pla"]["nivell_pista"],
                        "fallback": tr["fallback"],
                        "intents": len(tr["intents"]),
                        "draft_errors": sum(1 for i in tr["intents"] if not i.get("missatge")),
                        "intencio": tr["diagnosi"]["intencio"],
                        "errors": tr["diagnosi"]["errors_detectats"],
                        "want_intent": want_intent,
                        "want_error": want_error,
                        "crides": tr["crides"],
                        "latencia_ms": tr["latencia_ms"],
                    }
                )
            except Exception as e:  # a failed diagnosis aborts the turn; record it and go on
                turns.append(
                    {
                        "alumne": msg,
                        "error": f"{type(e).__name__}: {e}"[:500],
                        "want_intent": want_intent,
                        "want_error": want_error,
                        "latencia_ms": int((time.perf_counter() - t0) * 1000),
                    }
                )
        sessions.append({"exercici": ex_id, "torns": turns})
    return {"config": name, "stages": stages_json(CONFIGS[name]), "sessions": sessions, "metrics": metrics(sessions)}


def metrics(sessions: list[Json]) -> Json:
    turns = [t for s in sessions for t in s["torns"]]
    ok = [t for t in turns if "error" not in t]
    calls = [c for t in ok for c in t["crides"]]
    n = len(turns)
    return {
        "turns": n,
        "failed_turns": n - len(ok),
        "fallback": sum(t["fallback"] for t in ok),
        "drafts_per_turn": round(sum(t["intents"] for t in ok) / max(1, len(ok)), 2),
        "draft_errors": sum(t["draft_errors"] for t in ok),
        # Small models often write "\frac" unescaped in JSON: \f, \b, \t arrive as control characters.
        "latex_broken": sum(any(ch in t["tutor"] for ch in "\x08\x0c\t") for t in ok),
        "intent_match": sum(t["intencio"] == t["want_intent"] for t in ok),
        "error_match": sum(
            (t["want_error"] in t["errors"]) if t["want_error"] else not [e for e in t["errors"] if e != "altre"]
            for t in ok
        ),
        "cost_usd": round(sum(cost(c) for c in calls), 4),
        "cost_per_turn_usd": round(sum(cost(c) for c in calls) / max(1, len(ok)), 5),
        "latency_s": round(sum(t["latencia_ms"] for t in ok) / max(1, len(ok)) / 1000, 1),
        "input_tokens": sum(c["input_tokens"] for c in calls),
        "cached_tokens": sum(c["cached_tokens"] for c in calls),
        "output_tokens": sum(c["output_tokens"] for c in calls),
    }


def transcript(res: Json) -> str:
    lines = [f"# {res['config']}", "", f"Stages: {res['stages']}", "", f"Metrics: {res['metrics']}", ""]
    for s in res["sessions"]:
        lines.append(f"## {s['exercici']}")
        for i, t in enumerate(s["torns"], 1):
            lines.append(f"**{i}. ALUMNE:** {t['alumne']}")
            if "error" in t:
                lines.append(f"**ERROR:** {t['error']}")
            else:
                flag = " (FALLBACK)" if t["fallback"] else ""
                lines.append(
                    f"**TUTOR{flag}** [{t['accio']}, pista {t['nivell']}, intents {t['intents']}, "
                    f"diag {t['intencio']}/{t['errors']} vs {t['want_intent']}/{t['want_error']}, refs {t['referencies']}]: "
                    f"{t['tutor']}"
                )
            lines.append("")
    return "\n".join(lines)


async def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("configs", nargs="*", help=f"configs to run (default: all): {', '.join(CONFIGS)}")
    args = ap.parse_args(argv)
    names = args.configs or list(CONFIGS)
    if unknown := [n for n in names if n not in CONFIGS]:
        ap.error(f"unknown configs {unknown}; known: {', '.join(CONFIGS)}")
    load_dotenv(ROOT_DIR / ".env")
    course = load_course()
    OUT.mkdir(parents=True, exist_ok=True)
    limit = asyncio.Semaphore(5)

    async with scratch_database() as provider:

        async def one(name: str) -> Json:
            async with limit:
                res = await run_config(name, course, provider)
            (OUT / f"{name}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
            (OUT / f"{name}.md").write_text(transcript(res), encoding="utf-8")
            return res

        results = await asyncio.gather(*(one(n) for n in names))
    print(
        f"{'config':13s} {'fail':>4s} {'fallb':>5s} {'latex':>5s} {'drafts':>6s} {'intent':>6s} {'error':>5s} {'$/turn':>8s} {'lat s':>6s}"
    )
    for r in results:
        m = r["metrics"]
        print(
            f"{r['config']:13s} {m['failed_turns']:4d} {m['fallback']:5d} {m['latex_broken']:5d} {m['drafts_per_turn']:6.2f} "
            f"{m['intent_match']:3d}/{m['turns']:<2d} {m['error_match']:2d}/{m['turns']:<2d} {m['cost_per_turn_usd']:8.5f} {m['latency_s']:6.1f}"
        )


if __name__ == "__main__":
    asyncio.run(main())
