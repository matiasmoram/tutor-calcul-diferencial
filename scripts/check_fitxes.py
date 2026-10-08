"""Validate solution sheets: structure, theory references, leak regexes, LaTeX delimiters.

    python scripts/check_fitxes.py                      # every list in backend/exercicis/
    python scripts/check_fitxes.py chunk.yaml --tema 3  # a file holding only `problemes:` (authoring chunks)

Problems name the authored (Catalan) YAML fields. Exit code 1 if any problem is found, or if the content does
not load (the course loader rejects duplicate ids and unknown theory references outright).
"""

import argparse
import re
import sys
import tempfile
from pathlib import Path

import yaml
from pydantic import ValidationError

from core.course.domain.entities.course import Course
from core.course.domain.entities.exercise import Exercise
from core.course.domain.exceptions import InvalidCourseContentException
from core.course.infra.yaml_course_source import YamlCourseSource
from settings import BACKEND_DIR

EXERCISES_DIR = BACKEND_DIR / "exercicis"
THEORY_DIR = BACKEND_DIR / "teoria"
ID = re.compile(r"^t[1-6]-\d+[a-z]?$")
# Step fields as the YAML names them -> entity attribute.
STEP_FIELDS = {"titol": "title", "objectiu": "objective", "idea": "idea", "detall": "detail"}
HINT_FIELDS = ("objectiu", "idea")


def _dollars_balanced(text: str) -> bool:
    return len(re.findall(r"(?<!\\)\$", text)) % 2 == 0


def problems_of(ex: Exercise, course: Course) -> list[str]:
    out: list[str] = []
    if not ID.match(ex.id):
        out.append(f"id must look like t3-5 or t2-4c, got {ex.id!r}")
    if len(ex.steps) < 2:
        out.append("needs at least 2 steps")
    if len(ex.common_mistakes) < 2:
        out.append("needs at least 2 common errors")
    texts = {"enunciat": ex.statement, "preambul": ex.preamble, "resultat": ex.result.value}
    for p in ex.steps:
        texts |= {f"{p.id}.{k}": getattr(p, attr) for k, attr in STEP_FIELDS.items()}
        if p.leak_patterns and not any(re.search(r, p.detail, re.IGNORECASE) for r in p.leak_patterns):
            out.append(f"step {p.id}: no leak regex matches its own detall")
        for r in p.leak_patterns + ex.result.leak_patterns:
            for field in HINT_FIELDS:
                if re.search(r, getattr(p, STEP_FIELDS[field]), re.IGNORECASE):
                    out.append(f"step {p.id}: {field} matches banned regex {r!r}")
    for m in ex.common_mistakes:
        texts |= {f"error {m.id}": m.description + " " + m.question}
        for r in ex.result.leak_patterns:
            if re.search(r, m.question, re.IGNORECASE):
                out.append(f"error {m.id}: Socratic question reveals the result ({r!r})")
        # The question is the fallback reply when every draft is rejected: if it matches a step's
        # banned content, the guard blocks it whenever that step is not yet allowed.
        for p in ex.steps:
            for r in p.leak_patterns:
                if re.search(r, m.question, re.IGNORECASE):
                    out.append(f"error {m.id}: Socratic question matches banned regex of step {p.id} ({r!r})")
    for name, text in texts.items():
        if not _dollars_balanced(text):
            out.append(f"{name}: unbalanced $")
    for r in ex.all_refs():
        if r.item_id not in course.theory:
            out.append(f"unknown theory reference {r}")
    if not ex.all_refs():
        out.append("cites no theory at all (add the definitions/results it uses)")
    return out


def _load_chunk(path: Path, topic: int | None) -> Course:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if "llista" not in data:
        header = {"id": f"tema-{topic}", "etiqueta": f"Tema {topic}", "titol": "chunk", "tema": topic}
        data = {"llista": header, "problemes": data["problemes"]}
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "chunk.yaml").write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
        return YamlCourseSource(Path(d), THEORY_DIR).load()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("--tema", type=int)
    args = ap.parse_args()

    try:
        course = (
            _load_chunk(Path(args.file), args.tema) if args.file else YamlCourseSource(EXERCISES_DIR, THEORY_DIR).load()
        )
    except (InvalidCourseContentException, ValidationError) as e:
        print(f"the content does not load: {e}")
        return 1

    bad = 0
    for ex in course.exercises.values():
        for p in problems_of(ex, course):
            print(f"{ex.id}: {p}")
            bad += 1
    print(f"{len(course.exercises)} exercises checked, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
