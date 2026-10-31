"""Builders for the quiz tests: the models' JSON outputs (Catalan keys, as the LLM writes them), a small quiz and the
wiring of the use cases."""

from collections.abc import Coroutine, Sequence
from random import Random

from core.quizzes.application.answers_grader import AnswersGrader, AnswersGraderInput
from core.quizzes.application.hint_revealer import HintRevealer
from core.quizzes.application.quiz_generator import QuizGenerator
from core.quizzes.application.quiz_provider import QuizProvider
from core.quizzes.application.quiz_session_starter import QuizSessionStarter, QuizSessionStarterInput
from core.quizzes.domain.entities.grading import Answer
from core.quizzes.domain.entities.quiz import Quiz
from core.quizzes.domain.entities.statement import Statement
from core.quizzes.domain.sources import QuizSource, quiz_source
from core.quizzes.domain.values.quiz_id import QuizId
from core.quizzes.infra.llm_answer_grader import LLMAnswerGrader
from core.quizzes.infra.llm_blind_solver import LLMBlindSolver
from core.quizzes.infra.llm_claim_extractor import LLMClaimExtractor
from core.quizzes.infra.llm_quiz_auditor import LLMQuizAuditor
from core.quizzes.infra.llm_quiz_writer import LLMQuizWriter
from core.quizzes.infra.sqlmodel_repository import SQLModelQuizRepository, SQLModelQuizSessionRepository
from core.quizzes.infra.sympy_check_evaluator import SympyCheckEvaluator
from core.shared.domain.clock import Clock
from core.shared.llm.client import CallMeta, JsonObject, LLMClient, LLMRequest, Stage
from core.shared.storage.session_provider import SQLModelSessionProvider
from tests.fakes.llm import ScriptedLLMClient
from tests.fixtures.course import authored_course

QUIZ_ID = "0123456789ab"


class FixedClock(Clock):
    def __init__(self, now: float = 1_700_000_000.0) -> None:
        self._now = now

    def now(self) -> float:
        return self._now

    def monotonic(self) -> float:
        return self._now


def source(source_id: str = "tema-2") -> QuizSource:
    return quiz_source(authored_course(), source_id)


def check(kind: str, expression: str, value: str = "", variable: str = "x", point: str = "0") -> JsonObject:
    return {"descripcio": "c", "tipus": kind, "expressio": expression, "variable": variable, "punt": point,
            "costat": "ambdos", "valor": value}  # fmt: skip


ITERATED = check("limit", "x*(m*x)/(x**2+(m*x)**2)", "m/(1+m**2)")


def item(statement: str, verdict: str = "fals", checks: Sequence[JsonObject] = (), **kw: object) -> JsonObject:
    return {
        "enunciat": statement,
        "veredicte": verdict,
        "trampa": "reciproc" if verdict == "fals" else "cert_resultat",
        "concepte": "Límits iterats",
        "contraexemple": "$f(x,y)=\\frac{xy}{x^2+y^2}$" if verdict == "fals" else "",
        "resolucio": "Resolució completa.",
        "idees_clau": ["idea"],
        "pista": "Què et diuen els iterats sobre la resta de camins?",
        "teoria": ["T2.12"],
        "comprovacions": list(checks),
    } | kw


def ok_solver(verdicts: Sequence[str]) -> JsonObject:
    return {
        "respostes": [
            {"num": i, "veredicte": v, "confianca": "alta", "ben_plantejada": True, "justificacio": "j"}
            for i, v in enumerate(verdicts, 1)
        ]
    }


def ok_audit(n: int) -> JsonObject:
    return {
        "revisions": [
            {"num": i, "resolucio_correcta": True, "teoria_correcta": True, "pista_neutra": True, "problemes": ""}
            for i in range(1, n + 1)
        ]
    }


def idea(num: int, quote: str) -> JsonObject:
    return {"num": num, "cita": quote}


def grader(*evaluations: JsonObject, summary: str = "r") -> JsonObject:
    return {"avaluacions": list(evaluations), "resum": summary}


def transcriber(**per_id: list[JsonObject]) -> JsonObject:
    return {"respostes": [{"id": k, "comprovacions": v} for k, v in per_id.items()]}


def statement(sid: str, text: str, verdict: str, counterexample: str = "") -> Statement:
    return Statement.model_validate(
        {"id": sid, "enunciat": text, "veredicte": verdict, "concepte": "c",
         "trampa": "reciproc" if verdict == "fals" else "cert_resultat", "contraexemple": counterexample,
         "resolucio": "r", "idees_clau": ["i"], "pista": "p"}
    )  # fmt: skip


def quiz() -> Quiz:
    return Quiz(
        id=QuizId(QUIZ_ID),
        source_id="tema-2",
        topic=2,
        difficulty="facil",
        statements=[
            statement("a1", "A.", "fals", "xy"),
            statement("a2", "B.", "cert"),
            statement("a3", "C.", "fals", "z"),
            statement("a4", "D.", "cert"),
        ],
        created=1.0,
    )


def generator(llm: LLMClient, rng: Random | None = None) -> QuizGenerator:
    return QuizGenerator(
        LLMQuizWriter(llm),
        LLMBlindSolver(llm),
        LLMQuizAuditor(llm),
        SympyCheckEvaluator(in_process=True),
        FixedClock(),
        rng or Random(0),
    )


def answers_grader(llm: LLMClient, provider: SQLModelSessionProvider, clock: Clock | None = None) -> AnswersGrader:
    return AnswersGrader(
        authored_course(),
        SQLModelQuizSessionRepository(provider),
        SQLModelQuizRepository(provider),
        LLMAnswerGrader(llm),
        LLMClaimExtractor(llm),
        SympyCheckEvaluator(in_process=True),
        clock or FixedClock(),
    )


def starter(provider: SQLModelSessionProvider, llm: LLMClient | None = None) -> QuizSessionStarter:
    quizzes = SQLModelQuizRepository(provider)
    quiz_provider = QuizProvider(quizzes, generator(llm or ScriptedLLMClient({})), Random(0))
    return QuizSessionStarter(authored_course(), quiz_provider, SQLModelQuizSessionRepository(provider), FixedClock())


def hints(provider: SQLModelSessionProvider) -> HintRevealer:
    return HintRevealer(SQLModelQuizSessionRepository(provider), SQLModelQuizRepository(provider), FixedClock())


async def started_session(provider: SQLModelSessionProvider) -> str:
    await SQLModelQuizRepository(provider).add(quiz())
    started = await starter(provider).start(QuizSessionStarterInput(source_id="tema-2", difficulty="facil"))
    return started.session.id


ANSWERS = AnswersGraderInput(answers=[Answer(statement_id="a1", verdict="fals", justification="sobre $y=x$")])


def graded(feedback: str = "f") -> JsonObject:
    return grader({"id": "a1", "idees": [idea(1, "sobre $y=x$")], "justificacio": "correcta", "feedback": feedback})


class InterleavingLLM(ScriptedLLMClient):
    """While the first grading waits for its grader call, `meanwhile` runs (a second submission)."""

    meanwhile: Coroutine[object, object, None] | None = None

    async def structured(self, stage: Stage, request: LLMRequest) -> tuple[JsonObject, CallMeta]:
        if stage == Stage.QUIZ_GRADING and self.meanwhile is not None:
            pending, self.meanwhile = self.meanwhile, None
            await pending
        return await super().structured(stage, request)
