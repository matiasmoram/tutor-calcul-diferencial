import pytest

from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.entities.mistake_grading import MistakeGrading
from core.mistakes.domain.grading import grade, locate_annotations
from core.mistakes.domain.values.mistake_source import MistakeSource
from core.mistakes.infra.llm_adapters import LLMAnnotationGrader
from core.shared.llm.client import LLMClient, Stage
from tests.core.mistakes.builders import problem_source, solution
from tests.fakes.llm import ScriptedLLMClient


async def grade_with(
    llm: LLMClient, source: MistakeSource, exercise: MistakeExercise, annotations: list[Annotation]
) -> MistakeGrading:
    """Code places the annotations, the model judges them (only when there is any), code scores."""
    located = locate_annotations(exercise, annotations)
    if not located:
        return grade(exercise, located, None, None)
    report, call = await LLMAnnotationGrader(llm).grade(source, exercise, located)
    return grade(exercise, located, report, call)


async def test_grading_scores_in_code_and_enforces_candidates() -> None:
    sol = solution()
    e1 = sol.mistakes[0]
    anots = [
        Annotation(id="a1", fragment=2, start=e1.start, end=e1.end, comment="la desigualtat va al revés"),
        Annotation(id="a2", fragment=3, start=0, end=4, comment="no se segueix"),  # right fragment, off the quote
        Annotation(id="a3", fragment=1, start=0, end=10, comment="crec que està malament"),
    ]
    llm = ScriptedLLMClient(
        {
            Stage.MISTAKES_GRADING: [
                {
                    "avaluacions": [
                        {"anotacio": "a1", "error": "e1", "explicacio": "correcta", "feedback": "Molt bé."},
                        {"anotacio": "a2", "error": "e2", "explicacio": "parcial", "feedback": "Gairebé."},
                        # The model tries to credit a1's error to an annotation in another fragment: code refuses.
                        {"anotacio": "a3", "error": "e1", "explicacio": "correcta", "feedback": "?"},
                    ],
                    "resum": "Bé.",
                }
            ]
        }
    )
    r = await grade_with(llm, problem_source(), sol, anots)
    by = {a.id: a for a in r.annotations}
    assert by["a1"].location == "exacta" and by["a1"].points == 1.0
    assert by["a2"].location == "aproximada" and by["a2"].points == pytest.approx(0.6 * 0.8)
    assert by["a3"].mistake_id == "cap"
    assert r.found == 2 and r.false_positives == 1
    assert r.score == round(100 * ((1.0 + 0.48) / 2 - 0.1))
    assert r.call is not None and r.call.model == "scripted"
    # The student-facing JSON keeps the legacy keys.
    dumped = r.model_dump()
    assert set(dumped) == {"nota", "trobats", "total", "falsos_positius", "anotacions", "errors", "resum", "crida"}
    assert set(dumped["anotacions"][0]) == {"id", "error", "localitzacio", "explicacio", "feedback", "punts"}
    assert set(dumped["errors"][0]) == {
        "id",
        "fragment",
        "cita",
        "inici",
        "fi",
        "tipus",
        "explicacio",
        "correccio",
        "pista",
    }
    # The grader only chooses among the candidates code computed.
    user = llm.requests[Stage.MISTAKES_GRADING][0].user
    assert "candidats: ['e1']" in user and "candidats: cap" in user


async def test_grading_without_annotations_skips_llm() -> None:
    llm = ScriptedLLMClient({})
    r = await grade_with(llm, problem_source(), solution(), [])
    assert r.score == 0 and r.found == 0 and len(r.mistakes) == 2 and r.call is None
    assert llm.calls(Stage.MISTAKES_GRADING) == 0


async def test_grading_tolerates_malformed_llm_evaluation() -> None:
    sol = solution()
    e1 = sol.mistakes[0]
    llm = ScriptedLLMClient(
        {
            Stage.MISTAKES_GRADING: [
                {"avaluacions": [{"anotacio": "a1", "error": "e1", "explicacio": "genial"}, "soroll", {}], "resum": ""}
            ]
        }
    )
    r = await grade_with(llm, problem_source(), sol, [Annotation(id="a1", fragment=2, start=e1.start, end=e1.end)])
    assert r.annotations[0].explanation == "absent" and r.found == 1


def test_annotations_outside_the_document_or_empty_are_dropped() -> None:
    sol = solution()
    located = locate_annotations(
        sol,
        [
            Annotation(id="out", fragment=9, start=0, end=3),
            Annotation(id="empty", fragment=2, start=5, end=5),
            Annotation(id="clipped", fragment=1, start=-4, end=10_000),
        ],
    )
    assert [a.id for a in located] == ["clipped"]
    assert (located[0].start, located[0].end) == (0, len(sol.fragments[0]))
