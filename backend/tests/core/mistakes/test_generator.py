import asyncio
import random
from collections.abc import Mapping, Sequence

import pytest

from core.mistakes.application.mistake_exercise_generator import MistakeExerciseGenerator
from core.mistakes.application.mistake_exercise_provider import MistakeExerciseProvider, MistakeGenerations
from core.mistakes.domain.exceptions import MistakeGenerationFailedException, MistakeGenerationTimeoutException
from core.mistakes.infra.json_file_source import JsonFileMistakeSource
from core.mistakes.infra.llm_mistake_generator import LLMMistakeGenerator
from core.mistakes.infra.llm_mistake_verifier import LLMMistakeVerifier
from core.mistakes.infra.llm_schemas import generation_schema
from core.mistakes.infra.sqlmodel_repository import SQLModelMistakeExerciseRepository
from core.shared.domain.single_flight import SingleFlight
from core.shared.llm.client import CallMeta, JsonObject, LLMRequest, Stage
from core.shared.storage.session_provider import SQLModelSessionProvider
from tests.core.mistakes.builders import (
    FixedClock,
    err,
    exercise_generator,
    finding,
    gen,
    problem_source,
    terr,
    tgen,
    theory_source,
)
from tests.fakes.llm import ScriptedLLMClient


async def test_generate_regenerates_until_verified(session_provider: SQLModelSessionProvider, tmp_path) -> None:
    bad_quote = gen([err(2, "no hi és")])
    good = gen([err(2, "$x^4 \\ge x^4+y^2$")])
    llm = ScriptedLLMClient(
        {
            Stage.MISTAKES_GENERATION: [bad_quote, good, good],
            Stage.MISTAKES_VERIFICATION: [
                {"problemes": [finding(3, "demostra", "error", "salt"), finding(2, "x")], "valoracio": ""},
                {"problemes": [finding(2, "x")], "valoracio": "ok"},
            ],
        }
    )
    sol = await exercise_generator(llm).generate(problem_source(), "facil")
    log = sol.verification.attempts or []
    assert len(log) == 3 and log[0].validation and log[1].discrepancies and not log[2].discrepancies
    assert log[0].verification is None and log[2].verification is not None
    # Feedback from the failed attempts reaches the generator.
    gen_prompts = [r.user for r in llm.requests[Stage.MISTAKES_GENERATION]]
    assert "no apareix literalment" in gen_prompts[1] and "NO intencionat" in gen_prompts[2]
    # The verifier never sees the declared errors.
    ver_prompt = llm.requests[Stage.MISTAKES_VERIFICATION][0].user
    assert "correccio" not in ver_prompt and "pista" not in ver_prompt and "no hi és" not in ver_prompt
    # The solution sheet travels as the cacheable context, identical for generation and verification.
    ctxs = {r.context for stage in llm.requests for r in llm.requests[stage]}
    assert len(ctxs) == 1 and "RESULTAT CORRECTE" in str(next(iter(ctxs)))
    assert sol.n_mistakes == 1 and sol.verification.origin == "llm" and sol.verification.assessment == "ok"

    repo = SQLModelMistakeExerciseRepository(session_provider)
    await repo.save(sol)
    assert (await repo.of_source("t2-4c", "facil"))[0].id == sol.id
    files = JsonFileMistakeSource(tmp_path)
    assert files.save(sol) == tmp_path / "t2-4c" / "facil" / f"{sol.id}.json"
    assert files.load() == [sol]


class SlowLLM(ScriptedLLMClient):
    """The scripted model, answering after `delay` seconds."""

    def __init__(self, script: Mapping[Stage, Sequence[JsonObject | Exception]], delay: float) -> None:
        super().__init__(script)
        self._delay = delay

    async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
        await asyncio.sleep(self._delay)
        return await super().structured(stage, request)


def verified_script() -> dict[Stage, list[JsonObject | Exception]]:
    """One generation that passes validation and verification at the first attempt."""
    return {
        Stage.MISTAKES_GENERATION: [gen([err(2, "$x^4 \\ge x^4+y^2$")])],
        Stage.MISTAKES_VERIFICATION: [{"problemes": [finding(2, "x")], "valoracio": "ok"}],
    }


async def test_a_generation_past_its_deadline_fails() -> None:
    llm = SlowLLM(verified_script(), delay=30)
    generator = MistakeExerciseGenerator(LLMMistakeGenerator(llm), LLMMistakeVerifier(llm), FixedClock(), 0.05)
    with pytest.raises(MistakeGenerationTimeoutException) as e:
        await asyncio.wait_for(generator.generate(problem_source(), "facil"), 10)
    assert e.value.error_code == 502 and "no s'ha pogut generar el document en" in e.value.message


async def test_concurrent_requests_share_one_generation(session_provider: SQLModelSessionProvider) -> None:
    llm = SlowLLM(verified_script(), delay=0.05)  # scripted for one generation only
    repo = SQLModelMistakeExerciseRepository(session_provider)
    generations: MistakeGenerations = SingleFlight()
    providers = [
        MistakeExerciseProvider(repo, exercise_generator(llm), random.Random(i), generations=generations)
        for i in range(3)
    ]
    provided = await asyncio.gather(*(p.get_or_generate(problem_source(), "facil") for p in providers))
    assert len({p.exercise.id for p in provided}) == 1 and all(p.freshly_generated for p in provided)
    assert llm.calls(Stage.MISTAKES_GENERATION) == 1
    assert len(await repo.of_source("t2-4c", "facil")) == 1
    assert not generations.in_flight(("problema", "t2-4c", "facil"))


async def test_generate_gives_up_after_max_attempts() -> None:
    llm = ScriptedLLMClient({Stage.MISTAKES_GENERATION: [gen([])] * 3})
    with pytest.raises(MistakeGenerationFailedException) as e:
        await exercise_generator(llm).generate(problem_source(), "normal")
    assert e.value.error_code == 502 and "3 intents" in e.value.message
    assert llm.calls(Stage.MISTAKES_GENERATION) == 3 and llm.calls(Stage.MISTAKES_VERIFICATION) == 0


async def test_theory_generation_uses_notes_as_reference_and_never_shows_errors_to_verifier() -> None:
    source = theory_source("T3.21")
    good = tgen([terr(1, "diferenciable"), terr(5, "les parcials són contínues", "pas_injustificat")])
    llm = ScriptedLLMClient(
        {
            Stage.MISTAKES_GENERATION: [good],
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
        }
    )
    sol = await exercise_generator(llm).generate(source, "normal")
    assert sol.source_kind == "teoria" and sol.source_id == "T3.21" and sol.statement_fragments == 2
    assert sol.model_dump()["n_enunciat"] == 2 and sol.model_dump()["font"] == "teoria"
    ctx = str(llm.requests[Stage.MISTAKES_GENERATION][0].context)
    assert "versió CORRECTA" in ctx and source.item.proof.strip()[:40] in ctx
    ver = llm.requests[Stage.MISTAKES_VERIFICATION][0].user
    assert "(enunciat)" in ver and "(demostració)" in ver and "pista" not in ver
    # The generator's schema asks for the statement split.
    required = generation_schema(True)["required"]
    assert isinstance(required, list) and "n_enunciat" in required
