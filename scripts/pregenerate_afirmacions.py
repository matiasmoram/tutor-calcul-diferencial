"""Pre-generate verified 'Cert o fals' quizzes with the LLM so the demo doesn't wait on them.

Usage: python scripts/pregenerate_afirmacions.py tema-2:normal T2.12:facil tema-3:dificil ...
A source is a whole tema ("tema-2") or a result of the notes as the focus ("T2.12").
"""

import argparse
import asyncio
import random
import time

from dotenv import load_dotenv

from core.course.domain.entities.course import Course
from core.course.infra.yaml_course_source import YamlCourseSource
from core.quizzes.application.quiz_generator import QuizGenerator
from core.quizzes.domain.sources import quiz_source
from core.quizzes.domain.values.difficulty import difficulty_of
from core.quizzes.infra.json_quiz_files import JsonQuizFiles
from core.quizzes.infra.llm_blind_solver import LLMBlindSolver
from core.quizzes.infra.llm_quiz_auditor import LLMQuizAuditor
from core.quizzes.infra.llm_quiz_writer import LLMQuizWriter
from core.quizzes.infra.sympy_check_evaluator import SympyCheckEvaluator
from core.shared.domain.clock import SystemClock
from core.shared.llm.infra.factory import make_llm_client
from settings import BACKEND_DIR, ROOT_DIR, Config

GENERATED_DIR = BACKEND_DIR / "generats" / "afirmacions"


def load_course() -> Course:
    return YamlCourseSource(BACKEND_DIR / "exercicis", BACKEND_DIR / "teoria").load()


async def pregenerate(specs: list[str], course: Course, generator: QuizGenerator, files: JsonQuizFiles) -> None:
    for spec in specs:
        source_id, _, name = spec.partition(":")
        name = name or "normal"
        t0 = time.perf_counter()
        print(f"=== {source_id} ({name})", flush=True)
        try:
            difficulty = difficulty_of(name)
            if difficulty is None:
                raise ValueError(f"unknown difficulty {name!r}")
            quiz = await generator.generate(quiz_source(course, source_id), difficulty)
        except Exception as e:  # report and continue with the next spec
            print(f"  FAILED: {type(e).__name__}: {e}", flush=True)
            continue
        files.save(quiz)
        for r in quiz.verification.rounds if quiz.verification else []:
            print(
                f"  ronda {r.round}: demanades {r.requested}, rebudes {r.received}, "
                f"acceptades en total {r.accepted_total}"
            )
            for rejected in r.rejected:
                print(f"    REBUTJADA «{rejected.statement[:90]}»: {'; '.join(rejected.reasons)[:300]}")
        for s in quiz.statements:
            print(f"  [{s.id}] ({s.verdict}, {s.trap}, CAS {s.checks_passed}/{len(s.checks)}) {s.statement}")
            if s.counterexample:
                print(f"       contraexemple: {s.counterexample}")
        print(f"  saved {quiz.id} in {time.perf_counter() - t0:.0f}s", flush=True)


async def main(specs: list[str]) -> None:
    load_dotenv(ROOT_DIR / ".env")
    llm = make_llm_client(Config())
    generator = QuizGenerator(
        LLMQuizWriter(llm),
        LLMBlindSolver(llm),
        LLMQuizAuditor(llm),
        SympyCheckEvaluator(),
        SystemClock(),
        random.Random(),
    )
    await pregenerate(specs, load_course(), generator, JsonQuizFiles(GENERATED_DIR))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("specs", nargs="*", default=["tema-2:normal"], help="<source id>[:<difficulty>]")
    asyncio.run(main(parser.parse_args().specs))
