"""'Cert o fals' quizzes written offline (by an agent or by hand), gated like the LLM pipeline (QuizGenerator).

A batch file (JSON) is one quiz's candidate statements in the writer's output format, plus its source:
  {"font": "tema-2" | "T2.12", "dificultat": "facil" | "normal" | "dificil", "autor": "<who wrote it>",
   "afirmacions": [{"enunciat", "veredicte", "trampa", "concepte", "contraexemple", "resolucio", "idees_clau",
                    "pista", "teoria", "comprovacions"}, ...]}
Write a few more statements than the quiz size: the ones a gate rejects are dropped.

Steps (the same gates as QuizGenerator):
  brief <font> <dificultat> <out.md>  the writer's instructions for that source: the generation prompt, the notes,
                                      the request and the JSON schema of the statements
  validate <batch.json>               code validation and sympy checks of every statement (writes nothing)
  blind <batch.json>                  writes <batch>.solver.md (statements only, for a blind solver) and
                                      <batch>.audit.md (with the declared solutions, for an auditor): two
                                      independent reviewers, as the solver and audit stages
  import <batch.json>                 needs <batch>.solver.json {"respostes": [...]} and <batch>.audit.json
                                      {"revisions": [...]} in those stages' formats. Code judges every statement
                                      (judging.judge), keeps a balanced quiz of the difficulty's size and saves it to
                                      backend/generats/afirmacions, which seeds the database on the next start.
"""

import argparse
import io
import json
import random
import sys
import time
from pathlib import Path
from typing import Any

from core.course.domain.entities.course import Course
from core.course.infra.yaml_course_source import YamlCourseSource
from core.quizzes.domain.entities.quiz import GenerationRound, RejectedStatement
from core.quizzes.domain.entities.statement import StatementVerification
from core.quizzes.domain.ports import CheckEvaluator
from core.quizzes.domain.services.assembly import build_quiz
from core.quizzes.domain.services.balance import false_range, is_complete, trim
from core.quizzes.domain.services.judging import judge
from core.quizzes.domain.services.sources import quiz_source
from core.quizzes.domain.services.validation import (
    all_checks,
    check_problems,
    normal_key,
    validate_draft,
    with_results,
)
from core.quizzes.domain.values.difficulty import QUIZ_SIZES, Difficulty, difficulty_of
from core.quizzes.domain.values.drafts import BatchRequest, StatementDraft
from core.quizzes.domain.values.quiz_source import QuizSource
from core.quizzes.domain.values.verification import AuditReview, SolverAnswer
from core.quizzes.infra.json_quiz_files import JsonQuizFiles
from core.quizzes.infra.llm_schemas import audit_schema, generation_schema, solver_schema
from core.quizzes.infra.prompts import (
    AUDIT_SYSTEM,
    GENERATION_SYSTEM,
    SOLVER_SYSTEM,
    audit_request,
    generation_request,
    solver_request,
    source_context,
)
from core.quizzes.infra.sympy_check_evaluator import SympyCheckEvaluator
from core.shared.domain.model_usage import ModelUsage
from settings import BACKEND_DIR

GENERATED_DIR = BACKEND_DIR / "generats" / "afirmacions"
EXTRA = 3  # statements asked for beyond the quiz size, so a few rejections still leave a full quiz

type Rejected = list[tuple[StatementDraft, list[str]]]


def load_course() -> Course:
    return YamlCourseSource(BACKEND_DIR / "exercicis", BACKEND_DIR / "teoria").load()


def parse_difficulty(name: str) -> Difficulty:
    difficulty = difficulty_of(name)
    if difficulty is None:
        raise SystemExit(f"unknown difficulty {name!r}")
    return difficulty


def load_batch(path: Path, course: Course) -> tuple[QuizSource, Difficulty, list[StatementDraft], dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    drafts = [StatementDraft.model_validate(d) for d in data.get("afirmacions", [])]
    return quiz_source(course, data["font"]), parse_difficulty(data["dificultat"]), drafts, data


def gate(
    source: QuizSource, drafts: list[StatementDraft], checks: CheckEvaluator
) -> tuple[list[StatementDraft], Rejected]:
    """The statements that pass the code validation and their sympy checks, in order, and the rejected ones."""
    refs = set(source.allowed_refs)
    seen: set[str] = set()
    candidates: list[StatementDraft] = []
    rejected: Rejected = []
    for d in drafts:
        problems = validate_draft(d, refs)
        key = normal_key(d.statement)
        if key in seen:
            problems.append("repeteix una afirmació que ja hi és")
        seen.add(key)
        if problems:
            rejected.append((d, problems))
        else:
            candidates.append(d)
    if candidates:
        results = checks.evaluate(all_checks(candidates))
        failures = [(d, check_problems(d)) for d in with_results(candidates, results)]
        rejected += [(d, p) for d, p in failures if p]
        candidates = [d for d, p in failures if not p]
    return candidates, rejected


def report(rejected: Rejected) -> None:
    for d, problems in rejected:
        print(f"  REJECTED «{d.statement[:90]}»: {'; '.join(problems)}")


def cmd_brief(font: str, difficulty_name: str, out: Path) -> int:
    source = quiz_source(load_course(), font)
    difficulty = parse_difficulty(difficulty_name)
    n = QUIZ_SIZES[difficulty]
    lo, hi = false_range(n)
    request = BatchRequest(
        difficulty=difficulty, count=n + EXTRA, false_min=lo + 1, false_max=hi + 1, kept=[], rejected=[]
    )
    out.write_text(
        f"# Writer brief: {source.id}, {difficulty} ({n} statements in the quiz)\n\n"
        f"## Instructions\n\n{GENERATION_SYSTEM}\n\n## Notes\n\n{source_context(source)}\n\n"
        f"## Request\n\n{generation_request(source, request)}\n\n"
        "## Output\n\nA JSON file: "
        f'{{"font": "{source.id}", "dificultat": "{difficulty}", "autor": "<your model>", "afirmacions": [...]}}, '
        "each statement following this schema:\n\n```json\n"
        f"{json.dumps(generation_schema(source.allowed_refs), ensure_ascii=False, indent=2)}\n```\n",
        encoding="utf-8",
    )
    print(f"wrote {out}")
    return 0


def cmd_validate(path: Path, checks: CheckEvaluator) -> int:
    source, difficulty, drafts, _ = load_batch(path, load_course())
    candidates, rejected = gate(source, drafts, checks)
    report(rejected)
    falses = sum(d.verdict == "fals" for d in candidates)
    n = QUIZ_SIZES[difficulty]
    print(
        f"{path.name}: {len(candidates)}/{len(drafts)} pass ({falses} false); the quiz needs {n}, "
        f"with {false_range(n)[0]}-{false_range(n)[1]} false"
    )
    return 1 if rejected else 0


def cmd_blind(path: Path, checks: CheckEvaluator) -> int:
    source, _, drafts, _ = load_batch(path, load_course())
    candidates, rejected = gate(source, drafts, checks)
    report(rejected)
    context = source_context(source)
    for kind, system, request, schema in (
        ("solver", SOLVER_SYSTEM, solver_request(candidates), solver_schema()),
        ("audit", AUDIT_SYSTEM, audit_request(candidates), audit_schema()),
    ):
        target = path.with_name(f"{path.stem}.{kind}.md")
        target.write_text(
            f"# {kind}\n\n## Instructions\n\n{system}\n\n## Notes\n\n{context}\n\n## Statements\n\n{request}\n\n"
            f"## Output\n\nWrite {path.stem}.{kind}.json following this schema:\n\n```json\n"
            f"{json.dumps(schema, ensure_ascii=False, indent=2)}\n```\n",
            encoding="utf-8",
        )
        print(f"wrote {target} ({len(candidates)} statements)")
    return 0


def offline_call(name: str) -> ModelUsage:
    return ModelUsage(model=f"offline:{name}", latency_ms=0)


def cmd_import(path: Path, checks: CheckEvaluator, directory: Path = GENERATED_DIR) -> int:
    source, difficulty, drafts, data = load_batch(path, load_course())
    candidates, rejected = gate(source, drafts, checks)
    solver_data = json.loads(path.with_name(f"{path.stem}.solver.json").read_text(encoding="utf-8"))
    audit_data = json.loads(path.with_name(f"{path.stem}.audit.json").read_text(encoding="utf-8"))
    answers = [SolverAnswer.model_validate(a) for a in solver_data.get("respostes", [])]
    reviews = [AuditReview.model_validate(r) for r in audit_data.get("revisions", [])]
    if len(answers) != len(candidates) or len(reviews) != len(candidates):
        print(
            f"{path.name}: {len(candidates)} statements pass the gates but the reviews have {len(answers)} answers "
            f"and {len(reviews)} reviews: run blind again and review its output"
        )
        return 1
    by_num = {a.num: a for a in answers}
    accepted: list[StatementDraft] = []
    for i, (d, problems) in enumerate(zip(candidates, judge(candidates, answers, reviews), strict=True), 1):
        if problems:
            rejected.append((d, problems))
            continue
        s = by_num[i]
        verification = StatementVerification(solver_justification=s.justification, confidence=s.confidence, round=1)
        accepted.append(d.model_copy(update={"verification": verification}))
    report(rejected)
    n = QUIZ_SIZES[difficulty]
    kept = trim(accepted, n)
    if not is_complete(kept, n):
        lo, hi = false_range(n)
        falses = sum(d.verdict == "fals" for d in kept)
        print(
            f"{path.name}: not imported: {len(kept)} usable statements ({falses} false); the quiz needs {n}, "
            f"with {lo}-{hi} false"
        )
        return 1
    author = str(data.get("autor") or "agent")
    round_log = GenerationRound(
        round=1,
        requested=len(drafts),
        received=len(drafts),
        generation=offline_call(author),
        rejected=[RejectedStatement(statement=d.statement, reasons=p) for d, p in rejected],
        solver=offline_call(str(solver_data.get("autor") or "reviewer")),
        audit=offline_call(str(audit_data.get("autor") or "reviewer")),
        accepted_total=len(kept),
    )
    quiz = build_quiz(source.id, source.topic, difficulty, kept, [round_log], random.Random(), time.time())
    saved = JsonQuizFiles(directory).save(quiz)
    print(f"{path.name}: imported {saved.relative_to(directory.parent)} ({n} statements)")
    return 0


if __name__ == "__main__":
    # Statements are Catalan with maths symbols: UTF-8 output whatever the console's default encoding.
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["brief", "validate", "blind", "import"])
    parser.add_argument("args", nargs="+", help="brief: <font> <dificultat> <out.md>; the others: batch files")
    args = parser.parse_args()
    if args.command == "brief":
        if len(args.args) != 3:
            parser.error("brief needs <font> <dificultat> <out.md>")
        sys.exit(cmd_brief(args.args[0], args.args[1], Path(args.args[2])))
    evaluator = SympyCheckEvaluator(timeout_s=60.0)
    command = {"validate": cmd_validate, "blind": cmd_blind, "import": cmd_import}[args.command]
    sys.exit(max(command(Path(p), evaluator) for p in args.args))
