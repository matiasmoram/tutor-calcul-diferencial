"""The quiz generation under failures and load: lost calls, truncation, surplus drafts, deadline, concurrency, and
the cost policy of the provider."""

import asyncio
from collections.abc import Mapping, Sequence
from random import Random

import pytest

from core.quizzes.application.quiz_generator import QuizGenerator
from core.quizzes.application.quiz_provider import QuizNotReadyException, QuizProvider
from core.quizzes.domain.exceptions import QuizGenerationException
from core.quizzes.domain.values.quiz_id import QuizId
from core.quizzes.infra.llm_blind_solver import LLMBlindSolver
from core.quizzes.infra.llm_quiz_auditor import LLMQuizAuditor
from core.quizzes.infra.llm_quiz_writer import LLMQuizWriter
from core.quizzes.infra.sqlmodel_repository import SQLModelQuizRepository
from core.quizzes.infra.sympy_check_evaluator import SympyCheckEvaluator
from core.shared.domain.single_flight import SingleFlight
from core.shared.llm.client import (
    CallMeta,
    JsonObject,
    LLMProviderError,
    LLMRequest,
    MalformedOutputError,
    Stage,
    TruncatedOutputError,
)
from core.shared.storage.session_provider import SQLModelSessionProvider
from tests.core.quizzes.builders import QUIZ_ID, FixedClock, generator, item, ok_audit, ok_solver, quiz, source
from tests.fakes.llm import ScriptedLLMClient


class SlowLLM(ScriptedLLMClient):
    """The scripted model, answering after `delay` seconds."""

    def __init__(self, script: Mapping[Stage, Sequence[JsonObject | Exception]], delay: float) -> None:
        super().__init__(script)
        self._delay = delay

    async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
        await asyncio.sleep(self._delay)
        return await super().structured(stage, request)


def batch(*statements: tuple[str, str]) -> JsonObject:
    return {"afirmacions": [item(text, verdict) for text, verdict in statements]}


# facil: 6 statements, 3 or 4 false. Seven valid drafts: only 5 fit the first verification (4 false at most).
SEVEN = batch(("F1.", "fals"), ("F2.", "fals"), ("F3.", "fals"), ("F4.", "fals"), ("C1.", "cert"), ("C2.", "cert"),
              ("C3.", "cert"))  # fmt: skip


def surplus_script() -> dict[Stage, list[JsonObject | Exception]]:
    return {
        Stage.QUIZ_GENERATION: [SEVEN],
        Stage.QUIZ_VERIFICATION: [ok_solver(["fals"] * 4 + ["cert"]), ok_solver(["cert"])],
        Stage.QUIZ_AUDIT: [ok_audit(5), ok_audit(1)],
    }


async def test_surplus_drafts_wait_for_the_next_round_instead_of_being_verified_and_dropped() -> None:
    llm = ScriptedLLMClient(surplus_script())
    q = await generator(llm).generate(source(), "facil")
    assert sorted(s.statement for s in q.statements) == ["C1.", "C2.", "F1.", "F2.", "F3.", "F4."]
    assert llm.calls(Stage.QUIZ_GENERATION) == 1  # the second round needed no writer call
    first, second = (r.user for r in llm.requests[Stage.QUIZ_VERIFICATION])
    assert "C2." not in first and "C2." in second and "C3." not in second
    assert q.verification is not None and [r.requested for r in q.verification.rounds] == [5, 0]


async def test_a_lost_call_costs_its_round_not_the_statements_already_verified() -> None:
    llm = ScriptedLLMClient(
        {
            Stage.QUIZ_GENERATION: [
                batch(("F1.", "fals"), ("F2.", "fals"), ("C1.", "cert")),
                batch(("F3.", "fals"), ("C2.", "cert"), ("C3.", "cert")),
            ],
            Stage.QUIZ_VERIFICATION: [
                ok_solver(["fals", "fals", "cert"]),
                MalformedOutputError("quiz_verification: character U+0000 in the model's output"),
                ok_solver(["fals", "cert", "cert"]),
            ],
            Stage.QUIZ_AUDIT: [ok_audit(3), ok_audit(3), ok_audit(3)],
        }
    )
    q = await generator(llm).generate(source(), "facil")
    assert len(q.statements) == 6
    # Round 2 lost its verification: its valid statements were verified in round 3 without writing new ones.
    assert llm.calls(Stage.QUIZ_GENERATION) == 2 and llm.calls(Stage.QUIZ_VERIFICATION) == 3
    assert q.verification is not None and [r.accepted_total for r in q.verification.rounds] == [3, 3, 6]


async def test_a_lost_writer_call_does_not_end_the_generation() -> None:
    llm = ScriptedLLMClient(
        {
            Stage.QUIZ_GENERATION: [
                batch(("F1.", "fals"), ("F2.", "fals"), ("C1.", "cert")),
                MalformedOutputError("quiz_generation: invalid JSON from the model"),
                batch(("F3.", "fals"), ("C2.", "cert"), ("C3.", "cert")),
            ],
            Stage.QUIZ_VERIFICATION: [ok_solver(["fals", "fals", "cert"]), ok_solver(["fals", "cert", "cert"])],
            Stage.QUIZ_AUDIT: [ok_audit(3), ok_audit(3)],
        }
    )
    q = await generator(llm).generate(source(), "facil")
    assert len(q.statements) == 6 and q.verification is not None and len(q.verification.rounds) == 3


async def test_a_truncated_round_is_asked_again_with_half_the_batch() -> None:
    pairs = [batch((f"F{i}.", "fals"), (f"C{i}.", "cert")) for i in range(1, 4)]
    llm = ScriptedLLMClient(
        {
            Stage.QUIZ_GENERATION: [TruncatedOutputError("quiz_generation: output truncated"), *pairs],
            Stage.QUIZ_VERIFICATION: [ok_solver(["fals", "cert"])] * 3,
            Stage.QUIZ_AUDIT: [ok_audit(2)] * 3,
        }
    )
    q = await generator(llm).generate(source(), "facil")
    assert len(q.statements) == 6
    requests = [r.user for r in llm.requests[Stage.QUIZ_GENERATION]]
    assert "EXACTAMENT 5 " in requests[0] and all("EXACTAMENT 2 " in r for r in requests[1:])
    # The truncated attempt is retried as the same round, not counted against the budget.
    assert q.verification is not None and [r.round for r in q.verification.rounds] == [1, 2, 3]


async def test_a_provider_failure_still_fails_at_once() -> None:
    llm = ScriptedLLMClient({Stage.QUIZ_GENERATION: [LLMProviderError("401"), SEVEN]})
    with pytest.raises(LLMProviderError):
        await generator(llm).generate(source(), "facil")
    assert llm.calls(Stage.QUIZ_GENERATION) == 1


async def test_the_generation_has_a_deadline() -> None:
    llm = SlowLLM(surplus_script(), delay=1.0)
    gen = QuizGenerator(
        LLMQuizWriter(llm),
        LLMBlindSolver(llm),
        LLMQuizAuditor(llm),
        SympyCheckEvaluator(in_process=True),
        FixedClock(),
        Random(0),
        deadline_s=0.05,
    )
    with pytest.raises(QuizGenerationException) as e:
        await gen.generate(source(), "facil")
    assert e.value.error_code == 502 and "no s'ha pogut generar el qüestionari en" in e.value.message


async def test_concurrent_requests_share_one_generation(session_provider: SQLModelSessionProvider) -> None:
    llm = SlowLLM(surplus_script(), delay=0.05)  # scripted for one generation only
    repo = SQLModelQuizRepository(session_provider)
    generations = SingleFlight()
    providers = [QuizProvider(repo, generator(llm), Random(i), generations=generations) for i in range(3)]
    provided = await asyncio.gather(*(p.get_or_generate(source(), "facil") for p in providers))
    assert len({p.quiz.id for p in provided}) == 1 and all(p.generated_now for p in provided)
    assert llm.calls(Stage.QUIZ_GENERATION) == 1
    assert len(await repo.of_source(source().id, "facil")) == 1
    assert not generations.in_flight((source().id, "facil"))


async def test_without_generation_rights_new_picks_another_stored_quiz(
    session_provider: SQLModelSessionProvider,
) -> None:
    repo = SQLModelQuizRepository(session_provider)
    await repo.add(quiz())
    await repo.add(quiz().model_copy(update={"id": QuizId("bbbbbbbbbbbb")}))
    llm = ScriptedLLMClient({})
    provider = QuizProvider(repo, generator(llm), Random(0), may_generate=False)
    assert not await provider.will_generate(source(), "facil", new=True)
    for _ in range(5):
        provided = await provider.get_or_generate(source(), "facil", new=True, except_id=QUIZ_ID)
        assert provided.quiz.id == "bbbbbbbbbbbb" and not provided.generated_now
    assert llm.calls(Stage.QUIZ_GENERATION) == 0


async def test_without_generation_rights_a_new_source_is_a_409(session_provider: SQLModelSessionProvider) -> None:
    llm = ScriptedLLMClient({})
    provider = QuizProvider(SQLModelQuizRepository(session_provider), generator(llm), Random(0), may_generate=False)
    assert not await provider.will_generate(source(), "facil")
    with pytest.raises(QuizNotReadyException) as e:
        await provider.get_or_generate(source(), "facil")
    assert e.value.error_code == 409 and "demana-ho al professorat" in e.value.message
    assert llm.calls(Stage.QUIZ_GENERATION) == 0
