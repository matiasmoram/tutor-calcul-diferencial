"""'Find the error' documents written offline (by an agent or by hand), gated like the LLM pipeline.

A batch file (JSON) is a list of documents, each in the generator's output format plus its source:
  {"font": "teoria" | "problema", "id": "T3.21" | "t3-5", "dificultat": "facil" | "normal" | "dificil",
   "n_enunciat": 2,            # theory only: statement fragments first
   "fragments": [...], "errors": [{"fragment", "cita", "tipus", "explicacio", "correccio", "pista"}]}

Steps (the same gates as MistakeExerciseGenerator):
  validate <batch.json>   code validation (counts, quotes, $ balance, statement/proof split)
  blind <batch.json>      writes <batch>.blind.md: the documents WITHOUT the declared errors, plus the
                          reference (sheet or original item of the notes), for an independent reviewer
  import <batch.json>     needs <batch>.ver.json from the reviewer: {"<id>:<dificultat>": {"problemes": [...],
                          "valoracio": ""}} in the verifier's format. Code compares (every declared error
                          found, nothing else wrong) and saves only the documents that pass.
  check-cache             re-validates every cached document against the current sheets / notes
"""

import argparse
import json
import sys
from functools import cache
from pathlib import Path
from typing import Any

from core.course.domain.entities.course import Course
from core.course.infra.yaml_course_source import YamlCourseSource
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise, Verification
from core.mistakes.domain.generation_checks import GenerationCheck, compare_verification, validate_generation
from core.mistakes.domain.sources import theory_results
from core.mistakes.domain.values.difficulty import MISTAKES_PER_DIFFICULTY
from core.mistakes.domain.values.llm_outputs import GenerationDraft, VerifierFinding
from core.mistakes.domain.values.mistake_exercise_id import MistakeExerciseId
from core.mistakes.domain.values.mistake_source import MistakeSource, ProblemSource, TheorySource
from core.mistakes.infra import prompts
from core.mistakes.infra.json_file_source import JsonFileMistakeSource
from core.shared.domain.clock import SystemClock
from settings import BACKEND_DIR

GENERATED_DIR = BACKEND_DIR / "generats" / "errades"

# A batch document: the generator's JSON output plus its source ("font", "id", "dificultat").
type BatchDoc = dict[str, Any]


@cache
def load_course() -> Course:
    return YamlCourseSource(BACKEND_DIR / "exercicis", BACKEND_DIR / "teoria").load()


def is_theory(doc: BatchDoc) -> bool:
    return doc.get("font") == "teoria"


def source_of(doc: BatchDoc) -> MistakeSource:
    course = load_course()
    if is_theory(doc):
        item = next((it for it in theory_results(course) if it.id == doc["id"]), None)
        if item is None:
            raise KeyError(f"{doc['id']}: not a result with proof in the notes")
        return TheorySource.of(course, item)
    if doc["id"] not in course.exercises:
        raise KeyError(f"{doc['id']}: unknown exercise")
    return ProblemSource.of(course, course.exercises[doc["id"]])


def key(doc: BatchDoc) -> str:
    return f"{doc['id']}:{doc['dificultat']}"


def validate(doc: BatchDoc) -> GenerationCheck:
    def rejected(problem: str) -> GenerationCheck:
        return GenerationCheck(fragments=[], mistakes=[], statement_fragments=0, problems=[problem])

    try:
        source_of(doc)
    except KeyError as e:
        return rejected(str(e))
    if doc.get("dificultat") not in MISTAKES_PER_DIFFICULTY:
        return rejected(f"dificultat invàlida: {doc.get('dificultat')}")
    draft = GenerationDraft.model_validate(doc)
    return validate_generation(draft, MISTAKES_PER_DIFFICULTY[doc["dificultat"]], is_theory(doc))


def load(path: Path) -> list[BatchDoc]:
    return json.loads(path.read_text(encoding="utf-8"))


def cmd_validate(path: Path) -> int:
    bad = 0
    for doc in load(path):
        problems = validate(doc).problems
        if problems:
            bad += 1
            print(f"{key(doc)}:\n  - " + "\n  - ".join(problems))
    print(f"{len(load(path)) - bad} ok, {bad} with problems")
    return 1 if bad else 0


def cmd_blind(path: Path) -> int:
    out = []
    for doc in load(path):
        source = source_of(doc)
        fragments = validate(doc).fragments
        n_statement = doc.get("n_enunciat", 0) if isinstance(source, TheorySource) else 0
        out.append(
            f"## {key(doc)}\n\n### Referència\n\n{prompts.context(source)}\n\n"
            f"### Document a revisar\n\n{prompts.numbered(fragments, n_statement)}\n"
        )
    dest = path.with_suffix(".blind.md")
    dest.write_text("\n\n".join(out), encoding="utf-8")
    print(f"wrote {dest} ({len(out)} documents)")
    return 0


def cmd_import(path: Path, directory: Path = GENERATED_DIR) -> int:
    ver_path = path.with_suffix(".ver.json")
    ver = json.loads(ver_path.read_text(encoding="utf-8"))
    files = JsonFileMistakeSource(directory)
    clock = SystemClock()
    ok = bad = 0
    for doc in load(path):
        check = validate(doc)
        problems = list(check.problems)
        v = ver.get(key(doc))
        findings: list[VerifierFinding] = []
        assessment = ""
        if v is None:
            problems.append("no independent review for this document")
        else:
            findings = [VerifierFinding.model_validate(p) for p in v.get("problemes", [])]
            assessment = v.get("valoracio", "")
            problems += compare_verification(check.mistakes, findings, check.fragments)
        if problems:
            bad += 1
            print(f"REJECTED {key(doc)}:\n  - " + "\n  - ".join(problems))
            continue
        now = clock.now()
        files.save(
            MistakeExercise(
                id=MistakeExerciseId.new(check.fragments, now),
                source_id=doc["id"],
                source_kind="teoria" if is_theory(doc) else "problema",
                difficulty=doc["dificultat"],
                fragments=check.fragments,
                statement_fragments=check.statement_fragments,
                mistakes=check.mistakes,
                verification=Verification(origin="offline", batch=path.name, assessment=assessment, findings=findings),
                created_at=now,
            )
        )
        ok += 1
    print(f"imported {ok}, rejected {bad}")
    return 1 if bad else 0


def as_batch_doc(exercise: MistakeExercise) -> BatchDoc:
    return {
        "font": exercise.source_kind,
        "id": exercise.source_id,
        "dificultat": exercise.difficulty,
        "n_enunciat": exercise.statement_fragments,
        "fragments": exercise.fragments,
        "errors": [m.model_dump() for m in exercise.mistakes],
    }


def cmd_check_cache(directory: Path = GENERATED_DIR) -> int:
    bad = 0
    for exercise in JsonFileMistakeSource(directory).load():
        problems = validate(as_batch_doc(exercise)).problems
        if problems:
            bad += 1
            relative = Path(exercise.source_id, exercise.difficulty, f"{exercise.id}.json")
            print(f"{relative}: " + "; ".join(problems))
    print(f"{bad} cached documents with problems")
    return 1 if bad else 0


COMMANDS = {"validate": cmd_validate, "blind": cmd_blind, "import": cmd_import}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", default="check-cache", choices=[*COMMANDS, "check-cache"])
    parser.add_argument("batches", nargs="*", type=Path, help="batch JSON files (validate / blind / import)")
    args = parser.parse_args()
    if args.command == "check-cache":
        sys.exit(cmd_check_cache())
    if not args.batches:
        parser.error(f"{args.command} needs at least one batch file")
    sys.exit(max(COMMANDS[args.command](p) for p in args.batches))
