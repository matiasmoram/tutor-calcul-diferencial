"""Pre-generate verified 'find the error' documents with the LLM so the demo doesn't wait on it.

Usage: python scripts/pregenerate_errades.py t3-10:normal t2-4c:facil T3.21:dificil ...
Ids starting with "T" are results of the notes (theory activity); the rest are exercises.
"""

import argparse
import asyncio
import time

from dotenv import load_dotenv

from core.course.domain.entities.course import Course
from core.course.infra.yaml_course_source import YamlCourseSource
from core.mistakes.application.mistake_exercise_generator import MistakeExerciseGenerator
from core.mistakes.domain.services.sources import theory_result
from core.mistakes.domain.values.difficulty import DIFFICULTIES, Difficulty
from core.mistakes.domain.values.mistake_source import MistakeSource, ProblemSource, TheorySource
from core.mistakes.infra.json_file_source import JsonFileMistakeSource
from core.mistakes.infra.llm_mistake_generator import LLMMistakeGenerator
from core.mistakes.infra.llm_mistake_verifier import LLMMistakeVerifier
from core.shared.domain.clock import SystemClock
from core.shared.llm.infra.factory import make_llm_client
from settings import BACKEND_DIR, ROOT_DIR, Config

GENERATED_DIR = BACKEND_DIR / "generats" / "errades"
_BY_NAME: dict[str, Difficulty] = {d: d for d in DIFFICULTIES}


def load_course() -> Course:
    return YamlCourseSource(BACKEND_DIR / "exercicis", BACKEND_DIR / "teoria").load()


def source_of(course: Course, source_id: str) -> MistakeSource:
    if source_id.startswith("T"):
        return TheorySource.of(course, theory_result(course, source_id))
    return ProblemSource.of(course, course.exercise(source_id))


async def pregenerate(
    specs: list[str], course: Course, generator: MistakeExerciseGenerator, files: JsonFileMistakeSource
) -> None:
    for spec in specs:
        source_id, _, name = spec.partition(":")
        name = name or "normal"
        t0 = time.perf_counter()
        print(f"=== {source_id} ({name})", flush=True)
        try:
            difficulty = _BY_NAME.get(name)
            if difficulty is None:
                raise ValueError(f"unknown difficulty {name!r}")
            exercise = await generator.generate(source_of(course, source_id), difficulty)
        except Exception as e:  # report and continue with the next spec
            print(f"  FAILED: {e}", flush=True)
            continue
        files.save(exercise)
        for attempt in exercise.verification.attempts or []:
            print(f"  intent {attempt.attempt}: validacio={attempt.validation} discrepancies={attempt.discrepancies}")
        for i, f in enumerate(exercise.fragments, 1):
            print(f"  [{i}]{' (enunciat)' if i <= exercise.statement_fragments else ''} {f}")
        for m in exercise.mistakes:
            print(f"  ERROR {m.id} @[{m.fragment}] ({m.kind}) «{m.quote}» — {m.explanation}")
        print(f"  saved {exercise.id} in {time.perf_counter() - t0:.0f}s", flush=True)


async def main(specs: list[str]) -> None:
    load_dotenv(ROOT_DIR / ".env")
    llm = make_llm_client(Config())
    generator = MistakeExerciseGenerator(LLMMistakeGenerator(llm), LLMMistakeVerifier(llm), SystemClock())
    await pregenerate(specs, load_course(), generator, JsonFileMistakeSource(GENERATED_DIR))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("specs", nargs="*", default=["t3-6:normal"], help="<source id>[:<difficulty>]")
    asyncio.run(main(parser.parse_args().specs))
