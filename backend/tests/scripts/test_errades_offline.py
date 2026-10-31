"""The offline "troba l'error" pipeline (scripts/errades_offline.py): an agent-written batch through the same gates
as the LLM pipeline, and the re-check of the cached documents."""

import json
from pathlib import Path

import pytest

from core.mistakes.infra import prompts
from core.shared.llm.client import JsonObject
from tests.core.mistakes.builders import finding, gen, tgen
from tests.scripts.builders import PROBLEM_ERRORS, PROBLEM_FINDINGS, THEORY_ERRORS, THEORY_FINDINGS, stored
from tests.scripts.loader import load_script

errades_offline = load_script("errades_offline")


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


def test_offline_brief_gives_the_writer_the_generation_prompt_reference_and_schema(tmp_path: Path) -> None:
    out = tmp_path / "brief.md"
    assert errades_offline.cmd_brief("problema", "t2-4c", "normal", out) == 0
    text = out.read_text(encoding="utf-8")
    source = errades_offline.source_of({"font": "problema", "id": "t2-4c"})
    assert prompts.GENERATION_SYSTEM in text and prompts.context(source) in text
    assert prompts.generation_user(source, "normal", []) in text
    assert '{"font": "problema", "id": "t2-4c", "dificultat": "normal"}' in text
    assert '"cita"' in text and '"n_enunciat"' not in text

    assert errades_offline.cmd_brief("teoria", "T3.21", "facil", out) == 0
    text = out.read_text(encoding="utf-8")
    assert prompts.THEORY_GENERATION_SYSTEM in text and "<apunts>" in text and '"n_enunciat"' in text


@pytest.mark.parametrize(
    ("font", "source_id", "difficulty"),
    [
        ("problema", "nope", "normal"),
        ("teoria", "t2-4c", "normal"),
        ("problema", "t2-4c", "extrema"),
        ("x", "t2-4c", "normal"),
    ],
)
def test_offline_brief_refuses_an_unknown_source_or_difficulty(
    tmp_path: Path, font: str, source_id: str, difficulty: str
) -> None:
    with pytest.raises(SystemExit):
        errades_offline.cmd_brief(font, source_id, difficulty, tmp_path / "brief.md")
    assert not (tmp_path / "brief.md").exists()


def test_offline_blind_gives_the_reviewer_instructions_and_schema_but_not_the_declared_errors(tmp_path: Path) -> None:
    declared = [
        e | {"explicacio": f"EXPLICACIO-{i}", "correccio": f"CORRECCIO-{i}", "pista": f"PISTA-{i}"}
        for i, e in enumerate(PROBLEM_ERRORS)
    ]
    batch = write_json(tmp_path / "lot.json", [batch_doc(declared), theory_doc()])
    assert errades_offline.cmd_blind(batch) == 0
    text = (tmp_path / "lot.blind.md").read_text(encoding="utf-8")
    assert "## t2-4c:normal" in text and "<solucio_de_referencia>" in text and "[2] $x^4" not in text
    assert "## T3.21:normal" in text and "<apunts>" in text and "[1] (enunciat) Sigui" in text
    assert "[3] (demostració)" in text
    assert not any(f"{field}-" in text for field in ("EXPLICACIO", "CORRECCIO", "PISTA"))
    assert prompts.VERIFICATION_SYSTEM in text and prompts.THEORY_VERIFICATION_SYSTEM in text
    assert "Write lot.ver.json" in text
    schema = json.loads(text.split("```json\n")[-1].split("\n```")[0])
    assert schema["propertyNames"]["enum"] == ["t2-4c:normal", "T3.21:normal"]
    assert schema["additionalProperties"]["required"] == ["problemes", "valoracio"]

    only_problems = write_json(tmp_path / "problemes.json", [batch_doc(PROBLEM_ERRORS)])
    assert errades_offline.cmd_blind(only_problems) == 0
    text = (tmp_path / "problemes.blind.md").read_text(encoding="utf-8")
    assert prompts.VERIFICATION_SYSTEM in text and prompts.THEORY_VERIFICATION_SYSTEM not in text


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
        "hash_referencia": errades_offline.reference_hash(errades_offline.source_of(batch_doc(PROBLEM_ERRORS))),
    }
    assert [e["cita"] for e in doc["errors"]] == ["$x^4 \\ge x^4+y^2$", "demostra que el límit existeix"]

    assert errades_offline.cmd_check_cache(out_dir) == 0
    assert "0 cached documents with problems, 0 unhashed" in capsys.readouterr().out


def import_one(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> tuple[Path, Path]:
    out_dir = tmp_path / "errades"
    batch = write_json(tmp_path / "lot.json", [batch_doc(PROBLEM_ERRORS)])
    write_json(tmp_path / "lot.ver.json", {"t2-4c:normal": {"problemes": PROBLEM_FINDINGS, "valoracio": ""}})
    assert errades_offline.cmd_import(batch, out_dir) == 0
    capsys.readouterr()
    (path,) = stored(out_dir)
    return out_dir, path


def edit_verification(path: Path, **changes: object) -> None:
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc["verificacio"] |= changes
    doc["verificacio"] = {k: v for k, v in doc["verificacio"].items() if v is not None}
    write_json(path, doc)


def test_check_cache_reports_a_reference_changed_since_review_and_counts_unhashed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    out_dir, path = import_one(tmp_path, capsys)
    edit_verification(path, hash_referencia="0" * 64)
    assert errades_offline.cmd_check_cache(out_dir) == 1
    out = capsys.readouterr().out
    assert f"{path.stem}.json: the sheet / notes changed since the document was reviewed" in out

    edit_verification(path, hash_referencia=None)  # reviewed before hashes were recorded: not a failure
    assert errades_offline.cmd_check_cache(out_dir) == 0
    assert "0 cached documents with problems, 1 unhashed" in capsys.readouterr().out


def test_check_cache_reapplies_the_verification_gate_to_the_stored_review(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    out_dir, path = import_one(tmp_path, capsys)
    extra = finding(2, "el quocient està fitat per $|x|$", "error", "fita falsa")
    edit_verification(path, problemes=[*PROBLEM_FINDINGS, extra])
    assert errades_offline.cmd_check_cache(out_dir) == 1
    assert "hi ha un error NO intencionat al fragment 2" in capsys.readouterr().out
