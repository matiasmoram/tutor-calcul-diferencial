import pytest

from core.course.domain.exceptions import ExerciseNotFoundException
from core.shared.domain.ids import ExerciseId
from core.shared.storage.session_provider import SQLModelSessionProvider
from tests.core.tutoring.builders import COURSE, EX4C, tutoring
from tests.fakes.llm import ScriptedLLMClient


async def test_a_new_session_is_stored_with_what_the_web_shows(session_provider: SQLModelSessionProvider) -> None:
    t = tutoring(ScriptedLLMClient({}), session_provider)
    started = await t.starter.start(EX4C.id)
    assert await t.sessions.get(started.session.id) == started.session
    assert started.exercise == EX4C and started.sheet == COURSE.sheet(EX4C.sheet_id)
    reserved = COURSE.reserved_ids(EX4C)
    assert [it.id for it in started.background_theory] == [r.item_id for r in EX4C.theory if r.item_id not in reserved]
    uses = {u.item.id: u for u in started.sheet_theory}
    assert all(r.item_id in uses for r in EX4C.all_refs())
    assert all(u.reserved == (i in reserved) for i, u in uses.items())
    step = next(s for s in EX4C.steps if s.theory)
    assert step.id in uses[step.theory[0].item_id].used_in


async def test_an_unknown_exercise_is_not_found(session_provider: SQLModelSessionProvider) -> None:
    t = tutoring(ScriptedLLMClient({}), session_provider)
    with pytest.raises(ExerciseNotFoundException):
        await t.starter.start(ExerciseId("t9-99"))
