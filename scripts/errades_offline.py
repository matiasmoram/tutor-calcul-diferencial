"""'Find the error' documents written outside the app (by hand or with an external model), gated like the LLM pipeline.

Whole documents ("sencer", the gates of MistakeExerciseGenerator). A batch file (JSON) is a list of documents, each in
the generator's output format plus its source:
  {"font": "teoria" | "problema", "id": "T3.21" | "t3-5", "dificultat": "facil" | "normal" | "dificil",
   "n_enunciat": 2,            # theory only: statement fragments first
   "fragments": [...], "errors": [{"fragment", "cita", "tipus", "explicacio", "correccio", "pista"}]}

  brief <font> <id> <dificultat> <out.md>   the writer's instructions for that source: the generation prompt, the
                                            reference, the request and the JSON schema of a batch document
  validate <batch.json>   code validation (counts, quotes, $ balance, statement/proof split)
  blind <batch.json>      writes <batch>.blind.md for an independent reviewer: the verifier's instructions, the
                          documents WITHOUT the declared errors next to their reference (sheet or original item of
                          the notes), and the JSON schema of <batch>.ver.json
  import <batch.json>     needs <batch>.ver.json from the reviewer: {"<id>:<dificultat>": {"problemes": [...],
                          "valoracio": ""}} in the verifier's format. Code compares (every declared error
                          found, nothing else wrong) and saves only the documents that pass.

Step by step ("per_parts", the gates of PartedMistakeExerciseGenerator), two files per batch:
  <batch>.net.json  the correct resolutions (stage A), one per source:
                    {"font", "id", "parts": [{"pas", "fragments"}]}; theory: {"font", "id", "enunciat": [...],
                    "parts": [{"titol", "fragments"}]}
  <batch>.json      documents ({"format": "per_parts"}) written by assign, one per source and difficulty; the
                    corruption writer replaces each null of "corrupcions" with the stage B answer for that part:
                    {"format": "per_parts", "font", "id", "dificultat", "llavor", "parts_amb_error": [2, 3],
                     "corrupcions": {"2": {"apte", "canvis": [{"fragment", "original", "nou"}], "cita", "tipus",
                                           "explicacio", "correccio", "pista"}, "3": ...}}

  brief-net <font> <id> <out.md>   the writer's instructions for the correct resolution of that source
  validate-net <batch.net.json>    stage A's code gates
  blind-net <batch.net.json>       writes <batch>.net.blind.md, the whole correct resolutions for a reviewer, who
                                   answers <batch>.net.ver.json: {"<id>": {"problemes": [...], "valoracio": "",
                                   "arriba_al_resultat": true}}
  assign <batch.net.json> <dificultat> [--seed N]
                                   for every resolution that passes stage A (needs <batch>.net.ver.json), code picks
                                   the parts to corrupt from the seed like the live generator, adds the document to
                                   <batch>.json and writes <batch>.brief.<id>.<dificultat>.md for the corruption writer
  validate <batch.json>            stage B's code gates on the filled "corrupcions"
  blind <batch.json>               writes <batch>.blind.<j>.md, j the rank of the flawed part in its document (two
                                   difficulties of one source take separate files): the reference, the earlier parts
                                   correct and the flawed part, never its correct text, the later parts nor the errors.
                                   One reviewer per file, none of them the writer nor the reviewer of blind-net.
                                   Answers: <batch>.ver.<j>.json, {"<id>:<dificultat>:<part>": {"problemes": [...],
                                   "valoracio": "", "context_correcte": true, "alerta_context": ""}}
  import <batch.json>              saves a document only if its resolution passes stage A and every flawed part
                                   stages B and C
validate, blind and import take each document by its "format" ("sencer" when absent).

check-cache   re-validates every cached document (both layouts) against the current sheets / notes and re-applies the
              verification gates to its stored reviews; reports documents whose reference changed since import, and
              counts the older ones that carry no reference hash. Reports, never deletes.
"""

import argparse
import hashlib
import io
import json
import random
import sys
from collections.abc import Callable
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

from core.course.domain.entities.course import Course
from core.course.infra.yaml_course_source import YamlCourseSource
from core.mistakes.domain.entities.mistake_exercise import DeclaredMistake, MistakeExercise, Verification
from core.mistakes.domain.entities.parted_mistake_exercise import MistakePart, PartedMistakeExercise
from core.mistakes.domain.exceptions import MistakePartsUnavailableException
from core.mistakes.domain.services.generation_checks import (
    GenerationCheck,
    compare_verification,
    fragment_problems,
    validate_generation,
)
from core.mistakes.domain.services.part_checks import (
    check_corruption,
    check_resolution,
    part_verification_problems,
    require_parts,
    resolution_verification_problems,
)
from core.mistakes.domain.services.sources import theory_results
from core.mistakes.domain.values.difficulty import DIFFICULTIES, MISTAKES_PER_DIFFICULTY, Difficulty
from core.mistakes.domain.values.llm_outputs import (
    CorruptionDraft,
    GenerationDraft,
    PartReport,
    ResolutionDraft,
    ResolutionReport,
    VerificationReport,
    VerifierFinding,
)
from core.mistakes.domain.values.mistake_exercise_id import MistakeExerciseId
from core.mistakes.domain.values.mistake_source import MistakeSource, ProblemSource, TheorySource
from core.mistakes.domain.values.resolution import Resolution
from core.mistakes.infra import prompts
from core.mistakes.infra.json_file_source import JsonFileMistakeSource
from core.mistakes.infra.llm_schemas import (
    corruption_schema,
    generation_schema,
    part_verification_schema,
    resolution_schema,
    resolution_verification_schema,
    verification_schema,
)
from core.shared.domain.clock import SystemClock
from core.shared.llm.client import JsonObject
from settings import BACKEND_DIR

GENERATED_DIR = BACKEND_DIR / "generats" / "errades"
NET_SUFFIX = ".net.json"

# A batch document: the generator's JSON output plus its source ("font", "id", "dificultat").
type BatchDoc = dict[str, Any]


@cache
def load_course() -> Course:
    return YamlCourseSource(BACKEND_DIR / "exercicis", BACKEND_DIR / "teoria").load()


def is_theory(doc: BatchDoc) -> bool:
    return doc.get("font") == "teoria"


def is_parted(doc: BatchDoc) -> bool:
    return doc.get("format") == "per_parts"


def source_of(doc: BatchDoc) -> MistakeSource:
    course = load_course()
    if is_theory(doc):
        item = next((it for it in theory_results(course) if it.id == doc["id"]), None)
        if item is None:
            raise KeyError(f"{doc['id']}: not a result with proof in the notes")
        return TheorySource.of(course, item)
    if doc["id"] not in course.exercises:
        raise KeyError(f"{doc['id']}: unknown exercise")
    return ProblemSource.of(course, course.exercises[doc["id"]])


def reference_hash(source: MistakeSource) -> str:
    """Of the reference the reviewer compared the document against (the sheet or the item of the notes)."""
    return hashlib.sha256(prompts.reference(source).encode("utf-8")).hexdigest()


def key(doc: BatchDoc) -> str:
    return f"{doc['id']}:{doc['dificultat']}"


def validate(doc: BatchDoc) -> GenerationCheck:
    def rejected(problem: str) -> GenerationCheck:
        return GenerationCheck(fragments=[], mistakes=[], statement_fragments=0, problems=[problem])

    try:
        source_of(doc)
    except KeyError as e:
        return rejected(str(e))
    if doc.get("dificultat") not in MISTAKES_PER_DIFFICULTY:
        return rejected(f"dificultat invàlida: {doc.get('dificultat')}")
    draft = GenerationDraft.model_validate(doc)
    return validate_generation(draft, MISTAKES_PER_DIFFICULTY[doc["dificultat"]], is_theory(doc))


def load(path: Path) -> list[BatchDoc]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_json(path: Path) -> Any:
    """None when the file does not exist."""
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_difficulty(name: str) -> Difficulty:
    for difficulty in DIFFICULTIES:
        if difficulty == name:
            return difficulty
    raise SystemExit(f"unknown difficulty {name!r}")


def known_source(font: str, source_id: str) -> MistakeSource:
    if font not in ("problema", "teoria"):
        raise SystemExit(f"unknown font {font!r}: problema or teoria")
    try:
        return source_of({"font": font, "id": source_id})
    except KeyError as e:
        raise SystemExit(str(e)) from e


def cmd_brief(font: str, source_id: str, difficulty_name: str, out: Path) -> int:
    source = known_source(font, source_id)
    difficulty = parse_difficulty(difficulty_name)
    head = {"font": font, "id": source_id, "dificultat": difficulty}
    out.write_text(
        f"# Writer brief: {source_id}, {difficulty} ({MISTAKES_PER_DIFFICULTY[difficulty]} errors)\n\n"
        f"## Instructions\n\n{prompts.generation_system(source)}\n\n"
        f"## Reference\n\n{prompts.context(source)}\n\n"
        f"## Request\n\n{prompts.generation_user(source, difficulty, [])}\n\n"
        "## Output\n\nA batch file: a JSON list of documents (a batch may hold several sources and difficulties). "
        f"This document is {json.dumps(head, ensure_ascii=False)} plus the fields of this schema:\n\n```json\n"
        f"{json.dumps(generation_schema(is_theory(head)), ensure_ascii=False, indent=2)}\n```\n",
        encoding="utf-8",
    )
    print(f"wrote {out}")
    return 0


def print_problems(name: str, problems: list[str]) -> None:
    print(f"{name}:\n  - " + "\n  - ".join(problems))


def cmd_validate(path: Path) -> int:
    docs = load(path)
    nets = load_nets(path)
    bad = 0
    for doc in docs:
        problems = check_parted(doc, nets, net_of(path).name).problems if is_parted(doc) else validate(doc).problems
        if problems:
            bad += 1
            print_problems(key(doc), problems)
    print(f"{len(docs) - bad} ok, {bad} with problems")
    return 1 if bad else 0


def verifier_instructions(
    sources: list[MistakeSource], system: Callable[[MistakeSource], str] = prompts.verification_system
) -> str:
    """The verification prompt of each kind of document in the batch, told apart by the tag of its reference."""
    parts = []
    if problem := next((s for s in sources if isinstance(s, ProblemSource)), None):
        parts.append(f"### Documents with a <solucio_de_referencia>\n\n{system(problem)}")
    if theory := next((s for s in sources if isinstance(s, TheorySource)), None):
        parts.append(f"### Documents with <apunts>\n\n{system(theory)}")
    return "\n\n".join(parts)


def review_schema(docs: list[BatchDoc]) -> JsonObject:
    """Of <batch>.ver.json: one verifier report per document, keyed `<id>:<dificultat>`."""
    keys = [key(d) for d in docs]
    return {
        "type": "object",
        "required": keys,
        "propertyNames": {"enum": keys},
        "additionalProperties": verification_schema(),
    }


def keyed_schema(schemas: dict[str, JsonObject]) -> JsonObject:
    """One report per key, each with its own schema (its fragment numbers)."""
    return {"type": "object", "additionalProperties": False, "required": list(schemas), "properties": schemas}


def cmd_blind(path: Path) -> int:
    docs = load(path)
    whole = [d for d in docs if not is_parted(d)]
    parted = [d for d in docs if is_parted(d)]
    if whole:
        blind_whole(path, whole)
    return blind_parted(path, parted) if parted else 0


def blind_whole(path: Path, docs: list[BatchDoc]) -> None:
    sections = []
    for doc in docs:
        source = source_of(doc)
        fragments = validate(doc).fragments
        n_statement = doc.get("n_enunciat", 0) if isinstance(source, TheorySource) else 0
        sections.append(
            f"## {key(doc)}\n\n### Referència\n\n{prompts.context(source)}\n\n"
            f"### Document a revisar\n\n{prompts.verification_user(source, fragments, n_statement)}"
        )
    dest = path.with_suffix(".blind.md")
    dest.write_text(
        f"# Blind review: {path.name}\n\n## Instructions\n\n{verifier_instructions([source_of(d) for d in docs])}\n\n"
        + "\n\n".join(sections)
        + f"\n\n## Output\n\nWrite {path.stem}.ver.json following this schema:\n\n```json\n"
        f"{json.dumps(review_schema(docs), ensure_ascii=False, indent=2)}\n```\n",
        encoding="utf-8",
    )
    print(f"wrote {dest} ({len(docs)} documents)")


def cmd_import(path: Path, directory: Path = GENERATED_DIR) -> int:
    docs = load(path)
    files = JsonFileMistakeSource(directory)
    whole = [d for d in docs if not is_parted(d)]
    parted = [d for d in docs if is_parted(d)]
    ok = bad = 0
    for importer, batch in ((import_whole, whole), (import_parted, parted)):
        if batch:
            imported, rejected = importer(path, batch, files)
            ok += imported
            bad += rejected
    print(f"imported {ok}, rejected {bad}")
    return 1 if bad else 0


def import_whole(path: Path, docs: list[BatchDoc], files: JsonFileMistakeSource) -> tuple[int, int]:
    ver_path = path.with_suffix(".ver.json")
    ver = json.loads(ver_path.read_text(encoding="utf-8"))
    clock = SystemClock()
    ok = bad = 0
    for doc in docs:
        check = validate(doc)
        problems = list(check.problems)
        v = ver.get(key(doc))
        findings: list[VerifierFinding] = []
        assessment = ""
        if v is None:
            problems.append("no independent review for this document")
        else:
            findings = [VerifierFinding.model_validate(p) for p in v.get("problemes", [])]
            assessment = v.get("valoracio", "")
            problems += compare_verification(check.mistakes, findings, check.fragments)
        if problems:
            bad += 1
            print_problems(f"REJECTED {key(doc)}", problems)
            continue
        now = clock.now()
        files.save(
            MistakeExercise(
                id=MistakeExerciseId.new(check.fragments, now),
                source_id=doc["id"],
                source_kind="teoria" if is_theory(doc) else "problema",
                difficulty=doc["dificultat"],
                fragments=check.fragments,
                statement_fragments=check.statement_fragments,
                mistakes=check.mistakes,
                verification=Verification(
                    origin="offline",
                    batch=path.name,
                    assessment=assessment,
                    findings=findings,
                    reference_hash=reference_hash(source_of(doc)),
                ),
                created_at=now,
            )
        )
        ok += 1
    return ok, bad


# Step by step ("per_parts").


@dataclass
class Net:
    """A correct resolution of a <batch>.net.json, split into parts by stage A's code gates."""

    source: MistakeSource
    resolution: Resolution


def require_net_name(path: Path) -> None:
    if not path.name.endswith(NET_SUFFIX):
        raise SystemExit(f"{path.name}: a batch of correct resolutions is named <batch>{NET_SUFFIX}")


def net_of(path: Path) -> Path:
    """The correct resolutions of a per_parts batch: lot.json -> lot.net.json."""
    return path.with_suffix(NET_SUFFIX)


def batch_of(net_path: Path) -> Path:
    """lot.net.json -> lot.json."""
    return net_path.with_name(net_path.name.removesuffix(NET_SUFFIX) + ".json")


def load_nets(path: Path) -> dict[str, BatchDoc]:
    """The correct resolutions of the per_parts batch `path`, by source id; none when it has no .net.json."""
    return {d.get("id"): d for d in read_json(net_of(path)) or []}


def check_net(doc: BatchDoc) -> tuple[Net | None, list[str]]:
    """Stage A's code gates; no Net when the source is unknown or cannot make 2 parts."""
    try:
        source = source_of(doc)
        require_parts(source)
    except KeyError as e:
        return None, [str(e)]
    except MistakePartsUnavailableException as e:
        return None, [f"{doc['id']}: {e}"]
    check = check_resolution(ResolutionDraft.model_validate(doc), source)
    return Net(source, check.resolution), check.problems


def net_review(net: Net, reviews: dict[str, Any], reviews_name: str) -> tuple[ResolutionReport | None, list[str]]:
    """Stage A's blind check, judged as the live pipeline judges it."""
    answer = reviews.get(net.source.id)
    if answer is None:
        return None, [f"no independent review of the correct resolution in {reviews_name}"]
    report = ResolutionReport.model_validate(answer)
    return report, resolution_verification_problems(net.resolution, report, isinstance(net.source, TheorySource))


def cmd_brief_net(font: str, source_id: str, out: Path) -> int:
    source = known_source(font, source_id)
    try:
        require_parts(source)
    except MistakePartsUnavailableException as e:
        raise SystemExit(f"{source_id}: {e}") from e
    steps = source.exercise.step_ids if isinstance(source, ProblemSource) else None
    head = {"font": font, "id": source_id}
    out.write_text(
        f"# Writer brief: the correct resolution of {source_id}, in parts\n\n"
        f"## Instructions\n\n{prompts.resolution_system(source)}\n\n"
        f"## Reference\n\n{prompts.context(source)}\n\n"
        f"## Request\n\n{prompts.resolution_user(source, [])}\n\n"
        f"## Output\n\nA batch of correct resolutions, <batch>{NET_SUFFIX}: a JSON list with one resolution per "
        f"source. This one is {json.dumps(head, ensure_ascii=False)} plus the fields of this schema:\n\n```json\n"
        f"{json.dumps(resolution_schema(steps), ensure_ascii=False, indent=2)}\n```\n",
        encoding="utf-8",
    )
    print(f"wrote {out}")
    return 0


def cmd_validate_net(path: Path) -> int:
    require_net_name(path)
    docs = load(path)
    ids = [d.get("id") for d in docs]
    bad = 0
    for doc in docs:
        _, problems = check_net(doc)
        if ids.count(doc.get("id")) > 1:
            problems = [*problems, "the batch has another resolution of this source"]
        if problems:
            bad += 1
            print_problems(str(doc.get("id")), problems)
    print(f"{len(docs) - bad} ok, {bad} with problems")
    return 1 if bad else 0


def cmd_blind_net(path: Path) -> int:
    require_net_name(path)
    nets: list[Net] = []
    sections: list[str] = []
    schemas: dict[str, JsonObject] = {}
    left_out = 0
    for doc in load(path):
        net, problems = check_net(doc)
        if net is None or problems:
            left_out += 1
            print(f"{doc.get('id')}: left out, it does not pass validate-net")
            continue
        fragments = net.resolution.fragments
        nets.append(net)
        sections.append(
            f"## {net.source.id}\n\n### Referència\n\n{prompts.context(net.source)}\n\n### Document a revisar\n\n"
            f"{prompts.verification_user(net.source, fragments, net.resolution.statement_fragments)}"
        )
        schemas[net.source.id] = resolution_verification_schema(len(fragments))
    dest = path.with_suffix(".blind.md")
    instructions = verifier_instructions([n.source for n in nets], prompts.resolution_check_system)
    dest.write_text(
        f"# Blind review: {path.name}\n\n## Instructions\n\n{instructions}\n\n"
        + "\n\n".join(sections)
        + f"\n\n## Output\n\nWrite {path.with_suffix('.ver.json').name} following this schema:\n\n```json\n"
        f"{json.dumps(keyed_schema(schemas), ensure_ascii=False, indent=2)}\n```\n",
        encoding="utf-8",
    )
    print(f"wrote {dest} ({len(sections)} resolutions)")
    return 1 if left_out else 0


def choose_parts(source: MistakeSource, n_parts: int, difficulty: Difficulty, rng: random.Random) -> list[int]:
    """The parts to corrupt, by PartedMistakeExerciseGenerator's rule: k = min(the difficulty's errors, parts) drawn
    by `rng`; theory's statement (part 1) always."""
    k = min(MISTAKES_PER_DIFFICULTY[difficulty], n_parts)
    if isinstance(source, TheorySource):
        proof = list(range(2, n_parts + 1))
        rng.shuffle(proof)
        return sorted([1, *proof[: k - 1]])
    parts = list(range(1, n_parts + 1))
    rng.shuffle(parts)
    return sorted(parts[:k])


def part_rng(doc: BatchDoc) -> random.Random:
    """The document's own draw from the batch seed: its parts do not depend on the other documents."""
    return random.Random(f"{doc['llavor']}:{doc['id']}:{doc['dificultat']}")


def brief_path(batch_path: Path, doc: BatchDoc) -> Path:
    return batch_path.with_name(f"{batch_path.stem}.brief.{doc['id']}.{doc['dificultat']}.md")


def write_corruption_brief(batch_path: Path, doc: BatchDoc, net: Net) -> None:
    parts: list[int] = doc["parts_amb_error"]
    theory = isinstance(net.source, TheorySource)
    requests = "\n\n".join(
        f"### Part {p}\n\n{prompts.corruption_user(net.resolution, p, doc['dificultat'], [])}\n\n```json\n"
        f"{json.dumps(corruption_schema(len(net.resolution.parts[p - 1].fragments), theory), ensure_ascii=False, indent=2)}"
        "\n```"
        for p in parts
    )
    head = {"id": doc["id"], "dificultat": doc["dificultat"]}
    dest = brief_path(batch_path, doc)
    dest.write_text(
        f"# Corruption brief: {doc['id']}, {doc['dificultat']} (parts {', '.join(map(str, parts))})\n\n"
        f"## Instructions\n\n{prompts.corruption_system(net.source)}\n\n"
        f"## Reference and correct resolution\n\n{prompts.corruption_context(net.source, net.resolution)}\n\n"
        "## Requests\n\nOne answer per part, each made from the correct text above on its own: an error never "
        f"carries over to another part.\n\n{requests}\n\n"
        f"## Output\n\nIn {batch_path.name}, the document {json.dumps(head, ensure_ascii=False)}: replace each null "
        'of "corrupcions" with the answer for that part, following the schema of its part.\n',
        encoding="utf-8",
    )
    print(f"wrote {dest}")


def cmd_assign(path: Path, difficulty_name: str, seed: int | None = None) -> int:
    require_net_name(path)
    difficulty = parse_difficulty(difficulty_name)
    reviews_path = path.with_suffix(".ver.json")
    reviews = read_json(reviews_path)
    if reviews is None:
        raise SystemExit(f"assign needs {reviews_path.name}, the review of the blind-net file")
    seed = random.randrange(2**32) if seed is None else seed
    batch_path = batch_of(path)
    batch = load(batch_path) if batch_path.exists() else []
    assigned = {key(d) for d in batch}
    added = bad = 0
    for net_doc in load(path):
        net, problems = check_net(net_doc)
        if net is not None and not problems:
            problems = net_review(net, reviews, reviews_path.name)[1]
        if net is None or problems:
            bad += 1
            print_problems(f"{net_doc.get('id')}: not assigned, its correct resolution fails stage A", problems)
            continue
        doc: BatchDoc = {
            "format": "per_parts",
            "font": net.source.kind,
            "id": net.source.id,
            "dificultat": difficulty,
            "llavor": seed,
        }
        if key(doc) in assigned:
            print(f"{key(doc)}: already in {batch_path.name}, left as it is")
            continue
        parts = choose_parts(net.source, len(net.resolution.parts), difficulty, part_rng(doc))
        doc |= {"parts_amb_error": parts, "corrupcions": {str(p): None for p in parts}}
        batch.append(doc)
        assigned.add(key(doc))
        write_corruption_brief(batch_path, doc, net)
        added += 1
    write_json(batch_path, batch)
    print(f"wrote {batch_path} ({added} documents added, llavor {seed})")
    return 1 if bad else 0


@dataclass
class FlawedPart:
    part: int
    flawed_fragments: list[str]
    mistake: DeclaredMistake


@dataclass
class PartedCheck:
    """A per_parts batch document through stage A's and stage B's code gates: `flawed` holds the parts whose
    corruption passed."""

    net: Net | None
    flawed: list[FlawedPart]
    problems: list[str]


def check_parted(doc: BatchDoc, nets: dict[str, BatchDoc], net_name: str) -> PartedCheck:
    def rejected(*problems: str) -> PartedCheck:
        return PartedCheck(net=None, flawed=[], problems=list(problems))

    difficulty: Difficulty | None = next((d for d in DIFFICULTIES if d == doc.get("dificultat")), None)
    if difficulty is None:
        return rejected(f"dificultat invàlida: {doc.get('dificultat')}")
    if not isinstance(doc.get("llavor"), int):
        return rejected("no llavor: per_parts documents come from assign")
    net_doc = nets.get(doc.get("id", ""))
    if net_doc is None or net_doc.get("font") != doc.get("font"):
        return rejected(f"{doc.get('id')}: no correct resolution of this source in {net_name}")
    net, problems = check_net(net_doc)
    if net is None or problems:
        return rejected(*(f"resolució: {p}" for p in problems))
    parts = choose_parts(net.source, len(net.resolution.parts), difficulty, part_rng(doc))
    if doc.get("parts_amb_error") != parts:
        return rejected(f"parts_amb_error must be the parts its llavor picks: {parts}")
    corruptions = doc.get("corrupcions")
    if not isinstance(corruptions, dict):
        return rejected("corrupcions must be an object with one answer per part to corrupt")
    wanted = {str(p) for p in parts}
    problems = [f"corrupcions has part {p}, which is not to corrupt" for p in corruptions if p not in wanted]
    flawed: list[FlawedPart] = []
    theory = isinstance(net.source, TheorySource)
    for rank, part in enumerate(parts, 1):
        answer = corruptions.get(str(part))
        if answer is None:
            problems.append(f"part {part}: no corruption written")
            continue
        clean = net.resolution.parts[part - 1].fragments
        draft = CorruptionDraft.model_validate(answer)
        check = check_corruption(clean, draft, net.resolution.first_fragment(part), f"e{rank}", theory)
        problems += [f"part {part}: {p}" for p in check.problems]
        if check.mistake is not None:
            flawed.append(FlawedPart(part, check.flawed_fragments, check.mistake))
    return PartedCheck(net, flawed, problems)


def review_files(docs: list[BatchDoc]) -> dict[tuple[int, int], int]:
    """The blind file of each part to corrupt, by (document index, part): its rank in its document, after the parts of
    the earlier documents of the same source. Documents of one source share its correct resolution, so a file never
    holds two of them: no reviewer sees a part both correct and flawed."""
    taken: dict[str, int] = {}
    files: dict[tuple[int, int], int] = {}
    for i, doc in enumerate(docs):
        parts = doc.get("parts_amb_error") or []
        before = taken.get(doc["id"], 0)
        for rank, part in enumerate(parts, 1):
            files[(i, part)] = before + rank
        taken[doc["id"]] = before + len(parts)
    return files


def part_key(doc: BatchDoc, part: int) -> str:
    return f"{key(doc)}:{part}"


def part_reviews_path(path: Path, j: int) -> Path:
    return path.with_name(f"{path.stem}.ver.{j}.json")


def blind_parted(path: Path, docs: list[BatchDoc]) -> int:
    nets = load_nets(path)
    files = review_files(docs)
    sections: dict[int, list[str]] = {}
    schemas: dict[int, dict[str, JsonObject]] = {}
    left_out = 0
    for i, doc in enumerate(docs):
        check = check_parted(doc, nets, net_of(path).name)
        if check.net is None or check.problems:
            left_out += 1
            print(f"{key(doc)}: left out, it does not pass validate")
            continue
        resolution = check.net.resolution
        for f in check.flawed:
            j = files[(i, f.part)]
            shown = resolution.parts[f.part - 1].model_copy(update={"fragments": f.flawed_fragments})
            sections.setdefault(j, []).append(
                f"## {part_key(doc, f.part)}\n\n### Referència\n\n{prompts.context(check.net.source)}\n\n"
                f"### Part a revisar\n\n{prompts.part_verification_user(resolution.parts[: f.part - 1], shown)}"
            )
            schemas.setdefault(j, {})[part_key(doc, f.part)] = part_verification_schema(len(f.flawed_fragments))
    for j in sorted(sections):
        dest = path.with_name(f"{path.stem}.blind.{j}.md")
        dest.write_text(
            f"# Blind review: {path.name}, file {j}\n\n## Instructions\n\n{prompts.PART_VERIFICATION_SYSTEM}\n\n"
            + "\n\n".join(sections[j])
            + f"\n\n## Output\n\nWrite {part_reviews_path(path, j).name} following this schema:\n\n```json\n"
            f"{json.dumps(keyed_schema(schemas[j]), ensure_ascii=False, indent=2)}\n```\n",
            encoding="utf-8",
        )
        print(f"wrote {dest} ({len(sections[j])} parts)")
    return 1 if left_out else 0


def import_parted(path: Path, docs: list[BatchDoc], files: JsonFileMistakeSource) -> tuple[int, int]:
    nets = load_nets(path)
    net_reviews_path = net_of(path).with_suffix(".ver.json")
    net_reviews = read_json(net_reviews_path) or {}
    review_file = review_files(docs)
    reviews = {j: read_json(part_reviews_path(path, j)) or {} for j in set(review_file.values())}
    ok = bad = 0
    for i, doc in enumerate(docs):
        check = check_parted(doc, nets, net_of(path).name)
        problems = list(check.problems)
        net = check.net
        net_report = None
        part_reports: dict[int, PartReport] = {}
        if net is not None and not problems:
            net_report, issues = net_review(net, net_reviews, net_reviews_path.name)
            problems += [f"resolució: {p}" for p in issues]
            for f in check.flawed:
                j = review_file[(i, f.part)]
                answer = reviews[j].get(part_key(doc, f.part))
                if answer is None:
                    problems.append(f"part {f.part}: no independent review in {part_reviews_path(path, j).name}")
                    continue
                part_reports[f.part] = PartReport.model_validate(answer)
                first = net.resolution.first_fragment(f.part)
                issues = part_verification_problems(f.mistake, first, f.flawed_fragments, part_reports[f.part])
                problems += [f"part {f.part}: {p}" for p in issues]
        if net is None or net_report is None or problems:
            bad += 1
            print_problems(f"REJECTED {key(doc)}", problems)
            continue
        files.save(parted_document(path, doc, net, check.flawed, net_report, part_reports))
        ok += 1
    return ok, bad


def parted_document(
    path: Path,
    doc: BatchDoc,
    net: Net,
    flawed: list[FlawedPart],
    net_report: ResolutionReport,
    part_reports: dict[int, PartReport],
) -> PartedMistakeExercise:
    reference = reference_hash(net.source)

    def verification(report: VerificationReport) -> Verification:
        return Verification(
            origin="offline",
            batch=path.name,
            assessment=report.assessment,
            findings=report.findings,
            reference_hash=reference,
        )

    by_part = {f.part: f for f in flawed}
    parts: list[MistakePart] = []
    for i, p in enumerate(net.resolution.parts, 1):
        f = by_part.get(i)
        if f is None:
            parts.append(MistakePart(title=p.title, step=p.step, fragments=p.fragments))
            continue
        parts.append(
            MistakePart(
                title=p.title,
                step=p.step,
                fragments=p.fragments,
                flawed_fragments=f.flawed_fragments,
                mistake=f.mistake,
                verification=verification(part_reports[i]),
            )
        )
    now = SystemClock().now()
    return PartedMistakeExercise(
        id=MistakeExerciseId.new(net.resolution.fragments, now),
        source_id=net.source.id,
        source_kind=net.source.kind,
        difficulty=doc["dificultat"],
        statement_fragments=net.resolution.statement_fragments,
        parts=parts,
        verification=verification(net_report),
        created_at=now,
    )


# The cache, both layouts.


def as_batch_doc(exercise: MistakeExercise) -> BatchDoc:
    return {
        "font": exercise.source_kind,
        "id": exercise.source_id,
        "dificultat": exercise.difficulty,
        "n_enunciat": exercise.statement_fragments,
        "fragments": exercise.fragments,
        "errors": [m.model_dump() for m in exercise.mistakes],
    }


def as_net_doc(document: PartedMistakeExercise) -> BatchDoc:
    theory = document.source_kind == "teoria"
    proof = document.parts[1:] if theory else document.parts
    doc: BatchDoc = {
        "font": document.source_kind,
        "id": document.source_id,
        "parts": [{"pas": p.step, "titol": p.title, "fragments": p.fragments} for p in proof],
    }
    if theory:
        doc["enunciat"] = document.parts[0].fragments
    return doc


def cached_whole_problems(exercise: MistakeExercise) -> tuple[list[str], MistakeSource | None]:
    """The code gates, then the verification gate on the stored review; no source when the code gates fail."""
    doc = as_batch_doc(exercise)
    check = validate(doc)
    if not check.valid:
        return check.problems, None
    return compare_verification(check.mistakes, exercise.verification.findings, check.fragments), source_of(doc)


def cached_parted_problems(document: PartedMistakeExercise) -> tuple[list[str], MistakeSource | None]:
    """Stage A's code gates on the correct parts, then the stored blind checks of the resolution and of each flawed
    part. Stage B's gates need the edits, which a stored document does not keep: its flawed text must still render."""
    net, problems = check_net(as_net_doc(document))
    if net is None or problems:
        return [f"resolució: {p}" for p in problems], None
    # A stored review keeps no `arriba_al_resultat`: a document is only stored when it was true.
    stored = ResolutionReport(findings=document.verification.findings, reaches_result=True)
    theory = isinstance(net.source, TheorySource)
    problems = [f"resolució: {p}" for p in resolution_verification_problems(net.resolution, stored, theory)]
    for i in document.flawed_parts:
        part = document.parts[i - 1]
        if part.flawed_fragments is None or part.mistake is None or part.verification is None:
            problems.append(f"part {i}: no blind check stored")
            continue
        problems += [f"part {i}: {p}" for p in fragment_problems(part.flawed_fragments)]
        report = PartReport(findings=part.verification.findings, assessment=part.verification.assessment)
        first = document.part_range(i).start
        issues = part_verification_problems(part.mistake, first, part.flawed_fragments, report)
        problems += [f"part {i}: {p}" for p in issues]
    return problems, net.source


def cmd_check_cache(directory: Path = GENERATED_DIR) -> int:
    bad = unhashed = 0
    for document in JsonFileMistakeSource(directory).load_all():
        if isinstance(document, PartedMistakeExercise):
            problems, source = cached_parted_problems(document)
        else:
            problems, source = cached_whole_problems(document)
        if source is not None:
            stored = document.verification.reference_hash
            if stored is None:
                unhashed += 1
            elif stored != reference_hash(source):
                problems.append("the sheet / notes changed since the document was reviewed")
        if problems:
            bad += 1
            relative = Path(document.source_id, document.difficulty, f"{document.id}.json")
            print(f"{relative}: " + "; ".join(problems))
    print(f"{bad} cached documents with problems, {unhashed} unhashed (reviewed before the reference was recorded)")
    return 1 if bad else 0


COMMANDS = {
    "validate": cmd_validate,
    "blind": cmd_blind,
    "import": cmd_import,
    "validate-net": cmd_validate_net,
    "blind-net": cmd_blind_net,
}


if __name__ == "__main__":
    # Documents are Catalan with maths symbols: UTF-8 output whatever the console's default encoding.
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "command", nargs="?", default="check-cache", choices=["brief", "brief-net", "assign", *COMMANDS, "check-cache"]
    )
    parser.add_argument(
        "args",
        nargs="*",
        help="brief: <font> <id> <dificultat> <out.md>; brief-net: <font> <id> <out.md>; "
        "assign: <batch.net.json> <dificultat>; the others: batch files",
    )
    parser.add_argument("--seed", type=int, help="assign: the seed that picks the parts to corrupt (default: random)")
    args = parser.parse_args()
    if args.command == "check-cache":
        sys.exit(cmd_check_cache())
    if args.command == "brief":
        if len(args.args) != 4:
            parser.error("brief needs <font> <id> <dificultat> <out.md>")
        sys.exit(cmd_brief(args.args[0], args.args[1], args.args[2], Path(args.args[3])))
    if args.command == "brief-net":
        if len(args.args) != 3:
            parser.error("brief-net needs <font> <id> <out.md>")
        sys.exit(cmd_brief_net(args.args[0], args.args[1], Path(args.args[2])))
    if args.command == "assign":
        if len(args.args) != 2:
            parser.error("assign needs <batch.net.json> <dificultat>")
        sys.exit(cmd_assign(Path(args.args[0]), args.args[1], args.seed))
    if not args.args:
        parser.error(f"{args.command} needs at least one batch file")
    sys.exit(max(COMMANDS[args.command](Path(p)) for p in args.args))
