"""Grading rules. Code decides WHERE each annotation lands (character overlap with the declared errors); the model
only judges the student's explanation (port AnnotationGrader). The score is computed here."""

from collections.abc import Mapping

from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_exercise import DeclaredMistake, MistakeExercise
from core.mistakes.domain.entities.mistake_grading import AnnotationResult, Location, MistakeGrading
from core.mistakes.domain.exceptions import InvalidAnnotationsException
from core.mistakes.domain.services.locate import overlap, selectable_span
from core.mistakes.domain.values.llm_outputs import EXPLANATION_GRADES, NO_EXPLANATION, NO_MISTAKE, GraderReport
from core.mistakes.domain.values.located_annotation import LocatedAnnotation
from core.shared.domain.model_usage import ModelUsage

# The points of each grade, in the order of EXPLANATION_GRADES. Finding the error is worth something on its own; a
# wrong reason must never score below no reason at all.
EXPLANATION_POINTS: Mapping[str, float] = dict(zip(EXPLANATION_GRADES, (1.0, 0.6, 0.35, 0.3), strict=True))
APPROXIMATE_FACTOR = 0.8  # annotation in the right fragment but not on the quoted words
FALSE_POSITIVE_PENALTY = 0.1


def _storable(text: str) -> bool:
    """No control characters but tab, newline and carriage return (pasted text, which the API accepts too): the
    database refuses some (NUL in JSONB), and only after the paid grading call. Lone surrogates never get this far:
    pydantic refuses them when it parses the annotation."""
    return not any(ord(c) < 0x20 and c not in "\t\n\r" for c in text)


def check_annotations(annotations: list[Annotation]) -> None:
    """Before grading: ids unique (each result maps back to one annotation) and text the database can store."""
    ids = [a.id for a in annotations]
    if len(set(ids)) != len(ids):
        raise InvalidAnnotationsException("Hi ha anotacions amb el mateix identificador.")
    if not all(_storable(a.id) and _storable(a.comment) for a in annotations):
        raise InvalidAnnotationsException("Una anotació conté caràcters no vàlids (caràcters de control).")


def locate_annotations(exercise: MistakeExercise, annotations: list[Annotation]) -> list[LocatedAnnotation]:
    """Drops annotations outside the document or empty after clipping."""
    located: list[LocatedAnnotation] = []
    for a in annotations:
        if not 1 <= a.fragment <= len(exercise.fragments):
            continue
        text = exercise.fragments[a.fragment - 1]
        i0, i1 = max(0, a.start), min(len(text), a.end)
        if i1 <= i0:
            continue
        candidates = exercise.mistakes_in(a.fragment)
        located.append(
            LocatedAnnotation(
                id=a.id,
                key=f"a{len(located) + 1}",
                fragment=a.fragment,
                start=i0,
                end=i1,
                text=text[i0:i1],
                comment=a.comment.strip(),
                candidates=[e.id for e in candidates],
                overlapping=[e.id for e in candidates if overlap(i0, i1, e.start, e.end)],
                precise=[e.id for e in candidates if overlap(i0, i1, e.start, e.end) and _tight(text, i0, i1, e)],
            )
        )
    return located


def _tight(fragment: str, start: int, end: int, mistake: DeclaredMistake) -> bool:
    """The highlight is not much longer than the quote, measured against the shortest highlight the student can
    make over it (a quote inside a formula can only be selected with the whole formula)."""
    q0, q1 = selectable_span(fragment, mistake.start, mistake.end)
    return end - start <= 3 * (q1 - q0) + 10


def grade(
    exercise: MistakeExercise,
    located: list[LocatedAnnotation],
    report: GraderReport | None,
    call: ModelUsage | None,
) -> MistakeGrading:
    verdicts = {v.annotation: v for v in report.verdicts} if report else {}  # by key
    results: list[AnnotationResult] = []
    best: dict[str, float] = {}
    false_positives = 0
    for a in located:
        verdict = verdicts.get(a.key)
        claimed = verdict.mistake if verdict else NO_MISTAKE
        explanation = verdict.explanation if verdict else NO_EXPLANATION
        if explanation not in EXPLANATION_POINTS:
            explanation = NO_EXPLANATION
        # Where the highlight lands is decided by code: an annotation on an error's quoted words finds that error
        # even if the model's verdict is missing or says NO_MISTAKE. The model only grades the explanation.
        if a.overlapping:
            mistake_id = claimed if claimed in a.overlapping else a.overlapping[0]
        else:
            mistake_id = claimed if claimed in a.candidates else NO_MISTAKE
        location: Location | None = None
        points = 0.0
        if mistake_id != NO_MISTAKE:
            location = "exacta" if mistake_id in a.precise else "aproximada"
            points = EXPLANATION_POINTS[explanation] * (1.0 if location == "exacta" else APPROXIMATE_FACTOR)
            best[mistake_id] = max(best.get(mistake_id, 0.0), points)
        else:
            false_positives += 1
        results.append(
            AnnotationResult(
                id=a.id,
                mistake_id=mistake_id,
                location=location,
                explanation=explanation,
                feedback=verdict.feedback if verdict else "",
                points=round(points, 2),
            )
        )

    n = exercise.n_mistakes
    raw = sum(best.values()) / n if n else 0.0
    score = max(0.0, raw - FALSE_POSITIVE_PENALTY * false_positives)
    return MistakeGrading(
        score=round(100 * score),
        found=len(best),
        total=n,
        false_positives=false_positives,
        annotations=results,
        mistakes=exercise.mistakes,
        summary=report.summary if report else "",
        call=call,
    )
