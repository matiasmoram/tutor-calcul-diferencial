import pytest

from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_grading import MistakeGrading
from core.mistakes.domain.entities.mistake_session import MistakeSession
from core.mistakes.domain.exceptions import (
    MistakeExerciseNotFoundException,
    MistakeSessionAlreadyGradedException,
    MistakeSessionNotFoundException,
)
from core.mistakes.domain.services.grading import grade
from core.mistakes.domain.values.mistake_exercise_id import MistakeExerciseId
from core.mistakes.infra.sqlmodel_repository import (
    SQLModelMistakeExerciseRepository,
    SQLModelMistakeSessionRepository,
)
from core.shared.domain.ids import SessionId
from core.shared.storage.session_provider import SQLModelSessionProvider
from tests.core.mistakes.builders import solution


def session_of(exercise_id: str = "0000000000aa") -> MistakeSession:
    return MistakeSession(
        id=SessionId.generate(),
        source_kind="problema",
        source_id="t2-4c",
        exercise_id=MistakeExerciseId(exercise_id),
        difficulty="normal",
        created_at=10.0,
    )


def empty_grading() -> MistakeGrading:
    return grade(solution(), [], None, None)


async def test_documents_round_trip_and_are_replaced_by_id(session_provider: SQLModelSessionProvider) -> None:
    repo = SQLModelMistakeExerciseRepository(session_provider)
    doc = solution()
    await repo.save(doc)
    assert await repo.get(doc.id) == doc
    edited = doc.model_copy(update={"fragments": [*doc.fragments[:-1], "Per tant el límit val $0$."]})
    await repo.save(edited)
    assert await repo.get(doc.id) == edited
    assert await repo.ready_counts() == {"t2-4c": {"normal": 1}}
    with pytest.raises(MistakeExerciseNotFoundException):
        await repo.get(MistakeExerciseId("ffffffffffff"))


async def test_documents_of_a_source_are_ordered_by_id_and_counted(session_provider: SQLModelSessionProvider) -> None:
    repo = SQLModelMistakeExerciseRepository(session_provider)
    for i, doc_id in enumerate(("cccccccccccc", "aaaaaaaaaaaa", "bbbbbbbbbbbb")):
        await repo.save(solution(doc_id).model_copy(update={"difficulty": "dificil" if i == 0 else "normal"}))
    await repo.save(solution("dddddddddddd").model_copy(update={"source_id": "T3.21", "source_kind": "teoria"}))
    assert [d.id for d in await repo.of_source("t2-4c", "normal")] == ["aaaaaaaaaaaa", "bbbbbbbbbbbb"]
    assert await repo.of_source("t2-4c", "facil") == []
    assert await repo.ready_counts() == {"t2-4c": {"normal": 2, "dificil": 1}, "T3.21": {"normal": 1}}


async def test_sessions_round_trip_with_their_grading(session_provider: SQLModelSessionProvider) -> None:
    exercises = SQLModelMistakeExerciseRepository(session_provider)
    sessions = SQLModelMistakeSessionRepository(session_provider)
    await exercises.save(solution())
    s = session_of()
    await sessions.add(s)
    assert await sessions.get(s.id) == s
    annotations = [Annotation(id="a1", fragment=1, start=0, end=3, comment="?")]
    await sessions.save_grading(s.id, annotations, empty_grading(), 11.0)
    assert (await sessions.get(s.id)).grading == empty_grading()
    with pytest.raises(MistakeSessionNotFoundException):
        await sessions.get(SessionId.generate())


async def test_grading_claims_are_exclusive_until_released_or_stale(session_provider: SQLModelSessionProvider) -> None:
    exercises = SQLModelMistakeExerciseRepository(session_provider)
    sessions = SQLModelMistakeSessionRepository(session_provider)
    await exercises.save(solution())
    s = session_of()
    await sessions.add(s)
    assert await sessions.claim_grading(s.id, now=100.0, stale_before=0.0)
    assert not await sessions.claim_grading(s.id, now=101.0, stale_before=1.0)
    assert await sessions.claim_grading(s.id, now=500.0, stale_before=200.0)  # the first claim went stale
    await sessions.release_grading(s.id, claimed_at=100.0)  # the dead grading cannot drop the new claim
    assert not await sessions.claim_grading(s.id, now=501.0, stale_before=201.0)
    await sessions.release_grading(s.id, claimed_at=500.0)
    assert await sessions.claim_grading(s.id, now=501.0, stale_before=201.0)
    await sessions.save_grading(s.id, [], empty_grading(), 502.0)
    await sessions.release_grading(s.id, claimed_at=501.0)
    assert not await sessions.claim_grading(s.id, now=503.0, stale_before=203.0)  # graded: never again
    assert not await sessions.claim_grading(SessionId.generate(), now=1.0, stale_before=0.0)


async def test_a_session_is_graded_once_in_storage(session_provider: SQLModelSessionProvider) -> None:
    exercises = SQLModelMistakeExerciseRepository(session_provider)
    sessions = SQLModelMistakeSessionRepository(session_provider)
    await exercises.save(solution())
    s = session_of()
    await sessions.add(s)
    first = empty_grading()
    await sessions.save_grading(s.id, [], first, 11.0)
    second = first.model_copy(update={"summary": "una altra"})
    with pytest.raises(MistakeSessionAlreadyGradedException) as e:
        await sessions.save_grading(s.id, [], second, 12.0)
    assert e.value.error_code == 409
    assert (await sessions.get(s.id)).grading == first
