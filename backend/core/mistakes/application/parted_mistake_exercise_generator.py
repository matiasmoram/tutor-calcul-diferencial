import asyncio
import random

from loguru import logger
from pydantic import BaseModel

from core.mistakes.application.mistake_exercise_generator import GENERATION_DEADLINE_S, MAX_ATTEMPTS
from core.mistakes.domain.entities.mistake_exercise import DeclaredMistake, GenerationAttempt, Verification
from core.mistakes.domain.entities.parted_mistake_exercise import MistakePart, PartedMistakeExercise
from core.mistakes.domain.exceptions import MistakeGenerationFailedException, MistakeGenerationTimeoutException
from core.mistakes.domain.ports import PartCorrupter, PartVerifier, ResolutionVerifier, ResolutionWriter
from core.mistakes.domain.services.corruption_plan import CorruptionPlan, plan_corruptions
from core.mistakes.domain.services.part_checks import (
    check_corruption,
    check_resolution,
    part_verification_problems,
    require_parts,
    resolution_verification_problems,
)
from core.mistakes.domain.values.difficulty import MISTAKES_PER_DIFFICULTY, Difficulty
from core.mistakes.domain.values.mistake_exercise_id import MistakeExerciseId
from core.mistakes.domain.values.mistake_source import MistakeSource, TheorySource
from core.mistakes.domain.values.resolution import Resolution
from core.shared.domain.clock import Clock


class _FlawedPart(BaseModel):
    part: int
    flawed_fragments: list[str]
    mistake: DeclaredMistake
    verification: Verification


class PartedMistakeExerciseGenerator:
    """A "per_parts" document: the correct resolution first (stage A: write, code gates, blind check), then k parts
    chosen by code, each given one local error (stage B: edits, code gates) checked blind (stage C). The k parts are
    corrupted in parallel, each from the correct text, so their errors never compound. A part that keeps failing is
    swapped for an unused one; theory's statement (part 1) is always one of the k and is never swapped."""

    def __init__(
        self,
        writer: ResolutionWriter,
        resolution_verifier: ResolutionVerifier,
        corrupter: PartCorrupter,
        part_verifier: PartVerifier,
        clock: Clock,
        rng: random.Random | None = None,
        deadline_s: float = GENERATION_DEADLINE_S,
    ) -> None:
        self._writer = writer
        self._resolution_verifier = resolution_verifier
        self._corrupter = corrupter
        self._part_verifier = part_verifier
        self._clock = clock
        self._rng = rng or random.Random()
        self._deadline_s = deadline_s

    async def generate(self, source: MistakeSource, difficulty: Difficulty) -> PartedMistakeExercise:
        require_parts(source)
        deadline = asyncio.timeout(self._deadline_s)
        try:
            async with deadline:
                return await self._generate(source, difficulty)
        except TimeoutError:
            if not deadline.expired():
                raise
            raise MistakeGenerationTimeoutException(self._deadline_s) from None

    async def _generate(self, source: MistakeSource, difficulty: Difficulty) -> PartedMistakeExercise:
        resolution, verification = await self._resolution(source)
        chosen, reserve = self._choose(source, len(resolution.parts), difficulty)
        # Decided before the chains run in parallel: each corrupter prefers a distinct kind.
        plans = plan_corruptions(self._rng, chosen, isinstance(source, TheorySource))
        try:
            async with asyncio.TaskGroup() as group:
                tasks = [
                    group.create_task(
                        self._flawed_part(
                            source,
                            resolution,
                            difficulty,
                            part,
                            reserve,
                            swappable=not _is_statement(source, part),
                            plan=plans[part],
                        )
                    )
                    for part in chosen
                ]
        except ExceptionGroup as e:
            # One chain failed and the others were cancelled: its exception is the generation's.
            raise e.exceptions[0] from None
        flawed = {t.result().part: t.result() for t in tasks}
        parts: list[MistakePart] = []
        for i, p in enumerate(resolution.parts, 1):
            f = flawed.get(i)
            if f is None:
                parts.append(MistakePart(title=p.title, step=p.step, fragments=p.fragments))
                continue
            mistake_id = f"e{sum(1 for q in parts if q.mistake is not None) + 1}"
            parts.append(
                MistakePart(
                    title=p.title,
                    step=p.step,
                    fragments=p.fragments,
                    flawed_fragments=f.flawed_fragments,
                    mistake=f.mistake.model_copy(update={"id": mistake_id}),
                    verification=f.verification,
                )
            )
        now = self._clock.now()
        return PartedMistakeExercise(
            id=MistakeExerciseId.new(resolution.fragments, now),
            source_id=source.id,
            source_kind=source.kind,
            difficulty=difficulty,
            statement_fragments=resolution.statement_fragments,
            parts=parts,
            verification=verification,
            created_at=now,
        )

    async def _resolution(self, source: MistakeSource) -> tuple[Resolution, Verification]:
        """Stage A, regenerating with the reasons."""
        rejections: list[str] = []
        attempts: list[GenerationAttempt] = []
        failures: list[str] = []
        for attempt in range(1, MAX_ATTEMPTS + 1):
            draft, generation_call = await self._writer.write(source, rejections)
            check = check_resolution(draft, source)
            if not check.valid:
                attempts.append(
                    GenerationAttempt(attempt=attempt, generation=generation_call, validation=check.problems)
                )
                rejections = check.problems
                failures += _reasons("resolució", attempt, rejections)
                continue
            report, verification_call = await self._resolution_verifier.verify(source, check.resolution)
            issues = resolution_verification_problems(check.resolution, report, isinstance(source, TheorySource))
            attempts.append(
                GenerationAttempt(
                    attempt=attempt,
                    generation=generation_call,
                    validation=check.problems,
                    verification=verification_call,
                    verifier_findings=report.findings,
                    discrepancies=issues,
                )
            )
            if issues:
                rejections = issues
                failures += _reasons("resolució", attempt, rejections)
                continue
            return check.resolution, Verification(
                origin="llm", assessment=report.assessment, findings=report.findings, attempts=attempts
            )
        raise MistakeGenerationFailedException(MAX_ATTEMPTS, failures)

    def _choose(self, source: MistakeSource, n_parts: int, difficulty: Difficulty) -> tuple[list[int], list[int]]:
        """The k parts to corrupt, and the unused ones in the order a failing part is swapped for them."""
        k = min(MISTAKES_PER_DIFFICULTY[difficulty], n_parts)
        if isinstance(source, TheorySource):
            proof = list(range(2, n_parts + 1))
            self._rng.shuffle(proof)
            return [1, *proof[: k - 1]], proof[k - 1 :]
        parts = list(range(1, n_parts + 1))
        self._rng.shuffle(parts)
        return parts[:k], parts[k:]

    async def _flawed_part(
        self,
        source: MistakeSource,
        resolution: Resolution,
        difficulty: Difficulty,
        part: int,
        reserve: list[int],
        swappable: bool,
        plan: CorruptionPlan,
    ) -> _FlawedPart:
        """One chosen part's error; `reserve` is shared by the k chains."""
        failures: list[str] = []
        while True:
            flawed = await self._corrupt(source, resolution, difficulty, part, reserve, swappable, plan, failures)
            if flawed is not None:
                return flawed
            if not swappable or not reserve:
                raise MistakeGenerationFailedException(MAX_ATTEMPTS, failures)
            logger.info("mistakes: part {} of {} failed, trying part {}", part, source.id, reserve[0])
            part = reserve.pop(0)

    async def _corrupt(
        self,
        source: MistakeSource,
        resolution: Resolution,
        difficulty: Difficulty,
        part: int,
        reserve: list[int],
        swappable: bool,
        plan: CorruptionPlan,
        failures: list[str],
    ) -> _FlawedPart | None:
        """Stages B and C on one part, retried with the reasons; None when the part gives no verified error. A part
        answered unfit is given up at once only when it can be swapped; otherwise that answer is a rejected attempt."""
        clean = resolution.parts[part - 1]
        first = resolution.first_fragment(part)
        theory = isinstance(source, TheorySource)
        rejections: list[str] = []
        attempts: list[GenerationAttempt] = []
        for attempt in range(1, MAX_ATTEMPTS + 1):
            draft, generation_call = await self._corrupter.corrupt(
                source, resolution, part, difficulty, rejections, plan
            )
            # Read after the call: the other chains may have used the reserve up meanwhile.
            required = not (swappable and reserve)
            check = check_corruption(clean.fragments, draft, first, "e1", theory, required)
            if check.unfit:
                failures.append(f"part {part}: la part no és apta per a un error")
                return None
            if check.mistake is None:
                attempts.append(
                    GenerationAttempt(attempt=attempt, generation=generation_call, validation=check.problems)
                )
                rejections = check.problems
                failures += _reasons(f"part {part}", attempt, rejections)
                continue
            shown = clean.model_copy(update={"fragments": check.flawed_fragments})
            report, verification_call = await self._part_verifier.verify(source, resolution.parts[: part - 1], shown)
            issues = part_verification_problems(check.mistake, first, check.flawed_fragments, report)
            attempts.append(
                GenerationAttempt(
                    attempt=attempt,
                    generation=generation_call,
                    validation=check.problems,
                    verification=verification_call,
                    verifier_findings=report.findings,
                    discrepancies=issues,
                )
            )
            if issues:
                rejections = issues
                failures += _reasons(f"part {part}", attempt, rejections)
                continue
            return _FlawedPart(
                part=part,
                flawed_fragments=check.flawed_fragments,
                mistake=check.mistake,
                verification=Verification(
                    origin="llm", assessment=report.assessment, findings=report.findings, attempts=attempts
                ),
            )
        return None


def _reasons(stage: str, attempt: int, rejections: list[str]) -> list[str]:
    return [f"{stage}, intent {attempt}: {r}" for r in rejections]


def _is_statement(source: MistakeSource, part: int) -> bool:
    return isinstance(source, TheorySource) and part == 1
