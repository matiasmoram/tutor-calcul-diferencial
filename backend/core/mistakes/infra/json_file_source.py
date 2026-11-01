from pathlib import Path

from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.entities.parted_mistake_exercise import MISTAKE_DOCUMENT_ADAPTER, MistakeDocument
from core.mistakes.domain.ports import PregeneratedMistakeSource


class JsonFileMistakeSource(PregeneratedMistakeSource):
    """Documents as JSON files, ``<directory>/<source id>/<difficulty>/<id>.json`` (``backend/generats/errades``),
    both layouts in the same tree. Written by the offline scripts and committed; the database is seeded from them."""

    def __init__(self, directory: Path) -> None:
        self._directory = directory

    def load_all(self) -> list[MistakeDocument]:
        return [
            MISTAKE_DOCUMENT_ADAPTER.validate_json(p.read_text(encoding="utf-8"))
            for p in sorted(self._directory.glob("*/*/*.json"))
        ]

    def load(self) -> list[MistakeExercise]:
        """The "sencer" documents only."""
        return [d for d in self.load_all() if isinstance(d, MistakeExercise)]

    def save(self, exercise: MistakeDocument) -> Path:
        d = self._directory / exercise.source_id / exercise.difficulty
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"{exercise.id}.json"
        path.write_text(exercise.model_dump_json(indent=2), encoding="utf-8")
        return path
