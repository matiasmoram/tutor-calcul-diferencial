import asyncio
import re
from collections.abc import Mapping, Sequence

import pytest

from core.mistakes.domain.entities.parted_mistake_exercise import PartedMistakeExercise
from core.mistakes.domain.exceptions import (
    MistakeGenerationFailedException,
    MistakeGenerationTimeoutException,
    MistakePartsUnavailableException,
)
from core.mistakes.domain.values.mistake_source import ProblemSource
from core.shared.llm.client import CallMeta, JsonObject, LLMError, LLMRequest, Stage
from tests.core.mistakes.builders import (
    PART1_ERROR,
    PART2_ERROR,
    PART3_ERROR,
    PARTS,
    THEORY_PARTS,
    corruption,
    edit,
    finding,
    part_checked,
    parted_generator,
    problem_source,
    resolution_checked,
    seed_choosing,
    theory_source,
    theory_written,
    written,
)
from tests.fakes.llm import ScriptedLLMClient

type Outputs = list[JsonObject | Exception]

# What the blind part check answers when it finds exactly the declared error.
PART2_FOUND = part_checked(finding(1, "x^4 \\ge"))
PART3_FOUND = part_checked(finding(2, "és $1$"))
PART1_FOUND = part_checked(finding(1, "tendeix a $1$"))
TITLES = {"Trobar un candidat": 1, "Acotar el quocient": 2, "Concloure amb el sandvitx": 3}
STATEMENT_ERROR = corruption(
    [edit(1, "de classe $\\mathcal{C}^1$", "diferenciable")], "diferenciable", tipus="hipotesi"
)
STATEMENT_FOUND = part_checked(finding(1, "diferenciable"))
THEORY_TITLES = {"Enunciat": 1, **{t: i for i, (t, _) in enumerate(THEORY_PARTS, 2)}}


class PartRouter(ScriptedLLMClient):
    """Stage A and its check come from the script in order; stages B and C answer by the part they are about, each
    part with its own script, after `delay` seconds (so the chains of different parts interleave)."""

    def __init__(
        self,
        script: Mapping[Stage, Sequence[JsonObject | Exception]],
        parts: Mapping[int, Mapping[Stage, Outputs]],
        titles: Mapping[str, int] = TITLES,
        delay: float = 0.0,
    ) -> None:
        super().__init__(script)
        self._parts = {p: {stage: list(o) for stage, o in by_stage.items()} for p, by_stage in parts.items()}
        self._titles = titles
        self._delay = delay
        self.log: list[tuple[Stage, int]] = []
        self.by_part: dict[int, list[LLMRequest]] = {}

    def part_of(self, request: LLMRequest) -> int | None:
        if m := re.match(r"Introdueix UN error a la part (\d+)", request.user):
            return int(m.group(1))
        if m := re.search(r"<part_a_revisar>\n(.*)\n", request.user):
            return self._titles[m.group(1)]
        return None

    async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
        part = self.part_of(request)
        if part is None:
            return await super().structured(stage, request)
        self.requests[stage].append(request)
        self.by_part.setdefault(part, []).append(request)
        self.log.append((stage, part))
        await asyncio.sleep(self._delay)
        outputs = self._parts.get(part, {}).get(stage)
        if not outputs:
            raise LLMError(f"{stage} part {part}: script exhausted")
        out = outputs.pop(0)
        if isinstance(out, Exception):
            raise out
        return out, CallMeta(stage=stage, model="scripted", latency_ms=1, input_tokens=10, output_tokens=2)


def stage_a() -> dict[Stage, Outputs]:
    """Stage A written right at once and checked clean."""
    return {Stage.MISTAKES_GENERATION: [written()], Stage.MISTAKES_VERIFICATION: [resolution_checked(True)]}


def theory_a() -> dict[Stage, Outputs]:
    """A theory resolution written right at once and checked clean."""
    return {Stage.MISTAKES_GENERATION: [theory_written()], Stage.MISTAKES_VERIFICATION: [resolution_checked(True)]}


def chain(*steps: tuple[JsonObject, JsonObject | None]) -> dict[Stage, Outputs]:
    """One part's B→C attempts: (corruption, part check), the check None when the gates refuse the corruption."""
    return {
        Stage.MISTAKES_GENERATION: [b for b, _ in steps],
        Stage.MISTAKES_VERIFICATION: [c for _, c in steps if c is not None],
    }


async def test_a_per_parts_document_from_the_correct_resolution() -> None:
    llm = PartRouter(stage_a(), {2: chain((PART2_ERROR, PART2_FOUND)), 3: chain((PART3_ERROR, PART3_FOUND))})
    doc = await parted_generator(llm, seed=seed_choosing(2, 3)).generate(problem_source(), "normal")
    assert isinstance(doc, PartedMistakeExercise) and doc.layout == "per_parts"
    assert doc.flawed_parts == [2, 3] and [m.id for m in doc.mistakes] == ["e1", "e2"]
    assert [m.fragment for m in doc.mistakes] == [3, 6] and doc.fragments == [x for _, fs in PARTS for x in fs]
    assert doc.parts[2].flawed_fragments == [PARTS[2][1][0], "Per tant el límit és $1$."]
    assert doc.verification.origin == "llm" and doc.verification.attempts is not None
    part_check = doc.parts[1].verification
    assert part_check is not None and part_check.attempts is not None and len(part_check.attempts) == 1
    assert part_check.findings[0].quote == "x^4 \\ge"
    # Stage B always starts from the correct text: one cached context for every part.
    contexts = {r.context for r in llm.requests[Stage.MISTAKES_GENERATION][1:]}
    assert len(contexts) == 1 and "<resolucio_correcta>" in str(next(iter(contexts)))
    # Stage C sees the earlier parts correct and never the clean text of its part nor the later parts.
    (check3,) = [r for r in llm.by_part[3] if "<part_a_revisar>" in r.user]
    assert PARTS[1][1][0] in check3.user and PARTS[2][1][1] not in check3.user
    (check2,) = [r for r in llm.by_part[2] if "<part_a_revisar>" in r.user]
    assert PARTS[1][1][0] not in check2.user and PARTS[2][1][0] not in check2.user


async def test_stage_a_regenerates_with_the_gates_and_blind_check_reasons() -> None:
    unordered = written([PARTS[1], PARTS[0], PARTS[2]])
    llm = PartRouter(
        {
            Stage.MISTAKES_GENERATION: [unordered, written(), written()],
            Stage.MISTAKES_VERIFICATION: [
                resolution_checked(True, finding(3, "x^4 \\le", "error", "fals")),
                resolution_checked(True),
            ],
        },
        {2: chain((PART2_ERROR, PART2_FOUND)), 3: chain((PART3_ERROR, PART3_FOUND))},
    )
    doc = await parted_generator(llm, seed=seed_choosing(2, 3)).generate(problem_source(), "normal")
    attempts = doc.verification.attempts or []
    assert len(attempts) == 3 and attempts[0].validation and attempts[0].verification is None
    assert attempts[1].discrepancies == ["hi ha un error a la part 2, fragment 1: «x^4 \\le» — fals"]
    writes = [r.user for r in llm.requests[Stage.MISTAKES_GENERATION] if r.user.startswith("Escriu")]
    assert "seguir els passos" in writes[1] and "la part 2, fragment 1" in writes[2]


async def test_a_resolution_that_never_passes_fails_the_generation() -> None:
    llm = PartRouter(
        {Stage.MISTAKES_GENERATION: [written()] * 3, Stage.MISTAKES_VERIFICATION: [resolution_checked(False)] * 3},
        {},
    )
    with pytest.raises(MistakeGenerationFailedException) as e:
        await parted_generator(llm).generate(problem_source(), "normal")
    assert e.value.error_code == 502 and llm.log == []


async def test_a_corruption_refused_by_the_gates_is_retried_with_the_reasons() -> None:
    missing = corruption([edit(1, "no hi és", "x")], "x")
    llm = PartRouter(stage_a(), {2: chain((missing, None), (PART2_ERROR, PART2_FOUND))})
    doc = await parted_generator(llm, seed=seed_choosing(2, 1)).generate(problem_source(), "facil")
    assert doc.flawed_parts == [2]
    attempts = (doc.parts[1].verification and doc.parts[1].verification.attempts) or []
    assert (
        len(attempts) == 2 and attempts[0].verification is None and "exactament una vegada" in attempts[0].validation[0]
    )
    corruptions = [r.user for r in llm.by_part[2] if r.user.startswith("Introdueix")]
    assert "<correccio>" not in corruptions[0] and "exactament una vegada" in corruptions[1]


async def test_a_part_the_blind_check_keeps_refusing_is_swapped_for_an_unused_one() -> None:
    unintended = part_checked(finding(1, "x^4 \\ge"), finding(2, "Per tant", "error", "salt"))
    llm = PartRouter(stage_a(), {2: chain(*[(PART2_ERROR, unintended)] * 3), 1: chain((PART1_ERROR, PART1_FOUND))})
    doc = await parted_generator(llm, seed=seed_choosing(2, 1)).generate(problem_source(), "facil")
    assert doc.flawed_parts == [1] and doc.mistakes[0].id == "e1" and doc.mistakes[0].fragment == 1
    assert [(stage, part) for stage, part in llm.log].count((Stage.MISTAKES_VERIFICATION, 2)) == 3
    retries = [r.user for r in llm.by_part[2] if r.user.startswith("Introdueix")]
    assert "NO intencionat" in retries[1] and "NO intencionat" in retries[2]


async def test_an_unfit_part_is_swapped_at_once() -> None:
    llm = PartRouter(
        stage_a(), {2: chain((corruption([], "", apte=False), None)), 1: chain((PART1_ERROR, PART1_FOUND))}
    )
    doc = await parted_generator(llm, seed=seed_choosing(2, 1)).generate(problem_source(), "facil")
    assert doc.flawed_parts == [1] and llm.log[:2] == [(Stage.MISTAKES_GENERATION, 2), (Stage.MISTAKES_GENERATION, 1)]


async def test_with_no_unused_part_left_an_unfit_answer_is_retried_and_then_fails() -> None:
    unfit = (corruption([], "", apte=False), None)
    llm = PartRouter(stage_a(), {1: chain(unfit), 2: chain(unfit), 3: chain(*[unfit] * 3)})
    with pytest.raises(MistakeGenerationFailedException):
        await parted_generator(llm, seed=seed_choosing(2, 1, 3)).generate(problem_source(), "facil")
    assert [part for _, part in llm.log] == [2, 1, 3, 3, 3]
    retries = [r.user for r in llm.by_part[3][1:]]
    assert all("aquesta part ha de tenir un error («apte» ha de ser true)" in r for r in retries)


async def test_when_every_part_is_chosen_an_unfit_part_is_asked_again() -> None:
    unfit = corruption([], "", apte=False)
    llm = PartRouter(
        stage_a(),
        {
            1: chain((PART1_ERROR, PART1_FOUND)),
            2: chain((unfit, None), (PART2_ERROR, PART2_FOUND)),
            3: chain((PART3_ERROR, PART3_FOUND)),
        },
    )
    doc = await parted_generator(llm).generate(problem_source(), "dificil")
    assert doc.flawed_parts == [1, 2, 3]
    attempts = (doc.parts[1].verification and doc.parts[1].verification.attempts) or []
    assert len(attempts) == 2 and attempts[0].validation[0].startswith("aquesta part ha de tenir un error")


async def test_the_parts_are_corrupted_in_parallel_and_independently() -> None:
    refused = part_checked(finding(1, "Com que", "consequencia"), finding(1, "x^4 \\ge"))
    llm = PartRouter(
        stage_a(),
        {2: chain((PART2_ERROR, refused), (PART2_ERROR, PART2_FOUND)), 3: chain((PART3_ERROR, PART3_FOUND))},
        delay=0.01,
    )
    doc = await parted_generator(llm, seed=seed_choosing(2, 3)).generate(problem_source(), "normal")
    assert doc.flawed_parts == [2, 3]
    # Both corruptions are asked before either check: the chains run side by side.
    assert {llm.log[0], llm.log[1]} == {(Stage.MISTAKES_GENERATION, 2), (Stage.MISTAKES_GENERATION, 3)}
    # Part 2's rejection reaches only part 2's retry; part 3 was asked once.
    assert "anterior a l'error" in llm.by_part[2][2].user
    assert llm.by_part[3][0].user.startswith("Introdueix") and len(llm.by_part[3]) == 2
    assert all("<correccio>" not in r.user for r in llm.by_part[3])


async def test_a_generation_past_its_deadline_fails() -> None:
    llm = PartRouter(stage_a(), {2: chain((PART2_ERROR, PART2_FOUND))}, delay=30)
    generator = parted_generator(llm, seed=seed_choosing(2, 1), deadline_s=0.05)
    with pytest.raises(MistakeGenerationTimeoutException) as e:
        await asyncio.wait_for(generator.generate(problem_source(), "facil"), 10)
    assert e.value.error_code == 502


async def test_theory_always_puts_an_error_in_the_statement_and_never_swaps_it() -> None:
    llm = PartRouter(theory_a(), {1: chain((STATEMENT_ERROR, STATEMENT_FOUND))}, THEORY_TITLES)
    doc = await parted_generator(llm).generate(theory_source(), "facil")
    assert doc.source_kind == "teoria" and doc.statement_fragments == 1 and doc.flawed_parts == [1]
    assert doc.parts[0].title == "Enunciat" and doc.mistakes[0].kind == "hipotesi"
    (check,) = [r for r in llm.by_part[1] if "<part_a_revisar>" in r.user]
    assert check.user.startswith("<parts_anteriors>\n(cap)\n</parts_anteriors>")


async def test_an_unfit_statement_is_asked_again_within_its_attempts() -> None:
    unfit = (corruption([], "", apte=False), None)
    llm = PartRouter(theory_a(), {1: chain(unfit, (STATEMENT_ERROR, STATEMENT_FOUND))}, THEORY_TITLES)
    doc = await parted_generator(llm).generate(theory_source(), "facil")
    assert doc.flawed_parts == [1] and [part for _, part in llm.log] == [1, 1, 1]
    assert "l'enunciat sempre admet un error" in llm.by_part[1][1].user

    llm = PartRouter(theory_a(), {1: chain(*[unfit] * 3)}, THEORY_TITLES)
    with pytest.raises(MistakeGenerationFailedException):
        await parted_generator(llm).generate(theory_source(), "facil")
    assert [part for _, part in llm.log] == [1, 1, 1]


async def test_a_source_without_two_parts_is_refused_before_any_call() -> None:
    source = problem_source()
    single = source.exercise.model_copy(update={"steps": source.exercise.steps[:1]})
    llm = PartRouter({}, {})
    with pytest.raises(MistakePartsUnavailableException):
        await parted_generator(llm).generate(ProblemSource(exercise=single, theory=[], with_proof=frozenset()), "facil")
    assert llm.calls(Stage.MISTAKES_GENERATION) == 0
