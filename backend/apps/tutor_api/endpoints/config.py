from fastapi import APIRouter, Depends

from apps.tutor_api.dependencies import get_config, is_professor, may_generate
from apps.tutor_api.schemas.config import ConfigResponse, StageResponse
from core.shared.llm.infra.stage_configs import stage_configs
from settings import Config, api_key_variable

router = APIRouter()


@router.get("/api/config")
async def get_app_config(
    config: Config = Depends(get_config),
    professor: bool = Depends(is_professor),
    generation_allowed: bool = Depends(may_generate),
) -> ConfigResponse:
    if not (professor or config.DEMO_MODE):
        return ConfigResponse(panell_professor=professor, pot_generar=generation_allowed)
    return ConfigResponse(
        panell_professor=professor,
        pot_generar=generation_allowed,
        provider=config.LLM_PROVIDER,
        api_key=bool(config.api_key(api_key_variable(config))),
        stages={
            stage: StageResponse(model=c.model, effort=c.effort, max_tokens=c.max_tokens)
            for stage, c in stage_configs(config).items()
        },
    )
