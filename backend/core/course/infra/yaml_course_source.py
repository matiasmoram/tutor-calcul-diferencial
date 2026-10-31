"""The authored course content: one YAML file per topic for the notes (`teoria/temaN.yaml`) and for the problem
sheets (`exercicis/temaN.yaml`). The files keep their Catalan keys (they are edited by hand and validated by
scripts/check_fitxes.py); this module maps them onto the English domain entities."""

from collections.abc import Mapping
from pathlib import Path

import yaml

from core.course.domain.entities.course import Course
from core.course.domain.entities.exercise import CommonMistake, Exercise, ExpectedResult, Step
from core.course.domain.entities.problem_sheet import Problem, ProblemSheet
from core.course.domain.entities.theory_item import TheoryItem
from core.course.domain.entities.topic import Topic, TopicSection
from core.course.domain.exceptions import InvalidCourseContentException

type Raw = Mapping[str, object]


class YamlCourseSource:
    def __init__(self, exercises_dir: Path, theory_dir: Path) -> None:
        self._exercises_dir = exercises_dir
        self._theory_dir = theory_dir

    def load(self) -> Course:
        topics, theory = self._load_theory()
        sheets, exercises = self._load_sheets()
        return Course(topics=topics, theory=theory, sheets=sheets, exercises=exercises)

    def _load_theory(self) -> tuple[list[Topic], dict[str, TheoryItem]]:
        topics: list[Topic] = []
        items: dict[str, TheoryItem] = {}
        for path in sorted(self._theory_dir.glob("tema*.yaml")):
            data = _read(path)
            number = _int(data, "tema")
            sections = [TopicSection(id=str(s["id"]), title=str(s["titol"])) for s in _list(data, "seccions")]
            topics.append(Topic(number=number, title=str(data["titol"]), sections=sections))
            for raw in _list(data, "items"):
                item = _theory_item(_present(raw), number)
                if item.id in items:
                    raise InvalidCourseContentException(f"duplicate theory id {item.id} in {path}")
                items[item.id] = item
        return topics, items

    def _load_sheets(self) -> tuple[dict[str, ProblemSheet], dict[str, Exercise]]:
        sheets: dict[str, ProblemSheet] = {}
        exercises: dict[str, Exercise] = {}
        for path in sorted(self._exercises_dir.glob("*.yaml")):
            data = _read(path)
            sheet = _sheet(_present(_map(data, "llista")))
            if sheet.id in sheets:
                raise InvalidCourseContentException(f"duplicate list id {sheet.id} in {path}")
            for raw_problem in _list(data, "problemes"):
                problem = _problem(_present(raw_problem))
                for raw in _list(raw_problem, "exercicis"):
                    ex = _exercise(sheet, problem, _present(raw))
                    if ex.id in exercises:
                        raise InvalidCourseContentException(f"duplicate exercise id {ex.id} in {path}")
                    exercises[ex.id] = ex
                    problem.exercise_ids.append(ex.id)
                    sheet.exercise_ids.append(ex.id)
                sheet.problems.append(problem)
            sheets[sheet.id] = sheet
        return sheets, exercises


def _read(path: Path) -> Raw:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise InvalidCourseContentException(f"{path}: expected a mapping at the top level")
    return data


def _get(raw: Raw, key: str) -> object:
    if key not in raw:
        raise InvalidCourseContentException(f"missing key {key!r} in {dict(raw)!r:.200}")
    return raw[key]


def _int(raw: Raw, key: str) -> int:
    value = _get(raw, key)
    if not isinstance(value, int):
        raise InvalidCourseContentException(f"{key!r} must be an integer")
    return value


def _map(raw: Raw, key: str) -> Raw:
    value = _get(raw, key)
    if not isinstance(value, dict):
        raise InvalidCourseContentException(f"{key!r} must be a mapping")
    return value


def _list(raw: Raw, key: str) -> list[Raw]:
    value = raw.get(key) or []
    if not isinstance(value, list):
        raise InvalidCourseContentException(f"{key!r} must be a list")
    return value


def _present(raw: Raw) -> dict[str, object]:
    """Transcriptions write `key: null` for absent optional fields: treat them as absent."""
    return {k: v for k, v in raw.items() if v is not None}


def _rename(raw: Raw, names: Mapping[str, str]) -> dict[str, object]:
    return {names.get(k, k): v for k, v in raw.items()}


THEORY_KEYS: Mapping[str, str] = {
    "tipus": "kind", "num": "number", "resum": "summary_ref", "seccio": "section", "pagina": "page", "nom": "name",
    "enunciat": "statement", "demostracio": "proof", "problemes": "problems",
}  # fmt: skip
SHEET_KEYS: Mapping[str, str] = {
    "etiqueta": "label", "titol": "title", "descripcio": "description", "tema": "topic", "tipus": "kind",
}  # fmt: skip
PROBLEM_KEYS: Mapping[str, str] = {"num": "number", "font": "source", "preambul": "preamble", "indicacio": "hint"}
EXERCISE_KEYS: Mapping[str, str] = {
    "apartat": "part", "tipus": "kind", "enunciat": "statement", "resultat": "result", "passos": "steps",
    "errors_comuns": "common_mistakes", "teoria": "theory", "teoria_reservada": "reserved_theory",
    "nota_professor": "professor_note", "etiqueta": "label", "font": "source", "preambul": "preamble",
    "indicacio": "hint", "llista": "sheet_id", "grup": "group", "tema": "topic", "problema": "problem",
}  # fmt: skip
STEP_KEYS: Mapping[str, str] = {
    "titol": "title", "objectiu": "objective", "detall": "detail", "fuites": "leak_patterns", "teoria": "theory",
}  # fmt: skip
MISTAKE_KEYS: Mapping[str, str] = {"descripcio": "description", "pregunta": "question"}
RESULT_KEYS: Mapping[str, str] = {"valor": "value", "fuites": "leak_patterns"}


def _theory_item(raw: Raw, topic: int) -> TheoryItem:
    return TheoryItem.model_validate(_rename(raw, THEORY_KEYS) | {"topic": topic})


def _sheet(raw: Raw) -> ProblemSheet:
    return ProblemSheet.model_validate(_rename(raw, SHEET_KEYS))


def _problem(raw: Raw) -> Problem:
    return Problem.model_validate(_rename({k: v for k, v in raw.items() if k != "exercicis"}, PROBLEM_KEYS))


def _exercise(sheet: ProblemSheet, problem: Problem, raw: Raw) -> Exercise:
    part = raw.get("apartat")
    defaults: dict[str, object] = {
        "sheet_id": sheet.id,
        "group": sheet.title,
        "topic": sheet.topic,
        "problem": problem.number,
        "format": sheet.format,
        "source": problem.source,
        "preamble": problem.preamble,
        "hint": problem.hint or "",
        "label": f"{problem.number}({part})" if part else str(problem.number),
    }
    fields = _rename(raw, EXERCISE_KEYS)
    fields["steps"] = [Step.model_validate(_rename(s, STEP_KEYS)) for s in _list(raw, "passos")]
    fields["common_mistakes"] = [
        CommonMistake.model_validate(_rename(m, MISTAKE_KEYS)) for m in _list(raw, "errors_comuns")
    ]
    fields["result"] = ExpectedResult.model_validate(_rename(_map(raw, "resultat"), RESULT_KEYS))
    return Exercise.model_validate(defaults | fields)
