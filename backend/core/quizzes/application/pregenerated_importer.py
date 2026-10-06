from core.quizzes.domain.ports import PregeneratedQuizSource
from core.quizzes.domain.repository import QuizRepository


class PregeneratedImporter:
    """Loads the quizzes generated offline into the store (on startup; re-running it is harmless)."""

    def __init__(self, source: PregeneratedQuizSource, quizzes: QuizRepository) -> None:
        self._source = source
        self._quizzes = quizzes

    async def import_all(self) -> int:
        quizzes = self._source.load_all()
        for quiz in quizzes:
            await self._quizzes.add(quiz)
        return len(quizzes)
