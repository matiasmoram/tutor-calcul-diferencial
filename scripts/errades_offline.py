"""'Find the error' documents written outside the app (by hand or with an external model), gated like the LLM pipeline.

A batch file (JSON) is a list of documents, each in the generator's output format plus its source:
  {"font": "teoria" | "problema", "id": "T3.21" | "t3-5", "dificultat": "facil" | "normal" | "dificil",
   "n_enunciat": 2,            # theory only: statement fragments first
   "fragments": [...], "errors": [{"fragment", "cita", "tipus", "explicacio", "correccio", "pista"}]}

Steps (the same gates as MistakeExerciseGenerator):
  brief <font> <id> <dificultat> <out.md>   the writer's instructions for that source: the generation prompt, the
                                            reference, the request and the JSON schema of a batch document
  validate <batch.json>   code validation (counts, quotes, $ balance, statement/proof split)
  blind <batch.json>      writes <batch>.blind.md for an independent reviewer: the verifier's instructions, the
                          documents WITHOUT the declared errors next to their reference (sheet or original item of
                          the notes), and the JSON schema of <batch>.ver.json
  import <batch.json>     needs <batch>.ver.json from the reviewer: {"<id>:<dificultat>": {"problemes": [...],
                          "valoracio": ""}} in the verifier's format. Code compares (every declared error
                          found, nothing else wrong) and saves only the documents that pass.
  check-cache             re-validates every cached document against the current sheets / notes and re-applies the
                          verification gate to its stored review; reports documents whose reference (sheet or
                          notes) changed since import, and counts the documents without a reference hash
"""

import argparse
import hashlib
import io
import json
import sys
from functools import cache
from pathlib import Path
from typing import Any

from core.course.domain.entities.course import Course
from core.course.infra.yaml_course_source import YamlCourseSource
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise, Verification
from core.mistakes.domain.services.generation_checks import GenerationCheck, compare_verification, validate_generation
from core.mistakes.domain.services.sources import theory_results
from core.mistakes.domain.values.difficulty import DIFFICULTIES, MISTAKES_PER_DIFFICULTY, Difficulty
from core.mistakes.domain.values.llm_outputs import GenerationDraft, VerifierFinding
from core.mistakes.domain.values.mistake_exercise_id import MistakeExerciseId
from core.mistakes.domain.values.mistake_source import MistakeSource, ProblemSource, TheorySource
from core.mistakes.infra import prompts
from core.mistakes.infra.json_file_source import JsonFileMistakeSource
from core.mistakes.infra.llm_schemas import generation_schema, verification_schema
from core.shared.domain.clock import SystemClock
from core.shared.llm.client import JsonObject
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


def reference_hash(source: MistakeSource) -> str:
    """Of the reference the reviewer compared the document against (the sheet or the item of the notes)."""
    return hashlib.sha256(prompts.reference(source).encode("utf-8")).hexdigest()


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


def parse_difficulty(name: str) -> Difficulty:
    for difficulty in DIFFICULTIES:
        if difficulty == name:
            return difficulty
    raise SystemExit(f"unknown difficulty {name!r}")


def cmd_brief(font: str, source_id: str, difficulty_name: str, out: Path) -> int:
    if font not in ("problema", "teoria"):
        raise SystemExit(f"unknown font {font!r}: problema or teoria")
    difficulty = parse_difficulty(difficulty_name)
    try:
        source = source_of({"font": font, "id": source_id})
    except KeyError as e:
        raise SystemExit(str(e)) from e
    head = {"font": font, "id": source_id, "dificultat": difficulty}
    out.write_text(
        f"# Writer brief: {source_id}, {difficulty} ({MISTAKES_PER_DIFFICULTY[difficulty]} errors)\n\n"
        f"## Instructions\n\n{prompts.generation_system(source)}\n\n"
        f"## Reference\n\n{prompts.context(source)}\n\n"
        f"## Request\n\n{prompts.generation_user(source, difficulty, [])}\n\n"
        "## Output\n\nA batch file: a JSON list of documents (a batch may hold several sources and difficulties). "
        f"This document is {json.dumps(head, ensure_ascii=False)} plus the fields of this schema:\n\n```json\n"
        f"{json.dumps(generation_schema(is_theory(head)), ensure_ascii=False, indent=2)}\n```\n",
        encoding="utf-8",
    )
    print(f"wrote {out}")
    return 0


def cmd_validate(path: Path) -> int:
    docs = load(path)
    bad = 0
    for doc in docs:
        problems = validate(doc).problems
        if problems:
            bad += 1
            print(f"{key(doc)}:\n  - " + "\n  - ".join(problems))
    print(f"{len(docs) - bad} ok, {bad} with problems")
    return 1 if bad else 0


def verifier_instructions(docs: list[BatchDoc]) -> str:
    """The verification prompt of each kind of document in the batch, told apart by the tag of its reference."""
    parts = []
    if any(not is_theory(d) for d in docs):
        parts.append(f"### Documents with a <solucio_de_referencia>\n\n{prompts.VERIFICATION_SYSTEM}")
    if any(is_theory(d) for d in docs):
        parts.append(f"### Documents with <apunts>\n\n{prompts.THEORY_VERIFICATION_SYSTEM}")
    return "\n\n".join(parts)


def review_schema(docs: list[BatchDoc]) -> JsonObject:
    """Of <batch>.ver.json: one verifier report per document, keyed `<id>:<dificultat>`."""
    keys = [key(d) for d in docs]
    return {
        "type": "object",
        "required": keys,
        "propertyNames": {"enum": keys},
        "additionalProperties": verification_schema(),
    }


def cmd_blind(path: Path) -> int:
    docs = load(path)
    sections = []
    for doc in docs:
        source = source_of(doc)
        fragments = validate(doc).fragments
        n_statement = doc.get("n_enunciat", 0) if isinstance(source, TheorySource) else 0
        sections.append(
            f"## {key(doc)}\n\n### Referència\n\n{prompts.context(source)}\n\n"
            f"### Document a revisar\n\n{prompts.verification_user(source, fragments, n_statement)}"
        )
    dest = path.with_suffix(".blind.md")
    dest.write_text(
        f"# Blind review: {path.name}\n\n## Instructions\n\n{verifier_instructions(docs)}\n\n"
        + "\n\n".join(sections)
        + f"\n\n## Output\n\nWrite {path.stem}.ver.json following this schema:\n\n```json\n"
        f"{json.dumps(review_schema(docs), ensure_ascii=False, indent=2)}\n```\n",
        encoding="utf-8",
    )
    print(f"wrote {dest} ({len(docs)} documents)")
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
                verification=Verification(
                    origin="offline",
                    batch=path.name,
                    assessment=assessment,
                    findings=findings,
                    reference_hash=reference_hash(source_of(doc)),
                ),
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
    bad = unhashed = 0
    for exercise in JsonFileMistakeSource(directory).load():
        doc = as_batch_doc(exercise)
        check = validate(doc)
        problems = list(check.problems)
        if check.valid:
            problems += compare_verification(check.mistakes, exercise.verification.findings, check.fragments)
            stored = exercise.verification.reference_hash
            if stored is None:
                unhashed += 1
            elif stored != reference_hash(source_of(doc)):
                problems.append("the sheet / notes changed since the document was reviewed")
        if problems:
            bad += 1
            relative = Path(exercise.source_id, exercise.difficulty, f"{exercise.id}.json")
            print(f"{relative}: " + "; ".join(problems))
    print(f"{bad} cached documents with problems, {unhashed} unhashed (reviewed before the reference was recorded)")
    return 1 if bad else 0


COMMANDS = {"validate": cmd_validate, "blind": cmd_blind, "import": cmd_import}


if __name__ == "__main__":
    # Documents are Catalan with maths symbols: UTF-8 output whatever the console's default encoding.
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", default="check-cache", choices=["brief", *COMMANDS, "check-cache"])
    parser.add_argument(
        "args", nargs="*", help="brief: <font> <id> <dificultat> <out.md>; validate / blind / import: batch files"
    )
    args = parser.parse_args()
    if args.command == "check-cache":
        sys.exit(cmd_check_cache())
    if args.command == "brief":
        if len(args.args) != 4:
            parser.error("brief needs <font> <id> <dificultat> <out.md>")
        sys.exit(cmd_brief(args.args[0], args.args[1], args.args[2], Path(args.args[3])))
    if not args.args:
        parser.error(f"{args.command} needs at least one batch file")
    sys.exit(max(COMMANDS[args.command](Path(p)) for p in args.args))
