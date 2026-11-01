"""The pre-generation scripts (composition roots in ``scripts/``) driven by the scripted LLM, writing to a tmp dir."""

from pathlib import Path

import pytest

from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.infra.json_file_source import JsonFileMistakeSource
from core.quizzes.domain.entities.quiz import Quiz
from core.quizzes.infra.json_quiz_files import JsonQuizFiles
from core.shared.llm.client import Stage
from tests.core.mistakes.builders import COURSE, exercise_generator, gen, tgen
from tests.core.quizzes.builders import generator as quiz_generator
from tests.core.quizzes.builders import item, ok_audit, ok_solver
from tests.fakes.llm import ScriptedLLMClient
from tests.scripts.builders import PROBLEM_ERRORS, PROBLEM_FINDINGS, THEORY_ERRORS, THEORY_FINDINGS, stored
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
