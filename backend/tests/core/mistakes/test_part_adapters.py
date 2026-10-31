"""The model stages of the per-parts pipeline: prompts, schemas and what each stage may see."""

import json

from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.services.grading import locate_annotations
from core.mistakes.domain.services.part_checks import check_resolution
from core.mistakes.domain.values.llm_outputs import ResolutionDraft
from core.mistakes.domain.values.resolution import ResolutionPart
from core.mistakes.infra import prompts
from core.mistakes.infra.llm_annotation_grader import LLMAnnotationGrader
from core.mistakes.infra.llm_part_corrupter import LLMPartCorrupter
from core.mistakes.infra.llm_part_verifier import LLMPartVerifier
from core.mistakes.infra.llm_resolution_verifier import LLMResolutionVerifier
from core.mistakes.infra.llm_resolution_writer import LLMResolutionWriter
from core.shared.llm.client import Stage
from tests.core.mistakes.builders import (
    PART2_ERROR,
    PARTS,
    part_checked,
    parted,
    problem_source,
    resolution,
    resolution_checked,
    theory_source,
    theory_written,
    written,
)
from tests.fakes.llm import ScriptedLLMClient


async def test_the_writer_follows_the_sheet_steps_and_gets_the_rejections() -> None:
    llm = ScriptedLLMClient({Stage.MISTAKES_GENERATION: [written(), theory_written()]})
    draft, usage = await LLMResolutionWriter(llm).write(problem_source(), ["la part 2 és buida"])
    assert [p.step for p in draft.parts] == ["candidat", "acotar", "concloure"] and usage.model == "scripted"
    request = llm.requests[Stage.MISTAKES_GENERATION][0]
    assert request.system == prompts.RESOLUTION_SYSTEM and request.context == prompts.context(problem_source())
    assert "candidat, acotar, concloure" in request.user and "- la part 2 és buida" in request.user
    assert request.schema is not None and '"enum": ["candidat", "acotar", "concloure"]' in json.dumps(request.schema)

    theory, _ = await LLMResolutionWriter(llm).write(theory_source(), [])
    assert len(theory.statement) == 1 and theory.parts[0].title == "Derivades direccionals"
    request = llm.requests[Stage.MISTAKES_GENERATION][1]
    assert request.system == prompts.THEORY_RESOLUTION_SYSTEM and "<correccio>" not in request.user
    assert request.schema is not None and request.schema["required"] == ["enunciat", "parts"]


async def test_the_resolution_check_reviews_the_whole_document_and_whether_it_reaches_the_result() -> None:
    llm = ScriptedLLMClient({Stage.MISTAKES_VERIFICATION: [resolution_checked(True)]})
    report, _ = await LLMResolutionVerifier(llm).verify(problem_source(), resolution())
    assert report.reaches_result is True and report.findings == []
    request = llm.requests[Stage.MISTAKES_VERIFICATION][0]
    assert request.system.startswith(prompts.VERIFICATION_SYSTEM) and "arriba_al_resultat" in request.system
    assert (
        request.user.startswith("<resolucio_a_revisar>\n[1] Provem camins") and "[6] Per tant el límit" in request.user
    )
    schema = json.dumps(request.schema)
    assert '"enum": [1, 2, 3, 4, 5, 6]' in schema and '"arriba_al_resultat": {"type": "boolean"}' in schema


async def test_a_theory_resolution_check_labels_the_statement() -> None:
    check = check_resolution(ResolutionDraft.model_validate(theory_written()), theory_source())
    llm = ScriptedLLMClient({Stage.MISTAKES_VERIFICATION: [resolution_checked(True)]})
    await LLMResolutionVerifier(llm).verify(theory_source(), check.resolution)
    request = llm.requests[Stage.MISTAKES_VERIFICATION][0]
    assert request.system.startswith(prompts.THEORY_VERIFICATION_SYSTEM)
    assert "[1] (enunciat)" in request.user and "[2] (demostració)" in request.user


async def test_every_corruption_shares_the_cached_context_and_edits_only_its_part() -> None:
    clean = resolution()
    llm = ScriptedLLMClient({Stage.MISTAKES_GENERATION: [PART2_ERROR] * 3})
    corrupter = LLMPartCorrupter(llm)
    draft, _ = await corrupter.corrupt(problem_source(), clean, 2, "normal", [])
    assert draft.edits[0].new == "x^4 \\ge" and draft.fit is True
    await corrupter.corrupt(problem_source(), clean, 3, "normal", [])
    await corrupter.corrupt(problem_source(), resolution(), 2, "normal", ["la cita no hi és"])
    requests = llm.requests[Stage.MISTAKES_GENERATION]
    assert len({r.context for r in requests}) == 1
    context = str(requests[0].context)
    assert context.startswith(prompts.context(problem_source()))
    assert f"Part 2 — Acotar el quocient\n[1] {PARTS[1][1][0]}\n[2] {PARTS[1][1][1]}" in context
    assert (
        requests[0].user
        == "Introdueix UN error a la part 2 («Acotar el quocient»), que té 2 fragments. Dificultat: normal."
    )
    assert "la cita no hi és" in requests[2].user and requests[0].system == prompts.PART_CORRUPTION_SYSTEM
    schema = json.dumps(requests[0].schema)
    assert '"fragment": {"type": "integer", "enum": [1, 2]}' in schema and '"apte": {"type": "boolean"}' in schema
    assert '"teorema_mal_aplicat"' in schema


async def test_a_theory_corruption_uses_the_theory_kinds() -> None:
    check = check_resolution(ResolutionDraft.model_validate(theory_written()), theory_source())
    llm = ScriptedLLMClient({Stage.MISTAKES_GENERATION: [PART2_ERROR]})
    await LLMPartCorrupter(llm).corrupt(theory_source(), check.resolution, 1, "facil", [])
    request = llm.requests[Stage.MISTAKES_GENERATION][0]
    assert request.system == prompts.THEORY_PART_CORRUPTION_SYSTEM and "«Enunciat»" in request.user
    assert "<document_correcte>\nPart 1 — Enunciat\n[1]" in str(request.context)
    assert '"quantificador"' in json.dumps(request.schema)


async def test_the_part_check_sees_the_earlier_parts_as_context_and_never_the_clean_part_or_later_ones() -> None:
    doc = parted()
    clean = resolution()
    flawed = ResolutionPart(title=clean.parts[1].title, step="acotar", fragments=doc.parts[1].flawed_fragments or [])
    llm = ScriptedLLMClient({Stage.MISTAKES_VERIFICATION: [part_checked(alert="res")]})
    report, _ = await LLMPartVerifier(llm).verify(problem_source(), clean.parts[:1], flawed)
    assert report.context_alert == "res"
    request = llm.requests[Stage.MISTAKES_VERIFICATION][0]
    assert request.system == prompts.PART_VERIFICATION_SYSTEM and request.context == prompts.context(problem_source())
    earlier = f"<parts_anteriors>\nTrobar un candidat\n{PARTS[0][1][0]}\n{PARTS[0][1][1]}\n</parts_anteriors>"
    reviewed = (
        f"<part_a_revisar>\nAcotar el quocient\n[1] {flawed.fragments[0]}\n[2] {flawed.fragments[1]}\n</part_a_revisar>"
    )
    assert request.user == f"{earlier}\n\n{reviewed}"
    assert PARTS[1][1][0] not in request.user and PARTS[2][1][0] not in request.user
    assert "error" not in request.user.lower()
    schema = json.dumps(request.schema)
    assert '"enum": [1, 2]' in schema and '"alerta_context": {"type": "string"}' in schema


async def test_a_part_check_without_earlier_parts_says_so() -> None:
    llm = ScriptedLLMClient({Stage.MISTAKES_VERIFICATION: [part_checked()]})
    await LLMPartVerifier(llm).verify(theory_source(), [], ResolutionPart(title="Enunciat", step="", fragments=["x"]))
    assert llm.requests[Stage.MISTAKES_VERIFICATION][0].user.startswith("<parts_anteriors>\n(cap)\n</parts_anteriors>")


async def test_a_part_grading_sees_the_view_and_only_the_part_s_error() -> None:
    doc = parted()
    view = doc.view(3)
    e2 = doc.mistakes[1]
    located = locate_annotations(view, [Annotation(id="a", fragment=6, start=e2.start, end=e2.end, comment="és 0")])
    llm = ScriptedLLMClient({Stage.MISTAKES_GRADING: [{"avaluacions": [], "resum": ""}]})
    await LLMAnnotationGrader(llm).grade(problem_source(), view, located)
    request = llm.requests[Stage.MISTAKES_GRADING][0]
    assert f"[4] {PARTS[1][1][1]}" in request.user and "[6] Per tant el límit és $1$." in request.user
    assert "[e2] fragment 6" in request.user and "[e1]" not in request.user
    assert request.schema is not None and '"enum": ["e2", "cap"]' in json.dumps(request.schema)
