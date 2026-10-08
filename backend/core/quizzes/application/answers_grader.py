import asyncio
from collections.abc import Collection, Sequence

from pydantic import BaseModel, Field

from core.course.domain.entities.course import Course
from core.quizzes.domain.entities.grading import Answer, QuizGrading, StudentCheck
from core.quizzes.domain.entities.quiz import Quiz
from core.quizzes.domain.exceptions import ConcurrentQuizGradingException
from core.quizzes.domain.ports import AnswerGrader, CheckEvaluator, ClaimExtractor
from core.quizzes.domain.repository import QuizRepository, QuizSessionRepository
from core.quizzes.domain.services.scoring import admissible_claims, grade_quiz
from core.quizzes.domain.sources import QuizSource, quiz_source
from core.quizzes.domain.values.call_summary import CallSummary
from core.quizzes.domain.values.grading_inputs import AnsweredStatement, GraderEvaluation
from core.shared.domain.clock import Clock
from core.shared.llm.call_scope import call_scope

# A claim older than this belongs to a grading that died without releasing it.
GRADING_CLAIM_TIMEOUT_S = 300.0


class AnswersGraderInput(BaseModel):
    answers: list[Answer] = Field(max_length=20)


class AnswersGrader:
    """Grades a quiz once: the result reveals every verdict and solution, so a second submission gets the first
    result back. The grader LLM and a transcriber of the student's computations run in parallel; sympy checks
    those computations; code decides the score."""

    def __init__(
        self,
        course: Course,
        sessions: QuizSessionRepository,
        quizzes: QuizRepository,
        grader: AnswerGrader,
        extractor: ClaimExtractor,
        checks: CheckEvaluator,
        clock: Clock,
    ) -> None:
        self._course = course
        self._sessions = sessions
        self._quizzes = quizzes
        self._grader = grader
        self._extractor = extractor
        self._checks = checks
        self._clock = clock

    async def grade(self, session_id: str, request: AnswersGraderInput) -> QuizGrading:
        session = await self._sessions.get(session_id)
        if session.submission is not None:
            return session.submission.result
        # A second submission while the first is being graded is refused before any model is called.
        claimed_at = self._clock.now()
        if not await self._sessions.claim_grading(session_id, claimed_at, claimed_at - GRADING_CLAIM_TIMEOUT_S):
            return await self._stored_result(session_id)
        try:
            # Read again under the claim: the hints used up to now are the ones the grading counts.
            session = await self._sessions.get(session_id)
            quiz = await self._quizzes.get(session.quiz_id)
            source = quiz_source(self._course, session.source_id)
            with call_scope(session.id):
                result = await self.grade_answers(source, quiz, request.answers, set(session.hints_used))
            session.submit(request.answers, result, self._clock.now())
            await self._sessions.save(session)
        except ConcurrentQuizGradingException:
            # Our claim went stale and was taken over, and the other grading was stored first: it stands.
            return await self._stored_result(session_id)
        finally:
            await self._sessions.release_grading(session_id, claimed_at)
        return result

    async def _stored_result(self, session_id: str) -> QuizGrading:
        """The grading another submission stored; ConcurrentQuizGradingException while it is still running."""
        session = await self._sessions.get(session_id)
        if session.submission is None:
            raise ConcurrentQuizGradingException(session_id)
        return session.submission.result

    async def cited_theory(self, session_id: str) -> set[str]:
        """Items of the notes the session's solutions cite (shown with the grading)."""
        session = await self._sessions.get(session_id)
        return (await self._quizzes.get(session.quiz_id)).cited_theory()

    async def grade_answers(
        self, source: QuizSource, quiz: Quiz, answers: Sequence[Answer], hints: Collection[str]
    ) -> QuizGrading:
        by_id = {a.statement_id: a for a in answers if quiz.has_statement(a.statement_id)}
        answered = [
            AnsweredStatement(statement=s, answer=by_id[s.id])
            for s in quiz.statements
            if s.id in by_id and by_id[s.id].verdict
        ]
        evaluations: dict[str, GraderEvaluation] = {}
        transcribed: dict[str, list[StudentCheck]] = {}
        summary: str = ""
        call: CallSummary | None = None
        if answered:
            verdict, claims = await asyncio.gather(
                self._grader.grade(source, answered), self._extractor.extract(answered)
            )
            evaluations = {e.statement_id: e for e in verdict.evaluations}
            summary, call = verdict.summary, verdict.call
            transcribed = {c.statement_id: c.checks for c in claims}
        checked = await asyncio.to_thread(self._check_claims, answered, transcribed)
        return grade_quiz(quiz, by_id, hints, evaluations, checked, summary, call)

    def _check_claims(
        self, answered: Sequence[AnsweredStatement], transcribed: dict[str, list[StudentCheck]]
    ) -> dict[str, list[StudentCheck]]:
        """The student's own claims, checked by sympy in one batch: only those whose quote is in the answer and
        whose value is one the quote states."""
        kept = [admissible_claims(transcribed.get(a.statement.id, []), a.answer.justification) for a in answered]
        results = iter(self._checks.evaluate([c for cs in kept for c in cs]))
        return {
            a.statement.id: [c.with_result(next(results)) for c in cs] for a, cs in zip(answered, kept, strict=True)
        }
