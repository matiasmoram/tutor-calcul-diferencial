import asyncio
from dataclasses import dataclass, field
from random import Random

from loguru import logger

from core.quizzes.domain.entities.quiz import GenerationRound, Quiz, RejectedStatement
from core.quizzes.domain.entities.statement import StatementVerification
from core.quizzes.domain.exceptions import QuizGenerationException
from core.quizzes.domain.ports import BlindSolver, CheckEvaluator, QuizAuditor, QuizWriter
from core.quizzes.domain.services.assembly import build_quiz
from core.quizzes.domain.services.balance import (
    BATCH_SIZE,
    batch_false_bounds,
    is_complete,
    max_rounds,
    select_for_verification,
    trim,
)
from core.quizzes.domain.services.judging import judge
from core.quizzes.domain.services.validation import (
    all_checks,
    check_problems,
    normal_key,
    validate_draft,
    with_results,
)
from core.quizzes.domain.sources import QuizSource
from core.quizzes.domain.values.call_summary import CallSummary
from core.quizzes.domain.values.difficulty import QUIZ_SIZES, Difficulty
from core.quizzes.domain.values.drafts import BatchRequest, StatementDraft
from core.shared.domain.clock import Clock
from core.shared.domain.ids import TheoryItemId
from core.shared.llm.client import LLMError, LLMProviderError, TruncatedOutputError

# A request must not hang for tens of minutes: past this the generation fails (the rounds paid are in the call log).
GENERATION_DEADLINE_S = 420.0


class QuizGenerator:
    """Builds a verified quiz in batches: the writer proposes, code validates and runs the sympy checks, a blind
    solver and an auditor verify in parallel, and code decides. Rejected statements are replaced (not the whole
    quiz), with the reasons, in a few extra rounds. Only as many statements as the quiz still needs are verified;
    the valid surplus waits for a later round. A lost call costs its round, never the statements already kept."""

    def __init__(
        self,
        writer: QuizWriter,
        solver: BlindSolver,
        auditor: QuizAuditor,
        checks: CheckEvaluator,
        clock: Clock,
        rng: Random,
        deadline_s: float = GENERATION_DEADLINE_S,
    ) -> None:
        self._writer = writer
        self._solver = solver
        self._auditor = auditor
        self._checks = checks
        self._clock = clock
        self._rng = rng
        self._deadline_s = deadline_s

    async def generate(self, source: QuizSource, difficulty: Difficulty) -> Quiz:
        deadline = asyncio.timeout(self._deadline_s)
        try:
            async with deadline:
                return await self._generate(source, difficulty)
        except TimeoutError:
            if not deadline.expired():
                raise
            raise QuizGenerationException(
                f"no s'ha pogut generar el qüestionari en {self._deadline_s:.0f} s: torna-ho a provar més tard"
            ) from None

    async def _generate(self, source: QuizSource, difficulty: Difficulty) -> Quiz:
        n = QUIZ_SIZES[difficulty]
        refs = set(source.allowed_refs)
        kept: list[StatementDraft] = []
        # Statements that passed the code validation and sympy but were not verified yet: the surplus of a batch,
        # or a batch whose verification failed. Verified in later rounds instead of asking the writer again.
        backups: list[StatementDraft] = []
        feedback: list[RejectedStatement] = []
        rounds: list[GenerationRound] = []
        batch_size = BATCH_SIZE
        number = 0
        while number < max_rounds(n, batch_size):
            number += 1
            limit = min(batch_size, n - len(kept))
            to_verify, backups = select_for_verification(kept, backups, n, limit)
            round_log = GenerationRound(round=number, requested=0, received=0)
            rejected: list[tuple[StatementDraft, list[str]]] = []
            try:
                if len(to_verify) < limit:
                    k = limit - len(to_verify)
                    written = await self._write(source, difficulty, n, kept, to_verify, backups, k, feedback, refs)
                    round_log.requested, round_log.received, round_log.generation = k, written.received, written.call
                    rejected += written.rejected
                    chosen, extra = select_for_verification([*kept, *to_verify], written.candidates, n, k)
                    to_verify, backups = [*to_verify, *chosen], [*backups, *extra]
                if to_verify:
                    verified = await self._verify(source, to_verify, number)
                    to_verify = []
                    kept += verified.accepted
                    rejected += verified.rejected
                    round_log.solver, round_log.audit = verified.solver, verified.audit
            except TruncatedOutputError as e:
                backups = [*to_verify, *backups]
                if batch_size > 1:
                    # Asking for as much again would be cut again: this round is retried with half the batch.
                    batch_size //= 2
                    number -= 1
                    logger.warning("quiz {} ({}): {}; batches of {} now", source.id, difficulty, e.message, batch_size)
                    continue
                logger.warning("quiz {} ({}): round {} lost: {}", source.id, difficulty, number, e.message)
            except LLMProviderError:
                raise
            except LLMError as e:
                # One unusable output (still malformed after the client's retry) costs this round only: the
                # statements already verified stay, and the unverified ones are tried again.
                backups = [*to_verify, *backups]
                logger.warning("quiz {} ({}): round {} lost: {}", source.id, difficulty, number, e.message)

            kept = trim(kept, n)
            round_log.rejected = [RejectedStatement(statement=d.statement, reasons=p) for d, p in rejected]
            round_log.accepted_total = len(kept)
            rounds.append(round_log)
            logger.info(
                "quiz {} ({}): round {} kept {}/{}, rejected {}, waiting {}",
                source.id,
                difficulty,
                number,
                len(kept),
                n,
                len(rejected),
                len(backups),
            )
            if is_complete(kept, n):
                return build_quiz(source.id, source.topic, difficulty, kept, rounds, self._rng, self._clock.now())
            feedback = round_log.rejected
        raise QuizGenerationException(
            f"no s'ha pogut generar un qüestionari verificat de {n} afirmacions després de {number} rondes"
        )

    async def _write(
        self,
        source: QuizSource,
        difficulty: Difficulty,
        n: int,
        kept: list[StatementDraft],
        to_verify: list[StatementDraft],
        backups: list[StatementDraft],
        k: int,
        feedback: list[RejectedStatement],
        refs: set[TheoryItemId],
    ) -> "_Written":
        """Asks the writer for `k` statements and keeps the ones that pass the code validation and sympy."""
        pending = [*kept, *to_verify]
        false_min, false_max = batch_false_bounds(n, pending, k)
        batch = await self._writer.write(
            source,
            BatchRequest(
                difficulty=difficulty,
                count=k,
                false_min=false_min,
                false_max=false_max,
                kept=[*pending, *backups],
                rejected=feedback,
            ),
        )
        drafts = batch.drafts[: k + 2]
        rejected: list[tuple[StatementDraft, list[str]]] = []
        seen = {normal_key(d.statement) for d in (*pending, *backups)}
        candidates: list[StatementDraft] = []
        for d in drafts:
            problems = validate_draft(d, refs)
            key = normal_key(d.statement)
            if key in seen:
                problems.append("repeteix una afirmació que ja hi és")
            seen.add(key)
            if problems:
                rejected.append((d, problems))
            else:
                candidates.append(d)
        if candidates:
            results = await asyncio.to_thread(self._checks.evaluate, all_checks(candidates))
            failures = [(d, check_problems(d)) for d in with_results(candidates, results)]
            rejected += [(d, p) for d, p in failures if p]
            candidates = [d for d, p in failures if not p]
        return _Written(candidates=candidates, rejected=rejected, received=len(drafts), call=batch.call)

    async def _verify(self, source: QuizSource, drafts: list[StatementDraft], number: int) -> "_Verified":
        solved, audited = await asyncio.gather(self._solver.solve(source, drafts), self._auditor.audit(source, drafts))
        verdicts = judge(drafts, solved.answers, audited.reviews)
        by_num = {a.num: a for a in solved.answers}
        out = _Verified(solver=solved.call, audit=audited.call)
        for i, (d, problems) in enumerate(zip(drafts, verdicts, strict=True), 1):
            if problems:
                out.rejected.append((d, problems))
                continue
            s = by_num.get(i)
            verification = StatementVerification(
                solver_justification=s.justification if s else "",
                confidence=s.confidence if s else "",
                round=number,
            )
            out.accepted.append(d.model_copy(update={"verification": verification}))
        return out


@dataclass
class _Written:
    candidates: list[StatementDraft]
    rejected: list[tuple[StatementDraft, list[str]]]
    received: int
    call: CallSummary


@dataclass
class _Verified:
    solver: CallSummary
    audit: CallSummary
    accepted: list[StatementDraft] = field(default_factory=list)
    rejected: list[tuple[StatementDraft, list[str]]] = field(default_factory=list)
