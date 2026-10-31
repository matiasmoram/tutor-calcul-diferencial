import asyncio

import pytest

from core.mistakes.application import part_annotations_grader as part_grader_module
from core.mistakes.application.annotations_grader import AnnotationsGrader
from core.mistakes.application.mistake_exercise_provider import MistakeExerciseProvider
from core.mistakes.application.mistake_session_starter import MistakeSessionStarter, MistakeSessionStarterInput
from core.mistakes.application.part_annotations_grader import PartAnnotationsGrader
from core.mistakes.application.part_hint_revealer import PartHintRevealer
from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.parted_mistake_exercise import PartedMistakeExercise
from core.mistakes.domain.exceptions import (
    GradingInProgressException,
    InvalidAnnotationsException,
    MistakeGradingTimeoutException,
    MistakeLayoutMismatchException,
    MistakePartOutOfOrderException,
    UnknownMistakePartException,
)
from core.mistakes.infra.llm_annotation_grader import LLMAnnotationGrader
from core.mistakes.infra.sqlmodel_repository import (
    SQLModelMistakeExerciseRepository,
    SQLModelMistakeSessionRepository,
)
from core.shared.domain.ids import SessionId
from core.shared.llm.client import CallMeta, JsonObject, LLMRequest, Stage
from core.shared.storage.session_provider import SQLModelSessionProvider
from tests.core.mistakes.builders import COURSE, PARTS, FixedClock, exercise_generator, parted, solution
from tests.fakes.llm import ScriptedLLMClient


class Wiring:
    def __init__(self, provider: SQLModelSessionProvider, llm: ScriptedLLMClient) -> None:
        self.clock = FixedClock()
        self.exercises = SQLModelMistakeExerciseRepository(provider)
        self.sessions = SQLModelMistakeSessionRepository(provider)
        documents = MistakeExerciseProvider(self.exercises, exercise_generator(llm, self.clock), may_generate=False)
        self.starter = MistakeSessionStarter(COURSE, documents, self.sessions, self.clock)
        self.grader = PartAnnotationsGrader(COURSE, self.sessions, self.exercises, LLMAnnotationGrader(llm), self.clock)
        self.hints = PartHintRevealer(self.sessions, self.exercises, self.clock)
        self.whole = AnnotationsGrader(COURSE, self.sessions, self.exercises, LLMAnnotationGrader(llm), self.clock)

    async def start(self, document: PartedMistakeExercise | None = None, theory: bool = False) -> SessionId:
        await self.exercises.save(document or parted())
        source = {"theory_id": "T3.21"} if theory else {"exercise_id": "t2-4c"}
        started = await self.starter.start(MistakeSessionStarterInput(**source, layout="per_parts"))
        return started.session.id


def found(mistake: str, explanation: str = "correcta") -> JsonObject:
    return {
        "avaluacions": [{"anotacio": "a1", "error": mistake, "explicacio": explanation, "feedback": "Bé."}],
        "resum": "Molt bé.",
    }


def on(document: PartedMistakeExercise, k: int, comment: str = "està girada") -> Annotation:
    """An annotation on the quote of the document's k-th error."""
    m = document.mistakes[k]
    return Annotation(id=f"meva-{k}", fragment=m.fragment, start=m.start, end=m.end, comment=comment)


async def test_a_session_is_reviewed_part_by_part_in_order(session_provider: SQLModelSessionProvider) -> None:
    llm = ScriptedLLMClient({Stage.MISTAKES_GRADING: [found("e1")]})
    w = Wiring(session_provider, llm)
    sid = await w.start()
    doc = parted()
    with pytest.raises(MistakePartOutOfOrderException) as order:
        await w.grader.grade(sid, 3, [])
    assert order.value.error_code == 409 and order.value.message == "Primer cal corregir la part anterior."
    for clean_or_missing in (1, 4):
        with pytest.raises(UnknownMistakePartException) as unknown:
            await w.grader.grade(sid, clean_or_missing, [])
        assert unknown.value.error_code == 404

    first = await w.grader.grade(sid, 2, [on(doc, 0)])
    assert first.graded.part == 2 and not first.graded.hint_used
    g = first.graded.grading
    assert g.score == 100 and g.found == 1 and g.total == 1 and g.mistakes == [doc.mistakes[0]]
    assert first.correct == PARTS[1][1]
    assert first.next is not None and first.next.model_dump() == {
        "part": 3,
        "primer_fragment": 5,
        "fragments": doc.parts[2].flawed_fragments,
        "anteriors": [],
    }
    assert first.final is None and first.resolution is None and first.original is None
    # The grader sees the earlier parts and this one, nothing after it, and only this part's error.
    user = llm.requests[Stage.MISTAKES_GRADING][0].user
    assert "[4] " in user and "[5] " not in user and "[e1]" in user and "[e2]" not in user

    # "No el trobo": nothing submitted, no model call, 0 for the part, and the session goes on.
    last = await w.grader.grade(sid, 3, [])
    assert last.graded.grading.score == 0 and last.graded.grading.mistakes == [doc.mistakes[1]]
    assert last.next is None and llm.calls(Stage.MISTAKES_GRADING) == 1
    assert last.final is not None and last.final.model_dump() == {
        "nota": 50,
        "trobats": 1,
        "total": 2,
        "falsos_positius": 0,
        "parts": [{"part": 2, "nota": 100, "pista": False}, {"part": 3, "nota": 0, "pista": False}],
    }
    assert last.resolution == doc.resolution() and last.original is None

    # A graded part is graded once: a resubmission gets the stored result.
    again = await w.grader.grade(sid, 2, [])
    assert again.graded == first.graded and again.final == last.final and llm.calls(Stage.MISTAKES_GRADING) == 1
    stored = await w.sessions.get(sid)
    assert [p.part for p in stored.part_gradings] == [2, 3] and stored.grading is None


async def test_a_hint_is_recorded_once_and_costs_its_part(session_provider: SQLModelSessionProvider) -> None:
    llm = ScriptedLLMClient({Stage.MISTAKES_GRADING: [found("e1")]})
    w = Wiring(session_provider, llm)
    sid = await w.start()
    doc = parted()
    with pytest.raises(MistakePartOutOfOrderException):
        await w.hints.reveal(sid, 3)
    with pytest.raises(UnknownMistakePartException):
        await w.hints.reveal(sid, 1)
    hint = await w.hints.reveal(sid, 2)
    assert hint.model_dump() == {"part": 2, "hint": "pista 2"}
    assert await w.hints.reveal(sid, 2) == hint
    assert (await w.sessions.get(sid)).hinted_parts == [2]

    graded = await w.grader.grade(sid, 2, [on(doc, 0)])
    assert graded.graded.hint_used and graded.graded.grading.score == 85
    # After the grading the hint costs nothing.
    assert (await w.hints.reveal(sid, 2)).hint == "pista 2"
    last = await w.grader.grade(sid, 3, [])
    assert last.final is not None and last.final.score == 42
    assert [(p.part, p.score, p.hint_used) for p in last.final.parts] == [(2, 85, True), (3, 0, False)]
    assert (await w.sessions.get(sid)).hinted_parts == [2]


async def test_theory_reveals_the_original_item_only_at_the_end(session_provider: SQLModelSessionProvider) -> None:
    doc = PartedMistakeExercise.model_validate(
        parted().model_dump(mode="json") | {"font": "teoria", "exercici": "T3.21", "n_enunciat": 2}
    )
    w = Wiring(session_provider, ScriptedLLMClient({}))
    sid = await w.start(doc, theory=True)
    assert (await w.grader.grade(sid, 2, [])).original is None
    last = await w.grader.grade(sid, 3, [])
    assert last.original == COURSE.theory_item("T3.21") and last.final is not None


async def test_each_layout_has_its_own_grading(session_provider: SQLModelSessionProvider) -> None:
    w = Wiring(session_provider, ScriptedLLMClient({}))
    await w.exercises.save(solution())
    sencer = (await w.starter.start(MistakeSessionStarterInput(exercise_id="t2-4c"))).session.id
    for call in (w.grader.grade(sencer, 2, []), w.hints.reveal(sencer, 2)):
        with pytest.raises(MistakeLayoutMismatchException) as e:
            await call
        assert e.value.error_code == 409 and e.value.message == "Aquest document es corregeix sencer, no per parts."
    per_parts = await w.start()
    with pytest.raises(MistakeLayoutMismatchException):
        await w.whole.grade(per_parts, [])


async def test_a_running_part_grading_blocks_the_hint_and_another_grading(
    session_provider: SQLModelSessionProvider,
) -> None:
    w = Wiring(session_provider, ScriptedLLMClient({}))
    sid = await w.start()
    assert await w.sessions.claim_part(sid, 2, w.clock.now(), w.clock.now() - 300)
    for call in (w.hints.reveal(sid, 2), w.grader.grade(sid, 2, [])):
        with pytest.raises(GradingInProgressException) as e:
            await call
        assert e.value.error_code == 409
    assert (await w.sessions.get(sid)).hinted_parts == []


async def test_an_invalid_submission_is_refused_before_anything(session_provider: SQLModelSessionProvider) -> None:
    w = Wiring(session_provider, ScriptedLLMClient({}))
    sid = await w.start()
    good = on(parted(), 0)
    with pytest.raises(InvalidAnnotationsException):
        await w.grader.grade(sid, 2, [good, good])
    assert (await w.sessions.get(sid)).part_gradings == []


async def test_a_part_grading_past_its_deadline_fails_and_releases_its_claim(
    session_provider: SQLModelSessionProvider, monkeypatch: pytest.MonkeyPatch
) -> None:
    class SlowGrader(ScriptedLLMClient):
        async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
            await asyncio.sleep(30)
            return await super().structured(stage, request)

    monkeypatch.setattr(part_grader_module, "GRADING_DEADLINE_S", 0.1)
    w = Wiring(session_provider, SlowGrader({Stage.MISTAKES_GRADING: [found("e1")]}))
    sid = await w.start()
    with pytest.raises(MistakeGradingTimeoutException) as e:
        await asyncio.wait_for(w.grader.grade(sid, 2, [on(parted(), 0)]), 10)
    assert e.value.error_code == 504 and (await w.sessions.get(sid)).part_gradings == []
    fast = Wiring(session_provider, ScriptedLLMClient({Stage.MISTAKES_GRADING: [found("e1")]}))
    assert (await fast.grader.grade(sid, 2, [on(parted(), 0)])).graded.grading.score == 100
