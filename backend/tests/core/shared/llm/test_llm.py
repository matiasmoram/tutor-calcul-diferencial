import pytest

from core.shared.llm.call_scope import call_scope
from core.shared.llm.client import (
    LLMError,
    LLMRequest,
    MalformedOutputError,
    Stage,
    parse_json,
    plain_text,
    repair_latex,
)
from core.shared.llm.infra.logged_client import LoggedLLMClient
from core.shared.llm.infra.retrying_client import RetryingLLMClient
from core.shared.llm.infra.stage_router import StageRouter
from core.shared.llm_calls.domain.llm_call import LLMCall
from core.shared.llm_calls.domain.repository import LLMCallRepository
from core.shared.llm_calls.infra.sqlmodel_repository import SQLModelLLMCallRepository
from core.shared.storage.session_provider import SQLModelSessionProvider
from tests.fakes.llm import ScriptedLLMClient


def test_repair_latex_undoes_json_escape_damage() -> None:
    damaged = {"m": "Fixa't en $\frac{1}{2}$ i $x \neq 0$", "l": ["\theta"], "n": 3}
    assert repair_latex(damaged) == {"m": "Fixa't en $\\frac{1}{2}$ i $x \\neq 0$", "l": ["\\theta"], "n": 3}
    assert repair_latex("línia\nnova fora de fórmules") == "línia\nnova fora de fórmules"


def test_invalid_json_is_an_llm_error() -> None:
    with pytest.raises(LLMError):
        parse_json("diagnosis", "{not json")
    with pytest.raises(LLMError):
        parse_json("diagnosis", "[1, 2]")


def test_text_no_column_can_store_is_malformed_output() -> None:
    # Real gpt-5.4-mini output that crashed the Postgres save of a whole quiz: a NUL inside a formula.
    with pytest.raises(MalformedOutputError, match=r"U\+0000"):
        parse_json("quiz_verification", r'{"r": [{"j": "Si $f\\neq$ \u00e9s $\u0000ab$"}]}')
    with pytest.raises(MalformedOutputError, match=r"U\+D800"):
        parse_json("quiz_grading", r'{"f": "\ud800"}')
    with pytest.raises(MalformedOutputError):
        plain_text("reply", "Fixa't en $\x00ab$")
    # What repair_latex turns back into LaTeX, and plain newlines, stay valid.
    assert parse_json("reply", r'{"m": "$\frac{1}{2}$\nl\u00ednia"}') == {"m": "$\\frac{1}{2}$\nlínia"}
    assert plain_text("reply", "línia\nnova") == {"text": "línia\nnova"}


def test_plain_text_keeps_tabs_and_carriage_returns() -> None:
    # No JSON escaping happened, so a tab or a CRLF is what the model wrote: asking again would only pay twice.
    assert plain_text("reply", "a\tb\r\nc") == {"text": "a\tb\r\nc"}
    for bad in ("\x00", "\x07", "\x0b", "\x0c", "\x1b", "\ud800"):
        with pytest.raises(MalformedOutputError):
            plain_text("reply", f"x{bad}y")
    # In JSON a tab is escape damage ("\\theta"), which repair_latex maps back to the LaTeX backslash.
    assert parse_json("reply", r'{"m": "$\theta$"}') == {"m": "$\\theta$"}
    with pytest.raises(MalformedOutputError):
        parse_json("reply", r'{"m": "a\u0007b"}')


async def test_a_malformed_answer_is_asked_again_once() -> None:
    inner = ScriptedLLMClient({Stage.GUARD: [MalformedOutputError("guard: bad"), {"ok": True}]})
    assert (await RetryingLLMClient(inner).structured(Stage.GUARD, LLMRequest("s", "u", {})))[0] == {"ok": True}
    assert inner.calls(Stage.GUARD) == 2
    twice = ScriptedLLMClient({Stage.GUARD: [MalformedOutputError("a"), MalformedOutputError("b"), {"ok": True}]})
    with pytest.raises(MalformedOutputError, match="b"):
        await RetryingLLMClient(twice).structured(Stage.GUARD, LLMRequest("s", "u", {}))
    # Truncation or a provider failure would only fail again (and cost again): never retried.
    truncated = ScriptedLLMClient({Stage.GUARD: [LLMError("guard: output truncated"), {"ok": True}]})
    with pytest.raises(LLMError, match="truncated"):
        await RetryingLLMClient(truncated).structured(Stage.GUARD, LLMRequest("s", "u", {}))
    assert truncated.calls(Stage.GUARD) == 1


async def test_stage_router_sends_each_stage_to_its_backend() -> None:
    a = ScriptedLLMClient({Stage.DIAGNOSIS: [{"x": 1}]})
    b = ScriptedLLMClient({Stage.REPLY: [{"text": "hola"}]})
    router = StageRouter({Stage.DIAGNOSIS: a, Stage.REPLY: b})
    assert (await router.structured(Stage.DIAGNOSIS, LLMRequest("s", "u", {})))[0] == {"x": 1}
    assert (await router.structured(Stage.REPLY, LLMRequest("s", "u")))[0] == {"text": "hola"}
    assert a.calls(Stage.DIAGNOSIS) == 1 and b.calls(Stage.REPLY) == 1


async def test_every_call_is_logged_with_its_scope_even_failures(session_provider: SQLModelSessionProvider) -> None:
    calls = SQLModelLLMCallRepository(session_provider)
    inner = ScriptedLLMClient({Stage.REPLY: [{"text": "hola"}], Stage.GUARD: [RuntimeError("boom")]})
    llm = LoggedLLMClient(inner, calls)
    with call_scope("s9", turn=3):
        assert (await llm.structured(Stage.REPLY, LLMRequest("sys", "user")))[0] == {"text": "hola"}
        with pytest.raises(RuntimeError):
            await llm.structured(Stage.GUARD, LLMRequest("sys", "user", {}))
    logged = await calls.of_session("s9")
    assert [(c.stage, c.ok, c.turn) for c in reversed(logged)] == [("reply", True, 3), ("guard", False, 3)]
    assert logged[1].response == {"text": "hola"} and logged[1].input_tokens == 10
    assert logged[0].error == "RuntimeError: boom" and logged[0].prompt is None  # prompts only with LOG_PROMPTS


async def test_a_failing_log_never_breaks_the_call() -> None:
    class BrokenLog(LLMCallRepository):
        async def add(self, call: LLMCall) -> None:
            raise OSError("database down")

        async def of_session(self, session_id: str, limit: int = 500) -> list[LLMCall]:
            return []

    llm = LoggedLLMClient(ScriptedLLMClient({Stage.REPLY: [{"text": "ok"}]}), BrokenLog())
    assert (await llm.structured(Stage.REPLY, LLMRequest("s", "u")))[0] == {"text": "ok"}
