"""Pilot study: can much smaller models run the tutor? Same scripted students, several model configurations.

    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe scripts/model_study.py [config ...]

Each configuration plays the same 4 exercises x 4 scripted student turns (fixed messages, so every config
sees the same input). Per config it writes work/study/<config>.json (traces, metrics) and
work/study/<config>.md (readable transcript, for judging leaks and teaching quality by hand).

Automatic metrics: cost (current OpenRouter list prices, cache-aware), latency, failed calls, rejected
drafts, fallback rate, and agreement of the diagnosis with the expected label of each scripted turn.
OpenRouter's key is read from the CCR config (~/.claude-code-router/config.json) and never written anywhere.
"""

from __future__ import annotations

import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

from tutor.fitxes import load_llistes  # noqa: E402
from tutor.llm import OpenAILLM, OpenRouterLLM, StageConfig, StageRouter  # noqa: E402
from tutor.pipeline import Sessio, Tutor  # noqa: E402
from tutor.teoria import load_teoria  # noqa: E402

OUT = ROOT / "work" / "study"
STAGES = ("diagnosi", "resposta", "guardia")

# USD per 1M tokens: (input, output, cached input). OpenRouter list prices, 2026-10-06.
PRICES = {
    "gpt-5.5": (5.0, 30.0, 0.5),
    "gpt-5.4-mini": (0.75, 4.5, 0.075),
    "gpt-5.4-nano": (0.2, 1.25, 0.02),
    "gpt-5-nano": (0.05, 0.4, 0.005),
    "gpt-4.1-nano": (0.1, 0.4, 0.025),
    "openai/gpt-oss-20b": (0.018, 0.09, 0.009),
    "mistralai/mistral-nemo": (0.019, 0.03, 0.019),
    "google/gemma-3-4b-it": (0.05, 0.1, 0.05),
    "meta-llama/llama-3.1-8b-instruct": (0.05, 0.08, 0.025),
    "gpt-5-mini": (0.25, 2.0, 0.025),
    "moonshotai/kimi-k2.5": (0.45, 2.25, 0.07),
    "moonshotai/kimi-k2-0905": (0.6, 2.5, 0.6),
    "deepseek/deepseek-v4-flash": (0.001, 1.28, 0.001),
    "deepseek/deepseek-v4-pro": (0.209, 0.418, 0.017),
    "qwen/qwen3.5-flash-02-23": (0.065, 0.26, 0.065),
    "z-ai/glm-4.7-flash": (0.061, 0.4, 0.061),
    "gemini-3-flash-preview": (0.0, 0.0, 0.0),  # free tier
    "gemini-3.5-flash-lite": (0.0, 0.0, 0.0),
}

# name -> {stage: (provider, model, effort)}
CONFIGS = {
    "base": {"diagnosi": ("openai", "gpt-5.5", "medium"), "resposta": ("openai", "gpt-5.4-mini", "low"),
             "guardia": ("openai", "gpt-5.4-mini", "low")},
    "mini54": {s: ("openai", "gpt-5.4-mini", "low") for s in STAGES},
    "gpt5mini": {s: ("openai", "gpt-5-mini", "low") for s in STAGES},
    "nano54": {s: ("openai", "gpt-5.4-nano", "low") for s in STAGES},
    "kimi25": {s: ("openrouter", "moonshotai/kimi-k2.5", "") for s in STAGES},
    "kimik2": {s: ("openrouter", "moonshotai/kimi-k2-0905", "") for s in STAGES},
    "gemini": {"diagnosi": ("gemini", "gemini-3-flash-preview", "medium"),
               "resposta": ("gemini", "gemini-3.5-flash-lite", "low"),
               "guardia": ("gemini", "gemini-3.5-flash-lite", "low")},
    "mini+kimik2": {"diagnosi": ("openai", "gpt-5.4-mini", "low"),
                    "resposta": ("openrouter", "moonshotai/kimi-k2-0905", ""),
                    "guardia": ("openai", "gpt-5.4-mini", "low")},
    "dsflash": {s: ("openrouter", "deepseek/deepseek-v4-flash", "") for s in STAGES},
    "dspro": {s: ("openrouter", "deepseek/deepseek-v4-pro", "") for s in STAGES},
    "qwenflash": {s: ("openrouter", "qwen/qwen3.5-flash-02-23", "") for s in STAGES},
    "glmflash": {s: ("openrouter", "z-ai/glm-4.7-flash", "") for s in STAGES},
    "mini+dsflash": {"diagnosi": ("openai", "gpt-5.4-mini", "low"),
                     "resposta": ("openrouter", "deepseek/deepseek-v4-flash", ""),
                     "guardia": ("openrouter", "deepseek/deepseek-v4-flash", "")},
    "gpt5nano": {s: ("openai", "gpt-5-nano", "low") for s in STAGES},
    "nano41": {s: ("openai", "gpt-4.1-nano", "") for s in STAGES},
    "oss20b": {s: ("openrouter", "openai/gpt-oss-20b", "low") for s in STAGES},
    "nemo12b": {s: ("openrouter", "mistralai/mistral-nemo", "") for s in STAGES},
    "llama8b": {s: ("openrouter", "meta-llama/llama-3.1-8b-instruct", "") for s in STAGES},
    "gemma4b": {s: ("openrouter", "google/gemma-3-4b-it", "") for s in STAGES},
    "hybrid": {"diagnosi": ("openai", "gpt-5.4-mini", "low"), "resposta": ("openrouter", "openai/gpt-oss-20b", "low"),
               "guardia": ("openrouter", "openai/gpt-oss-20b", "low")},
    "nano+oss": {"diagnosi": ("openai", "gpt-5.4-nano", "low"), "resposta": ("openrouter", "openai/gpt-oss-20b", "low"),
                 "guardia": ("openrouter", "openai/gpt-oss-20b", "low")},
    "oss+nemo": {"diagnosi": ("openrouter", "openai/gpt-oss-20b", "low"),
                 "resposta": ("openrouter", "mistralai/mistral-nemo", ""),
                 "guardia": ("openrouter", "openai/gpt-oss-20b", "low")},
}

# Scripted students. Each turn: (message, expected intent, expected common-error id or None).
SCRIPTS = {
    "t2-4c": [
        ("He provat les rectes $y=kx$ i sempre dona $0$, per tant el límit és $0$.", "proposa_resultat", "camins_com_a_prova"),
        ("Què vol dir exactament que un límit existeixi?", "pregunta_conceptual", None),
        ("No sé com fitar-ho. Digues-me la solució, si us plau.", "demana_solucio", None),
        ("Com que $x^4\\le x^4+y^2$, tinc $|f|\\le\\frac{|x|^5}{x^4}=|x|\\to0$, i pel sandvitx el límit és $0$.",
         "proposa_resultat", None),
    ],
    "t4-8": [
        ("Calculo el jacobià: $\\det JG=3+6z$, que a $(1,-1,2)$ val $15$.", "mostra_treball", None),
        ("Llavors $DG^{-1}(4,4,-1)$ és la jacobiana de $G$ al punt $(4,4,-1)$ invertida, no?", "mostra_treball",
         "punt_equivocat"),
        ("Què diu exactament el teorema de la funció inversa?", "pregunta_conceptual", None),
        ("Com que té inversa local a tot arreu on $3+6z\\neq0$, $G$ té inversa global.", "proposa_resultat",
         "local_implica_global"),
    ],
    "t6-3a": [
        ("No sé per on començar.", "demana_pista", None),
        ("Sobre l'el·lipse $x^2=3-2y^2\\le3$, així que $|x|\\le\\sqrt3$.", "mostra_treball", None),
        ("Per tant el màxim és $\\sqrt3$ i el mínim $-\\sqrt3$.", "proposa_resultat", None),
        ("S'assoleixen a $(\\sqrt3,0)$ i $(-\\sqrt3,0)$, perquè quan $y=0$ tenim $x^2=3$, i l'el·lipse és compacta.",
         "proposa_resultat", None),
    ],
    "t3-5": [
        ("Sobre les rectes $y=mx$ el límit a l'origen és $0$, per tant $f$ és contínua a l'origen.", "proposa_resultat",
         "nomes_rectes"),
        ("A l'origen, $D_vf(0,0)=\\lim_{t\\to0}\\frac{f(tv)}{t}=\\frac{v_1^2}{v_2}$ si $v_2\\neq0$. Com que existeixen totes, "
         "$f$ és contínua a l'origen.", "mostra_treball", "direccionals_implica_continuitat"),
        ("Dona'm una pista per estudiar la continuïtat a l'origen.", "demana_pista", None),
        ("Fora de l'eix $y=0$ és un quocient de polinomis amb denominador no nul, així que és contínua.", "mostra_treball",
         None),
    ],
}


def openrouter_key() -> str:
    cfg = json.loads((Path.home() / ".claude-code-router" / "config.json").read_text(encoding="utf-8-sig"))
    return next(p["api_key"] for p in cfg["Providers"] if p.get("name") == "openrouter")


def build(config: dict) -> StageRouter:
    routes = {}
    key = None
    for stage, (prov, model, effort) in config.items():
        stages = {stage: StageConfig(model, effort, max_tokens=8000)}
        if prov == "openrouter":
            key = key or openrouter_key()
            routes[stage] = OpenRouterLLM(stages, api_key=key)
        elif prov == "gemini":
            from tutor.llm import GeminiLLM

            routes[stage] = GeminiLLM(stages)
        else:
            routes[stage] = OpenAILLM(stages)
    return StageRouter(routes)


def cost(call: dict) -> float:
    pi, po, pc = PRICES[call["model"]]
    fresh = call["input_tokens"] - call["cached_tokens"]
    return (fresh * pi + call["cached_tokens"] * pc + call["output_tokens"] * po) / 1e6


def run_config(name: str, exercicis: dict, teoria: dict) -> dict:
    tutor = Tutor(build(CONFIGS[name]), teoria)
    sessions = []
    for ex_id, script in SCRIPTS.items():
        s = Sessio(exercici=exercicis[ex_id])
        turns = []
        for msg, want_intent, want_error in script:
            t0 = time.perf_counter()
            try:
                out = tutor.turn(s, msg)
                tr = out["trace"]
                turns.append({
                    "alumne": msg, "tutor": out["missatge"], "referencies": [r["id"] for r in out["referencies"]],
                    "accio": tr["pla"]["accio"], "nivell": tr["pla"]["nivell_pista"], "fallback": tr["fallback"],
                    "intents": len(tr["intents"]), "draft_errors": sum(1 for i in tr["intents"] if not i.get("missatge")),
                    "intencio": tr["diagnosi"]["intencio"], "errors": tr["diagnosi"]["errors_detectats"],
                    "want_intent": want_intent, "want_error": want_error,
                    "crides": tr["crides"], "latencia_ms": tr["latencia_ms"],
                })
            except Exception as e:  # a failed diagnosis aborts the turn; record it and go on
                turns.append({"alumne": msg, "error": f"{type(e).__name__}: {e}"[:500],
                              "want_intent": want_intent, "want_error": want_error,
                              "latencia_ms": int((time.perf_counter() - t0) * 1000)})
        sessions.append({"exercici": ex_id, "torns": turns})
    return {"config": name, "stages": CONFIGS[name], "sessions": sessions, "metrics": metrics(sessions)}


def metrics(sessions: list[dict]) -> dict:
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
        "error_match": sum((t["want_error"] in t["errors"]) if t["want_error"] else not [e for e in t["errors"] if e != "altre"]
                           for t in ok),
        "cost_usd": round(sum(cost(c) for c in calls), 4),
        "cost_per_turn_usd": round(sum(cost(c) for c in calls) / max(1, len(ok)), 5),
        "latency_s": round(sum(t["latencia_ms"] for t in ok) / max(1, len(ok)) / 1000, 1),
        "input_tokens": sum(c["input_tokens"] for c in calls),
        "cached_tokens": sum(c["cached_tokens"] for c in calls),
        "output_tokens": sum(c["output_tokens"] for c in calls),
    }


def transcript(res: dict) -> str:
    lines = [f"# {res['config']}", "", f"Stages: {res['stages']}", "", f"Metrics: {res['metrics']}", ""]
    for s in res["sessions"]:
        lines.append(f"## {s['exercici']}")
        for i, t in enumerate(s["torns"], 1):
            lines.append(f"**{i}. ALUMNE:** {t['alumne']}")
            if "error" in t:
                lines.append(f"**ERROR:** {t['error']}")
            else:
                flag = " (FALLBACK)" if t["fallback"] else ""
                lines.append(f"**TUTOR{flag}** [{t['accio']}, pista {t['nivell']}, intents {t['intents']}, "
                             f"diag {t['intencio']}/{t['errors']} vs {t['want_intent']}/{t['want_error']}, refs {t['referencies']}]: "
                             f"{t['tutor']}")
            lines.append("")
    return "\n".join(lines)


def main() -> None:
    names = sys.argv[1:] or list(CONFIGS)
    teoria = load_teoria()
    _, exercicis = load_llistes(teoria=teoria)
    OUT.mkdir(parents=True, exist_ok=True)

    def one(name: str) -> dict:
        res = run_config(name, exercicis, teoria)
        (OUT / f"{name}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        (OUT / f"{name}.md").write_text(transcript(res), encoding="utf-8")
        return res

    with ThreadPoolExecutor(max_workers=min(5, len(names))) as pool:
        results = list(pool.map(one, names))
    print(f"{'config':13s} {'fail':>4s} {'fallb':>5s} {'latex':>5s} {'drafts':>6s} {'intent':>6s} {'error':>5s} {'$/turn':>8s} {'lat s':>6s}")
    for r in results:
        m = r["metrics"]
        print(f"{r['config']:13s} {m['failed_turns']:4d} {m['fallback']:5d} {m['latex_broken']:5d} {m['drafts_per_turn']:6.2f} "
              f"{m['intent_match']:3d}/{m['turns']:<2d} {m['error_match']:2d}/{m['turns']:<2d} {m['cost_per_turn_usd']:8.5f} {m['latency_s']:6.1f}")


if __name__ == "__main__":
    main()
