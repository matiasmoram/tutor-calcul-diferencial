import random

from pydantic import BaseModel

from core.mistakes.application.mistake_exercise_generator import MistakeExerciseGenerator
from core.mistakes.application.parted_mistake_exercise_generator import PartedMistakeExerciseGenerator
from core.mistakes.domain.entities.parted_mistake_exercise import MistakeDocument
from core.mistakes.domain.exceptions import MistakeExerciseNotReadyException
from core.mistakes.domain.repository import MistakeExerciseRepository
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.layout import Layout
from core.mistakes.domain.values.mistake_source import MistakeSource
from core.shared.domain.single_flight import SingleFlight

type MistakeGenerations = SingleFlight[tuple[str, str, Difficulty, Layout], MistakeDocument]


class ProvidedMistakeExercise(BaseModel):
    exercise: MistakeDocument
    generated_now: bool


class MistakeExerciseProvider:
    """A ready document of the source, difficulty and layout, or a new one generated (and stored) when there is
    none.

    `may_generate` is the cost policy: without it, `fresh` only picks another ready document, and a source and
    difficulty with none ready is a MistakeExerciseNotReadyException. `generations` is shared by the whole process, so
    concurrent requests for the same source, difficulty and layout wait for one generation instead of paying for
    several. Without `parted_generator`, "per_parts" documents are served from the ready ones only."""

    def __init__(
        self,
        exercises: MistakeExerciseRepository,
        generator: MistakeExerciseGenerator,
        rng: random.Random | None = None,
        generations: MistakeGenerations | None = None,
        may_generate: bool = True,
        parted_generator: PartedMistakeExerciseGenerator | None = None,
    ) -> None:
        self._exercises = exercises
        self._generator = generator
        self._rng = rng or random.Random()
        self._generations: MistakeGenerations = generations if generations is not None else SingleFlight()
        self._may_generate = may_generate
        self._parted_generator = parted_generator

    async def is_ready(self, source: MistakeSource, difficulty: Difficulty, layout: Layout = "sencer") -> bool:
        """Whether a document can be served without calling the model."""
        return bool(await self._exercises.of_source(source.id, difficulty, layout))

    async def will_generate(
        self, source: MistakeSource, difficulty: Difficulty, fresh: bool = False, layout: Layout = "sencer"
    ) -> bool:
        """Whether `get_or_generate` will call the model (the API checks the provider key first)."""
        if not self._can_generate(layout):
            return False
        return fresh or not await self.is_ready(source, difficulty, layout)

    async def get_or_generate(
        self,
        source: MistakeSource,
        difficulty: Difficulty,
        fresh: bool = False,
        avoid_id: str | None = None,
        layout: Layout = "sencer",
    ) -> ProvidedMistakeExercise:
        """`fresh`: always generate a new one. `avoid_id`: a document not to repeat when the pool has others
        ("another one" without generating)."""
        fresh = fresh and self._can_generate(layout)
        pool = [] if fresh else await self._exercises.of_source(source.id, difficulty, layout)
        if len(pool) > 1 and avoid_id:
            pool = [e for e in pool if e.id != avoid_id] or pool
        if pool:
            return ProvidedMistakeExercise(exercise=self._rng.choice(pool), generated_now=False)
        if not self._can_generate(layout):
            raise MistakeExerciseNotReadyException(source.id, difficulty)
        key = (source.kind, str(source.id), difficulty, layout)
        exercise = await self._generations.run(key, lambda: self._generate(source, difficulty, layout))
        return ProvidedMistakeExercise(exercise=exercise, generated_now=True)

    def _can_generate(self, layout: Layout) -> bool:
        return self._may_generate and (layout == "sencer" or self._parted_generator is not None)

    async def _generate(self, source: MistakeSource, difficulty: Difficulty, layout: Layout) -> MistakeDocument:
        exercise: MistakeDocument
        if layout == "sencer":
            exercise = await self._generator.generate(source, difficulty)
        elif self._parted_generator is not None:
            exercise = await self._parted_generator.generate(source, difficulty)
        else:
            raise MistakeExerciseNotReadyException(source.id, difficulty)
        await self._exercises.save(exercise)
        return exercise
