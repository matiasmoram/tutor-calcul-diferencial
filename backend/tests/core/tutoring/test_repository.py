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

    stale.record_turn("una altra pestanya", "...", stale.state, now=1.0)
    with pytest.raises(ConcurrentTurnException) as e:
        await t.sessions.save_turn(stale, turn.model_copy(update={"number": 2}))
    assert e.value.error_code == 409
    assert [x.number for x in await t.sessions.turns(sid)] == [1]  # the conflicting turn left nothing behind
    current = await t.sessions.get(sid)
    assert current.version == 1 and current.history[0].text == "no sé"
    saved = await t.sessions.save_turn(current, turn.model_copy(update={"number": 2}))
    assert saved.version == 2 and (await t.sessions.get(sid)).version == 2
