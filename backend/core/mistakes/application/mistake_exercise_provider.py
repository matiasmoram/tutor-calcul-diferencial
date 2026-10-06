import random

from pydantic import BaseModel

from core.mistakes.application.mistake_exercise_generator import MistakeExerciseGenerator
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.repository import MistakeExerciseRepository
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.mistake_source import MistakeSource


class ProvidedMistakeExercise(BaseModel):
    exercise: MistakeExercise
    freshly_generated: bool


class MistakeExerciseProvider:
    """A ready document of the source and difficulty, or a new one generated (and stored) when there is none."""

    def __init__(
        self,
        exercises: MistakeExerciseRepository,
        generator: MistakeExerciseGenerator,
        rng: random.Random | None = None,
    ) -> None:
        self._exercises = exercises
        self._generator = generator
        self._rng = rng or random.Random()

    async def has_ready(self, source: MistakeSource, difficulty: Difficulty) -> bool:
        """Whether `get_or_generate(..., fresh=False)` can answer without calling the model."""
        return bool(await self._exercises.of_source(source.id, difficulty))

    async def get_or_generate(
        self, source: MistakeSource, difficulty: Difficulty, fresh: bool = False, avoid: str | None = None
    ) -> ProvidedMistakeExercise:
        """`fresh`: always generate a new one. `avoid`: a document id not to repeat when the pool has others
        ("another one" without generating)."""
        pool = [] if fresh else await self._exercises.of_source(source.id, difficulty)
        if len(pool) > 1 and avoid:
            pool = [e for e in pool if e.id != avoid] or pool
        if pool:
            return ProvidedMistakeExercise(exercise=self._rng.choice(pool), freshly_generated=False)
        exercise = await self._generator.generate(source, difficulty)
        await self._exercises.save(exercise)
        return ProvidedMistakeExercise(exercise=exercise, freshly_generated=True)
