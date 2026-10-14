"""A turn survives a truncated diagnosis, counts the tokens of failed calls, and its fallback links what it cites."""

import pytest

from core.shared.llm.client import CallMeta, JsonObject, LLMError, LLMProviderError, Stage, TruncatedOutputError
from core.shared.storage.session_provider import SQLModelSessionProvider
from core.tutoring.application.turn_handler import TurnInput
from core.tutoring.domain.exceptions import ModelOutputException
from tests.core.tutoring.builders import COURSE, EX4C, OK, diagnosis_json, tutoring
from tests.fakes.llm import ScriptedLLMClient


def _billed(error: LLMError, stage: Stage, output_tokens: int) -> LLMError:
    error.meta = CallMeta(stage=stage, model="scripted", latency_ms=5, input_tokens=100, output_tokens=output_tokens)
    return error


async def test_a_truncated_diagnosis_is_asked_again_once_and_both_calls_are_traced(
    session_provider: SQLModelSessionProvider,
) -> None:
    looped = _billed(TruncatedOutputError("diagnosis: output truncated at max_tokens=3000"), Stage.DIAGNOSIS, 3000)
    llm = ScriptedLLMClient(
        {
            Stage.DIAGNOSIS: [looped, diagnosis_json()],
            Stage.REPLY: [{"text": "Què has provat fins ara?"}],
            Stage.GUARD: [OK],
        }
    )
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    out = await t.turns.handle(TurnInput(session_id=sid, text="no sé què fer"))
    assert llm.calls(Stage.DIAGNOSIS) == 2
    diagnosis_calls = [c for c in out.trace.calls if c.stage == Stage.DIAGNOSIS]
    assert [c.output_tokens for c in diagnosis_calls] == [3000, 2]


async def test_a_diagnosis_truncated_twice_fails_the_turn(session_provider: SQLModelSessionProvider) -> None:
    llm = ScriptedLLMClient({Stage.DIAGNOSIS: [TruncatedOutputError("diagnosis: output truncated")] * 3})
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    with pytest.raises(ModelOutputException):
        await t.turns.handle(TurnInput(session_id=sid, text="no sé què fer"))
    assert llm.calls(Stage.DIAGNOSIS) == 2


@pytest.mark.parametrize("error", [LLMError("diagnosis: empty response"), LLMProviderError("outage")])
async def test_other_diagnosis_failures_are_not_retried(
    session_provider: SQLModelSessionProvider, error: LLMError
) -> None:
    llm = ScriptedLLMClient({Stage.DIAGNOSIS: [error, diagnosis_json()]})
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    with pytest.raises((ModelOutputException, LLMProviderError)):
        await t.turns.handle(TurnInput(session_id=sid, text="no sé què fer"))
    assert llm.calls(Stage.DIAGNOSIS) == 1


async def test_a_failed_draft_counts_its_billed_tokens(session_provider: SQLModelSessionProvider) -> None:
    truncated = _billed(TruncatedOutputError("reply: output truncated at max_tokens=1500"), Stage.REPLY, 1500)
    llm = ScriptedLLMClient(
        {
            Stage.DIAGNOSIS: [diagnosis_json()],
            Stage.REPLY: [truncated, {"text": "Què has provat fins ara?"}],
            Stage.GUARD: [OK],
        }
    )
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    out = await t.turns.handle(TurnInput(session_id=sid, text="no sé què fer"))
    assert [c.output_tokens for c in out.trace.calls if c.stage == Stage.REPLY] == [1500, 2]


async def test_the_concept_fallback_cites_the_answering_item_and_links_it(
    session_provider: SQLModelSessionProvider,
) -> None:
    background = EX4C.theory[0].item_id
    bad: JsonObject = {"veredicte": "rebutjat", "infraccions": ["no_segueix_l_accio"], "explicacio": "x"}
    llm = ScriptedLLMClient(
        {
            Stage.DIAGNOSIS: [diagnosis_json(intencio="pregunta_conceptual", teoria_pregunta=[background])],
            Stage.REPLY: [{"text": "Pensa-hi. Ho veus?"}] * 3,
            Stage.GUARD: [bad] * 3,
        }
    )
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    out = await t.turns.handle(TurnInput(session_id=sid, text="Què vol dir que existeixi el límit?"))
    assert out.trace.fallback
    assert COURSE.theory_item(background).label.split(" (")[0] in out.message
    assert [r.id for r in out.references] == [background]
