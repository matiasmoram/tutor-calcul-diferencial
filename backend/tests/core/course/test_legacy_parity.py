"""TEMPORARY (phase 2-5 of work/ARQUITECTURA.md): the new loader reads exactly what the old one read.

Deleted together with backend/tutor in phase 6."""

from tests.fixtures.course import authored_course
from tutor.fitxes import load_llistes
from tutor.teoria import load_teoria

COURSE = authored_course()
OLD_THEORY = load_teoria()
OLD_SHEETS, OLD_EXERCISES = load_llistes(teoria=OLD_THEORY)


def test_same_exercises_with_the_same_content() -> None:
    assert list(COURSE.exercises) == list(OLD_EXERCISES)
    for ex_id, old in OLD_EXERCISES.items():
        new = COURSE.exercise(ex_id)
        assert new.statement_md() == old.enunciat_md(), ex_id
        assert new.full_reference() == old.full_reference(), ex_id
        assert [str(r) for r in new.all_refs()] == old.all_refs(), ex_id
        assert {str(i) for i in COURSE.reserved_ids(new)} == old.reserved_ids(OLD_THEORY), ex_id
        assert (new.sheet_id, new.group, new.topic, new.problem, new.part, new.label, new.kind, new.format) == (
            old.llista,
            old.grup,
            old.tema,
            old.problema,
            old.apartat,
            old.etiqueta,
            old.tipus,
            old.format,
        ), ex_id
        assert (new.source, new.preamble, new.hint, new.professor_note) == (
            old.font,
            old.preambul,
            old.indicacio,
            old.nota_professor,
        ), ex_id
        for s, o in zip(new.steps, old.passos, strict=True):
            assert (s.id, s.title, s.objective, s.idea, s.detail, s.leak_patterns, [str(r) for r in s.theory]) == (
                o.id,
                o.titol,
                o.objectiu,
                o.idea,
                o.detall,
                o.fuites,
                o.teoria,
            ), (ex_id, s.id)
        for m, o in zip(new.common_mistakes, old.errors_comuns, strict=True):
            assert (m.id, m.description, m.question) == (o.id, o.descripcio, o.pregunta)
        assert (new.result.value, new.result.leak_patterns) == (old.resultat.valor, old.resultat.fuites)


def test_same_theory_items() -> None:
    assert list(COURSE.theory) == list(OLD_THEORY)
    for item_id, old in OLD_THEORY.items():
        new = COURSE.theory_item(item_id)
        assert (
            new.label == old.etiqueta and new.render(True) == old.render(True) and new.index_line() == old.index_line()
        )
        assert (new.summary_ref, new.page, new.problems, new.section) == (
            old.resum,
            old.pagina,
            old.problemes,
            old.seccio,
        )


def test_same_sheets_and_problems() -> None:
    assert list(COURSE.sheets) == list(OLD_SHEETS)
    for sheet_id, old in OLD_SHEETS.items():
        new = COURSE.sheet(sheet_id)
        assert (new.label, new.title, new.description, new.topic, new.kind, new.format) == (
            old.etiqueta,
            old.titol,
            old.descripcio,
            old.tema,
            old.tipus,
            old.format,
        )
        assert [str(e) for e in new.exercise_ids] == old.exercicis
        assert [(p.number, p.source, p.preamble, p.hint, [str(e) for e in p.exercise_ids]) for p in new.problems] == [
            (p.num, p.font, p.preambul, p.indicacio, p.exercicis) for p in old.problemes
        ]
