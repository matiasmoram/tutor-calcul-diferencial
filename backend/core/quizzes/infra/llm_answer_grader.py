from collections.abc import Sequence

from core.quizzes.domain.sources import QuizSource
from core.quizzes.domain.values.grading_inputs import (
    AnsweredStatement,
    GraderEvaluation,
    GraderVerdict,
    IdeaCitation,
)
from core.quizzes.infra.llm_outputs import objects, parse_all
from core.quizzes.infra.llm_schemas import grading_schema
from core.quizzes.infra.prompts import GRADING_SYSTEM, grading_request, source_context
from core.shared.llm.client import LLMClient, LLMRequest, Stage


class LLMAnswerGrader:
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    async def grade(self, source: QuizSource, answered: Sequence[AnsweredStatement]) -> GraderVerdict:
        data, meta = await self._llm.structured(
            Stage.QUIZ_GRADING,
            LLMRequest(
                system=GRADING_SYSTEM,
                user=grading_request(answered),
                schema=grading_schema([a.statement.id for a in answered]),
                context=source_context(source),
            ),
        )
        evaluations = [
            GraderEvaluation(
                statement_id=str(raw["id"]),
                ideas=parse_all(
                    IdeaCitation, [i for i in objects(raw, "idees") if _integer(i.get("num"))], Stage.QUIZ_GRADING
                ),
                justification=_text(raw.get("justificacio")),
                feedback=str(raw.get("feedback", "")),
            )
            for raw in objects(data, "avaluacions")
            if raw.get("id")
        ]
        summary = data.get("resum", "")
        return GraderVerdict(evaluations=evaluations, summary=str(summary), call=meta.usage())


def _text(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)
