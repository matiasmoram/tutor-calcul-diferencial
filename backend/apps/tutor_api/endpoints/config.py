from fastapi import APIRouter, Depends
from pydantic import BaseModel

from apps.tutor_api.dependencies import KEY_VARIABLES, get_config, is_professor
from core.shared.llm.infra.stage_configs import stage_configs
from settings import Config

router = APIRouter()


class StageResponse(BaseModel):
    model: str
    effort: str
    max_tokens: int


class ConfigResponse(BaseModel):
    panell_professor: bool
    provider: str
    api_key: bool
    stages: dict[str, StageResponse]


@router.get("/api/config")
async def get_app_config(
    config: Config = Depends(get_config), professor: bool = Depends(is_professor)
) -> ConfigResponse:
    return ConfigResponse(
        panell_professor=professor,
        provider=config.LLM_PROVIDER,
        api_key=bool(config.api_key(KEY_VARIABLES.get(config.LLM_PROVIDER, "ANTHROPIC_API_KEY"))),
        stages={
            stage: StageResponse(model=c.model, effort=c.effort, max_tokens=c.max_tokens)
            for stage, c in stage_configs(config).items()
        },
    )
