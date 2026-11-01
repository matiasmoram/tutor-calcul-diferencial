import asyncio

from core.mistakes.domain.entities.mistake_exercise import GenerationAttempt, MistakeExercise, Verification
from core.mistakes.domain.exceptions import MistakeGenerationFailedException, MistakeGenerationTimeoutException
from core.mistakes.domain.ports import MistakeGenerator, MistakeVerifier
from core.mistakes.domain.services.generation_checks import compare_verification, validate_generation
from core.mistakes.domain.values.difficulty import MISTAKES_PER_DIFFICULTY, Difficulty
from core.mistakes.domain.values.mistake_exercise_id import MistakeExerciseId
from core.mistakes.domain.values.mistake_source import MistakeSource, TheorySource
from core.shared.domain.clock import Clock

MAX_ATTEMPTS = 3
# A request must not hang for tens of minutes: past this the generation fails (the attempts paid are in the call log).
GENERATION_DEADLINE_S = 300.0


class MistakeExerciseGenerator:
    """Generate → validate (code) → verify (blind model pass + code comparison), regenerating with the reasons."""

    def __init__(
        self,
        generator: MistakeGenerator,
        verifier: MistakeVerifier,
        clock: Clock,
        deadline_s: float = GENERATION_DEADLINE_S,
    ) -> None:
        self._generator = generator
        self._verifier = verifier
        self._clock = clock
        self._deadline_s = deadline_s

    async def generate(self, source: MistakeSource, difficulty: Difficulty) -> MistakeExercise:
        deadline = asyncio.timeout(self._deadline_s)
        try:
            async with deadline:
                return await self._generate(source, difficulty)
        except TimeoutError:
            if not deadline.expired():
                raise
            raise MistakeGenerationTimeoutException(self._deadline_s) from None

    async def _generate(self, source: MistakeSource, difficulty: Difficulty) -> MistakeExercise:
        theory = isinstance(source, TheorySource)
        n = MISTAKES_PER_DIFFICULTY[difficulty]
        rejections: list[str] = []
        attempts: list[GenerationAttempt] = []
        for attempt in range(1, MAX_ATTEMPTS + 1):
            draft, generation_call = await self._generator.generate(source, difficulty, rejections)
            check = validate_generation(draft, n, theory)
            if not check.valid:
                attempts.append(
                    GenerationAttempt(attempt=attempt, generation=generation_call, validation=check.problems)
                )
                rejections = check.problems
                continue

            report, verification_call = await self._verifier.verify(source, check.fragments, check.statement_fragments)
            issues = compare_verification(check.mistakes, report.findings, check.fragments)
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
                continue

            now = self._clock.now()
            return MistakeExercise(
                id=MistakeExerciseId.new(check.fragments, now),
                source_id=source.id,
                source_kind=source.kind,
                difficulty=difficulty,
                fragments=check.fragments,
                statement_fragments=check.statement_fragments,
                mistakes=check.mistakes,
                verification=Verification(
                    origin="llm", assessment=report.assessment, findings=report.findings, attempts=attempts
                ),
                created_at=now,
            )
        raise MistakeGenerationFailedException(MAX_ATTEMPTS)
