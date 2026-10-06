"""The use cases the API calls (the old endpoint test, minus HTTP: that layer is built in phase 6)."""

from pathlib import Path
from random import Random

import pytest

from core.quizzes.application.answers_grader import AnswersGraderInput
from core.quizzes.application.hint_revealer import HintRevealer
from core.quizzes.application.pregenerated_importer import PregeneratedImporter
from core.quizzes.application.quiz_provider import QuizProvider
from core.quizzes.application.quiz_session_starter import QuizSessionStarter, QuizSessionStarterInput
from core.quizzes.application.source_lister import SourceLister
from core.quizzes.domain.entities.grading import Answer
from core.quizzes.domain.exceptions import (
    QuizSessionNotFoundException,
    StatementNotFoundException,
    UnknownQuizSourceException,
)
from core.quizzes.domain.values.quiz_id import QuizId
from core.quizzes.infra.json_quiz_files import JsonQuizFiles
from core.quizzes.infra.sqlmodel_repository import SQLModelQuizRepository, SQLModelQuizSessionRepository
from core.shared.llm.client import LLMClient, Stage
from core.shared.storage.session_provider import SQLModelSessionProvider
from tests.core.quizzes.builders import (
    QUIZ_ID,
    FixedClock,
    answers_grader,
    generator,
    item,
    ok_audit,
    ok_solver,
    quiz,
    source,
)
from tests.fakes.llm import ScriptedLLMClient
from tests.fixtures.course import authored_course


def starter(provider: SQLModelSessionProvider, llm: LLMClient | None = None) -> QuizSessionStarter:
    quizzes = SQLModelQuizRepository(provider)
    quiz_provider = QuizProvider(quizzes, generator(llm or ScriptedLLMClient({})), Random(0))
    return QuizSessionStarter(authored_course(), quiz_provider, SQLModelQuizSessionRepository(provider), FixedClock())


def hints(provider: SQLModelSessionProvider) -> HintRevealer:
    return HintRevealer(SQLModelQuizSessionRepository(provider), SQLModelQuizRepository(provider), FixedClock())


async def test_a_session_on_a_stored_quiz_never_calls_the_model(session_provider: SQLModelSessionProvider) -> None:
    await SQLModelQuizRepository(session_provider).add(quiz())
    index = await SourceLister(authored_course(), SQLModelQuizRepository(session_provider)).list_sources()
    assert {t.source_id for t in index.topics} >= {"tema-1", "tema-2"}
    assert any(f.item.id == "T2.12" for t in index.topics for f in t.focus)
    assert next(t for t in index.topics if t.source_id == "tema-2").available == {"facil": 1}
    assert index.sizes == {"facil": 6, "normal": 8, "dificil": 10}

    started = await starter(session_provider).start(QuizSessionStarterInput(source_id="tema-2", difficulty="facil"))
    assert started.quiz.id == QUIZ_ID and not started.generated_now and started.source.focus is None
    sid = started.session.id
    hint = await hints(session_provider).reveal(sid, "a1")
    assert hint.hint == "p" and hint.statement_id == "a1"
    with pytest.raises(StatementNotFoundException):
        await hints(session_provider).reveal(sid, "a9")
    with pytest.raises(QuizSessionNotFoundException):
        await hints(session_provider).reveal("0" * 32, "a1")
    with pytest.raises(UnknownQuizSourceException) as e:
        await starter(session_provider).start(QuizSessionStarterInput(source_id="tema-9"))
    assert e.value.error_code == 404

    # No answers: graded by code alone, the hint is recorded.
    grading = answers_grader(ScriptedLLMClient({}), session_provider)
    r = await grading.grade(sid, AnswersGraderInput(answers=[]))
    assert r.grade == 0 and r.statements[0].hint_used
    # One grading per quiz: the result reveals every verdict, so resubmitting returns the first result.
    again = await grading.grade(sid, AnswersGraderInput(answers=[Answer(statement_id="a1", verdict="fals")]))
    assert again == r


async def test_a_missing_quiz_is_generated_and_stored(session_provider: SQLModelSessionProvider) -> None:
    llm = ScriptedLLMClient(
        {
            Stage.QUIZ_GENERATION: [{"afirmacions": [item(f"F{i}.") for i in range(3)] + [item("C1.", "cert")]},
                                    {"afirmacions": [item("C2.", "cert"), item("F9.")]}],
            Stage.QUIZ_VERIFICATION: [ok_solver(["fals"] * 3 + ["cert"]), ok_solver(["cert", "fals"])],
            Stage.QUIZ_AUDIT: [ok_audit(4), ok_audit(2)],
        }
    )  # fmt: skip
    started = await starter(session_provider, llm).start(QuizSessionStarterInput(source_id="T2.12", difficulty="facil"))
    assert started.generated_now and started.quiz.source_id == "T2.12" and started.source.focus is not None
    assert await SQLModelQuizRepository(session_provider).availability() == {"T2.12": {"facil": 1}}
    assert all(
        "<resultat_focus>" in (r.context or "") for r in llm.requests[Stage.QUIZ_GENERATION]
    )  # the focus result goes with every call


async def test_the_provider_prefers_a_quiz_not_just_seen(session_provider: SQLModelSessionProvider) -> None:
    repo = SQLModelQuizRepository(session_provider)
    await repo.add(quiz())
    await repo.add(quiz().model_copy(update={"id": QuizId("bbbbbbbbbbbb")}))
    provider = QuizProvider(repo, generator(ScriptedLLMClient({})), Random(0))
    for _ in range(5):
        provided = await provider.get_or_generate(source(), "facil", except_id=QUIZ_ID)
        assert provided.quiz.id == "bbbbbbbbbbbb" and not provided.generated_now
    assert await provider.is_ready(source(), "facil") and not await provider.is_ready(source(), "dificil")


async def test_pregenerated_quizzes_seed_the_store(session_provider: SQLModelSessionProvider, tmp_path: Path) -> None:
    files = JsonQuizFiles(tmp_path)
    path = files.save(quiz())
    assert path == tmp_path / "tema-2" / "facil" / f"{QUIZ_ID}.json"
    repo = SQLModelQuizRepository(session_provider)
    importer = PregeneratedImporter(files, repo)
    assert await importer.import_all() == 1 and await importer.import_all() == 1
    assert await repo.of_source("tema-2", "facil") == [quiz()]
