import pytest

from core.course.domain.exceptions import ExerciseNotFoundException
from core.mistakes.application.annotations_grader import AnnotationsGrader
from core.mistakes.application.availability_lister import AvailabilityLister
from core.mistakes.application.mistake_exercise_provider import MistakeExerciseProvider
from core.mistakes.application.mistake_session_starter import MistakeSessionStarter, MistakeSessionStarterInput
from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.exceptions import (
    GradingInProgressException,
    MistakeSessionNotFoundException,
    MistakeSourceRequiredException,
    UnknownTheoryResultException,
)
from core.mistakes.domain.sources import theory_results
from core.mistakes.infra.llm_adapters import LLMAnnotationGrader
from core.mistakes.infra.sqlmodel_repository import (
    SQLModelMistakeExerciseRepository,
    SQLModelMistakeSessionRepository,
)
from core.shared.domain.ids import SessionId
from core.shared.llm.client import JsonObject, LLMError, Stage
from core.shared.storage.session_provider import SQLModelSessionProvider
from tests.core.mistakes.builders import (
    COURSE,
    FixedClock,
    err,
    exercise_generator,
    finding,
    gen,
    problem_source,
    solution,
)
from tests.fakes.llm import ScriptedLLMClient


class Wiring:
    def __init__(self, provider: SQLModelSessionProvider, llm: ScriptedLLMClient) -> None:
        self.clock = FixedClock()
        self.exercises = SQLModelMistakeExerciseRepository(provider)
        self.sessions = SQLModelMistakeSessionRepository(provider)
        self.provider = MistakeExerciseProvider(self.exercises, exercise_generator(llm, self.clock))
        self.starter = MistakeSessionStarter(COURSE, self.provider, self.sessions, self.clock)
        self.grader = AnnotationsGrader(COURSE, self.sessions, self.exercises, LLMAnnotationGrader(llm), self.clock)
        self.lister = AvailabilityLister(COURSE, self.exercises)


def grader_answer(feedback: str = "Bé.") -> JsonObject:
    return {
        "avaluacions": [{"anotacio": "a1", "error": "e1", "explicacio": "correcta", "feedback": feedback}],
        "resum": "Molt bé.",
    }


def test_theory_items_are_results_with_proof() -> None:
    items = theory_results(COURSE)
    assert items and all(
        it.kind in ("teorema", "proposicio", "lema", "corollari") and it.proof.strip() and it.number for it in items
    )
    ids = {it.id for it in items}
    assert "T3.21" in ids  # Regla de la cadena
    assert not any(COURSE.theory[i].kind == "definicio" for i in ids)


async def test_disponibles_and_avoid_repeating(session_provider: SQLModelSessionProvider) -> None:
    w = Wiring(session_provider, ScriptedLLMClient({}))
    await w.exercises.save(solution("aaaaaaaaaaaa"))
    await w.exercises.save(solution("bbbbbbbbbbbb"))
    assert await w.lister.ready_counts() == {"t2-4c": {"normal": 2}}
    for _ in range(10):
        provided = await w.provider.get_or_generate(problem_source(), "normal", fresh=False, avoid="aaaaaaaaaaaa")
        assert provided.exercise.id == "bbbbbbbbbbbb" and not provided.freshly_generated


async def test_avoid_is_ignored_when_it_is_the_only_document(session_provider: SQLModelSessionProvider) -> None:
    w = Wiring(session_provider, ScriptedLLMClient({}))
    await w.exercises.save(solution("aaaaaaaaaaaa"))
    provided = await w.provider.get_or_generate(problem_source(), "normal", avoid="aaaaaaaaaaaa")
    assert provided.exercise.id == "aaaaaaaaaaaa"


async def test_fresh_generates_and_stores_even_with_ready_documents(session_provider: SQLModelSessionProvider) -> None:
    good = gen([err(2, "$x^4 \\ge x^4+y^2$")])
    llm = ScriptedLLMClient(
        {
            Stage.MISTAKES_GENERATION: [good],
            Stage.MISTAKES_VERIFICATION: [{"problemes": [finding(2, "x")], "valoracio": "ok"}],
        }
    )
    w = Wiring(session_provider, llm)
    await w.exercises.save(solution("aaaaaaaaaaaa"))
    data = MistakeSessionStarterInput(exercise_id="t2-4c", difficulty="facil")
    assert await w.starter.needs_generation(data)
    started = await w.starter.start(data)
    assert started.freshly_generated and started.session.exercise_id == started.exercise.id
    assert await w.lister.ready_counts() == {"t2-4c": {"normal": 1, "facil": 1}}
    assert not await w.starter.needs_generation(data)
    assert await w.starter.needs_generation(data.model_copy(update={"fresh": True}))


async def test_session_start_validates_its_source(session_provider: SQLModelSessionProvider) -> None:
    w = Wiring(session_provider, ScriptedLLMClient({}))
    with pytest.raises(MistakeSourceRequiredException) as e:
        await w.starter.start(MistakeSessionStarterInput())
    assert e.value.error_code == 422
    with pytest.raises(MistakeSourceRequiredException):
        await w.starter.start(MistakeSessionStarterInput(exercise_id="t2-4c", theory_id="T3.21"))
    with pytest.raises(ExerciseNotFoundException):
        await w.starter.start(MistakeSessionStarterInput(exercise_id="t9-99"))
    definition = next(it.id for it in COURSE.theory.values() if it.kind == "definicio")
    with pytest.raises(UnknownTheoryResultException) as e2:
        await w.starter.start(MistakeSessionStarterInput(theory_id=definition))
    assert e2.value.error_code == 404


async def test_a_session_is_graded_once(session_provider: SQLModelSessionProvider) -> None:
    llm = ScriptedLLMClient({Stage.MISTAKES_GRADING: [grader_answer()]})
    w = Wiring(session_provider, llm)
    await w.exercises.save(solution())
    started = await w.starter.start(MistakeSessionStarterInput(exercise_id="t2-4c"))
    assert not started.freshly_generated and started.exercise.id == "0000000000aa"
    e1 = started.exercise.mistakes[0]
    annotation = Annotation(id="a1", fragment=2, start=e1.start, end=e1.end, comment="al revés")

    first = await w.grader.grade(started.session.id, [annotation])
    assert first.grading.score == 50 and first.original is None
    # The result reveals every error: a second submission gets the stored result, without calling the model.
    again = await w.grader.grade(started.session.id, [])
    assert again.grading == first.grading and llm.calls(Stage.MISTAKES_GRADING) == 1
    assert (await w.sessions.get(started.session.id)).grading == first.grading


async def test_a_theory_grading_returns_the_original_item(session_provider: SQLModelSessionProvider) -> None:
    w = Wiring(session_provider, ScriptedLLMClient({}))
    doc = solution().model_copy(update={"source_id": "T3.21", "source_kind": "teoria"})
    await w.exercises.save(doc)
    started = await w.starter.start(MistakeSessionStarterInput(theory_id="T3.21"))
    outcome = await w.grader.grade(started.session.id, [])
    assert outcome.original == COURSE.theory_item("T3.21") and outcome.grading.total == 2


async def test_a_failed_grading_can_be_retried_and_a_running_one_blocks(
    session_provider: SQLModelSessionProvider,
) -> None:
    llm = ScriptedLLMClient({Stage.MISTAKES_GRADING: [LLMError("model down"), grader_answer()]})
    w = Wiring(session_provider, llm)
    await w.exercises.save(solution())
    started = await w.starter.start(MistakeSessionStarterInput(exercise_id="t2-4c"))
    e1 = started.exercise.mistakes[0]
    annotation = Annotation(id="a1", fragment=2, start=e1.start, end=e1.end)
    with pytest.raises(LLMError):
        await w.grader.grade(started.session.id, [annotation])
    assert (await w.grader.grade(started.session.id, [annotation])).grading.found == 1

    other = await w.starter.start(MistakeSessionStarterInput(exercise_id="t2-4c"))
    assert await w.sessions.claim_grading(other.session.id, w.clock.now(), w.clock.now() - 300)
    with pytest.raises(GradingInProgressException) as e:
        await w.grader.grade(other.session.id, [annotation])
    assert e.value.error_code == 409


async def test_unknown_session_is_not_found(session_provider: SQLModelSessionProvider) -> None:
    w = Wiring(session_provider, ScriptedLLMClient({}))
    with pytest.raises(MistakeSessionNotFoundException) as e:
        await w.grader.grade(SessionId.generate(), [])
    assert e.value.error_code == 404


async def test_theory_results_are_listed_by_topic_with_their_ready_documents(
    session_provider: SQLModelSessionProvider,
) -> None:
    w = Wiring(session_provider, ScriptedLLMClient({}))
    await w.exercises.save(solution().model_copy(update={"source_id": "T3.21", "source_kind": "teoria"}))
    topics = await w.lister.theory_results()
    assert [t.topic.number for t in topics] == [t.number for t in COURSE.topics]
    t3 = next(t for t in topics if t.topic.number == 3)
    entry = next(i for i in t3.items if i.item.id == "T3.21")
    assert entry.ready == {"normal": 1}
    assert all(i.ready == {} for t in topics for i in t.items if i.item.id != "T3.21")
