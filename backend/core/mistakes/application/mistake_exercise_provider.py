import random

from pydantic import BaseModel

from core.mistakes.application.mistake_exercise_generator import MistakeExerciseGenerator
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.exceptions import MistakeExerciseNotReadyException
from core.mistakes.domain.repository import MistakeExerciseRepository
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.mistake_source import MistakeSource
from core.shared.domain.single_flight import SingleFlight

type MistakeGenerations = SingleFlight[tuple[str, str, Difficulty], MistakeExercise]


class ProvidedMistakeExercise(BaseModel):
    exercise: MistakeExercise
    generated_now: bool


class MistakeExerciseProvider:
    """A ready document of the source and difficulty, or a new one generated (and stored) when there is none.

    `may_generate` is the cost policy: without it, `fresh` only picks another ready document, and a source and
    difficulty with none ready is a MistakeExerciseNotReadyException. `generations` is shared by the whole process, so
    concurrent requests for the same source and difficulty wait for one generation instead of paying for several."""

    def __init__(
        self,
        exercises: MistakeExerciseRepository,
        generator: MistakeExerciseGenerator,
        rng: random.Random | None = None,
        generations: MistakeGenerations | None = None,
        may_generate: bool = True,
    ) -> None:
        self._exercises = exercises
        self._generator = generator
        self._rng = rng or random.Random()
        self._generations: MistakeGenerations = generations if generations is not None else SingleFlight()
        self._may_generate = may_generate

    async def is_ready(self, source: MistakeSource, difficulty: Difficulty) -> bool:
        """Whether a document can be served without calling the model."""
        return bool(await self._exercises.of_source(source.id, difficulty))

    async def will_generate(self, source: MistakeSource, difficulty: Difficulty, fresh: bool = False) -> bool:
        """Whether `get_or_generate` will call the model (the API checks the provider key first)."""
        if not self._may_generate:
            return False
        return fresh or not await self.is_ready(source, difficulty)

    async def get_or_generate(
        self, source: MistakeSource, difficulty: Difficulty, fresh: bool = False, avoid_id: str | None = None
    ) -> ProvidedMistakeExercise:
        """`fresh`: always generate a new one. `avoid_id`: a document not to repeat when the pool has others
        ("another one" without generating)."""
        fresh = fresh and self._may_generate
        pool = [] if fresh else await self._exercises.of_source(source.id, difficulty)
        if len(pool) > 1 and avoid_id:
            pool = [e for e in pool if e.id != avoid_id] or pool
        if pool:
            return ProvidedMistakeExercise(exercise=self._rng.choice(pool), generated_now=False)
        if not self._may_generate:
            raise MistakeExerciseNotReadyException(source.id, difficulty)
        key = (source.kind, str(source.id), difficulty)
        exercise = await self._generations.run(key, lambda: self._generate(source, difficulty))
        return ProvidedMistakeExercise(exercise=exercise, generated_now=True)

    async def _generate(self, source: MistakeSource, difficulty: Difficulty) -> MistakeExercise:
        exercise = await self._generator.generate(source, difficulty)
        await self._exercises.save(exercise)
        return exercise
