"""Grading rules. Code decides WHERE each annotation lands (character overlap with the declared errors); the model
only judges the student's explanation (port AnnotationGrader). The score is computed here."""

from collections.abc import Mapping

from pydantic import BaseModel

from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.entities.mistake_grading import AnnotationResult, Location, MistakeGrading
from core.mistakes.domain.locate import overlap
from core.mistakes.domain.values.call_record import CallRecord
from core.mistakes.domain.values.llm_outputs import GraderReport

# Finding the error is worth something on its own; a wrong reason must never score below no reason at all.
EXPLANATION_POINTS: Mapping[str, float] = {"correcta": 1.0, "parcial": 0.6, "incorrecta": 0.35, "absent": 0.3}
APPROXIMATE_FACTOR = 0.8  # annotation in the right fragment but not on the quoted words
FALSE_POSITIVE_PENALTY = 0.1
NO_MISTAKE = "cap"


class LocatedAnnotation(BaseModel):
    """An annotation clipped to its fragment, with the declared errors it can be about."""

    id: str
    fragment: int
    start: int
    end: int
    text: str  # the underlined passage
    comment: str
    candidates: list[str]  # errors of the same fragment
    overlapping: list[str]  # candidates whose quote the underline touches
    # Candidates hit on their quoted words, not by a highlight of the whole fragment that happens to contain them.
    precise: list[str]


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
                fragment=a.fragment,
                start=i0,
                end=i1,
                text=text[i0:i1],
                comment=a.comment.strip(),
                candidates=[e.id for e in candidates],
                overlapping=[e.id for e in candidates if overlap(i0, i1, e.start, e.end)],
                precise=[
                    e.id
                    for e in candidates
                    if overlap(i0, i1, e.start, e.end) and (i1 - i0) <= 3 * (e.end - e.start) + 10
                ],
            )
        )
    return located


def grade(
    exercise: MistakeExercise,
    located: list[LocatedAnnotation],
    report: GraderReport | None,
    call: CallRecord | None,
) -> MistakeGrading:
    verdicts = {v.annotation: v for v in report.verdicts} if report else {}
    results: list[AnnotationResult] = []
    best: dict[str, float] = {}
    false_positives = 0
    for a in located:
        verdict = verdicts.get(a.id)
        claimed = verdict.mistake if verdict else NO_MISTAKE
        explanation = verdict.explanation if verdict else "absent"
        if explanation not in EXPLANATION_POINTS:
            explanation = "absent"
        # Where the highlight lands is decided by code: an annotation on an error's quoted words finds that error
        # even if the model's verdict is missing or says "cap". The model only grades the explanation.
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
