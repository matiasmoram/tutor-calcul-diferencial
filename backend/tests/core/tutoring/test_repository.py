"""The tutor session store on a real (SQLite) database, and the professor's view of it."""

import pytest

from core.shared.domain.ids import ExerciseId, SessionId
from core.shared.llm.client import Stage
from core.shared.storage.session_provider import SQLModelSessionProvider
from core.tutoring.application.turn_handler import TurnInput
from core.tutoring.domain.entities.tutor_session import TutorSession
from core.tutoring.domain.exceptions import ConcurrentTurnException, TutorSessionNotFoundException
from core.tutoring.infra.sqlmodel_repository import SQLModelTutorSessionRepository
from tests.core.tutoring.builders import EX4C, OK, diagnosis_json, tutoring
from tests.fakes.llm import ScriptedLLMClient


def _stuck_student_llm(turns: int) -> ScriptedLLMClient:
    """A student asking for help twice without trying: the same plan twice (a loop for the professor panel)."""
    return ScriptedLLMClient(
        {
            Stage.DIAGNOSIS: [diagnosis_json(intencio="demana_pista", nivell_desorientacio="encallat")] * turns,
            Stage.REPLY: [{"text": "Què obtens sobre les rectes?"}] * turns,
            Stage.GUARD: [OK] * turns,
        }
    )


async def test_a_session_round_trips(session_provider: SQLModelSessionProvider) -> None:
    repo = SQLModelTutorSessionRepository(session_provider)
    session = TutorSession.start(ExerciseId("t2-4c"), now=100.0)
    await repo.add(session)
    assert await repo.get(session.id) == session
    with pytest.raises(TutorSessionNotFoundException) as e:
        await repo.get(SessionId.generate())
    assert e.value.error_code == 404


async def test_session_turns_and_professor_flags(session_provider: SQLModelSessionProvider) -> None:
    t = tutoring(_stuck_student_llm(2), session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    for text in ("no sé", "res"):
        await t.turns.handle(TurnInput(session_id=sid, text=text))
    await t.starter.start(EX4C.id)  # a session without turns is not listed

    stored = await t.sessions.get(sid)
    assert stored.state.turns == 2 and stored.history[0].text == "no sé"
    [row] = await t.browser.list_sessions()
    assert row.turns == 2 and row.loops == 1 and not row.closed and row.frustration == 0
    assert row.model_dump()["bucles"] == 1 and row.model_dump()["exercici"] == "t2-4c"
    transcript = await t.browser.transcript(sid)
    assert [turn.number for turn in transcript.turns] == [1, 2] and transcript.exercise_id == "t2-4c"
    assert transcript.turns[0].trace.model_dump()["pla"]["accio"] == "pista"


async def test_the_professor_view_of_an_unknown_or_empty_session_is_not_found(
    session_provider: SQLModelSessionProvider,
) -> None:
    t = tutoring(_stuck_student_llm(0), session_provider)
    empty = (await t.starter.start(EX4C.id)).session.id
    for sid in (empty, SessionId.generate()):
        with pytest.raises(TutorSessionNotFoundException):
            await t.browser.transcript(sid)


async def test_saving_a_turn_on_a_stale_version_is_a_conflict(session_provider: SQLModelSessionProvider) -> None:
    t = tutoring(_stuck_student_llm(1), session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    stale = await t.sessions.get(sid)
    await t.turns.handle(TurnInput(session_id=sid, text="no sé"))
    [turn] = await t.sessions.turns(sid)

    assert await t.sessions.claim_turn(sid, now=5.0, stale_before=0.0)
    stale.record_turn("una altra pestanya", "...", stale.state, now=1.0)
    with pytest.raises(ConcurrentTurnException) as e:
        await t.sessions.save_turn(stale, turn.model_copy(update={"number": 2}), claimed_at=5.0)
    assert e.value.error_code == 409
    assert [x.number for x in await t.sessions.turns(sid)] == [1]  # the conflicting turn left nothing behind
    current = await t.sessions.get(sid)
    assert current.version == 1 and current.history[0].text == "no sé"
    saved = await t.sessions.save_turn(current, turn.model_copy(update={"number": 2}), claimed_at=5.0)
    assert saved.version == 2 and (await t.sessions.get(sid)).version == 2


async def test_a_turn_claim_is_released_or_used_only_by_its_owner(session_provider: SQLModelSessionProvider) -> None:
    """A turn whose claim went stale and was taken over can neither drop the new claim nor store its turn."""
    t = tutoring(_stuck_student_llm(1), session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    await t.turns.handle(TurnInput(session_id=sid, text="no sé"))
    [turn] = await t.sessions.turns(sid)
    current = await t.sessions.get(sid)
    current.record_turn("tard", "...", current.state, now=1.0)
    late = turn.model_copy(update={"number": 2})

    assert await t.sessions.claim_turn(sid, now=100.0, stale_before=0.0)
    assert not await t.sessions.claim_turn(sid, now=101.0, stale_before=1.0)
    assert await t.sessions.claim_turn(sid, now=1000.0, stale_before=500.0)  # the first claim went stale
    with pytest.raises(ConcurrentTurnException):
        await t.sessions.save_turn(current, late, claimed_at=100.0)
    await t.sessions.release_turn(sid, claimed_at=100.0)
    assert not await t.sessions.claim_turn(sid, now=1001.0, stale_before=501.0)  # the takeover still holds it
    saved = await t.sessions.save_turn(current, late, claimed_at=1000.0)  # and its save releases it
    assert saved.version == 2 and [x.number for x in await t.sessions.turns(sid)] == [1, 2]
    assert await t.sessions.claim_turn(sid, now=1002.0, stale_before=502.0)
    await t.sessions.release_turn(sid, claimed_at=1002.0)
    assert await t.sessions.claim_turn(sid, now=1003.0, stale_before=503.0)


async def test_claiming_a_turn_of_an_unknown_session_is_not_found(session_provider: SQLModelSessionProvider) -> None:
    repo = SQLModelTutorSessionRepository(session_provider)
    with pytest.raises(TutorSessionNotFoundException) as e:
        await repo.claim_turn(SessionId.generate(), now=1.0, stale_before=0.0)
    assert e.value.error_code == 404
