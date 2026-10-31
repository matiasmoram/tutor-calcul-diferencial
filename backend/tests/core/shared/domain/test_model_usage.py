import pytest

from core.shared.domain.model_usage import ModelUsage
from core.shared.llm.client import CallMeta, Stage
from core.tutoring.domain.values.turn_trace import ModelCall

USAGE: dict[str, object] = {
    "model": "gpt-x",
    "latency_ms": 1234,
    "input_tokens": 900,
    "output_tokens": 120,
    "cached_tokens": 512,
}
UNREPORTED_TOKENS: dict[str, object] = {"model": "offline:x", "latency_ms": 0}


def test_usage_is_stored_with_its_english_keys() -> None:
    usage = ModelUsage.model_validate(USAGE)

    assert usage.model_dump(mode="json") == USAGE
    assert ModelUsage.model_validate_json(usage.model_dump_json()) == usage


def test_unreported_token_counts_are_zero() -> None:
    assert ModelUsage.model_validate(UNREPORTED_TOKENS).model_dump(mode="json") == {
        **UNREPORTED_TOKENS,
        "input_tokens": 0,
        "output_tokens": 0,
        "cached_tokens": 0,
    }


@pytest.mark.parametrize("data", [USAGE, UNREPORTED_TOKENS])
def test_usage_writes_the_same_json_as_the_per_context_copies(data: dict[str, object]) -> None:
    expected = ModelUsage.model_validate(data).model_dump_json()

    assert ModelCall.model_validate({"stage": "diagnosis", **data}).model_dump_json(exclude={"stage"}) == expected


def test_call_meta_maps_every_counter_to_the_usage() -> None:
    meta = CallMeta(
        stage=Stage.QUIZ_GRADING, model="gpt-x", latency_ms=1234, input_tokens=900, output_tokens=120, cached_tokens=512
    )

    assert meta.usage() == ModelUsage.model_validate(USAGE)
