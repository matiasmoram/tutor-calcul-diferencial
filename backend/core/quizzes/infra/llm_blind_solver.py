from collections.abc import Sequence

from core.quizzes.domain.values.drafts import StatementDraft
from core.quizzes.domain.values.quiz_source import QuizSource
from core.quizzes.domain.values.verification import SolverAnswer, SolverAnswers
from core.quizzes.infra.llm_outputs import objects, parse_all
from core.quizzes.infra.llm_schemas import solver_schema
from core.quizzes.infra.prompts import SOLVER_SYSTEM, solver_request, source_context
from core.shared.llm.client import LLMClient, LLMRequest, Stage


class LLMBlindSolver:
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    async def solve(self, source: QuizSource, drafts: Sequence[StatementDraft]) -> SolverAnswers:
        data, meta = await self._llm.structured(
            Stage.QUIZ_VERIFICATION,
            LLMRequest(
                system=SOLVER_SYSTEM,
                user=solver_request(drafts),
                schema=solver_schema(),
                context=source_context(source),
            ),
        )
        answers = parse_all(SolverAnswer, objects(data, "respostes"), Stage.QUIZ_VERIFICATION)
        return SolverAnswers(answers=answers, call=meta.usage())
