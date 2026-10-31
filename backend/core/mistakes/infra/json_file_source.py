from pathlib import Path

from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.ports import GeneratedMistakesSource


class JsonFileMistakeSource(GeneratedMistakesSource):
    """Documents as JSON files, ``<directory>/<source id>/<difficulty>/<id>.json`` (``backend/generats/errades``).
    Written by the offline scripts and committed; the database is seeded from them."""

    def __init__(self, directory: Path) -> None:
        self._directory = directory

    def load(self) -> list[MistakeExercise]:
        return [
            MistakeExercise.model_validate_json(p.read_text(encoding="utf-8"))
            for p in sorted(self._directory.glob("*/*/*.json"))
        ]

    def save(self, exercise: MistakeExercise) -> Path:
        d = self._directory / exercise.source_id / exercise.difficulty
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"{exercise.id}.json"
        path.write_text(exercise.model_dump_json(indent=2), encoding="utf-8")
        return path
