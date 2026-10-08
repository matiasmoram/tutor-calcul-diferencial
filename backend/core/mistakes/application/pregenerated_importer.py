from core.mistakes.domain.ports import GeneratedMistakesSource
from core.mistakes.domain.repository import MistakeExerciseRepository


class PregeneratedImporter:
    """Loads the documents generated offline into the database (idempotent: same id, same row)."""

    def __init__(self, source: GeneratedMistakesSource, exercises: MistakeExerciseRepository) -> None:
        self._source = source
        self._exercises = exercises

    async def import_all(self) -> int:
        documents = self._source.load()
        for exercise in documents:
            await self._exercises.save(exercise)
        return len(documents)
