from collections.abc import Mapping

from core.shared.llm.client import Stage, StageConfig
from settings import Config

DEFAULT_MODELS: Mapping[str, str] = {
    "anthropic": "claude-opus-5-5",
    "gemini": "gemini-3.5-flash",
    "openai": "gpt-5.5",
    "openrouter": "openai/gpt-oss-20b",
}
# Gemini quotas are per model: the stages are spread over several models.
GEMINI_STAGE_MODELS: Mapping[Stage, str] = {
    Stage.DIAGNOSIS: "gemini-3.5-flash",
    Stage.REPLY: "gemini-3.5-flash-lite",
    Stage.GUARD: "gemini-3-flash-preview",
    Stage.TRANSCRIPTION: "gemini-3.5-flash",
    Stage.QUIZ_GENERATION: "gemini-3.5-flash",
    Stage.QUIZ_VERIFICATION: "gemini-3-flash-preview",
    Stage.QUIZ_AUDIT: "gemini-3.5-flash-lite",
    Stage.QUIZ_GRADING: "gemini-3-flash-preview",
    Stage.QUIZ_EXTRACTION: "gemini-3.5-flash-lite",
}
# Diagnosis needs the strongest judgment; phrasing and checking run on a faster model.
OPENAI_STAGE_MODELS: Mapping[Stage, str] = {
    Stage.DIAGNOSIS: "gpt-5.5",
    Stage.REPLY: "gpt-5.4-mini",
    Stage.GUARD: "gpt-5.4-mini",
    Stage.TRANSCRIPTION: "gpt-5.5",
    Stage.MISTAKES_GENERATION: "gpt-5.5",
    Stage.MISTAKES_VERIFICATION: "gpt-5.5",
    Stage.MISTAKES_GRADING: "gpt-5.5",
    Stage.QUIZ_GENERATION: "gpt-5.5",
    Stage.QUIZ_VERIFICATION: "gpt-5.5",
    Stage.QUIZ_AUDIT: "gpt-5.5",
    Stage.QUIZ_GRADING: "gpt-5.5",
    Stage.QUIZ_EXTRACTION: "gpt-5.4-mini",
}
STAGE_MODELS: Mapping[str, Mapping[Stage, str]] = {"gemini": GEMINI_STAGE_MODELS, "openai": OPENAI_STAGE_MODELS}

DEFAULT_EFFORT: Mapping[Stage, str] = {
    Stage.DIAGNOSIS: "medium",
    Stage.REPLY: "low",
    Stage.GUARD: "low",
    # Handwriting OCR: reading maths reliably needs a strong vision model, not deep reasoning.
    Stage.TRANSCRIPTION: "low",
    # "Find the error": writing plausible, subtle errors and checking them both need real reasoning.
    Stage.MISTAKES_GENERATION: "medium",
    Stage.MISTAKES_VERIFICATION: "medium",
    Stage.MISTAKES_GRADING: "low",
    # "Cert o fals": generated in batches of a few statements; the blind solver must really reason.
    Stage.QUIZ_GENERATION: "medium",
    Stage.QUIZ_VERIFICATION: "medium",
    Stage.QUIZ_AUDIT: "medium",
    Stage.QUIZ_GRADING: "low",
    # Transcribes the student's computations for sympy: no judgment, never sees the solutions.
    Stage.QUIZ_EXTRACTION: "low",
}
# 20000 is the most Anthropic accepts without streaming. The tutor stages are capped a little above their real output
# size (reasoning included), so a model stuck in a repetition loop stops within seconds.
MAX_TOKENS: Mapping[Stage, int] = {
    Stage.DIAGNOSIS: 3000,
    Stage.REPLY: 1500,
    Stage.GUARD: 1500,
    Stage.TRANSCRIPTION: 4000,
    Stage.QUIZ_GENERATION: 20000,
    Stage.QUIZ_VERIFICATION: 20000,
    Stage.QUIZ_AUDIT: 20000,
    Stage.QUIZ_GRADING: 20000,
}


def stage_configs(config: Config) -> dict[Stage, StageConfig]:
    provider = config.LLM_PROVIDER

    def model(stage: Stage) -> str:
        default = config.TUTOR_MODEL or STAGE_MODELS.get(provider, {}).get(stage, DEFAULT_MODELS[provider])
        return config.stage_model(stage) or default

    return {
        stage: StageConfig(
            model=model(stage),
            effort=config.stage_effort(stage) or DEFAULT_EFFORT[stage],
            max_tokens=MAX_TOKENS.get(stage, 16000),
        )
        for stage in Stage
    }
