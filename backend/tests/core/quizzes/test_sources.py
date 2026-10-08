import pytest

from core.quizzes.domain.exceptions import UnknownQuizSourceException
from core.quizzes.domain.sources import focus_items, quiz_source
from core.quizzes.infra.prompts import source_context
from tests.fixtures.course import authored_course

COURSE = authored_course()


def test_focus_sources() -> None:
    f = quiz_source(COURSE, "T2.12")
    assert f.topic == 2 and f.id == "T2.12" and "<resultat_focus>" in source_context(f)
    assert quiz_source(COURSE, "tema-3").focus is None
    with pytest.raises(UnknownQuizSourceException) as e:
        quiz_source(COURSE, "T9.1")
    assert e.value.error_code == 404
    with pytest.raises(UnknownQuizSourceException):
        quiz_source(COURSE, "tema-9")
    assert all(i in COURSE.theory for i in quiz_source(COURSE, "tema-2").allowed_refs)


def test_a_topic_source_carries_its_notes_and_the_citable_items_up_to_it() -> None:
    s = quiz_source(COURSE, "tema-2")
    assert s.notes and all(it.topic == 2 for it in s.notes)
    assert {COURSE.theory[r].topic for r in s.allowed_refs} == {1, 2}
    assert source_context(s).startswith('<apunts tema="2" titol="')


def test_focus_items_are_numbered_results_and_definitions() -> None:
    items = focus_items(COURSE)
    assert items and all(it.number is not None and it.kind in ("teorema", "proposicio", "lema", "corollari",
                                                                   "definicio") for it in items)  # fmt: skip
    assert "T2.12" in {it.id for it in items}
