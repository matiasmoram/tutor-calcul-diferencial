"""The pre-generation scripts (composition roots in ``scripts/``) driven by the scripted LLM, writing to a tmp dir."""

from pathlib import Path

import pytest

from core.mistakes.application.mistake_exercise_generator import MistakeExerciseGenerator
from core.mistakes.application.parted_mistake_exercise_generator import PartedMistakeExerciseGenerator
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.entities.parted_mistake_exercise import PartedMistakeExercise
from core.mistakes.infra.json_file_source import JsonFileMistakeSource
from core.quizzes.domain.entities.quiz import Quiz
from core.quizzes.infra.json_quiz_files import JsonQuizFiles
from core.shared.llm.client import CallMeta, LLMError, LLMQuotaExhaustedError, LLMRequest, Stage
from tests.core.mistakes.builders import (
    COURSE,
    exercise_generator,
    gen,
    parted_generator,
    resolution_checked,
    seed_choosing,
    tgen,
    written,
)
from tests.core.quizzes.builders import generator as quiz_generator
from tests.core.quizzes.builders import item, ok_audit, ok_solver
from tests.fakes.llm import ScriptedLLMClient
from tests.scripts.builders import (
    PART_ERRORS,
    PART_FOUND,
    PROBLEM_ERRORS,
    PROBLEM_FINDINGS,
    THEORY_ERRORS,
    THEORY_FINDINGS,
    stored,
)
from tests.scripts.loader import load_script

pregenerate_errades = load_script("pregenerate_errades")
pregenerate_afirmacions = load_script("pregenerate_afirmacions")


async def test_pregenerate_errades_saves_problem_and_theory_documents(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    llm = ScriptedLLMClient(
        {
            Stage.MISTAKES_GENERATION: [gen(PROBLEM_ERRORS), tgen(THEORY_ERRORS)],
            Stage.MISTAKES_VERIFICATION: [
                {"problemes": PROBLEM_FINDINGS, "valoracio": "ok"},
                {"problemes": THEORY_FINDINGS, "valoracio": "ok"},
            ],
        }
    )
    specs = ["t2-4c:normal", "T3.21", "nope:normal", "t2-4c:extrema"]
    await pregenerate_errades.pregenerate(specs, COURSE, exercise_generator(llm), JsonFileMistakeSource(tmp_path))

    paths = {p.relative_to(tmp_path).parent.as_posix(): p for p in stored(tmp_path)}
    assert sorted(paths) == ["T3.21/normal", "t2-4c/normal"]
    problem_path = paths["t2-4c/normal"]
    problem = MistakeExercise.model_validate_json(problem_path.read_text(encoding="utf-8"))
    theory = MistakeExercise.model_validate_json(paths["T3.21/normal"].read_text(encoding="utf-8"))
    assert problem.source_kind == "problema" and problem.n_mistakes == 2 and problem.statement_fragments == 0
    assert theory.source_kind == "teoria" and theory.statement_fragments == 2
    assert problem_path.name == f"{problem.id}.json"
    assert problem_path.read_text(encoding="utf-8") == problem.model_dump_json(indent=2)
    out = capsys.readouterr().out
    assert "=== t2-4c (normal)" in out and "=== T3.21 (normal)" in out
    assert "intent 1: validacio=[] discrepancies=[]" in out
    assert "[1] (enunciat) " in out and "ERROR e1 @[2] (desigualtat)" in out
    assert f"saved {problem.id}" in out and out.count("FAILED") == 2
    # The failed specs never reached the model.
    assert llm.calls(Stage.MISTAKES_GENERATION) == 2


async def test_pregenerate_errades_per_parts_reports_attempts_calls_and_tokens(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    calls = pregenerate_errades.CallLog(
        ScriptedLLMClient(
            {
                Stage.MISTAKES_GENERATION: [written(), PART_ERRORS[2], PART_ERRORS[3]],
                Stage.MISTAKES_VERIFICATION: [resolution_checked(True), PART_FOUND[2], PART_FOUND[3]],
            }
        )
    )
    generator = parted_generator(calls, seed=seed_choosing(2, 3))
    files = JsonFileMistakeSource(tmp_path)
    await pregenerate_errades.pregenerate(["t2-4c:normal", "t2-4c:extrema"], COURSE, generator, files, calls)

    (path,) = stored(tmp_path)
    document = PartedMistakeExercise.model_validate_json(path.read_text(encoding="utf-8"))
    assert document.flawed_parts == [2, 3] and path.name == f"{document.id}.json"
    out = capsys.readouterr().out
    assert "resolució correcta (A):\n    intent 1: validacio=[] discrepancies=[]" in out
    assert "part 2 «Acotar el quocient» (B, C)" in out and "correcte: Com que $x^4 \\le x^4+y^2$" in out
    assert "ERROR e2 @[6] (calcul) «el límit és $1$»" in out
    usage = "calls 6 (mistakes_generation 3, mistakes_verification 3); tokens in 60 (cached 0), out 12"
    assert f"{usage}; cost $0.0000 (no price for scripted); wall " in out
    assert f"saved {document.id}" in out and out.count("FAILED") == 1


async def test_call_log_keeps_billed_failures_and_prices_them_with_the_harness() -> None:
    billed = LLMError("truncated")
    billed.meta = CallMeta(
        stage=Stage.MISTAKES_GENERATION,
        model="gpt-5.5",
        latency_ms=1,
        input_tokens=1_000_000,
        output_tokens=100_000,
        cached_tokens=200_000,
    )
    calls = pregenerate_errades.CallLog(
        ScriptedLLMClient({Stage.MISTAKES_GENERATION: [billed, LLMError("refused before billing")]})
    )
    for _ in range(2):
        with pytest.raises(LLMError):
            await calls.structured(Stage.MISTAKES_GENERATION, LLMRequest(system="", user=""))
    assert calls.calls == [billed.meta]
    price_in, price_out, price_cached = pregenerate_errades.PRICES["gpt-5.5"]
    usd = (800_000 * price_in + 200_000 * price_cached + 100_000 * price_out) / 1e6
    assert pregenerate_errades.usage(calls.calls) == (
        f"calls 1 (mistakes_generation 1); tokens in 1000000 (cached 200000), out 100000; cost ${usd:.4f}"
    )


async def test_pregenerate_errades_prints_the_rejection_reasons_of_a_failed_document(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    calls = pregenerate_errades.CallLog(
        ScriptedLLMClient(
            {Stage.MISTAKES_GENERATION: [written()] * 3, Stage.MISTAKES_VERIFICATION: [resolution_checked(False)] * 3}
        )
    )
    files = JsonFileMistakeSource(tmp_path)
    await pregenerate_errades.pregenerate(["t2-4c:normal"], COURSE, parted_generator(calls), files, calls)
    out = capsys.readouterr().out
    assert "FAILED:" in out and "resolució, intent 1:" in out and "resolució, intent 3:" in out
    assert not stored(tmp_path)


async def test_pregenerate_errades_names_an_exhausted_quota(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    quota = LLMQuotaExhaustedError("insufficient_quota: no credit")
    calls = pregenerate_errades.CallLog(ScriptedLLMClient({Stage.MISTAKES_GENERATION: [quota]}))
    files = JsonFileMistakeSource(tmp_path)
    await pregenerate_errades.pregenerate(["t2-4c:normal"], COURSE, parted_generator(calls), files, calls)
    out = capsys.readouterr().out
    assert "FAILED:" in out and "provider: insufficient_quota: no credit" in out


def test_pregenerate_errades_builds_the_generator_of_the_format() -> None:
    llm = ScriptedLLMClient({})
    assert isinstance(pregenerate_errades.make_generator("per_parts", llm), PartedMistakeExerciseGenerator)
    assert isinstance(pregenerate_errades.make_generator("sencer", llm), MistakeExerciseGenerator)


async def test_pregenerate_afirmacions_saves_the_quiz(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    llm = ScriptedLLMClient(
        {
            Stage.QUIZ_GENERATION: [
                {"afirmacions": [item(f"F{i}.") for i in range(3)] + [item("C1.", "cert")]},
                {"afirmacions": [item("C2.", "cert"), item("F9.")]},
            ],
            Stage.QUIZ_VERIFICATION: [ok_solver(["fals"] * 3 + ["cert"]), ok_solver(["cert", "fals"])],
            Stage.QUIZ_AUDIT: [ok_audit(4), ok_audit(2)],
        }
    )
    await pregenerate_afirmacions.pregenerate(
        ["tema-2:facil", "tema-9:facil", "tema-2:extrema"], COURSE, quiz_generator(llm), JsonQuizFiles(tmp_path)
    )

    (path,) = stored(tmp_path)
    quiz = Quiz.model_validate_json(path.read_text(encoding="utf-8"))
    assert path.relative_to(tmp_path).parent.as_posix() == "tema-2/facil" and path.name == f"{quiz.id}.json"
    assert len(quiz.statements) == 6 and quiz.topic == 2
    assert path.read_text(encoding="utf-8") == quiz.model_dump_json(indent=2)
    out = capsys.readouterr().out
    assert "ronda 1: demanades 5, rebudes 4, acceptades en total 4" in out
    assert "contraexemple: " in out and f"saved {quiz.id}" in out
    assert "FAILED: UnknownQuizSourceException" in out and "FAILED: ValueError" in out
