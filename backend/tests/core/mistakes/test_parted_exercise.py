import pytest
from pydantic import ValidationError

from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.entities.mistake_grading import PartGrading
from core.mistakes.domain.entities.mistake_session import MistakeSession
from core.mistakes.domain.entities.parted_mistake_exercise import (
    MISTAKE_DOCUMENT_ADAPTER,
    PartedMistakeExercise,
)
from core.mistakes.domain.exceptions import UnknownMistakePartException
from core.mistakes.domain.services.grading import HINT_FACTOR, aggregate_parts, grade, locate_annotations
from core.mistakes.domain.values.llm_outputs import GraderReport
from core.mistakes.domain.values.mistake_exercise_id import MistakeExerciseId
from core.shared.domain.ids import SessionId
from tests.core.mistakes.builders import PART1_ERROR, PART3_ERROR, PARTS, parted, solution, theory_parted


def test_a_document_in_parts_numbers_its_errors_across_the_whole_document() -> None:
    doc = parted()
    assert doc.flawed_parts == [2, 3] and doc.n_mistakes == 2
    assert [m.id for m in doc.mistakes] == ["e1", "e2"] and [m.fragment for m in doc.mistakes] == [3, 6]
    assert doc.fragments == [f for _, fragments in PARTS for f in fragments]
    assert [doc.part_range(i) for i in (1, 2, 3)] == [range(1, 3), range(3, 5), range(5, 7)]
    assert doc.parts[1].flawed_fragments == [
        "Com que $x^4 \\ge x^4+y^2$, el quocient està fitat per $|x|$.",
        PARTS[1][1][1],
    ]
    assert [p.title for p in doc.parts] == ["Trobar un candidat", "Acotar el quocient", "Concloure amb el sandvitx"]


def test_its_json_has_the_per_parts_format_and_clean_parts_carry_no_error_keys() -> None:
    dumped = parted().model_dump(mode="json")
    assert dumped["format"] == "per_parts" and list(dumped) == [
        "id",
        "exercici",
        "font",
        "dificultat",
        "format",
        "n_enunciat",
        "parts",
        "verificacio",
        "creat",
    ]
    assert set(dumped["parts"][0]) == {"titol", "pas", "fragments"}
    assert set(dumped["parts"][1]) == {"titol", "pas", "fragments", "fragments_errats", "error", "verificacio"}


def test_both_layouts_load_through_the_document_union() -> None:
    sencer = MISTAKE_DOCUMENT_ADAPTER.validate_python(solution().model_dump(mode="json"))
    assert isinstance(sencer, MistakeExercise) and "format" not in sencer.model_dump()
    explicit = MISTAKE_DOCUMENT_ADAPTER.validate_python(solution().model_dump(mode="json") | {"format": "sencer"})
    assert isinstance(explicit, MistakeExercise)
    doc = parted()
    loaded = MISTAKE_DOCUMENT_ADAPTER.validate_json(doc.model_dump_json())
    assert isinstance(loaded, PartedMistakeExercise) and loaded == doc
    with pytest.raises(ValidationError):
        MistakeExercise.model_validate(doc.model_dump(mode="json"))


def _broken(update: dict[str, object], part: int = 2) -> dict[str, object]:
    data = parted().model_dump(mode="json")
    data["parts"][part - 1] |= update
    return data


@pytest.mark.parametrize(
    ("data", "message"),
    [
        (_broken({"fragments_errats": ["un sol fragment"]}), "fragments"),
        (_broken({"error": None}), "go together"),
        (_broken({"error": parted().parts[1].mistake.model_dump() | {"fragment": 5}}), "outside the part"),  # type: ignore[union-attr]
        (_broken({"error": parted().parts[1].mistake.model_dump() | {"inici": 0}}), "offsets"),  # type: ignore[union-attr]
        (_broken({"error": parted().parts[1].mistake.model_dump() | {"cita": "", "inici": 8, "fi": 8}}), "empty"),  # type: ignore[union-attr]
        (_broken({"error": parted().parts[1].mistake.model_dump() | {"cita": "", "inici": 90, "fi": 95}}), "outside"),  # type: ignore[union-attr]
        (_broken({"fragments_errats": PARTS[1][1]}), "offsets"),
        (_broken({"error": None, "fragments_errats": None, "verificacio": None}, 3) | {"parts": []}, "at least 2"),
        (parted().model_dump(mode="json") | {"n_enunciat": 1}, "no statement"),
    ],
)
def test_invariants(data: dict[str, object], message: str) -> None:
    with pytest.raises(ValidationError, match=message):
        PartedMistakeExercise.model_validate(data)


def test_an_error_fragment_equal_to_the_correct_one_is_refused() -> None:
    data = parted().model_dump(mode="json")
    correct = data["parts"][1]["fragments"][0]
    data["parts"][1]["fragments_errats"][0] = correct
    data["parts"][1]["error"] |= {"cita": correct[4:10], "inici": 4, "fi": 10}
    with pytest.raises(ValidationError, match="is the correct one"):
        PartedMistakeExercise.model_validate(data)


def test_a_document_without_errors_is_refused() -> None:
    with pytest.raises(ValidationError, match="no part has an error"):
        parted(errors={})


def test_theory_part_one_is_the_statement_and_always_has_an_error() -> None:
    data = theory_parted().model_dump(mode="json")
    assert PartedMistakeExercise.model_validate(data).flawed_parts == [1, 3]
    with pytest.raises(ValidationError, match="statement"):
        PartedMistakeExercise.model_validate(data | {"n_enunciat": 1})
    with pytest.raises(ValidationError, match="statement"):
        PartedMistakeExercise.model_validate(data | {"n_enunciat": 0})
    clean_statement = parted().model_dump(mode="json") | {"font": "teoria", "exercici": "T3.21", "n_enunciat": 2}
    with pytest.raises(ValidationError, match=r"the statement \(part 1\) always has an error"):
        PartedMistakeExercise.model_validate(clean_statement)


def test_the_view_of_a_part_shows_the_earlier_parts_correct_and_nothing_after() -> None:
    doc = parted()
    view = doc.view(2)
    assert view.fragments == [*PARTS[0][1], *doc.parts[1].flawed_fragments]  # type: ignore[misc]
    assert view.mistakes == [doc.mistakes[0]] and view.annotatable == range(3, 5)
    last = doc.view(3)
    assert last.fragments[:4] == [*PARTS[0][1], *PARTS[1][1]] and last.fragments[4:] == doc.parts[2].flawed_fragments
    assert last.mistakes == [doc.mistakes[1]] and last.annotatable == range(5, 7)
    assert doc.view(1).mistakes == [] and doc.view(1).fragments == PARTS[0][1]
    with pytest.raises(UnknownMistakePartException) as e:
        doc.view(4)
    assert e.value.error_code == 404


def test_the_roadmap_and_the_parts_to_review_in_order() -> None:
    doc = parted()
    assert [(o.part, o.review) for o in doc.outline()] == [(1, False), (2, True), (3, True)]
    assert doc.outline()[0].model_dump() == {"part": 1, "titol": "Trobar un candidat", "revisar": False}
    first = doc.review_after(0)
    assert first is not None and first.model_dump() == {
        "part": 2,
        "primer_fragment": 3,
        "fragments": doc.parts[1].flawed_fragments,
        "anteriors": [{"part": 1, "fragments": PARTS[0][1]}],
    }
    second = doc.review_after(2)
    assert second is not None and second.part == 3 and second.earlier == [] and second.first_fragment == 5
    assert doc.review_after(3) is None


def test_a_clean_part_between_two_flawed_ones_comes_with_the_next_review() -> None:
    doc = parted(errors={1: PART1_ERROR, 3: PART3_ERROR})
    after = doc.review_after(1)
    assert after is not None and after.part == 3 and [p.part for p in after.earlier] == [2]
    assert after.earlier[0].fragments == PARTS[1][1]
    assert [p.fragments for p in doc.resolution()] == [fragments for _, fragments in PARTS]


def test_a_part_is_graded_on_its_own_fragments_only() -> None:
    doc = parted()
    view = doc.view(2)
    e1 = doc.mistakes[0]
    located = locate_annotations(
        view,
        [
            Annotation(id="on", fragment=3, start=e1.start, end=e1.end),
            Annotation(id="earlier", fragment=1, start=0, end=5),  # context, not annotatable
            Annotation(id="later", fragment=6, start=0, end=5),  # not shown yet
        ],
    )
    assert [a.id for a in located] == ["on"] and located[0].candidates == ["e1"]
    report = GraderReport.model_validate(
        {"avaluacions": [{"anotacio": "a1", "error": "e1", "explicacio": "correcta", "feedback": ""}]}
    )
    full = grade(view, located, report, None)
    assert full.score == 100 and full.total == 1 and full.mistakes == [e1]
    hinted = grade(view, located, report, None, HINT_FACTOR)
    assert hinted.score == 85


def test_the_session_score_is_the_mean_of_the_part_scores() -> None:
    doc = parted()
    nothing = grade(doc.view(3), [], None, None)
    found = grade(doc.view(2), locate_annotations(doc.view(2), []), None, None).model_copy(
        update={"score": 85, "found": 1, "false_positives": 1}
    )
    total = aggregate_parts(
        [PartGrading(part=3, hint_used=False, grading=nothing), PartGrading(part=2, hint_used=True, grading=found)]
    )
    assert total.model_dump() == {
        "nota": 42,
        "trobats": 1,
        "total": 2,
        "falsos_positius": 1,
        "parts": [{"part": 2, "nota": 85, "pista": True}, {"part": 3, "nota": 0, "pista": False}],
    }


def test_a_session_walks_the_flawed_parts_in_order() -> None:
    doc = parted()
    session = MistakeSession(
        id=SessionId.generate(),
        source_kind="problema",
        source_id="t2-4c",
        exercise_id=MistakeExerciseId(doc.id),
        difficulty="normal",
        created_at=1.0,
        layout="per_parts",
    )
    assert session.next_part(doc.flawed_parts) == 2 and session.part_grading(2) is None
    graded = PartGrading(part=2, hint_used=False, grading=grade(doc.view(2), [], None, None))
    session.part_gradings.append(graded)
    assert session.next_part(doc.flawed_parts) == 3 and session.part_grading(2) == graded
