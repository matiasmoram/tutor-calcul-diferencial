"""The offline "pas a pas" pipeline (scripts/errades_offline.py): correct resolutions, parts assigned by code, errors
put into them and blind checks, through the same gates as PartedMistakeExerciseGenerator."""

import json
import random
from pathlib import Path

import pytest

from core.mistakes.domain.entities.parted_mistake_exercise import PartedMistakeExercise
from core.mistakes.infra import prompts
from core.shared.llm.client import JsonObject
from tests.core.mistakes.builders import (
    PARTS,
    corruption,
    edit,
    finding,
    gen,
    part_checked,
    parted_generator,
    problem_source,
    resolution,
    resolution_checked,
    theory_source,
)
from tests.fakes.llm import ScriptedLLMClient
from tests.scripts.builders import (
    NET_PROBLEM,
    NET_THEORY,
    PART_ERRORS,
    PART_FOUND,
    PROBLEM_ERRORS,
    THEORY_PART_ERRORS,
    THEORY_PART_FOUND,
    stored,
    write_json,
)
from tests.scripts.loader import load_script

errades_offline = load_script("errades_offline")

# The correct text of the fragments PART_ERRORS change, and what they become.
CLEAN_2, FLAWED_2 = PARTS[1][1][0], "Com que $x^4 \\ge x^4+y^2$, el quocient està fitat per $|x|$."
CLEAN_3, FLAWED_3 = PARTS[2][1][1], "Per tant el límit és $1$."


def schema_of(text: str) -> JsonObject:
    return json.loads(text.split("```json\n")[-1].split("\n```")[0])


def seed_picking(difficulty: str, picks: dict[str, list[int]]) -> int:
    """A seed for assign under which every source of `picks` gets those parts (both test sources have 3)."""
    sources = {"t2-4c": problem_source(), "T3.21": theory_source()}
    for seed in range(1000):
        if all(
            errades_offline.choose_parts(
                sources[i], 3, difficulty, errades_offline.part_rng({"llavor": seed, "id": i, "dificultat": difficulty})
            )
            == parts
            for i, parts in picks.items()
        ):
            return seed
    raise AssertionError(f"no seed picks {picks}")


def assigned(tmp_path: Path, nets: list[JsonObject], difficulty: str, seed: int) -> Path:
    """The correct resolutions written and reviewed clean, and their parts assigned: the batch to corrupt."""
    net = write_json(tmp_path / "lot.net.json", nets)
    write_json(tmp_path / "lot.net.ver.json", {n["id"]: resolution_checked(True) for n in nets})
    assert errades_offline.cmd_assign(net, difficulty, seed) == 0
    return tmp_path / "lot.json"


def fill(batch: Path, corruptions: dict[str, dict[int, JsonObject]]) -> None:
    """The corruption writer's work: the answer for every assigned part, by document key."""
    docs = json.loads(batch.read_text(encoding="utf-8"))
    for doc in docs:
        answers = corruptions[f"{doc['id']}:{doc['dificultat']}"]
        doc["corrupcions"] = {str(p): answers[p] for p in doc["parts_amb_error"]}
    write_json(batch, docs)


def problem_batch(tmp_path: Path) -> Path:
    """t2-4c, normal: errors in parts 2 and 3, blinded."""
    batch = assigned(tmp_path, [NET_PROBLEM], "normal", seed_picking("normal", {"t2-4c": [2, 3]}))
    fill(batch, {"t2-4c:normal": PART_ERRORS})
    assert errades_offline.cmd_blind(batch) == 0
    return batch


def test_brief_net_gives_the_writer_the_resolution_prompt_reference_and_schema(tmp_path: Path) -> None:
    out = tmp_path / "brief.md"
    assert errades_offline.cmd_brief_net("problema", "t2-4c", out) == 0
    text = out.read_text(encoding="utf-8")
    source = problem_source()
    assert prompts.RESOLUTION_SYSTEM in text and prompts.context(source) in text
    assert prompts.resolution_user(source, []) in text and '{"font": "problema", "id": "t2-4c"}' in text
    assert schema_of(text)["properties"]["parts"]["items"]["properties"]["pas"]["enum"] == [
        "candidat",
        "acotar",
        "concloure",
    ]

    assert errades_offline.cmd_brief_net("teoria", "T3.21", out) == 0
    text = out.read_text(encoding="utf-8")
    assert prompts.THEORY_RESOLUTION_SYSTEM in text and "<apunts>" in text
    assert schema_of(text)["required"] == ["enunciat", "parts"]


@pytest.mark.parametrize(("font", "source_id"), [("problema", "nope"), ("teoria", "t2-4c"), ("x", "t2-4c")])
def test_brief_net_refuses_an_unknown_source(tmp_path: Path, font: str, source_id: str) -> None:
    with pytest.raises(SystemExit):
        errades_offline.cmd_brief_net(font, source_id, tmp_path / "brief.md")
    assert not (tmp_path / "brief.md").exists()


def test_validate_net_reports_each_bad_resolution(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    good = write_json(tmp_path / "bons.net.json", [NET_PROBLEM, NET_THEORY])
    assert errades_offline.cmd_validate_net(good) == 0
    assert "2 ok, 0 with problems" in capsys.readouterr().out

    reversed_steps = NET_PROBLEM | {"parts": NET_PROBLEM["parts"][::-1]}  # type: ignore[index]
    unknown = {"font": "problema", "id": "nope", "parts": []}
    bad = write_json(tmp_path / "dolents.net.json", [reversed_steps, NET_THEORY, NET_THEORY, unknown])
    assert errades_offline.cmd_validate_net(bad) == 1
    out = capsys.readouterr().out
    assert "les parts han de seguir els passos de la solució en ordre" in out
    assert out.count("the batch has another resolution of this source") == 2
    assert "nope: unknown exercise" in out and "0 ok, 4 with problems" in out

    with pytest.raises(SystemExit):
        errades_offline.cmd_validate_net(write_json(tmp_path / "lot.json", [NET_PROBLEM]))


def test_blind_net_gives_the_reviewer_the_whole_correct_resolutions(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    unknown = {"font": "problema", "id": "nope", "parts": []}
    net = write_json(tmp_path / "lot.net.json", [NET_PROBLEM, NET_THEORY, unknown])
    assert errades_offline.cmd_blind_net(net) == 1  # one resolution left out
    assert "nope: left out" in capsys.readouterr().out
    text = (tmp_path / "lot.net.blind.md").read_text(encoding="utf-8")
    assert prompts.resolution_check_system(problem_source()) in text
    assert prompts.resolution_check_system(theory_source()) in text
    assert f"[1] {PARTS[0][1][0]}" in text and f"[6] {PARTS[2][1][1]}" in text
    assert "[1] (enunciat) Sigui" in text and "[2] (demostració) Prenem" in text and "## nope" not in text
    assert "Write lot.net.ver.json" in text
    schema = schema_of(text)
    assert list(schema["properties"]) == ["t2-4c", "T3.21"]
    assert schema["properties"]["t2-4c"]["required"] == ["problemes", "valoracio", "arriba_al_resultat"]

    with pytest.raises(SystemExit):
        errades_offline.cmd_blind_net(write_json(tmp_path / "lot.json", [NET_PROBLEM]))


def test_assign_picks_the_parts_by_the_seed_and_briefs_the_corruption_writer(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    seed = seed_picking("normal", {"t2-4c": [2, 3]})
    batch = assigned(tmp_path, [NET_PROBLEM, NET_THEORY], "normal", seed)
    problem, theory = json.loads(batch.read_text(encoding="utf-8"))
    assert problem == {
        "format": "per_parts",
        "font": "problema",
        "id": "t2-4c",
        "dificultat": "normal",
        "llavor": seed,
        "parts_amb_error": [2, 3],
        "corrupcions": {"2": None, "3": None},
    }
    assert theory["font"] == "teoria" and theory["parts_amb_error"][0] == 1 and len(theory["parts_amb_error"]) == 2

    text = (tmp_path / "lot.brief.t2-4c.normal.md").read_text(encoding="utf-8")
    clean = resolution()
    assert prompts.PART_CORRUPTION_SYSTEM in text
    assert prompts.corruption_context(problem_source(), clean) in text
    assert prompts.corruption_user(clean, 2, "normal", []) in text
    assert prompts.corruption_user(clean, 3, "normal", []) in text and "### Part 1" not in text
    assert '"canvis"' in text and 'the document {"id": "t2-4c", "dificultat": "normal"}' in text
    theory_brief = (tmp_path / "lot.brief.T3.21.normal.md").read_text(encoding="utf-8")
    assert prompts.THEORY_PART_CORRUPTION_SYSTEM in theory_brief and "### Part 1" in theory_brief
    capsys.readouterr()

    # Assigning again never touches what the writer may already have filled.
    before = batch.read_text(encoding="utf-8")
    assert errades_offline.cmd_assign(tmp_path / "lot.net.json", "normal", seed + 1) == 0
    assert "t2-4c:normal: already in lot.json" in capsys.readouterr().out
    assert json.loads(batch.read_text(encoding="utf-8")) == json.loads(before)


def test_assign_needs_the_review_and_skips_a_resolution_that_fails_it(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    net = write_json(tmp_path / "lot.net.json", [NET_PROBLEM, NET_THEORY])
    with pytest.raises(SystemExit):
        errades_offline.cmd_assign(net, "normal", 1)
    assert not (tmp_path / "lot.json").exists()

    wrong = finding(1, "de classe", "error", "l'enunciat no és el dels apunts")
    write_json(
        tmp_path / "lot.net.ver.json", {"t2-4c": resolution_checked(True), "T3.21": resolution_checked(True, wrong)}
    )
    assert errades_offline.cmd_assign(net, "normal", 1) == 1
    out = capsys.readouterr().out
    assert "T3.21: not assigned" in out and "hi ha un error a la part 1, fragment 1" in out
    assert [d["id"] for d in json.loads((tmp_path / "lot.json").read_text(encoding="utf-8"))] == ["t2-4c"]
    assert not (tmp_path / "lot.brief.T3.21.normal.md").exists()


@pytest.mark.parametrize("difficulty", ["facil", "normal", "dificil"])
def test_assign_picks_parts_by_the_live_generators_rule(difficulty: str) -> None:
    for source, n_parts in ((problem_source(), 3), (problem_source(), 5), (theory_source(), 3), (theory_source(), 4)):
        for seed in range(30):
            live, _ = parted_generator(ScriptedLLMClient({}), seed=seed)._choose(source, n_parts, difficulty)  # type: ignore[arg-type]
            picked = errades_offline.choose_parts(source, n_parts, difficulty, random.Random(seed))
            assert picked == sorted(live)


def test_validate_runs_stage_b_gates_on_per_parts_documents(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    batch = assigned(tmp_path, [NET_PROBLEM], "normal", seed_picking("normal", {"t2-4c": [2, 3]}))
    fill(batch, {"t2-4c:normal": PART_ERRORS})
    assert errades_offline.cmd_validate(batch) == 0
    assert "1 ok, 0 with problems" in capsys.readouterr().out

    (doc,) = json.loads(batch.read_text(encoding="utf-8"))
    corruptions = doc["corrupcions"]
    whole = {"font": "problema", "id": "t2-4c", "dificultat": "normal"} | gen(PROBLEM_ERRORS)
    write_json(
        batch,
        [
            doc | {"parts_amb_error": [1, 2]},
            doc | {"corrupcions": corruptions | {"2": corruption([edit(1, "no hi és", "x")], "x")}},
            doc | {"corrupcions": corruptions | {"3": None}},
            doc | {"corrupcions": corruptions | {"2": corruptions["2"] | {"apte": False}}},
            whole,  # a "sencer" document of the same batch, through its own gates
        ],
    )
    assert errades_offline.cmd_validate(batch) == 1
    out = capsys.readouterr().out
    assert "parts_amb_error must be the parts its llavor picks: [2, 3]" in out
    assert "part 2: l'«original» del canvi 1 ha d'aparèixer exactament una vegada" in out
    assert "part 3: no corruption written" in out and "part 2: la part no és apta per a un error" in out
    assert "1 ok, 4 with problems" in out


def test_blind_splits_the_parts_by_rank_and_never_shows_one_part_both_ways(tmp_path: Path) -> None:
    problem_batch(tmp_path)
    first = (tmp_path / "lot.blind.1.md").read_text(encoding="utf-8")
    second = (tmp_path / "lot.blind.2.md").read_text(encoding="utf-8")
    assert not (tmp_path / "lot.blind.3.md").exists()
    for text in (first, second):
        assert prompts.PART_VERIFICATION_SYSTEM in text and "<solucio_de_referencia>" in text
        assert not any(field in text for field in ("EXPLICACIO", "CORRECCIO", "PISTA"))
    # File 1: part 1 as context, part 2 flawed; never its correct text nor anything after it.
    assert "## t2-4c:normal:2" in first and PARTS[0][1][0] in first and f"[1] {FLAWED_2}" in first
    assert CLEAN_2 not in first and PARTS[2][1][0] not in first
    # File 2: part 2 correct as context, part 3 flawed.
    assert "## t2-4c:normal:3" in second and CLEAN_2 in second and f"[2] {FLAWED_3}" in second
    assert FLAWED_2 not in second and CLEAN_3 not in second
    assert "Write lot.ver.2.json" in second
    schema = schema_of(second)["properties"]["t2-4c:normal:3"]
    assert schema["required"] == ["problemes", "valoracio", "alerta_context"]


def test_blind_gives_two_difficulties_of_one_source_separate_files(tmp_path: Path) -> None:
    batch = assigned(tmp_path, [NET_PROBLEM], "normal", seed_picking("normal", {"t2-4c": [2, 3]}))
    assert errades_offline.cmd_assign(tmp_path / "lot.net.json", "facil", seed_picking("facil", {"t2-4c": [2]})) == 0
    fill(batch, {"t2-4c:normal": PART_ERRORS, "t2-4c:facil": PART_ERRORS})
    assert errades_offline.cmd_blind(batch) == 0
    files = [(tmp_path / f"lot.blind.{j}.md").read_text(encoding="utf-8") for j in (1, 2, 3)]
    assert ["t2-4c:facil" in text for text in files] == [False, False, True]
    assert "## t2-4c:facil:2" in files[2] and CLEAN_2 not in files[2]


def test_import_saves_documents_whose_every_part_passes_and_check_cache_accepts_them(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    seed = seed_picking("normal", {"t2-4c": [2, 3], "T3.21": [1, 3]})
    batch = assigned(tmp_path, [NET_PROBLEM, NET_THEORY], "normal", seed)
    fill(batch, {"t2-4c:normal": PART_ERRORS, "T3.21:normal": THEORY_PART_ERRORS})
    assert errades_offline.cmd_blind(batch) == 0
    write_json(tmp_path / "lot.ver.1.json", {"t2-4c:normal:2": PART_FOUND[2], "T3.21:normal:1": THEORY_PART_FOUND[1]})
    write_json(tmp_path / "lot.ver.2.json", {"t2-4c:normal:3": PART_FOUND[3], "T3.21:normal:3": THEORY_PART_FOUND[3]})
    out_dir = tmp_path / "errades"
    assert errades_offline.cmd_import(batch, out_dir) == 0
    assert "imported 2, rejected 0" in capsys.readouterr().out

    saved = {p.relative_to(out_dir).parent.as_posix(): p for p in stored(out_dir)}
    assert sorted(saved) == ["T3.21/normal", "t2-4c/normal"]
    raw = json.loads(saved["t2-4c/normal"].read_text(encoding="utf-8"))
    problem = PartedMistakeExercise.model_validate(raw)
    assert raw["format"] == "per_parts" and saved["t2-4c/normal"].stem == problem.id
    assert problem.flawed_parts == [2, 3] and [m.id for m in problem.mistakes] == ["e1", "e2"]
    assert problem.fragments == [f for _, fragments in PARTS for f in fragments]
    reference = errades_offline.reference_hash(problem_source())
    assert raw["verificacio"] == {
        "origen": "offline",
        "lot": "lot.json",
        "valoracio": "ok",
        "problemes": [],
        "hash_referencia": reference,
    }
    assert raw["parts"][1]["verificacio"] == {
        "origen": "offline",
        "lot": "lot.json",
        "valoracio": "",
        "problemes": PART_FOUND[2]["problemes"],
        "hash_referencia": reference,
    }
    theory = PartedMistakeExercise.model_validate_json(saved["T3.21/normal"].read_text(encoding="utf-8"))
    assert theory.source_kind == "teoria" and theory.statement_fragments == 1 and theory.flawed_parts == [1, 3]
    assert theory.parts[0].title == "Enunciat" and [m.kind for m in theory.mistakes] == ["hipotesi", "conclusio"]

    assert errades_offline.cmd_check_cache(out_dir) == 0
    assert "0 cached documents with problems, 0 unhashed" in capsys.readouterr().out


def test_import_refuses_a_document_with_one_failing_part(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    batch = problem_batch(tmp_path)
    out_dir = tmp_path / "errades"
    write_json(tmp_path / "lot.ver.1.json", {"t2-4c:normal:2": PART_FOUND[2]})
    write_json(tmp_path / "lot.ver.2.json", {"t2-4c:normal:3": part_checked()})  # misses part 3's error
    assert errades_offline.cmd_import(batch, out_dir) == 1
    out = capsys.readouterr().out
    assert "REJECTED t2-4c:normal" in out and "imported 0, rejected 1" in out
    assert "part 3: l'error declarat al fragment 2 («el límit és $1$») no l'ha detectat" in out
    assert "part 2:" not in out
    assert stored(out_dir) == []

    (tmp_path / "lot.ver.2.json").unlink()
    (tmp_path / "lot.net.ver.json").unlink()
    assert errades_offline.cmd_import(batch, out_dir) == 1
    out = capsys.readouterr().out
    assert "resolució: no independent review of the correct resolution in lot.net.ver.json" in out
    assert "part 3: no independent review in lot.ver.2.json" in out
    assert stored(out_dir) == []


def test_check_cache_rechecks_the_stored_reviews_of_a_per_parts_document(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    batch = problem_batch(tmp_path)
    write_json(tmp_path / "lot.ver.1.json", {"t2-4c:normal:2": PART_FOUND[2]})
    write_json(tmp_path / "lot.ver.2.json", {"t2-4c:normal:3": PART_FOUND[3]})
    out_dir = tmp_path / "errades"
    assert errades_offline.cmd_import(batch, out_dir) == 0
    capsys.readouterr()
    (path,) = stored(out_dir)

    doc = json.loads(path.read_text(encoding="utf-8"))
    doc["verificacio"]["problemes"].append(finding(1, "el quocient tendeix", "consequencia"))
    doc["parts"][1]["verificacio"]["problemes"].append(finding(2, "Per tant", "error", "salta un pas"))
    write_json(path, doc)
    assert errades_offline.cmd_check_cache(out_dir) == 1
    out = capsys.readouterr().out
    assert f"{path.relative_to(out_dir)}: resolució: hi ha un error a la part 1, fragment 1" in out
    assert "part 2: hi ha un error NO intencionat al fragment 2: «Per tant» — salta un pas" in out
    assert path.exists()
