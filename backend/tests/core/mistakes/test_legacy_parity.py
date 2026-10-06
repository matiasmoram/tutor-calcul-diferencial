"""TEMPORARY (phases 2-5 of work/ARQUITECTURA.md): the new "troba l'error" context behaves exactly like
``tutor/errades.py``: same prompts, schemas and contexts sent to the model, same documents, same grading results,
and every pre-generated document loads to the same JSON.

Deleted together with backend/tutor in phase 6."""

import copy
from pathlib import Path

import pytest

from core.mistakes.application.pregenerated_importer import PregeneratedImporter
from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.exceptions import MistakeGenerationFailedException
from core.mistakes.domain.grading import grade, locate_annotations
from core.mistakes.domain.sources import source_of, theory_results
from core.mistakes.domain.values.mistake_source import MistakeSource
from core.mistakes.infra.json_file_source import JsonFileMistakeSource
from core.mistakes.infra.llm_adapters import LLMAnnotationGrader
from core.mistakes.infra.sqlmodel_repository import SQLModelMistakeExerciseRepository
from core.shared.llm.client import JsonObject, LLMRequest, Stage
from core.shared.storage.session_provider import SQLModelSessionProvider
from settings import BACKEND_DIR
from tests.core.mistakes.builders import (
    COURSE,
    err,
    exercise_generator,
    finding,
    gen,
    terr,
    tgen,
)
from tests.fakes.llm import ScriptedLLMClient
from tutor import errades
from tutor.fitxes import load_llistes
from tutor.llm import CallMeta as LegacyCallMeta
from tutor.teoria import load_teoria

GENERATED = BACKEND_DIR / "generats" / "errades"
FILES = sorted(GENERATED.glob("*/*/*.json"))
TEXTS = {p: p.read_text(encoding="utf-8") for p in FILES}
OLD_THEORY = load_teoria()
_, OLD_EXERCISES = load_llistes(teoria=OLD_THEORY)
LEGACY_STAGES = {
    "errades_generacio": Stage.MISTAKES_GENERATION,
    "errades_verificacio": Stage.MISTAKES_VERIFICATION,
    "errades_correccio": Stage.MISTAKES_GRADING,
}


class LegacyRecorder:
    """The legacy StructuredLLM, scripted like ScriptedLLMClient and with the same call metadata."""

    def __init__(self, script: dict[Stage, list[JsonObject]]) -> None:
        self._script = copy.deepcopy(script)
        self.requests: dict[Stage, list[LLMRequest]] = {}

    def structured(self, stage, system, user, schema, image=None, context=None):
        new_stage = LEGACY_STAGES[stage]
        self.requests.setdefault(new_stage, []).append(LLMRequest(system, user, schema, context=context))
        meta = LegacyCallMeta(stage=stage, model="scripted", latency_ms=1, input_tokens=10, output_tokens=2)
        return copy.deepcopy(self._script[new_stage].pop(0)), meta


def both(script: dict[Stage, list[JsonObject]]) -> tuple[LegacyRecorder, ScriptedLLMClient]:
    return LegacyRecorder(script), ScriptedLLMClient(copy.deepcopy(script))


def legacy_font(source_kind: str, source_id: str) -> errades.FontProblema | errades.FontTeoria:
    if source_kind == "teoria":
        return errades.FontTeoria(OLD_THEORY[source_id])
    return errades.FontProblema(OLD_EXERCISES[source_id])


def assert_same_requests(old: LegacyRecorder, new: ScriptedLLMClient) -> None:
    assert set(old.requests) == {s for s, rs in new.requests.items() if rs}
    for stage, requests in old.requests.items():
        assert len(requests) == len(new.requests[stage]), stage
        for o, n in zip(requests, new.requests[stage], strict=True):
            assert (o.system, o.user, o.schema, o.context) == (n.system, n.user, n.schema, n.context), stage


GENERATION_CASES = {
    "problem-retries": (
        "problema",
        "t2-4c",
        "facil",
        {
            Stage.MISTAKES_GENERATION: [
                gen([err(2, "no hi és")]),
                gen([err(2, "$x^4 \\ge x^4+y^2$")]),
                gen([err(2, "$x^4 \\ge x^4+y^2$")]),
            ],
            Stage.MISTAKES_VERIFICATION: [
                {"problemes": [finding(3, "demostra", "error", "salt"), finding(2, "x")], "valoracio": ""},
                {"problemes": [finding(2, "x"), finding(5, "límit", "consequencia")], "valoracio": "ok"},
            ],
        },
    ),
    "problem-two-errors": (
        "problema",
        "t3-1a",
        "normal",
        {
            Stage.MISTAKES_GENERATION: [
                gen([err(2, "$x^4 \\ge x^4+y^2$"), err(4, "criteri del sandvitx")]),
            ],
            Stage.MISTAKES_VERIFICATION: [
                {"problemes": [finding(2, "\\ge"), finding(4, "sandvitx")], "valoracio": "bé"},
            ],
        },
    ),
    "theory": (
        "teoria",
        "T3.21",
        "normal",
        {
            Stage.MISTAKES_GENERATION: [
                tgen([terr(1, "diferenciable")], n_enunciat=4),
                tgen([terr(1, "diferenciable"), terr(5, "les parcials són contínues", "pas_injustificat")]),
            ],
            Stage.MISTAKES_VERIFICATION: [
                {
                    "problemes": [
                        finding(1, "diferenciable"),
                        finding(5, "contínues"),
                        finding(3, "Prenem", "imprecisio"),
                    ],
                    "valoracio": "ok",
                }
            ],
        },
    ),
}


@pytest.mark.parametrize("case", sorted(GENERATION_CASES))
async def test_generation_sends_the_same_requests_and_builds_the_same_document(case: str) -> None:
    kind, source_id, difficulty, script = GENERATION_CASES[case]
    old_llm, new_llm = both(script)
    old, _ = errades.generate(old_llm, legacy_font(kind, source_id), difficulty)
    new = await exercise_generator(new_llm).generate(source_of(COURSE, kind, source_id), difficulty)
    assert_same_requests(old_llm, new_llm)
    assert new.model_dump(mode="json", exclude={"id", "created_at"}) == old.model_dump(
        mode="json", exclude={"id", "creat"}
    )


async def test_generation_gives_up_like_the_legacy() -> None:
    script = {Stage.MISTAKES_GENERATION: [gen([err(1, "no hi és")])] * 3}
    old_llm, new_llm = both(script)
    with pytest.raises(errades.LLMError) as old_error:
        errades.generate(old_llm, legacy_font("problema", "t2-4c"), "facil")
    with pytest.raises(MistakeGenerationFailedException) as new_error:
        await exercise_generator(new_llm).generate(source_of(COURSE, "problema", "t2-4c"), "facil")
    assert str(old_error.value) == new_error.value.args[0]
    assert_same_requests(old_llm, new_llm)


def annotations_for(doc: MistakeExercise) -> list[Annotation]:
    """Every kind of placement: on the quote, on the whole fragment, near it, on a correct fragment, outside."""
    out: list[Annotation] = []
    for k, e in enumerate(doc.mistakes):
        text = doc.fragments[e.fragment - 1]
        out.append(Annotation(id=f"q{k}", fragment=e.fragment, start=e.start, end=e.end, comment="és fals"))
        out.append(Annotation(id=f"w{k}", fragment=e.fragment, start=0, end=len(text), comment=""))
        out.append(Annotation(id=f"n{k}", fragment=e.fragment, start=max(0, e.start - 3), end=e.start + 1))
    clean = [i for i in range(1, len(doc.fragments) + 1) if not doc.mistakes_in(i)]
    if clean:
        out.append(Annotation(id="c", fragment=clean[0], start=0, end=5, comment="crec que no"))
    out.append(Annotation(id="x", fragment=len(doc.fragments) + 1, start=0, end=5))
    out.append(Annotation(id="z", fragment=1, start=4, end=4))
    return out


def grader_script(doc: MistakeExercise, annotations: list[Annotation]) -> dict[Stage, list[JsonObject]]:
    """Mixed verdicts, including wrong error claims, unknown grades and missing annotations."""
    grades = ["correcta", "parcial", "incorrecta", "absent", "genial"]
    claims = [e.id for e in doc.mistakes] + ["cap"]
    verdicts: list[JsonObject] = [
        {"anotacio": a.id, "error": claims[i % len(claims)], "explicacio": grades[i % len(grades)], "feedback": f"f{i}"}
        for i, a in enumerate(annotations)
        if i % 4 != 3
    ]
    return {Stage.MISTAKES_GRADING: [{"avaluacions": verdicts, "resum": "Resum."}]}


async def grade_new(llm: ScriptedLLMClient, source: MistakeSource, doc: MistakeExercise, annotations: list[Annotation]):
    located = locate_annotations(doc, annotations)
    if not located:
        return grade(doc, located, None, None)
    report, call = await LLMAnnotationGrader(llm).grade(source, doc, located)
    return grade(doc, located, report, call)


@pytest.mark.parametrize("path", FILES[::7], ids=lambda p: f"{p.parent.parent.name}-{p.parent.name}-{p.stem}")
async def test_grading_sends_the_same_request_and_gives_the_same_result(path: Path) -> None:
    doc = MistakeExercise.model_validate_json(TEXTS[path])
    old_doc = errades.SolucioAmbErrors.model_validate_json(TEXTS[path])
    annotations = annotations_for(doc)
    old_llm, new_llm = both(grader_script(doc, annotations))
    old = errades.grade(
        old_llm,
        legacy_font(doc.source_kind, doc.source_id),
        old_doc,
        [errades.Anotacio.model_validate(a.model_dump()) for a in annotations],
    )
    new = await grade_new(new_llm, source_of(COURSE, doc.source_kind, doc.source_id), doc, annotations)
    assert new.model_dump(mode="json") == old
    assert_same_requests(old_llm, new_llm)


async def test_grading_without_annotations_is_the_same() -> None:
    path = FILES[0]
    doc = MistakeExercise.model_validate_json(TEXTS[path])
    old_doc = errades.SolucioAmbErrors.model_validate_json(TEXTS[path])
    old = errades.grade(LegacyRecorder({}), legacy_font(doc.source_kind, doc.source_id), old_doc, [])
    new = await grade_new(ScriptedLLMClient({}), source_of(COURSE, doc.source_kind, doc.source_id), doc, [])
    assert new.model_dump(mode="json") == old


@pytest.mark.parametrize("path", FILES, ids=lambda p: f"{p.parent.parent.name}-{p.parent.name}-{p.stem}")
def test_every_pregenerated_document_loads_to_the_same_json(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    new = MistakeExercise.model_validate_json(text)
    old = errades.SolucioAmbErrors.model_validate_json(text)
    assert new.model_dump(mode="json") == old.model_dump(mode="json")
    assert (new.source_id, new.difficulty, new.id) == (path.parent.parent.name, path.parent.name, path.stem)
    # Its source still exists and is eligible, so a session on it can be graded.
    assert source_of(COURSE, new.source_kind, new.source_id).id == new.source_id


async def test_the_seed_gives_the_same_availability_as_the_file_cache(
    session_provider: SQLModelSessionProvider,
) -> None:
    repo = SQLModelMistakeExerciseRepository(session_provider)
    imported = await PregeneratedImporter(JsonFileMistakeSource(GENERATED), repo).import_all()
    assert imported == len(FILES) > 0
    assert await repo.ready_counts() == errades.disponibles(GENERATED)
    await PregeneratedImporter(JsonFileMistakeSource(GENERATED), repo).import_all()  # idempotent
    assert await repo.ready_counts() == errades.disponibles(GENERATED)


def test_same_theory_results() -> None:
    assert [it.id for it in theory_results(COURSE)] == [it.id for it in errades.items_teoria(OLD_THEORY)]
