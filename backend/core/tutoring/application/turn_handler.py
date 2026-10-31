import asyncio

from pydantic import BaseModel

from core.course.domain.citations import cited_items
from core.course.domain.entities.course import Course
from core.course.domain.entities.exercise import Exercise
from core.course.domain.entities.theory_item import TheoryItem
from core.shared.domain.claims import claim_timeout
from core.shared.domain.clock import Clock, SystemClock
from core.shared.domain.ids import SessionId, TheoryItemId
from core.shared.llm.call_scope import call_scope
from core.tutoring.domain.entities.tutor_session import TutorSession
from core.tutoring.domain.entities.tutor_turn import TutorTurn
from core.tutoring.domain.exceptions import (
    ConcurrentTurnException,
    ModelOutputException,
    TruncatedModelOutputException,
    TurnTimeoutException,
)
from core.tutoring.domain.ports import Diagnoser, ReplyJudge, ReplyWriter
from core.tutoring.domain.repository import TutorSessionRepository
from core.tutoring.domain.services.fallback import fallback_message
from core.tutoring.domain.services.guard import citation_problems, deterministic_check
from core.tutoring.domain.services.policy import allowed_content, allowed_theory, decide
from core.tutoring.domain.services.theory_access import concept_question_ids
from core.tutoring.domain.values.chat_message import ChatMessage, TurnOrigin
from core.tutoring.domain.values.guard_verdict import GuardVerdict
from core.tutoring.domain.values.plan import Plan
from core.tutoring.domain.values.turn_trace import CheckedDraft, DraftAttempt, FailedDraft, ModelCall, TurnTrace

MAX_ATTEMPTS = 3  # first draft + 2 rewrites
TURN_DEADLINE_S = 300.0  # the whole turn, every model call and retry included
TURN_CLAIM_TIMEOUT_S = claim_timeout(TURN_DEADLINE_S)
# The sympy guard of one draft. A timed-out check keeps running in its worker thread (threads cannot be
# cancelled); only its result is dropped.
GUARD_DEADLINE_S = 20.0
GUARD_TIMEOUT_PROBLEM = "comprovació CAS: temps esgotat"


class TurnInput(BaseModel):
    session_id: SessionId
    text: str
    origin: TurnOrigin = "text"


class TurnResult(BaseModel):
    message: str
    references: list[TheoryItem]  # the allowed items the message cites, for the web to link
    trace: TurnTrace


class _Reply(BaseModel):
    message: str
    references: list[TheoryItemId]


class TurnHandler:
    """One tutor turn: diagnosis -> policy -> reply -> guard (with bounded retries, then an authored fallback).

    Atomic: the session is stored only when the whole turn succeeded, so on any failure the stored session is
    exactly as before and the student can resend."""

    def __init__(
        self,
        course: Course,
        sessions: TutorSessionRepository,
        diagnoser: Diagnoser,
        writer: ReplyWriter,
        judge: ReplyJudge,
        clock: Clock | None = None,
    ) -> None:
        self._course = course
        self._sessions = sessions
        self._diagnoser = diagnoser
        self._writer = writer
        self._judge = judge
        self._clock = clock or SystemClock()

    async def handle(self, request: TurnInput) -> TurnResult:
        claimed_at = self._clock.now()
        # A second message while one is being answered is refused before any model is called (two tabs, a retry).
        # Claimed before the session is read, so the turn runs on the version no other turn can change meanwhile.
        if not await self._sessions.claim_turn(request.session_id, claimed_at, claimed_at - TURN_CLAIM_TIMEOUT_S):
            raise ConcurrentTurnException(request.session_id)
        deadline = asyncio.timeout(TURN_DEADLINE_S)
        try:
            async with deadline:
                session = await self._sessions.get(request.session_id)
                return await self._handle(session, request, claimed_at)
        except TimeoutError:
            if deadline.expired():
                raise TurnTimeoutException(request.session_id) from None
            raise
        finally:
            await self._sessions.release_turn(request.session_id, claimed_at)

    async def _handle(self, session: TutorSession, request: TurnInput, claimed_at: float) -> TurnResult:
        ex = self._course.exercise(session.exercise_id)
        text = request.text.strip()
        with call_scope(session.id, session.next_turn):
            reply, trace = await self._run(session, ex, text, request.origin)
        turn = TutorTurn(
            session_id=session.id,
            number=trace.turn,
            created_at=self._clock.now(),
            origin=request.origin,
            student_text=text,
            tutor_text=reply.message,
            trace=trace,
        )
        session.record_turn(text, reply.message, trace.state, turn.created_at)
        await self._sessions.save_turn(session, turn, claimed_at)
        return TurnResult(
            message=reply.message, references=[self._course.theory[i] for i in reply.references], trace=trace
        )

    async def _run(
        self, session: TutorSession, ex: Exercise, text: str, origin: TurnOrigin
    ) -> tuple[_Reply, TurnTrace]:
        t0 = self._clock.monotonic()
        calls: list[ModelCall] = []
        history = session.history_with(text)

        concept_ids = concept_question_ids(self._course, ex)
        try:
            raw, call = await self._diagnoser.diagnose(ex, session.state, history, concept_ids)
        except TruncatedModelOutputException as e:
            # A degenerate loop up to max_tokens is a sampling accident: asked once more, the model usually
            # answers. Both calls are paid for, so both are in the trace.
            if e.call is not None:
                calls.append(e.call)
            raw, call = await self._diagnoser.diagnose(ex, session.state, history, concept_ids)
        calls.append(call)
        diagnosis = raw.normalized(ex.step_ids, concept_ids)
        student_texts = [m.text for m in history if m.role == "alumne"]
        # The policy may compare the student's text with the result in sympy: off the event loop.
        plan, state = await asyncio.to_thread(decide, ex, diagnosis, session.state, student_texts)
        content = allowed_content(ex, plan, state.completed, state.shown)
        theory = allowed_theory(self._course, ex, plan, state.completed)

        # Where the reply may legitimately take formulas from (the sympy guard compares against these).
        permitted = [content, ex.statement_md(), *[it.statement for it in theory], *student_texts]
        attempts: list[DraftAttempt] = []
        final: _Reply | None = None
        feedback: str | None = None
        for _ in range(MAX_ATTEMPTS):
            attempt = await self._attempt(ex, history, plan, content, theory, permitted, feedback, calls)
            attempts.append(attempt)
            if isinstance(attempt, FailedDraft):
                continue
            if attempt.approved:
                final = _Reply(message=attempt.message, references=attempt.references)
                break
            feedback = "\n".join(f"- {r}" for r in attempt.rejection_reasons())

        used_fallback = final is None
        if final is None:
            message = fallback_message(ex, plan, theory)
            final = _Reply(message=message, references=cited_items(message, theory, ex.topic))

        trace = TurnTrace(
            turn=state.turns,
            origin=origin,
            diagnosis=diagnosis,
            plan=plan,
            allowed_content=content,
            allowed_theory=[it.id for it in theory],
            attempts=attempts,
            fallback=used_fallback,
            previous_state=session.state,
            state=state,
            calls=calls,
            latency_ms=int((self._clock.monotonic() - t0) * 1000),
        )
        return final, trace

    async def _attempt(
        self,
        ex: Exercise,
        history: list[ChatMessage],
        plan: Plan,
        content: str,
        theory: list[TheoryItem],
        permitted: list[str],
        feedback: str | None,
        calls: list[ModelCall],
    ) -> DraftAttempt:
        try:
            message, call = await self._writer.write(ex, history, plan, content, theory, feedback)
        except ModelOutputException as e:
            if e.call is not None:
                calls.append(e.call)
            return FailedDraft(error=e.detail)
        calls.append(call)
        # References are the allowed items the message actually cites ("Teorema 12 del Tema 3").
        references = cited_items(message, theory, ex.topic)
        # sympy work (the CAS provenance check): off the event loop, other students' turns keep running.
        try:
            problems = await asyncio.wait_for(
                asyncio.to_thread(deterministic_check, message, plan, permitted), GUARD_DEADLINE_S
            )
        except TimeoutError:
            # Fail closed: a draft the CAS could not verify never reaches the student.
            problems = [GUARD_TIMEOUT_PROBLEM]
        problems += citation_problems(message, theory, ex.topic, permitted)
        verdict: GuardVerdict | None = None
        if not problems:
            # Only pay for the LLM judge once the cheap checks pass.
            try:
                raw, call = await self._judge.judge(ex, plan, content, theory, history, message, references)
                calls.append(call)
                verdict = raw.consistent()
            except ModelOutputException as e:
                if e.call is not None:
                    calls.append(e.call)
                verdict = GuardVerdict.unavailable(e.detail)
        return CheckedDraft(message=message, references=references, deterministic_problems=problems, verdict=verdict)
