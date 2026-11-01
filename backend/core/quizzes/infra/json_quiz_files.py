"""Quizzes generated offline (scripts), one JSON document per quiz: ``<dir>/<source id>/<difficulty>/<id>.json``.
They seed the quiz store; at run time the database is the store."""

from pathlib import Path

from core.quizzes.domain.entities.quiz import Quiz
from core.quizzes.domain.ports import PregeneratedQuizSource


class JsonQuizFiles(PregeneratedQuizSource):
    def __init__(self, directory: Path) -> None:
        self._directory = directory

    def load_all(self) -> list[Quiz]:
        return [Quiz.model_validate_json(p.read_text(encoding="utf-8")) for p in self.paths()]

    def paths(self) -> list[Path]:
        return sorted(self._directory.glob("*/*/*.json"))

    def save(self, quiz: Quiz) -> Path:
        folder = self._directory / quiz.source_id / quiz.difficulty
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{quiz.id}.json"
        path.write_text(quiz.model_dump_json(indent=2), encoding="utf-8")
        return path
