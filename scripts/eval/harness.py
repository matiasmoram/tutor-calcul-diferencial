"""Shared toolkit of the evaluation scripts (model_study.py, simulate.py, smoke_turn.py).

Named tutor configurations and per-stage client building, the authored course, a throwaway database, `LocalTutor`
(the real tutor use cases) and the list prices that turn token counts into cost.
"""

from __future__ import annotations

import tempfile
from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import openai
from google import genai

from core.course.domain.entities.course import Course
from core.course.infra.yaml_course_source import YamlCourseSource
from core.shared.domain.clock import SystemClock
from core.shared.domain.ids import ExerciseId, SessionId
from core.shared.llm.client import LLMClient, Stage, StageConfig
from core.shared.llm.infra.gemini_client import GeminiLLMClient
from core.shared.llm.infra.openai_client import OPENROUTER_BASE_URL, OpenAILLMClient
from core.shared.llm.infra.stage_router import StageRouter
from core.shared.storage.session_provider import SQLModelSessionProvider, create_schema_if_sqlite, make_engine
from core.shared.storage.table_registry import register_all_tables
from core.tutoring.application.session_starter import SessionStarter
from core.tutoring.application.turn_handler import TurnHandler, TurnHandlerInput, TurnResult
from core.tutoring.infra.llm_diagnoser import LLMDiagnoser
from core.tutoring.infra.llm_reply_judge import LLMReplyJudge
from core.tutoring.infra.llm_reply_writer import LLMReplyWriter
from core.tutoring.infra.sqlmodel_repository import SQLModelTutorSessionRepository
from settings import BACKEND_DIR, Config

type Json = dict[str, Any]  # a record of the JSON reports
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
type TutorConfig = Mapping[Stage, StageSpec]

D, R, G = STAGES
# name -> {stage: (provider, model, effort)}
CONFIGS: dict[str, TutorConfig] = {
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


def cost(call: Json) -> float:
    """USD of one recorded call. A model missing from PRICES counts as 0: report those separately."""
    if call["model"] not in PRICES:
        return 0.0
    pi, po, pc = PRICES[call["model"]]
    fresh = call["input_tokens"] - call["cached_tokens"]
    return (fresh * pi + call["cached_tokens"] * pc + call["output_tokens"] * po) / 1e6


def stages_json(config: TutorConfig) -> dict[str, list[str]]:
    return {str(stage): list(spec) for stage, spec in config.items()}


def stage_client(provider: str, stages: Mapping[Stage, StageConfig], timeout_s: float = TIMEOUT_S) -> LLMClient:
    """One backend serving `stages`: provider "openai", "openrouter" or "gemini"."""
    config = Config()
    if provider == "gemini":
        return GeminiLLMClient(stages, genai.Client(api_key=config.api_key("GEMINI_API_KEY")))
    if provider == "openrouter":
        client = openai.AsyncOpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=config.api_key("OPENROUTER_API_KEY"),
            timeout=timeout_s,
            max_retries=2,
        )
        # Only route to providers that honour every parameter sent (the JSON schema, when there is one).
        return OpenAILLMClient(stages, client, extra_body={"provider": {"require_parameters": True}})
    return OpenAILLMClient(stages, openai.AsyncOpenAI(timeout=timeout_s, max_retries=2))


def build(config: TutorConfig, timeout_s: float = TIMEOUT_S) -> StageRouter:
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
        clock = SystemClock()
        self._starter = SessionStarter(course, sessions, clock)
        self._turns = TurnHandler(
            course, sessions, LLMDiagnoser(llm, course), LLMReplyWriter(llm), LLMReplyJudge(llm, course), clock
        )

    async def start(self, exercise_id: str) -> SessionId:
        return (await self._starter.start(ExerciseId(exercise_id))).session.id

    async def turn(self, session_id: SessionId, text: str) -> TurnResult:
        return await self._turns.handle(TurnHandlerInput(session_id=session_id, text=text))
