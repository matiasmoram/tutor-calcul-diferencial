import random

from pydantic import BaseModel

from core.mistakes.application.mistake_exercise_generator import MistakeExerciseGenerator
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
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

    `generations` is shared by the whole process, so concurrent requests for the same source and difficulty wait for
    one generation instead of paying for several."""

    def __init__(
        self,
        exercises: MistakeExerciseRepository,
        generator: MistakeExerciseGenerator,
        rng: random.Random | None = None,
        generations: MistakeGenerations | None = None,
    ) -> None:
        self._exercises = exercises
        self._generator = generator
        self._rng = rng or random.Random()
        self._generations: MistakeGenerations = generations if generations is not None else SingleFlight()

    async def is_ready(self, source: MistakeSource, difficulty: Difficulty) -> bool:
        """Whether `get_or_generate(..., fresh=False)` can answer without calling the model."""
        return bool(await self._exercises.of_source(source.id, difficulty))

    async def get_or_generate(
        self, source: MistakeSource, difficulty: Difficulty, fresh: bool = False, avoid_id: str | None = None
    ) -> ProvidedMistakeExercise:
        """`fresh`: always generate a new one. `avoid_id`: a document not to repeat when the pool has others
        ("another one" without generating)."""
        pool = [] if fresh else await self._exercises.of_source(source.id, difficulty)
        if len(pool) > 1 and avoid_id:
            pool = [e for e in pool if e.id != avoid_id] or pool
        if pool:
            return ProvidedMistakeExercise(exercise=self._rng.choice(pool), generated_now=False)
        key = (source.kind, str(source.id), difficulty)
        exercise = await self._generations.run(key, lambda: self._generate(source, difficulty))
        return ProvidedMistakeExercise(exercise=exercise, generated_now=True)

    async def _generate(self, source: MistakeSource, difficulty: Difficulty) -> MistakeExercise:
        exercise = await self._generator.generate(source, difficulty)
        await self._exercises.save(exercise)
        return exercise
