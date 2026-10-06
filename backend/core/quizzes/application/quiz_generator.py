import asyncio
from random import Random

from loguru import logger

from core.quizzes.domain.entities.quiz import GenerationRound, Quiz, RejectedStatement
from core.quizzes.domain.entities.statement import StatementVerification
from core.quizzes.domain.exceptions import QuizGenerationException
from core.quizzes.domain.ports import BlindSolver, CheckEvaluator, QuizAuditor, QuizWriter
from core.quizzes.domain.services.assembly import build_quiz
from core.quizzes.domain.services.balance import BATCH_SIZE, batch_false_bounds, is_complete, max_rounds, trim
from core.quizzes.domain.services.judging import judge
from core.quizzes.domain.services.validation import (
    all_checks,
    check_problems,
    normal_key,
    validate_draft,
    with_results,
)
from core.quizzes.domain.sources import QuizSource
from core.quizzes.domain.values.difficulty import QUIZ_SIZES, Difficulty
from core.quizzes.domain.values.drafts import BatchRequest, StatementDraft
from core.shared.domain.clock import Clock


class QuizGenerator:
    """Builds a verified quiz in batches: the writer proposes, code validates and runs the sympy checks, a blind
    solver and an auditor verify in parallel, and code decides. Rejected statements are replaced (not the whole
    quiz), with the reasons, in a few extra rounds."""

    def __init__(
        self,
        writer: QuizWriter,
        solver: BlindSolver,
        auditor: QuizAuditor,
        checks: CheckEvaluator,
        clock: Clock,
        rng: Random,
    ) -> None:
        self._writer = writer
        self._solver = solver
        self._auditor = auditor
        self._checks = checks
        self._clock = clock
        self._rng = rng

    async def generate(self, source: QuizSource, difficulty: Difficulty) -> Quiz:
        n = QUIZ_SIZES[difficulty]
        refs = set(source.allowed_refs)
        kept: list[StatementDraft] = []
        feedback: list[RejectedStatement] = []
        rounds: list[GenerationRound] = []
        last_round = max_rounds(n)
        for number in range(1, last_round + 1):
            k = min(BATCH_SIZE, n - len(kept))
            false_min, false_max = batch_false_bounds(n, kept, k)
            batch = await self._writer.write(
                source,
                BatchRequest(
                    difficulty=difficulty,
                    count=k,
                    false_min=false_min,
                    false_max=false_max,
                    kept=kept,
                    rejected=feedback,
                ),
            )
            drafts = batch.drafts[: k + 2]
            rejected: list[tuple[StatementDraft, list[str]]] = []

            seen = {normal_key(d.statement) for d in kept}
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

            round_log = GenerationRound(round=number, requested=k, received=len(drafts), generation=batch.call)
            if candidates:
                solved, audited = await asyncio.gather(
                    self._solver.solve(source, candidates), self._auditor.audit(source, candidates)
                )
                verdicts = judge(candidates, solved.answers, audited.reviews)
                by_num = {a.num: a for a in solved.answers}
                for i, (d, problems) in enumerate(zip(candidates, verdicts, strict=True), 1):
                    if problems:
                        rejected.append((d, problems))
                        continue
                    s = by_num.get(i)
                    verification = StatementVerification(
                        solver_justification=s.justification if s else "",
                        confidence=s.confidence if s else "",
                        round=number,
                    )
                    kept.append(d.model_copy(update={"verification": verification}))
                round_log.solver, round_log.audit = solved.call, audited.call

            kept = trim(kept, n)
            round_log.rejected = [RejectedStatement(statement=d.statement, reasons=p) for d, p in rejected]
            round_log.accepted_total = len(kept)
            rounds.append(round_log)
            logger.info(
                "quiz {} ({}): round {} kept {}/{}, rejected {}",
                source.id,
                difficulty,
                number,
                len(kept),
                n,
                len(rejected),
            )
            if is_complete(kept, n):
                return build_quiz(source.id, source.topic, difficulty, kept, rounds, self._rng, self._clock.now())
            feedback = round_log.rejected
        raise QuizGenerationException(
            f"no s'ha pogut generar un qüestionari verificat de {n} afirmacions després de {last_round} rondes"
        )
