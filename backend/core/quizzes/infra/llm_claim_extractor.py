from collections.abc import Sequence

from core.quizzes.domain.entities.grading import StudentCheck
from core.quizzes.domain.ports import ClaimExtractor
from core.quizzes.domain.values.grading_inputs import AnsweredStatement, StudentClaims
from core.quizzes.infra.llm_outputs import objects, parse_all
from core.quizzes.infra.llm_schemas import extraction_schema
from core.quizzes.infra.prompts import EXTRACTION_SYSTEM, extraction_request
from core.shared.llm.client import LLMClient, LLMRequest, Stage


class LLMClaimExtractor(ClaimExtractor):
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    async def extract(self, answered: Sequence[AnsweredStatement]) -> list[StudentClaims]:
        # No context: the transcriber must not see the notes or the solutions.
        data, _ = await self._llm.structured(
            Stage.QUIZ_EXTRACTION,
            LLMRequest(
                system=EXTRACTION_SYSTEM,
                user=extraction_request(answered),
                schema=extraction_schema([a.statement.id for a in answered]),
            ),
        )
        return [
            StudentClaims(
                statement_id=str(raw["id"]),
                checks=parse_all(StudentCheck, objects(raw, "comprovacions"), Stage.QUIZ_EXTRACTION),
            )
            for raw in objects(data, "respostes")
            if raw.get("id")
        ]
