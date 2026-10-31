import asyncio

from pydantic import BaseModel

from core.course.domain.entities.course import Course
from core.course.domain.entities.theory_item import TheoryItem
from core.mistakes.application.annotations_grader import GRADING_CLAIM_TIMEOUT_S, GRADING_DEADLINE_S
from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_grading import PartedMistakeGrading, PartGrading
from core.mistakes.domain.entities.mistake_session import MistakeSession
from core.mistakes.domain.entities.parted_mistake_exercise import PartedMistakeExercise, PartText, PartToReview
from core.mistakes.domain.exceptions import (
    GradingInProgressException,
    MistakeGradingTimeoutException,
    MistakeLayoutMismatchException,
    MistakePartAlreadyGradedException,
    MistakePartOutOfOrderException,
    UnknownMistakePartException,
)
from core.mistakes.domain.ports import AnnotationGrader
from core.mistakes.domain.repository import MistakeExerciseRepository, MistakeSessionRepository
from core.mistakes.domain.services.grading import (
    HINT_FACTOR,
    aggregate_parts,
    check_annotations,
    grade,
    locate_annotations,
)
from core.mistakes.domain.services.sources import source_of
from core.mistakes.domain.values.mistake_source import TheorySource
from core.shared.domain.clock import Clock
from core.shared.domain.ids import SessionId
from core.shared.llm.call_scope import call_scope


class PartGradingOutcome(BaseModel):
    """One graded part, and what comes next: the next flawed part to review, or, after the last one, the whole
    session's result with the correct resolution (and, for theory, the original item of the notes)."""

    graded: PartGrading
    correct: list[str]  # the part's correct fragments
    next: PartToReview | None
    final: PartedMistakeGrading | None
    resolution: list[PartText] | None  # with `final`
    original: TheoryItem | None  # with `final`, theory only


async def parted_session(
    sessions: MistakeSessionRepository, exercises: MistakeExerciseRepository, session_id: SessionId, part: int
) -> tuple[MistakeSession, PartedMistakeExercise]:
    """A per-parts session and its document, `part` being one of its flawed parts. Raises
    MistakeLayoutMismatchException for a whole-document session, UnknownMistakePartException otherwise."""
    session = await sessions.get(session_id)
    if session.layout != "per_parts":
        raise MistakeLayoutMismatchException(session_id, session.layout)
    document = await exercises.get(session.exercise_id)
    if not isinstance(document, PartedMistakeExercise):
        raise MistakeLayoutMismatchException(session_id, document.layout)
    if part not in document.flawed_parts:
        raise UnknownMistakePartException(part)
    return session, document


class PartAnnotationsGrader:
    """Grades the flawed parts of a per-parts session one at a time, in order, each once: a later submission for a
    graded part gets the stored result. Code places the annotations inside the part, the model judges the
    explanations, a hinted part scores x HINT_FACTOR."""

    def __init__(
        self,
        course: Course,
        sessions: MistakeSessionRepository,
        exercises: MistakeExerciseRepository,
        grader: AnnotationGrader,
        clock: Clock,
    ) -> None:
        self._course = course
        self._sessions = sessions
        self._exercises = exercises
        self._grader = grader
        self._clock = clock

    async def grade(self, session_id: SessionId, part: int, annotations: list[Annotation]) -> PartGradingOutcome:
        check_annotations(annotations)
        session, document = await parted_session(self._sessions, self._exercises, session_id, part)
        if (stored := session.part_grading(part)) is not None:
            return self._outcome(session, document, stored)
        if session.next_part(document.flawed_parts) != part:
            raise MistakePartOutOfOrderException(part)
        claimed_at = self._clock.now()
        if not await self._sessions.claim_part(session_id, part, claimed_at, claimed_at - GRADING_CLAIM_TIMEOUT_S):
            return await self._stored_outcome(session_id, document, part)
        deadline = asyncio.timeout(GRADING_DEADLINE_S)
        try:
            async with deadline:
                session = await self._sessions.get(session_id)  # with every hint recorded before the claim
                graded = await self._grade(session, document, part, annotations)
                await self._sessions.save_part_grading(session_id, annotations, graded, self._clock.now())
        except MistakePartAlreadyGradedException:
            # Our claim went stale and was taken over, and the other grading was stored first: it stands.
            return await self._stored_outcome(session_id, document, part)
        except TimeoutError:
            if deadline.expired():
                raise MistakeGradingTimeoutException(session_id) from None
            raise
        finally:
            await self._sessions.release_grading(session_id, claimed_at)
        session = session.model_copy(update={"part_gradings": [*session.part_gradings, graded]})
        return self._outcome(session, document, graded)

    async def _stored_outcome(
        self, session_id: SessionId, document: PartedMistakeExercise, part: int
    ) -> PartGradingOutcome:
        """The grading another submission stored; GradingInProgressException while it is still running."""
        session = await self._sessions.get(session_id)
        stored = session.part_grading(part)
        if stored is None:
            raise GradingInProgressException()
        return self._outcome(session, document, stored)

    async def _grade(
        self, session: MistakeSession, document: PartedMistakeExercise, part: int, annotations: list[Annotation]
    ) -> PartGrading:
        view = document.view(part)
        hinted = part in session.hinted_parts
        factor = HINT_FACTOR if hinted else 1.0
        located = locate_annotations(view, annotations)
        if not located:
            return PartGrading(part=part, hint_used=hinted, grading=grade(view, located, None, None, factor))
        source = source_of(self._course, session.source_kind, session.source_id)
        with call_scope(session.id):
            report, call = await self._grader.grade(source, view, located)
        return PartGrading(part=part, hint_used=hinted, grading=grade(view, located, report, call, factor))

    def _outcome(
        self, session: MistakeSession, document: PartedMistakeExercise, graded: PartGrading
    ) -> PartGradingOutcome:
        done = session.next_part(document.flawed_parts) is None
        original = None
        if done:
            source = source_of(self._course, session.source_kind, session.source_id)
            original = source.item if isinstance(source, TheorySource) else None
        return PartGradingOutcome(
            graded=graded,
            correct=document.part(graded.part).fragments,
            next=document.review_after(graded.part),
            final=aggregate_parts(session.part_gradings) if done else None,
            resolution=document.resolution() if done else None,
            original=original,
        )
