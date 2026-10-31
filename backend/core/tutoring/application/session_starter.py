from pydantic import BaseModel

from core.course.domain.entities.course import Course
from core.course.domain.entities.exercise import Exercise
from core.course.domain.entities.problem_sheet import ProblemSheet
from core.course.domain.entities.theory_item import TheoryItem
from core.shared.domain.clock import Clock, SystemClock
from core.shared.domain.ids import ExerciseId
from core.tutoring.domain.entities.tutor_session import TutorSession
from core.tutoring.domain.repository import TutorSessionRepository
from core.tutoring.domain.services.theory_access import SheetTheoryUse, background_theory, sheet_theory


class StartedSession(BaseModel):
    session: TutorSession
    exercise: Exercise
    sheet: ProblemSheet
    # Background theory the student may read from the start (never the items that solve the exercise).
    background_theory: list[TheoryItem]
    # Professor panel only: every item the sheet cites, with where it is used.
    sheet_theory: list[SheetTheoryUse]


class SessionStarter:
    def __init__(self, course: Course, sessions: TutorSessionRepository, clock: Clock | None = None) -> None:
        self._course = course
        self._sessions = sessions
        self._clock = clock or SystemClock()

    async def start(self, exercise_id: ExerciseId) -> StartedSession:
        ex = self._course.exercise(exercise_id)
        session = TutorSession.start(ex.id, self._clock.now())
        await self._sessions.add(session)
        return StartedSession(
            session=session,
            exercise=ex,
            sheet=self._course.sheet(ex.sheet_id),
            background_theory=background_theory(self._course, ex),
            sheet_theory=sheet_theory(self._course, ex),
        )
