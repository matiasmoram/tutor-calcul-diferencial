import pytest

from core.shared.llm.call_scope import call_scope
from core.shared.llm.client import LLMError, LLMRequest, Stage, parse_json, repair_latex
from core.shared.llm.infra.logged_client import LoggedLLMClient
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
