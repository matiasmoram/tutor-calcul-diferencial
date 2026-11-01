from core.course.domain.services.citations import cited_items
from core.course.domain.values.theory_ref import TheoryRef
from tests.fixtures.course import authored_course

COURSE = authored_course()


def test_citations_resolve_to_allowed_items_only() -> None:
    allowed = [it for it in COURSE.theory.values() if it.topic == 3 and it.number is not None][:5]
    first = allowed[0]
    name = {"teorema": "Teorema", "definicio": "Definició", "proposicio": "Proposició"}.get(first.kind, "Lema")
    if first.kind not in ("teorema", "definicio", "proposicio", "lema"):
        return
    text = f"Pel {name} {first.number} del Tema 3, i també el {name} {first.number} (Tema 3)."
    assert cited_items(text, allowed, default_topic=1) == [first.id]
    assert cited_items(f"Pel {name} {first.number}", allowed, default_topic=3) == [first.id]
    assert cited_items(f"Pel {name} {first.number}", allowed, default_topic=2) == []
    assert cited_items(f"Pel {name} {first.number} del Tema 3", [], default_topic=3) == []


def test_theory_refs_parse_statement_and_proof() -> None:
    assert TheoryRef("T3.12").item_id == "T3.12" and not TheoryRef("T3.12").with_proof
    assert TheoryRef("T3.x4+dem").item_id == "T3.x4" and TheoryRef("T3.x4+dem").with_proof
