from random import Random

from pydantic import BaseModel

from core.quizzes.application.quiz_generator import QuizGenerator
from core.quizzes.domain.entities.quiz import Quiz
from core.quizzes.domain.repository import QuizRepository
from core.quizzes.domain.sources import QuizSource
from core.quizzes.domain.values.difficulty import Difficulty


class ProvidedQuiz(BaseModel):
    quiz: Quiz
    generated_now: bool


class QuizProvider:
    """A stored quiz of the source and difficulty when there is one; otherwise a new one, generated and stored."""

    def __init__(self, quizzes: QuizRepository, generator: QuizGenerator, rng: Random) -> None:
        self._quizzes = quizzes
        self._generator = generator
        self._rng = rng

    async def get_or_generate(
        self, source: QuizSource, difficulty: Difficulty, new: bool = False, except_id: str | None = None
    ) -> ProvidedQuiz:
        """`new` forces a generation; `except_id` (the quiz just seen) is avoided when there is another one."""
        pool = [] if new else await self._quizzes.of_source(source.id, difficulty)
        if len(pool) > 1 and except_id:
            pool = [q for q in pool if q.id != except_id] or pool
        if pool:
            return ProvidedQuiz(quiz=self._rng.choice(pool), generated_now=False)
        quiz = await self._generator.generate(source, difficulty)
        await self._quizzes.add(quiz)
        return ProvidedQuiz(quiz=quiz, generated_now=True)

    async def is_ready(self, source: QuizSource, difficulty: Difficulty) -> bool:
        """Whether a quiz can be served without calling the model."""
        return bool(await self._quizzes.of_source(source.id, difficulty))
