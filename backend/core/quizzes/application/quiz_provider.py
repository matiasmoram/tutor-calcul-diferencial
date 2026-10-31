from random import Random

from pydantic import BaseModel

from core.quizzes.application.quiz_generator import QuizGenerator
from core.quizzes.domain.entities.quiz import Quiz
from core.quizzes.domain.exceptions import QuizNotReadyException
from core.quizzes.domain.repository import QuizRepository
from core.quizzes.domain.values.difficulty import Difficulty
from core.quizzes.domain.values.quiz_source import QuizSource
from core.shared.domain.single_flight import SingleFlight

type QuizGenerations = SingleFlight[tuple[str, Difficulty], Quiz]


class ProvidedQuiz(BaseModel):
    quiz: Quiz
    generated_now: bool


class QuizProvider:
    """A stored quiz of the source and difficulty when there is one; otherwise a new one, generated and stored.

    `may_generate` is the cost policy: without it, `fresh` only picks another stored quiz, and a source and difficulty
    with nothing stored is a QuizNotReadyException. `generations` is shared by the whole process, so concurrent
    requests for the same source and difficulty wait for one generation instead of paying for several."""

    def __init__(
        self,
        quizzes: QuizRepository,
        generator: QuizGenerator,
        rng: Random,
        generations: QuizGenerations | None = None,
        may_generate: bool = True,
    ) -> None:
        self._quizzes = quizzes
        self._generator = generator
        self._rng = rng
        self._generations: QuizGenerations = generations if generations is not None else SingleFlight()
        self._may_generate = may_generate

    async def get_or_generate(
        self, source: QuizSource, difficulty: Difficulty, fresh: bool = False, avoid_id: str | None = None
    ) -> ProvidedQuiz:
        """`fresh` forces a generation; `avoid_id` (the quiz just seen) is avoided when there is another one."""
        fresh = fresh and self._may_generate
        pool = [] if fresh else await self._quizzes.of_source(source.id, difficulty)
        if len(pool) > 1 and avoid_id:
            pool = [q for q in pool if q.id != avoid_id] or pool
        if pool:
            return ProvidedQuiz(quiz=self._rng.choice(pool), generated_now=False)
        if not self._may_generate:
            raise QuizNotReadyException(source.id, difficulty)
        quiz = await self._generations.run((source.id, difficulty), lambda: self._generate(source, difficulty))
        return ProvidedQuiz(quiz=quiz, generated_now=True)

    async def needs_generation(self, source: QuizSource, difficulty: Difficulty, fresh: bool = False) -> bool:
        """Whether `get_or_generate` will call the model."""
        if not self._may_generate:
            return False
        return fresh or not await self.is_ready(source, difficulty)

    async def is_ready(self, source: QuizSource, difficulty: Difficulty) -> bool:
        """Whether a quiz can be served without calling the model."""
        return bool(await self._quizzes.of_source(source.id, difficulty))

    async def _generate(self, source: QuizSource, difficulty: Difficulty) -> Quiz:
        quiz = await self._generator.generate(source, difficulty)
        await self._quizzes.save(quiz)
        return quiz
