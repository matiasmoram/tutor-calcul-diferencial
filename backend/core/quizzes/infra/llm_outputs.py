"""Reading the stages' JSON into domain values. The schemas make malformed output rare; what still does not fit
(a non-object item, a value of the wrong type) is dropped, never trusted."""

from loguru import logger
from pydantic import BaseModel, ValidationError

from core.shared.llm.client import JsonObject


def objects(data: JsonObject, key: str) -> list[dict[str, object]]:
    """The JSON objects of the list `data[key]` (anything else in it is ignored)."""
    value = data.get(key)
    if not isinstance(value, list):
        return []
    return [{str(k): v for k, v in item.items()} for item in value if isinstance(item, dict)]


def parse_all[M: BaseModel](model: type[M], items: list[dict[str, object]], stage: str) -> list[M]:
    out: list[M] = []
    for item in items:
        try:
            out.append(model.model_validate(item))
        except ValidationError as e:
            logger.warning("{}: dropped a malformed {} ({} errors)", stage, model.__name__, e.error_count())
    return out
