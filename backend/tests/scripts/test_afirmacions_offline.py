"""The offline 'Cert o fals' pipeline: an agent-written batch through the same gates as QuizGenerator."""

import json
from pathlib import Path

from core.quizzes.infra.json_quiz_files import JsonQuizFiles
from core.quizzes.infra.sympy_check_evaluator import SympyCheckEvaluator
from settings import BACKEND_DIR
from tests.scripts.test_pregenerate import load_script

afirmacions_offline = load_script("afirmacions_offline")
CHECKS = SympyCheckEvaluator(in_process=True)


def stored_quiz_batch(tmp_path: Path) -> Path:
    """A batch made of the statements of the cached T2.12 quiz (already verified), as an agent would write it."""
    quizzes = JsonQuizFiles(BACKEND_DIR / "generats" / "afirmacions").load_all()
    quiz = next(q for q in quizzes if q.source_id == "T2.12" and q.difficulty == "facil")
    statements = [s.model_dump(exclude={"id", "verification"}) for s in quiz.statements]
    for s in statements:
        s["comprovacions"] = [
            {k: v for k, v in c.items() if k not in ("estat", "calculat", "detall")} for c in s["comprovacions"]
        ]
    path = tmp_path / "batch.json"
    data = {"font": quiz.source_id, "dificultat": quiz.difficulty, "autor": "test", "afirmacions": statements}
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path


def write_reviews(path: Path, verdicts: list[str]) -> None:
    answers = [
        {"num": i, "veredicte": v, "confianca": "alta", "ben_plantejada": True, "justificacio": "ok"}
        for i, v in enumerate(verdicts, 1)
    ]
    reviews = [
        {"num": i, "resolucio_correcta": True, "teoria_correcta": True, "pista_neutra": True, "problemes": ""}
        for i in range(1, len(verdicts) + 1)
    ]
    path.with_name(f"{path.stem}.solver.json").write_text(json.dumps({"respostes": answers}), encoding="utf-8")
    path.with_name(f"{path.stem}.audit.json").write_text(json.dumps({"revisions": reviews}), encoding="utf-8")


def verdicts_of(path: Path) -> list[str]:
    return [s["veredicte"] for s in json.loads(path.read_text(encoding="utf-8"))["afirmacions"]]


def test_a_batch_that_passes_every_gate_is_imported(tmp_path: Path) -> None:
    batch = stored_quiz_batch(tmp_path)
    assert afirmacions_offline.cmd_validate(batch, CHECKS) == 0
    assert afirmacions_offline.cmd_blind(batch, CHECKS) == 0
    assert (tmp_path / "batch.solver.md").exists() and (tmp_path / "batch.audit.md").exists()
    assert "veredicte declarat" not in (tmp_path / "batch.solver.md").read_text(encoding="utf-8")
    write_reviews(batch, verdicts_of(batch))
    out = tmp_path / "afirmacions"
    assert afirmacions_offline.cmd_import(batch, CHECKS, out) == 0
    [quiz] = JsonQuizFiles(out).load_all()
    assert len(quiz.statements) == 6
    assert all(s.verification is not None for s in quiz.statements)
    assert quiz.verification is not None
    generation = quiz.verification.rounds[0].generation
    assert generation is not None and generation.model == "offline:test"


def test_a_solver_disagreement_drops_the_statement_and_an_incomplete_quiz_is_not_imported(tmp_path: Path) -> None:
    batch = stored_quiz_batch(tmp_path)
    verdicts = verdicts_of(batch)
    verdicts[0] = "cert" if verdicts[0] == "fals" else "fals"
    write_reviews(batch, verdicts)
    out = tmp_path / "afirmacions"
    assert afirmacions_offline.cmd_import(batch, CHECKS, out) == 1
    assert not out.exists()


def test_an_invented_latex_command_is_rejected_by_the_gate(tmp_path: Path) -> None:
    batch = stored_quiz_batch(tmp_path)
    data = json.loads(batch.read_text(encoding="utf-8"))
    data["afirmacions"][0]["enunciat"] += r" $\fterm{0}$"
    batch.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    assert afirmacions_offline.cmd_validate(batch, CHECKS) == 1
