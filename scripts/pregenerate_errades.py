"""Pre-generate verified 'find the error' documents with the LLM so the demo doesn't wait on it.

Usage: python scripts/pregenerate_errades.py [--format sencer|per_parts] t3-10:normal t2-4c:facil T3.21:dificil ...
Ids starting with "T" are results of the notes (theory activity); the rest are exercises. Each document reports its
attempts per stage, its model calls and tokens, the cost at the evaluation harness's list prices, and the wall clock.
"""

import argparse
import asyncio
import sys
import time
from collections import Counter
from dataclasses import asdict

from dotenv import load_dotenv
from eval.harness import PRICES, cost

from core.course.domain.entities.course import Course
from core.course.infra.yaml_course_source import YamlCourseSource
from core.mistakes.application.mistake_exercise_generator import MistakeExerciseGenerator
from core.mistakes.application.parted_mistake_exercise_generator import PartedMistakeExerciseGenerator
from core.mistakes.domain.entities.mistake_exercise import GenerationAttempt, MistakeExercise
from core.mistakes.domain.entities.parted_mistake_exercise import PartedMistakeExercise
from core.mistakes.domain.services.sources import theory_result
from core.mistakes.domain.values.difficulty import DIFFICULTIES, Difficulty
from core.mistakes.domain.values.layout import LAYOUTS, Layout
from core.mistakes.domain.values.mistake_source import MistakeSource, ProblemSource, TheorySource
from core.mistakes.infra.json_file_source import JsonFileMistakeSource
from core.mistakes.infra.llm_mistake_generator import LLMMistakeGenerator
from core.mistakes.infra.llm_mistake_verifier import LLMMistakeVerifier
from core.mistakes.infra.llm_part_corrupter import LLMPartCorrupter
from core.mistakes.infra.llm_part_verifier import LLMPartVerifier
from core.mistakes.infra.llm_resolution_verifier import LLMResolutionVerifier
from core.mistakes.infra.llm_resolution_writer import LLMResolutionWriter
from core.shared.domain.clock import SystemClock
from core.shared.llm.client import CallMeta, JsonObject, LLMClient, LLMError, LLMQuotaExhaustedError, LLMRequest, Stage
from core.shared.llm.infra.factory import make_llm_client
from settings import BACKEND_DIR, ROOT_DIR, Config

GENERATED_DIR = BACKEND_DIR / "generats" / "errades"
_BY_NAME: dict[str, Difficulty] = {d: d for d in DIFFICULTIES}

type Generator = MistakeExerciseGenerator | PartedMistakeExerciseGenerator


class CallLog(LLMClient):
    """The model client, keeping the usage of every call: the failed ones the provider billed too."""

    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm
        self.calls: list[CallMeta] = []

    def model_for(self, stage: Stage) -> str:
        return self._llm.model_for(stage)

    async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
        try:
            data, meta = await self._llm.structured(stage, request)
        except LLMError as e:
            if e.meta is not None:
                self.calls.append(e.meta)
            raise
        self.calls.append(meta)
        return data, meta


def usage(calls: list[CallMeta]) -> str:
    stages = ", ".join(f"{stage} {n}" for stage, n in Counter(c.stage for c in calls).items())
    unpriced = sorted({c.model for c in calls} - PRICES.keys())
    price = f"${sum(cost(asdict(c)) for c in calls):.4f}"
    if unpriced:
        price += f" (no price for {', '.join(unpriced)})"
    return (
        f"calls {len(calls)} ({stages}); tokens in {sum(c.input_tokens for c in calls)} "
        f"(cached {sum(c.cached_tokens for c in calls)}), out {sum(c.output_tokens for c in calls)}; cost {price}"
    )


def make_generator(layout: Layout, llm: LLMClient) -> Generator:
    if layout == "per_parts":
        return PartedMistakeExerciseGenerator(
            LLMResolutionWriter(llm),
            LLMResolutionVerifier(llm),
            LLMPartCorrupter(llm),
            LLMPartVerifier(llm),
            SystemClock(),
        )
    return MistakeExerciseGenerator(LLMMistakeGenerator(llm), LLMMistakeVerifier(llm), SystemClock())


def load_course() -> Course:
    return YamlCourseSource(BACKEND_DIR / "exercicis", BACKEND_DIR / "teoria").load()


def source_of(course: Course, source_id: str) -> MistakeSource:
    if source_id.startswith("T"):
        return TheorySource.of(course, theory_result(course, source_id))
    return ProblemSource.of(course, course.exercise(source_id))


def print_attempts(attempts: list[GenerationAttempt] | None, indent: str = "  ") -> None:
    for attempt in attempts or []:
        print(f"{indent}intent {attempt.attempt}: validacio={attempt.validation} discrepancies={attempt.discrepancies}")


def print_whole(exercise: MistakeExercise) -> None:
    print_attempts(exercise.verification.attempts)
    for i, f in enumerate(exercise.fragments, 1):
        print(f"  [{i}]{' (enunciat)' if i <= exercise.statement_fragments else ''} {f}")
    for m in exercise.mistakes:
        print(f"  ERROR {m.id} @[{m.fragment}] ({m.kind}) «{m.quote}» — {m.explanation}")


def print_parted(document: PartedMistakeExercise) -> None:
    print("  resolució correcta (A):")
    print_attempts(document.verification.attempts, "    ")
    for i, part in enumerate(document.parts, 1):
        print(f"  part {i} «{part.title}»{' (B, C)' if part.mistake is not None else ''}")
        shown = part.flawed_fragments or part.fragments
        for n, flawed, correct in zip(document.part_range(i), shown, part.fragments, strict=True):
            print(f"    [{n}] {flawed}")
            if flawed != correct:
                print(f"         correcte: {correct}")
        if part.mistake is not None:
            m = part.mistake
            print(f"    ERROR {m.id} @[{m.fragment}] ({m.kind}) «{m.quote}» — {m.explanation}")
            print_attempts(part.verification.attempts if part.verification is not None else None, "    ")


def print_usage(calls: CallLog | None, first_call: int, t0: float) -> None:
    """The calls of one document: those logged since `first_call`."""
    if calls is not None:
        print(f"  {usage(calls.calls[first_call:])}; wall {time.perf_counter() - t0:.0f}s", flush=True)


async def pregenerate(
    specs: list[str],
    course: Course,
    generator: Generator,
    files: JsonFileMistakeSource,
    calls: CallLog | None = None,
) -> None:
    for spec in specs:
        source_id, _, name = spec.partition(":")
        name = name or "normal"
        t0 = time.perf_counter()
        first_call = len(calls.calls) if calls is not None else 0
        print(f"=== {source_id} ({name})", flush=True)
        try:
            difficulty = _BY_NAME.get(name)
            if difficulty is None:
                raise ValueError(f"unknown difficulty {name!r}")
            document = await generator.generate(source_of(course, source_id), difficulty)
        except Exception as e:  # report and continue with the next spec
            print(f"  FAILED: {e}", flush=True)
            if isinstance(e, LLMQuotaExhaustedError):
                print(f"  provider: {e.detail}", flush=True)
            print_usage(calls, first_call, t0)
            continue
        files.save(document)
        if isinstance(document, PartedMistakeExercise):
            print_parted(document)
        else:
            print_whole(document)
        print_usage(calls, first_call, t0)
        print(f"  saved {document.id} in {time.perf_counter() - t0:.0f}s", flush=True)


async def main(specs: list[str], layout: Layout) -> None:
    load_dotenv(ROOT_DIR / ".env")
    calls = CallLog(make_llm_client(Config()))
    files = JsonFileMistakeSource(GENERATED_DIR)
    await pregenerate(specs, load_course(), make_generator(layout, calls), files, calls)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("specs", nargs="*", default=["t3-6:normal"], help="<source id>[:<difficulty>]")
    parser.add_argument(
        "--format", choices=LAYOUTS, default="sencer", help="sencer: the whole document; per_parts: step by step"
    )
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]  # the Windows console defaults to cp1252
    asyncio.run(main(args.specs, args.format))
