from pydantic import BaseModel

from core.course.domain.entities.course import Course
from core.course.domain.entities.theory_item import TheoryItem
from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_grading import MistakeGrading
from core.mistakes.domain.entities.mistake_session import MistakeSession
from core.mistakes.domain.exceptions import GradingInProgressException, MistakeSessionAlreadyGradedException
from core.mistakes.domain.grading import grade, locate_annotations
from core.mistakes.domain.ports import AnnotationGrader
from core.mistakes.domain.repository import MistakeExerciseRepository, MistakeSessionRepository
from core.mistakes.domain.sources import source_of
from core.mistakes.domain.values.mistake_source import TheorySource
from core.shared.domain.clock import Clock
from core.shared.domain.ids import SessionId
from core.shared.llm.call_scope import call_scope

# A claim older than this belongs to a grading that died without releasing it.
GRADING_CLAIM_TIMEOUT_S = 300.0


class AnnotationsGrading(BaseModel):
    grading: MistakeGrading
    # Theory documents: the original item of the notes, shown with the result (it was the answer key until now).
    original: TheoryItem | None


class AnnotationsGrader:
    """Grades a session's annotations once; later submissions get the stored result."""

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

    async def grade(self, session_id: SessionId, annotations: list[Annotation]) -> AnnotationsGrading:
        session = await self._sessions.get(session_id)
        if session.grading is not None:
            return self._outcome(session, session.grading)
        claimed_at = self._clock.now()
        if not await self._sessions.claim_grading(session_id, claimed_at, claimed_at - GRADING_CLAIM_TIMEOUT_S):
            return await self._stored_outcome(session_id)
        try:
            grading = await self._grade(session, annotations)
            await self._sessions.save_grading(session_id, annotations, grading, self._clock.now())
        except MistakeSessionAlreadyGradedException:
            # Our claim went stale and was taken over, and the other grading was stored first: it stands.
            return await self._stored_outcome(session_id)
        finally:
            await self._sessions.release_grading(session_id, claimed_at)
        return self._outcome(session, grading)

    async def _stored_outcome(self, session_id: SessionId) -> AnnotationsGrading:
        """The grading another submission stored; GradingInProgressException while it is still running."""
        session = await self._sessions.get(session_id)
        if session.grading is None:
            raise GradingInProgressException()
        return self._outcome(session, session.grading)

    async def _grade(self, session: MistakeSession, annotations: list[Annotation]) -> MistakeGrading:
        exercise = await self._exercises.get(session.exercise_id)
        source = source_of(self._course, session.source_kind, session.source_id)
        located = locate_annotations(exercise, annotations)
        if not located:
            return grade(exercise, located, None, None)
        with call_scope(session.id):
            report, call = await self._grader.grade(source, exercise, located)
        return grade(exercise, located, report, call)

    def _outcome(self, session: MistakeSession, grading: MistakeGrading) -> AnnotationsGrading:
        source = source_of(self._course, session.source_kind, session.source_id)
        return AnnotationsGrading(grading=grading, original=source.item if isinstance(source, TheorySource) else None)
