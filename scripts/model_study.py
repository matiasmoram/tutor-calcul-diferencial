"""Pilot study: can much smaller models run the tutor? Same scripted students, several model configurations.

    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe scripts/model_study.py [config ...]

Each configuration plays the same 4 exercises x 4 scripted student turns (fixed messages, so every config
sees the same input). Per config it writes work/study/<config>.json (traces, metrics) and
work/study/<config>.md (readable transcript, for judging leaks and teaching quality by hand).

Automatic metrics: cost (current OpenRouter list prices, cache-aware), latency, failed calls, rejected
drafts, fallback rate, and agreement of the diagnosis with the expected label of each scripted turn.
OpenRouter's key is read from the CCR config (~/.claude-code-router/config.json) and never written anywhere.

The tutor runs through the real use cases (SessionStarter + TurnHandler) over a throwaway SQLite database.
Stages are `core.shared.llm.client.Stage` values: the "stages" of each config in the JSON output are keyed
diagnosis / reply / guard (they were diagnosi / resposta / guardia).

Also the shared toolkit of the evaluation scripts (simulate.py, smoke_turn.py, live_demo.py): per-stage client
building, the authored course, a scratch database and `LocalTutor`.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import tempfile
import time
from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import openai
from dotenv import load_dotenv
from google import genai

from core.course.domain.entities.course import Course
from core.course.infra.yaml_course_source import YamlCourseSource
from core.shared.domain.ids import ExerciseId, SessionId
from core.shared.llm.client import LLMClient, Stage, StageConfig
from core.shared.llm.infra.gemini_client import GeminiLLMClient
from core.shared.llm.infra.openai_client import OPENROUTER_BASE_URL, OpenAILLMClient
from core.shared.llm.infra.stage_router import StageRouter
from core.shared.storage.session_provider import SQLModelSessionProvider, create_schema_if_sqlite, make_engine
from core.shared.storage.table_registry import register_all_tables
from core.tutoring.application.session_starter import SessionStarter
from core.tutoring.application.turn_handler import TurnHandler, TurnInput, TurnResult
from core.tutoring.infra.llm_diagnoser import LLMDiagnoser
from core.tutoring.infra.llm_reply_judge import LLMReplyJudge
from core.tutoring.infra.llm_reply_writer import LLMReplyWriter
from core.tutoring.infra.sqlmodel_repository import SQLModelTutorSessionRepository
from settings import BACKEND_DIR, ROOT_DIR, Config

type Json = dict[str, Any]  # a record of the JSON reports
OUT = ROOT_DIR / "work" / "study"
STAGES = (Stage.DIAGNOSIS, Stage.REPLY, Stage.GUARD)
TIMEOUT_S = 180  # per LLM request (the SDK retries twice on top)
MAX_TOKENS = 8000

# USD per 1M tokens: (input, output, cached input). OpenRouter list prices, 2026-10-06.
PRICES = {
    "gpt-5.5": (5.0, 30.0, 0.5),
    "gpt-5.4-mini": (0.75, 4.5, 0.075),
    "gpt-5.6-terra": (2.0, 12.0, 0.2),  # OpenAI list prices after the 2026-07-30 cut
    "gpt-5.6-luna": (0.2, 1.2, 0.02),
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

type StageSpec = tuple[str, str, str]  # (provider, model, effort)
type StudyConfig = Mapping[Stage, StageSpec]

D, R, G = STAGES
# name -> {stage: (provider, model, effort)}
CONFIGS: dict[str, StudyConfig] = {
    "base": {
        D: ("openai", "gpt-5.5", "medium"),
        R: ("openai", "gpt-5.4-mini", "low"),
        G: ("openai", "gpt-5.4-mini", "low"),
    },
    "mini54": dict.fromkeys(STAGES, ("openai", "gpt-5.4-mini", "low")),
    "luna": dict.fromkeys(STAGES, ("openai", "gpt-5.6-luna", "low")),
    "luna-none": dict.fromkeys(STAGES, ("openai", "gpt-5.6-luna", "none")),
    "luna+nano": {
        D: ("openai", "gpt-5.6-luna", "low"),
        R: ("openai", "gpt-5.4-nano", "low"),
        G: ("openai", "gpt-5.6-luna", "low"),
    },
    "mini+luna": {
        D: ("openai", "gpt-5.4-mini", "low"),
        R: ("openai", "gpt-5.6-luna", "low"),
        G: ("openai", "gpt-5.6-luna", "low"),
    },
    "terra+mini": {
        D: ("openai", "gpt-5.6-terra", "low"),
        R: ("openai", "gpt-5.4-mini", "low"),
        G: ("openai", "gpt-5.4-mini", "low"),
    },
    "gpt5mini": dict.fromkeys(STAGES, ("openai", "gpt-5-mini", "low")),
    "nano54": dict.fromkeys(STAGES, ("openai", "gpt-5.4-nano", "low")),
    "kimi25": dict.fromkeys(STAGES, ("openrouter", "moonshotai/kimi-k2.5", "")),
    "kimik2": dict.fromkeys(STAGES, ("openrouter", "moonshotai/kimi-k2-0905", "")),
    "gemini": {
        D: ("gemini", "gemini-3-flash-preview", "medium"),
        R: ("gemini", "gemini-3.5-flash-lite", "low"),
        G: ("gemini", "gemini-3.5-flash-lite", "low"),
    },
    "mini+kimik2": {
        D: ("openai", "gpt-5.4-mini", "low"),
        R: ("openrouter", "moonshotai/kimi-k2-0905", ""),
        G: ("openai", "gpt-5.4-mini", "low"),
    },
    "dsflash": dict.fromkeys(STAGES, ("openrouter", "deepseek/deepseek-v4-flash", "")),
    "dspro": dict.fromkeys(STAGES, ("openrouter", "deepseek/deepseek-v4-pro", "")),
    "qwenflash": dict.fromkeys(STAGES, ("openrouter", "qwen/qwen3.5-flash-02-23", "")),
    "glmflash": dict.fromkeys(STAGES, ("openrouter", "z-ai/glm-4.7-flash", "")),
    "mini+dsflash": {
        D: ("openai", "gpt-5.4-mini", "low"),
        R: ("openrouter", "deepseek/deepseek-v4-flash", ""),
        G: ("openrouter", "deepseek/deepseek-v4-flash", ""),
    },
    "gpt5nano": dict.fromkeys(STAGES, ("openai", "gpt-5-nano", "low")),
    "nano41": dict.fromkeys(STAGES, ("openai", "gpt-4.1-nano", "")),
    "oss20b": dict.fromkeys(STAGES, ("openrouter", "openai/gpt-oss-20b", "low")),
    "nemo12b": dict.fromkeys(STAGES, ("openrouter", "mistralai/mistral-nemo", "")),
    "llama8b": dict.fromkeys(STAGES, ("openrouter", "meta-llama/llama-3.1-8b-instruct", "")),
    "gemma4b": dict.fromkeys(STAGES, ("openrouter", "google/gemma-3-4b-it", "")),
    "hybrid": {
        D: ("openai", "gpt-5.4-mini", "low"),
        R: ("openrouter", "openai/gpt-oss-20b", "low"),
        G: ("openrouter", "openai/gpt-oss-20b", "low"),
    },
    "nano+oss": {
        D: ("openai", "gpt-5.4-nano", "low"),
        R: ("openrouter", "openai/gpt-oss-20b", "low"),
        G: ("openrouter", "openai/gpt-oss-20b", "low"),
    },
    "oss+nemo": {
        D: ("openrouter", "openai/gpt-oss-20b", "low"),
        R: ("openrouter", "mistralai/mistral-nemo", ""),
        G: ("openrouter", "openai/gpt-oss-20b", "low"),
    },
}

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


# ---------------------------------------------------------------- shared toolkit of the evaluation scripts


def openrouter_key() -> str:
    cfg = json.loads((Path.home() / ".claude-code-router" / "config.json").read_text(encoding="utf-8-sig"))
    return next(p["api_key"] for p in cfg["Providers"] if p.get("name") == "openrouter")


def stage_client(provider: str, stages: Mapping[Stage, StageConfig], timeout_s: float = TIMEOUT_S) -> LLMClient:
    """One backend serving `stages`: provider "openai", "openrouter" or "gemini"."""
    if provider == "gemini":
        return GeminiLLMClient(stages, genai.Client(api_key=Config().api_key("GEMINI_API_KEY")))
    if provider == "openrouter":
        client = openai.AsyncOpenAI(
            base_url=OPENROUTER_BASE_URL, api_key=openrouter_key(), timeout=timeout_s, max_retries=2
        )
        # Only route to providers that honour every parameter sent (the JSON schema, when there is one).
        return OpenAILLMClient(stages, client, extra_body={"provider": {"require_parameters": True}})
    return OpenAILLMClient(stages, openai.AsyncOpenAI(timeout=timeout_s, max_retries=2))


def build(config: StudyConfig, timeout_s: float = TIMEOUT_S) -> StageRouter:
    """Each stage on its own backend (stages of one config may mix providers)."""
    return StageRouter(
        {
            stage: stage_client(prov, {stage: StageConfig(model, effort, max_tokens=MAX_TOKENS)}, timeout_s)
            for stage, (prov, model, effort) in config.items()
        }
    )


def load_course() -> Course:
    return YamlCourseSource(BACKEND_DIR / "exercicis", BACKEND_DIR / "teoria").load()


@asynccontextmanager
async def scratch_database() -> AsyncIterator[SQLModelSessionProvider]:
    """A throwaway SQLite database with every table: evaluation sessions never reach the real one."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        engine = make_engine(f"sqlite+aiosqlite:///{(Path(tmp) / 'eval.db').as_posix()}")
        register_all_tables()
        await create_schema_if_sqlite(engine)
        try:
            yield SQLModelSessionProvider(engine)
        finally:
            await engine.dispose()


class LocalTutor:
    """The real tutor use cases (SessionStarter + TurnHandler) over `llm`, storing sessions in `provider`."""

    def __init__(self, course: Course, provider: SQLModelSessionProvider, llm: LLMClient) -> None:
        sessions = SQLModelTutorSessionRepository(provider)
        self._starter = SessionStarter(course, sessions)
        self._turns = TurnHandler(
            course, sessions, LLMDiagnoser(llm, course), LLMReplyWriter(llm), LLMReplyJudge(llm, course)
        )

    async def start(self, exercise_id: str) -> SessionId:
        return (await self._starter.start(ExerciseId(exercise_id))).session.id

    async def turn(self, session_id: SessionId, text: str) -> TurnResult:
        return await self._turns.handle(TurnInput(session_id=session_id, text=text))


# ---------------------------------------------------------------- the study


def cost(call: Json) -> float:
    pi, po, pc = PRICES[call["model"]]
    fresh = call["input_tokens"] - call["cached_tokens"]
    return (fresh * pi + call["cached_tokens"] * pc + call["output_tokens"] * po) / 1e6


def stages_json(config: StudyConfig) -> dict[str, list[str]]:
    return {str(stage): list(spec) for stage, spec in config.items()}


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
