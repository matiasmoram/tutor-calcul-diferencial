import pytest

from core.quizzes.domain.entities.grading import Answer, QuizGrading
from core.quizzes.domain.entities.quiz_session import QuizSession
from core.quizzes.domain.exceptions import (
    ConcurrentQuizGradingException,
    QuizNotFoundException,
    QuizSessionNotFoundException,
)
from core.quizzes.domain.values.quiz_id import QuizId
from core.quizzes.infra.sqlmodel_repository import SQLModelQuizRepository, SQLModelQuizSessionRepository
from core.shared.domain.ids import SessionId
from core.shared.storage.session_provider import SQLModelSessionProvider
from tests.core.quizzes.builders import QUIZ_ID, quiz


async def test_quizzes_round_trip_and_are_counted_per_source(session_provider: SQLModelSessionProvider) -> None:
    repo = SQLModelQuizRepository(session_provider)
    assert await repo.availability() == {} and await repo.of_source("tema-2", "facil") == []
    q = quiz()
    later = q.model_copy(update={"id": QuizId("bbbbbbbbbbbb"), "created_at": 2.0})
    other = q.model_copy(update={"id": QuizId("cccccccccccc"), "source_id": "T2.12", "difficulty": "normal"})
    for x in (later, q, other):
        await repo.save(x)
    assert await repo.get(QuizId(QUIZ_ID)) == q
    assert [x.id for x in await repo.of_source("tema-2", "facil")] == [QUIZ_ID, "bbbbbbbbbbbb"]  # oldest first
    assert await repo.availability() == {"tema-2": {"facil": 2}, "T2.12": {"normal": 1}}
    with pytest.raises(QuizNotFoundException):
        await repo.get(QuizId("ffffffffffff"))


async def test_saving_a_quiz_again_replaces_it(session_provider: SQLModelSessionProvider) -> None:
    repo = SQLModelQuizRepository(session_provider)
    await repo.save(quiz())
    changed = quiz()
    changed.statements[0].hint = "nova pista"
    await repo.save(changed)
    assert (await repo.get(QUIZ_ID)).statements[0].hint == "nova pista"
    assert await repo.availability() == {"tema-2": {"facil": 1}}


def _session() -> QuizSession:
    return QuizSession(
        id=SessionId.generate(),
        source_id="tema-2",
        difficulty="facil",
        quiz_id=QuizId(QUIZ_ID),
        created_at=1.0,
        updated_at=1.0,
    )


def _grading() -> QuizGrading:
    return QuizGrading(grade=0, correct=0, total=4, statements=[], summary="", call=None)


async def test_sessions_keep_hints_and_their_one_grading(session_provider: SQLModelSessionProvider) -> None:
    await SQLModelQuizRepository(session_provider).save(quiz())
    repo = SQLModelQuizSessionRepository(session_provider)
    s = _session()
    await repo.add(s)
    assert await repo.get(s.id) == s
    assert s.use_hint("a1", 2.0) and not s.use_hint("a1", 2.0)
    await repo.save(s)
    s.submit([Answer(statement_id="a1", verdict="fals", justification="j")], _grading(), 3.0)
    assert not s.use_hint("a2", 3.0)  # after the grading hints are free and not recorded
    await repo.save(s)
    stored = await repo.get(s.id)
    assert stored == s and stored.version == 2
    assert stored.submission is not None and stored.submission.hints == ["a1"]
    with pytest.raises(QuizSessionNotFoundException) as e:
        await repo.get(SessionId.generate())
    assert e.value.error_code == 404


async def test_a_stale_session_cannot_be_saved(session_provider: SQLModelSessionProvider) -> None:
    await SQLModelQuizRepository(session_provider).save(quiz())
    repo = SQLModelQuizSessionRepository(session_provider)
    s = _session()
    await repo.add(s)
    first, second = await repo.get(s.id), await repo.get(s.id)
    first.submit([], _grading(), 2.0)
    await repo.save(first)
    second.submit([], _grading(), 2.0)
    with pytest.raises(ConcurrentQuizGradingException) as e:
        await repo.save(second)
    assert e.value.error_code == 409


async def test_grading_claims_are_exclusive_owned_and_end_with_the_grading(
    session_provider: SQLModelSessionProvider,
) -> None:
    await SQLModelQuizRepository(session_provider).save(quiz())
    repo = SQLModelQuizSessionRepository(session_provider)
    s = _session()
    await repo.add(s)
    assert await repo.claim_grading(s.id, now=100.0, stale_before=0.0)
    assert not await repo.claim_grading(s.id, now=101.0, stale_before=1.0)
    assert await repo.claim_grading(s.id, now=500.0, stale_before=200.0)  # the first claim went stale
    await repo.release_grading(s.id, claimed_at=100.0)  # the dead grading cannot drop the new claim
    assert not await repo.claim_grading(s.id, now=501.0, stale_before=201.0)
    await repo.release_grading(s.id, claimed_at=500.0)
    assert await repo.claim_grading(s.id, now=502.0, stale_before=202.0)
    s.submit([], _grading(), 503.0)
    await repo.save(s)
    await repo.release_grading(s.id, claimed_at=502.0)
    assert not await repo.claim_grading(s.id, now=504.0, stale_before=204.0)  # graded: never again
    assert not await repo.claim_grading(SessionId.generate(), now=1.0, stale_before=0.0)
