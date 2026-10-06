"""One tutor turn end to end over the scripted LLM and a real database."""

import pytest

from core.shared.llm.call_scope import current_scope
from core.shared.llm.client import CallMeta, JsonObject, LLMError, LLMProviderError, LLMRequest, Stage
from core.shared.llm.infra.logged_client import LoggedLLMClient
from core.shared.llm_calls.infra.sqlmodel_repository import SQLModelLLMCallRepository
from core.shared.storage.session_provider import SQLModelSessionProvider
from core.tutoring.application.turn_handler import TurnInput
from core.tutoring.domain.exceptions import ConcurrentTurnException, ModelOutputException
from core.tutoring.domain.values.session_state import SessionState
from tests.core.tutoring.builders import COURSE, EX4C, OK, diagnosis_json, tutoring
from tests.fakes.llm import ScriptedLLMClient


def _users(llm: ScriptedLLMClient, stage: Stage) -> list[str]:
    return [r.user for r in llm.requests[stage]]


async def test_retries_after_rejection_and_the_writer_never_sees_the_solution(
    session_provider: SQLModelSessionProvider,
) -> None:
    llm = ScriptedLLMClient(
        {
            Stage.DIAGNOSIS: [diagnosis_json(steps={"candidat": "completat"}, nivell_desorientacio="en_cami")],
            Stage.REPLY: [
                {"text": r"El límit és 0 perquè $\le |x|$. Ho veus?"},  # leaks, rejected by regex
                {"text": "Bona feina amb els camins. Com podries fitar el quocient per una cosa que tendeixi a 0?"},
            ],
            Stage.GUARD: [OK],
        }
    )
    t = tutoring(llm, session_provider)
    started = await t.starter.start(EX4C.id)
    out = await t.turns.handle(TurnInput(session_id=started.session.id, text="He provat y=kx i y=kx^2 i dona 0"))
    assert out.message.startswith("Bona feina")
    trace = out.trace.model_dump()
    assert len(trace["intents"]) == 2 and trace["intents"][0]["determinista"]
    assert not trace["fallback"]
    writer_inputs = _users(llm, Stage.REPLY)
    for u in writer_inputs:
        assert EX4C.step("acotar").detail not in u
        assert "RESULTAT CORRECTE" not in u
    assert "REBUTJAT" in writer_inputs[1]
    stored = await t.sessions.get(started.session.id)
    assert [m.role for m in stored.history] == ["alumne", "tutor"] and stored.version == 1


async def test_falls_back_when_every_draft_is_rejected(session_provider: SQLModelSessionProvider) -> None:
    bad: JsonObject = {"veredicte": "rebutjat", "infraccions": ["revela_pas_futur"], "explicacio": "avança la fita"}
    llm = ScriptedLLMClient(
        {
            Stage.DIAGNOSIS: [diagnosis_json(errors_detectats=["camins_com_a_prova"])],
            Stage.REPLY: [{"text": "Pensa-hi, d'acord?"}] * 3,
            Stage.GUARD: [bad] * 3,
        }
    )
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    out = await t.turns.handle(TurnInput(session_id=sid, text="dona 0 per tots els camins, per tant és 0"))
    assert out.trace.fallback and out.references == []
    assert out.message == EX4C.mistake("camins_com_a_prova").question


async def test_guard_verdict_inconsistency_is_fail_closed(session_provider: SQLModelSessionProvider) -> None:
    llm = ScriptedLLMClient(
        {
            Stage.DIAGNOSIS: [diagnosis_json()],
            Stage.REPLY: [{"text": "Què has provat?"}] * 3,
            Stage.GUARD: [{"veredicte": "ok", "infraccions": ["revela_resultat"], "explicacio": ""}] * 3,
        }
    )
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    assert (await t.turns.handle(TurnInput(session_id=sid, text="no sé què fer"))).trace.fallback


async def test_an_unavailable_guard_or_writer_fails_closed(session_provider: SQLModelSessionProvider) -> None:
    llm = ScriptedLLMClient(
        {
            Stage.DIAGNOSIS: [diagnosis_json()],
            Stage.REPLY: [LLMError("reply: truncated"), {"text": "   "}, {"text": "Què has provat?"}],
            Stage.GUARD: [{"veredicte": "potser"}],
        }
    )
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    out = await t.turns.handle(TurnInput(session_id=sid, text="no sé què fer"))
    attempts = out.trace.model_dump()["intents"]
    assert attempts[0] == {"missatge": None, "error": "reply: truncated"}
    assert attempts[1] == {"missatge": None, "error": "resposta: empty message"}
    assert attempts[2]["llm"]["veredicte"] == "rebutjat"
    assert attempts[2]["llm"]["explicacio"].startswith("guardià no disponible:")
    assert out.trace.fallback
    # Every call that answered is accounted for, even when its answer was unusable.
    assert [c.stage for c in out.trace.calls] == ["diagnosis", "reply", "reply", "guard"]


async def test_turn_is_atomic_on_any_failure(session_provider: SQLModelSessionProvider) -> None:
    """An exception in any stage leaves the stored session exactly as before."""
    llm = ScriptedLLMClient({Stage.DIAGNOSIS: [diagnosis_json()], Stage.REPLY: [LLMProviderError("rate limited", 429)]})
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    with pytest.raises(LLMProviderError):
        await t.turns.handle(TurnInput(session_id=sid, text="hola"))
    stored = await t.sessions.get(sid)
    assert stored.history == [] and stored.state == SessionState() and stored.version == 0
    assert await t.sessions.turns(sid) == []


async def test_a_failed_diagnosis_does_not_record_the_turn(session_provider: SQLModelSessionProvider) -> None:
    llm = ScriptedLLMClient({Stage.DIAGNOSIS: [LLMError("diagnosis: invalid JSON from the model")]})
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    with pytest.raises(ModelOutputException) as e:
        await t.turns.handle(TurnInput(session_id=sid, text="hola"))
    assert e.value.error_code == 502 and e.value.message.startswith("La diagnosi ha fallat")
    stored = await t.sessions.get(sid)
    assert stored.history == [] and stored.state.turns == 0


async def test_fallback_delivers_the_planned_level(session_provider: SQLModelSessionProvider) -> None:
    """When every draft is rejected, the student still gets the content of the level the state records."""
    bad: JsonObject = {"veredicte": "rebutjat", "infraccions": ["no_segueix_l_accio"], "explicacio": "x"}
    llm = ScriptedLLMClient(
        {
            Stage.DIAGNOSIS: [diagnosis_json(intencio="demana_pista", nivell_desorientacio="perdut")],
            Stage.REPLY: [{"text": "Pensa-hi."}] * 3,
            Stage.GUARD: [bad] * 3,
        }
    )
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    out = await t.turns.handle(TurnInput(session_id=sid, text="no sé res"))
    assert out.trace.fallback and out.trace.plan.hint_level == 2
    assert EX4C.step("candidat").idea.strip()[:30] in out.message


async def test_reply_references_are_the_allowed_items_it_cites(session_provider: SQLModelSessionProvider) -> None:
    background = EX4C.theory[0].item_id
    item = COURSE.theory_item(background)
    name = item.label.split(" (")[0]  # "Definició 6"
    llm = ScriptedLLMClient(
        {
            Stage.DIAGNOSIS: [diagnosis_json(intencio="pregunta_conceptual", teoria_pregunta=[background])],
            # Cites the allowed item, and an item it was never shown (Teorema 4 del Tema 6): only the first counts.
            Stage.REPLY: [
                {"text": f"Recorda la {name} del Tema {item.topic} i el Teorema 4 del Tema 6. Com l'aplicaries aquí?"}
            ],
            Stage.GUARD: [OK],
        }
    )
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    out = await t.turns.handle(TurnInput(session_id=sid, text="Què vol dir exactament que existeixi el límit?"))
    assert [r.id for r in out.references] == [background]
    assert out.references[0] == item
    assert background in out.trace.allowed_theory
    assert item.statement.strip()[:40] in _users(llm, Stage.REPLY)[0]


async def test_static_context_is_identical_across_turns_for_caching(session_provider: SQLModelSessionProvider) -> None:
    llm = ScriptedLLMClient(
        {
            Stage.DIAGNOSIS: [diagnosis_json(), diagnosis_json()],
            Stage.REPLY: [{"text": "Què has provat?"}] * 2,
            Stage.GUARD: [OK, OK],
        }
    )
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    await t.turns.handle(TurnInput(session_id=sid, text="no sé per on començar"))
    await t.turns.handle(TurnInput(session_id=sid, text="he provat rectes"))
    diagnosis_ctx = [r.context for r in llm.requests[Stage.DIAGNOSIS]]
    guard_ctx = [r.context for r in llm.requests[Stage.GUARD]]
    assert diagnosis_ctx[0] == diagnosis_ctx[1] and guard_ctx[0] == guard_ctx[1]
    assert diagnosis_ctx[0] and EX4C.full_reference() in diagnosis_ctx[0]
    # The conversation is dynamic: it must not be part of the cached prefix.
    assert "he provat rectes" not in diagnosis_ctx[1]


async def test_a_photo_turn_is_traced_as_such(session_provider: SQLModelSessionProvider) -> None:
    llm = ScriptedLLMClient(
        {Stage.DIAGNOSIS: [diagnosis_json()], Stage.REPLY: [{"text": "Què has provat fins ara?"}], Stage.GUARD: [OK]}
    )
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    out = await t.turns.handle(TurnInput(session_id=sid, text="  no sé seguir ", origin="foto"))
    assert out.trace.model_dump()["origen"] == "foto"
    [turn] = await t.sessions.turns(sid)
    assert turn.origin == "foto" and turn.student_text == "no sé seguir"


async def test_turns_are_persisted_logged_and_survive_a_restart(session_provider: SQLModelSessionProvider) -> None:
    """Session row, turn row, one log row per model call filed under its session and turn; a new handler
    over the same database (a restart, another worker) continues the session."""
    llm = ScriptedLLMClient(
        {
            Stage.DIAGNOSIS: [diagnosis_json(), diagnosis_json()],
            Stage.REPLY: [{"text": "Què has provat?"}] * 2,
            Stage.GUARD: [OK, OK],
        }
    )
    calls = SQLModelLLMCallRepository(session_provider)
    logged = LoggedLLMClient(llm, calls)
    sid = (await tutoring(logged, session_provider).starter.start(EX4C.id)).session.id
    await tutoring(logged, session_provider).turns.handle(TurnInput(session_id=sid, text="no sé per on començar"))

    [turn] = await tutoring(logged, session_provider).sessions.turns(sid)
    assert turn.student_text == "no sé per on començar" and turn.tutor_text == "Què has provat?"
    assert turn.number == 1 and turn.trace.plan.action
    assert {(c.stage, c.turn) for c in await calls.of_session(sid)} == {
        ("diagnosis", 1),
        ("reply", 1),
        ("guard", 1),
    }

    again = tutoring(logged, session_provider)
    await again.turns.handle(TurnInput(session_id=sid, text="he provat rectes"))
    assert [t.number for t in await again.sessions.turns(sid)] == [1, 2]
    stored = await again.sessions.get(sid)
    assert len(stored.history) == 4 and stored.state.turns == 2 and stored.version == 2
    assert {c.turn for c in await calls.of_session(sid)} == {1, 2}


async def test_a_concurrent_turn_on_the_same_session_is_rejected(session_provider: SQLModelSessionProvider) -> None:
    """Two turns of one session in flight (two tabs): the second is refused with a 409 before any model call,
    and the first one completes."""
    refused: list[ConcurrentTurnException] = []

    class InterleavingLLM(ScriptedLLMClient):
        inner_turn: TurnInput | None = None

        async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
            pending, self.inner_turn = self.inner_turn, None
            if pending is not None:
                # While the first turn waits for its diagnosis, the second tab sends a message.
                assert current_scope().turn == 1
                with pytest.raises(ConcurrentTurnException) as e:
                    await t.turns.handle(pending)
                refused.append(e.value)
            return await super().structured(stage, request)

    llm = InterleavingLLM(
        {Stage.DIAGNOSIS: [diagnosis_json()], Stage.REPLY: [{"text": "Què has provat?"}], Stage.GUARD: [OK]}
    )
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    llm.inner_turn = TurnInput(session_id=sid, text="segona pestanya")
    await t.turns.handle(TurnInput(session_id=sid, text="primera pestanya"))
    assert [e.error_code for e in refused] == [409] and llm.calls(Stage.DIAGNOSIS) == 1
    [turn] = await t.sessions.turns(sid)
    assert turn.student_text == "primera pestanya"
    stored = await t.sessions.get(sid)
    assert [m.text for m in stored.history] == ["primera pestanya", "Què has provat?"] and stored.version == 1
    # The claim is released: the next message goes through.
    llm.then(Stage.DIAGNOSIS, diagnosis_json()).then(Stage.REPLY, {"text": "I ara?"}).then(Stage.GUARD, OK)
    assert (await t.turns.handle(TurnInput(session_id=sid, text="segona"))).trace.turn == 2


async def test_a_failed_turn_releases_its_claim(session_provider: SQLModelSessionProvider) -> None:
    llm = ScriptedLLMClient({Stage.DIAGNOSIS: [LLMError("boom")]})
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    with pytest.raises(ModelOutputException):
        await t.turns.handle(TurnInput(session_id=sid, text="hola"))
    llm.then(Stage.DIAGNOSIS, diagnosis_json()).then(Stage.REPLY, {"text": "Què has provat?"}).then(Stage.GUARD, OK)
    assert (await t.turns.handle(TurnInput(session_id=sid, text="hola"))).trace.turn == 1
