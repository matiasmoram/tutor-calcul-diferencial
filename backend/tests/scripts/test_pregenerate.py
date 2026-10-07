"""The pre-generation scripts (composition roots in ``scripts/``) driven by the scripted LLM, writing to a tmp dir."""

import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest

from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.infra.json_file_source import JsonFileMistakeSource
from core.quizzes.domain.entities.quiz import Quiz
from core.quizzes.infra.json_quiz_files import JsonQuizFiles
from core.shared.llm.client import JsonObject, Stage
from settings import ROOT_DIR
from tests.core.mistakes.builders import COURSE, err, exercise_generator, finding, gen, terr, tgen
from tests.core.quizzes.builders import generator as quiz_generator
from tests.core.quizzes.builders import item, ok_audit, ok_solver
from tests.fakes.llm import ScriptedLLMClient


def load_script(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(f"scripts_{name}", ROOT_DIR / "scripts" / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pregenerate_errades = load_script("pregenerate_errades")
errades_offline = load_script("errades_offline")
pregenerate_afirmacions = load_script("pregenerate_afirmacions")

PROBLEM_ERRORS = [err(2, "$x^4 \\ge x^4+y^2$"), err(3, "demostra que el límit existeix")]
PROBLEM_FINDINGS = [finding(2, "$x^4 \\ge x^4+y^2$"), finding(3, "demostra que el límit existeix")]
THEORY_ERRORS = [terr(1, "diferenciable en un obert $U$"), terr(4, "$D_vf(a)=Df(a)v$")]
THEORY_FINDINGS = [finding(1, "diferenciable"), finding(4, "$D_vf(a)=Df(a)v$")]


def stored(directory: Path) -> list[Path]:
    return sorted(directory.glob("*/*/*.json"))


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
            Stage.QUIZ_GENERATION: [{"afirmacions": [item(f"F{i}.") for i in range(3)] + [item("C1.", "cert")]},
                                    {"afirmacions": [item("C2.", "cert"), item("F9.")]}],
            Stage.QUIZ_VERIFICATION: [ok_solver(["fals"] * 3 + ["cert"]), ok_solver(["cert", "fals"])],
            Stage.QUIZ_AUDIT: [ok_audit(4), ok_audit(2)],
        }
    )  # fmt: skip
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


def batch_doc(errors: list[JsonObject], doc_id: str = "t2-4c", difficulty: str = "normal") -> JsonObject:
    return {"font": "problema", "id": doc_id, "dificultat": difficulty} | gen(errors)


def theory_doc() -> JsonObject:
    return {"font": "teoria", "id": "T3.21", "dificultat": "normal"} | tgen(THEORY_ERRORS)


def write_json(path: Path, data: object) -> Path:
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path


def test_offline_validate_reports_each_bad_document(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    good = write_json(tmp_path / "good.json", [batch_doc(PROBLEM_ERRORS), theory_doc()])
    assert errades_offline.cmd_validate(good) == 0
    assert "2 ok, 0 with problems" in capsys.readouterr().out

    bad = write_json(
        tmp_path / "bad.json",
        [
            batch_doc(PROBLEM_ERRORS[:1]),  # normal needs 2 errors
            batch_doc(PROBLEM_ERRORS, doc_id="nope"),
            batch_doc(PROBLEM_ERRORS, difficulty="extrema"),
            {"font": "teoria", "id": "T9.99", "dificultat": "normal"} | tgen(THEORY_ERRORS),
        ],
    )
    assert errades_offline.cmd_validate(bad) == 1
    out = capsys.readouterr().out
    assert "calen exactament 2 errors" in out and "nope: unknown exercise" in out
    assert "dificultat invàlida: extrema" in out and "T9.99: not a result with proof in the notes" in out
    assert "0 ok, 4 with problems" in out


def test_offline_blind_hides_the_declared_errors(tmp_path: Path) -> None:
    batch = write_json(tmp_path / "lot.json", [batch_doc(PROBLEM_ERRORS), theory_doc()])
    assert errades_offline.cmd_blind(batch) == 0
    text = (tmp_path / "lot.blind.md").read_text(encoding="utf-8")
    assert "## t2-4c:normal" in text and "<solucio_de_referencia>" in text and "[2] $x^4" not in text
    assert "## T3.21:normal" in text and "<apunts>" in text and "[1] (enunciat) Sigui" in text
    assert "[3] (demostració)" in text and "explicacio" not in text


def test_offline_import_saves_only_reviewed_documents_and_check_cache_accepts_them(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    out_dir = tmp_path / "errades"
    batch = write_json(
        tmp_path / "lot.json", [batch_doc(PROBLEM_ERRORS), theory_doc(), batch_doc(PROBLEM_ERRORS, difficulty="facil")]
    )
    write_json(
        tmp_path / "lot.ver.json",
        {
            "t2-4c:normal": {"problemes": PROBLEM_FINDINGS, "valoracio": "bé"},
            "T3.21:normal": {"problemes": THEORY_FINDINGS[:1], "valoracio": ""},  # misses the proof error
        },
    )
    assert errades_offline.cmd_import(batch, out_dir) == 1
    out = capsys.readouterr().out
    assert "imported 1, rejected 2" in out and "no independent review for this document" in out
    assert "no l'ha detectat el verificador" in out

    (path,) = stored(out_dir)
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert path.relative_to(out_dir).parent.as_posix() == "t2-4c/normal" and path.stem == doc["id"]
    assert doc["verificacio"] == {
        "origen": "offline",
        "lot": "lot.json",
        "valoracio": "bé",
        "problemes": PROBLEM_FINDINGS,
    }
    assert [e["cita"] for e in doc["errors"]] == ["$x^4 \\ge x^4+y^2$", "demostra que el límit existeix"]

    assert errades_offline.cmd_check_cache(out_dir) == 0
    assert "0 cached documents with problems" in capsys.readouterr().out
