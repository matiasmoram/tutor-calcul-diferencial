import asyncio

import pytest

from core.course.domain.exceptions import ExerciseNotFoundException
from core.mistakes.application import annotations_grader as annotations_grader_module
from core.mistakes.application.annotations_grader import GRADING_CLAIM_TIMEOUT_S, AnnotationsGrader, AnnotationsGrading
from core.mistakes.application.availability_lister import AvailabilityLister
from core.mistakes.application.mistake_exercise_provider import MistakeExerciseProvider
from core.mistakes.application.mistake_session_starter import MistakeSessionStarter, MistakeSessionStarterInput
from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_grading import MistakeGrading
from core.mistakes.domain.exceptions import (
    GradingInProgressException,
    InvalidAnnotationsException,
    MistakeGradingTimeoutException,
    MistakeSessionNotFoundException,
    MistakeSourceRequiredException,
    UnknownTheoryResultException,
)
from core.mistakes.domain.services.sources import theory_results
from core.mistakes.infra.llm_annotation_grader import LLMAnnotationGrader
from core.mistakes.infra.sqlmodel_repository import (
    SQLModelMistakeExerciseRepository,
    SQLModelMistakeSessionRepository,
)
from core.shared.domain.ids import SessionId
from core.shared.llm.client import CallMeta, JsonObject, LLMError, LLMRequest, Stage
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
    assert await w.lister.availability() == {"t2-4c": {"normal": 2}}
    for _ in range(10):
        provided = await w.provider.get_or_generate(problem_source(), "normal", fresh=False, avoid_id="aaaaaaaaaaaa")
        assert provided.exercise.id == "bbbbbbbbbbbb" and not provided.generated_now


async def test_avoid_is_ignored_when_it_is_the_only_document(session_provider: SQLModelSessionProvider) -> None:
    w = Wiring(session_provider, ScriptedLLMClient({}))
    await w.exercises.save(solution("aaaaaaaaaaaa"))
    provided = await w.provider.get_or_generate(problem_source(), "normal", avoid_id="aaaaaaaaaaaa")
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
    assert started.generated_now and started.session.exercise_id == started.exercise.id
    assert await w.lister.availability() == {"t2-4c": {"normal": 1, "facil": 1}}
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
    assert not started.generated_now and started.exercise.id == "0000000000aa"
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


async def test_an_invalid_submission_is_refused_before_paying_for_the_grading(
    session_provider: SQLModelSessionProvider,
) -> None:
    llm = ScriptedLLMClient({Stage.MISTAKES_GRADING: [grader_answer()]})
    w = Wiring(session_provider, llm)
    await w.exercises.save(solution())
    started = await w.starter.start(MistakeSessionStarterInput(exercise_id="t2-4c"))
    e1 = started.exercise.mistakes[0]
    good = Annotation(id="a1", fragment=2, start=e1.start, end=e1.end, comment="al revés")
    for bad in ([good, good], [good.model_copy(update={"comment": "al revés\x00"})]):
        with pytest.raises(InvalidAnnotationsException) as e:
            await w.grader.grade(started.session.id, bad)
        assert e.value.error_code == 422
    assert llm.calls(Stage.MISTAKES_GRADING) == 0
    # Nothing was claimed: the corrected submission is graded at once.
    assert (await w.grader.grade(started.session.id, [good])).grading.found == 1


async def test_a_failed_save_releases_the_claim(session_provider: SQLModelSessionProvider) -> None:
    """The database fails while storing the grading: the student can submit again at once (no 409 until the
    claim goes stale)."""

    class SaveFailsOnce(SQLModelMistakeSessionRepository):
        failed = False

        async def save_grading(
            self, session_id: SessionId, annotations: list[Annotation], grading: MistakeGrading, now: float
        ) -> None:
            if not self.failed:
                self.failed = True
                raise OSError("database down")
            await super().save_grading(session_id, annotations, grading, now)

    llm = ScriptedLLMClient({Stage.MISTAKES_GRADING: [grader_answer(), grader_answer()]})
    w = Wiring(session_provider, llm)
    w.grader = AnnotationsGrader(
        COURSE, SaveFailsOnce(session_provider), w.exercises, LLMAnnotationGrader(llm), w.clock
    )
    await w.exercises.save(solution())
    started = await w.starter.start(MistakeSessionStarterInput(exercise_id="t2-4c"))
    e1 = started.exercise.mistakes[0]
    annotation = Annotation(id="a1", fragment=2, start=e1.start, end=e1.end)
    with pytest.raises(OSError):
        await w.grader.grade(started.session.id, [annotation])
    assert (await w.grader.grade(started.session.id, [annotation])).grading.found == 1


async def test_a_grading_whose_claim_was_taken_over_returns_the_stored_one(
    session_provider: SQLModelSessionProvider,
) -> None:
    """A grading outlives its claim; a resubmission takes the stale claim over and stores its grading first. The
    first grading then gets that stored result instead of failing on the duplicate."""

    class SlowGrader(ScriptedLLMClient):
        resubmission: list[Annotation] | None = None

        async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
            pending, self.resubmission = self.resubmission, None
            if pending is not None:
                w.clock.t += GRADING_CLAIM_TIMEOUT_S + 1
                resubmitted.append(await w.grader.grade(started.session.id, pending))
            return await super().structured(stage, request)

    llm = SlowGrader({Stage.MISTAKES_GRADING: [grader_answer("de la segona"), grader_answer("de la primera")]})
    w = Wiring(session_provider, llm)
    await w.exercises.save(solution())
    started = await w.starter.start(MistakeSessionStarterInput(exercise_id="t2-4c"))
    e1 = started.exercise.mistakes[0]
    annotation = Annotation(id="a1", fragment=2, start=e1.start, end=e1.end)
    resubmitted: list[AnnotationsGrading] = []
    llm.resubmission = [annotation]
    first = await w.grader.grade(started.session.id, [annotation])
    assert [r.grading for r in resubmitted] == [first.grading]
    assert first.grading.annotations[0].feedback == "de la segona"
    assert (await w.sessions.get(started.session.id)).grading == first.grading


async def test_a_grading_past_its_deadline_fails_and_releases_its_claim(
    session_provider: SQLModelSessionProvider, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A model call can outlast the claim: the deadline cancels the grading first, so a resubmission never takes a
    live claim over and pays for a second grading beside it."""

    class SlowGrader(ScriptedLLMClient):
        async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
            await asyncio.sleep(30)
            return await super().structured(stage, request)

    assert annotations_grader_module.GRADING_DEADLINE_S < GRADING_CLAIM_TIMEOUT_S
    monkeypatch.setattr(annotations_grader_module, "GRADING_DEADLINE_S", 0.1)
    w = Wiring(session_provider, SlowGrader({Stage.MISTAKES_GRADING: [grader_answer()]}))
    await w.exercises.save(solution())
    started = await w.starter.start(MistakeSessionStarterInput(exercise_id="t2-4c"))
    e1 = started.exercise.mistakes[0]
    annotation = Annotation(id="a1", fragment=2, start=e1.start, end=e1.end)
    with pytest.raises(MistakeGradingTimeoutException) as e:
        await asyncio.wait_for(w.grader.grade(started.session.id, [annotation]), 10)
    assert e.value.error_code == 504
    assert (await w.sessions.get(started.session.id)).grading is None
    fast = Wiring(session_provider, ScriptedLLMClient({Stage.MISTAKES_GRADING: [grader_answer("ara sí")]}))
    graded = await fast.grader.grade(started.session.id, [annotation])
    assert graded.grading.annotations[0].feedback == "ara sí"


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
