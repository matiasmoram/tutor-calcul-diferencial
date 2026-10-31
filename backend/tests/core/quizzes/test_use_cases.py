"""The use cases the API calls, without the HTTP layer."""

from pathlib import Path
from random import Random

import pytest

from core.quizzes.application.answers_grader import GRADING_CLAIM_TIMEOUT_S, AnswersGraderInput
from core.quizzes.application.pregenerated_importer import PregeneratedImporter
from core.quizzes.application.quiz_provider import QuizProvider
from core.quizzes.application.quiz_session_starter import QuizSessionStarterInput
from core.quizzes.application.source_lister import SourceLister
from core.quizzes.domain.entities.grading import Answer, QuizGrading
from core.quizzes.domain.exceptions import (
    ConcurrentQuizGradingException,
    QuizSessionNotFoundException,
    StatementNotFoundException,
    UnknownQuizSourceException,
)
from core.quizzes.domain.values.quiz_id import QuizId
from core.quizzes.infra.json_quiz_files import JsonQuizFiles
from core.quizzes.infra.sqlmodel_repository import SQLModelQuizRepository
from core.shared.domain.ids import SessionId
from core.shared.llm.client import LLMError, Stage
from core.shared.storage.session_provider import SQLModelSessionProvider
from tests.core.quizzes.builders import (
    ANSWERS,
    QUIZ_ID,
    FixedClock,
    InterleavingLLM,
    answers_grader,
    generator,
    graded,
    hints,
    item,
    ok_audit,
    ok_solver,
    quiz,
    source,
    started_session,
    starter,
    transcriber,
)
from tests.fakes.llm import ScriptedLLMClient
from tests.fixtures.course import authored_course


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
        await hints(session_provider).reveal(SessionId("0" * 32), "a1")
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
        provided = await provider.get_or_generate(source(), "facil", avoid_id=QUIZ_ID)
        assert provided.quiz.id == "bbbbbbbbbbbb" and not provided.generated_now
    assert await provider.is_ready(source(), "facil") and not await provider.is_ready(source(), "dificil")


async def test_the_starter_tells_when_a_start_needs_the_model(session_provider: SQLModelSessionProvider) -> None:
    await SQLModelQuizRepository(session_provider).add(quiz())
    s = starter(session_provider)
    assert not await s.needs_generation(QuizSessionStarterInput(source_id="tema-2", difficulty="facil"))
    assert await s.needs_generation(QuizSessionStarterInput(source_id="tema-2", difficulty="facil", fresh=True))
    assert await s.needs_generation(QuizSessionStarterInput(source_id="tema-2", difficulty="dificil"))
    with pytest.raises(UnknownQuizSourceException):
        await s.needs_generation(QuizSessionStarterInput(source_id="tema-9"))


async def test_pregenerated_quizzes_seed_the_store(session_provider: SQLModelSessionProvider, tmp_path: Path) -> None:
    files = JsonQuizFiles(tmp_path)
    path = files.save(quiz())
    assert path == tmp_path / "tema-2" / "facil" / f"{QUIZ_ID}.json"
    repo = SQLModelQuizRepository(session_provider)
    importer = PregeneratedImporter(files, repo)
    assert await importer.import_all() == 1 and await importer.import_all() == 1
    assert await repo.of_source("tema-2", "facil") == [quiz()]


async def test_a_second_submission_while_grading_is_refused_before_any_model_call(
    session_provider: SQLModelSessionProvider,
) -> None:
    refused: list[ConcurrentQuizGradingException] = []
    llm = InterleavingLLM({Stage.QUIZ_GRADING: [graded()], Stage.QUIZ_EXTRACTION: [transcriber()]})
    grading = answers_grader(llm, session_provider)
    sid = await started_session(session_provider)

    async def second_tab() -> None:
        with pytest.raises(ConcurrentQuizGradingException) as e:
            await grading.grade(sid, ANSWERS)
        refused.append(e.value)

    llm.meanwhile = second_tab()
    first = await grading.grade(sid, ANSWERS)
    assert [e.error_code for e in refused] == [409]
    assert llm.calls(Stage.QUIZ_GRADING) == 1 and llm.calls(Stage.QUIZ_EXTRACTION) == 1
    assert await grading.grade(sid, ANSWERS) == first  # done: the stored result, no model call
    assert llm.calls(Stage.QUIZ_GRADING) == 1


async def test_a_failed_grading_releases_its_claim(session_provider: SQLModelSessionProvider) -> None:
    llm = ScriptedLLMClient(
        {Stage.QUIZ_GRADING: [LLMError("model down"), graded()], Stage.QUIZ_EXTRACTION: [transcriber()] * 2}
    )
    grading = answers_grader(llm, session_provider)
    sid = await started_session(session_provider)
    with pytest.raises(LLMError):
        await grading.grade(sid, ANSWERS)
    assert (await grading.grade(sid, ANSWERS)).statements[0].feedback == "f"


async def test_a_grading_whose_claim_was_taken_over_returns_the_stored_one(
    session_provider: SQLModelSessionProvider,
) -> None:
    """The first grading outlives its claim; a later submission takes it over and stores its result first. The
    first one then returns that result instead of a conflict."""
    llm = InterleavingLLM(
        {
            Stage.QUIZ_GRADING: [graded("de la segona"), graded("de la primera")],
            Stage.QUIZ_EXTRACTION: [transcriber()] * 2,
        }
    )
    sid = await started_session(session_provider)
    later = answers_grader(llm, session_provider, FixedClock(1_700_000_000.0 + GRADING_CLAIM_TIMEOUT_S + 1))
    resubmitted: list[QuizGrading] = []

    async def resubmission() -> None:
        resubmitted.append(await later.grade(sid, ANSWERS))

    llm.meanwhile = resubmission()
    first = await answers_grader(llm, session_provider).grade(sid, ANSWERS)
    assert resubmitted == [first] and first.statements[0].feedback == "de la segona"
