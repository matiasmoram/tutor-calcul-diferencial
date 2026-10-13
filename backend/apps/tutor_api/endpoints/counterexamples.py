""" "Construeix el contraexemple": the student builds f with the properties a challenge asks for; sympy checks it.
No model is called: every verdict comes from code."""

from fastapi import APIRouter, Depends

from apps.tutor_api.dependencies import domain_errors, get_counterexamples, get_sympy_pool, is_professor, rate_limited
from apps.tutor_api.schemas.counterexamples import (
    SpecResponse,
    SpecSummaryResponse,
    SubmissionRequest,
    SubmissionResponse,
)
from core.counterexamples.application.submission_grader import SubmissionGrader, SubmissionGraderInput
from core.counterexamples.domain.entities.spec import SpecCatalog
from core.counterexamples.domain.values.spec_id import spec_id_of
from core.counterexamples.infra.pool_property_checker import PoolPropertyChecker
from core.shared.math.infra.sympy_pool import SympyCheckPool

router = APIRouter()


def _get_grader(
    catalog: SpecCatalog = Depends(get_counterexamples), pool: SympyCheckPool = Depends(get_sympy_pool)
) -> SubmissionGrader:
    return SubmissionGrader(catalog, PoolPropertyChecker(pool))


@router.get("/api/contraexemples")
async def list_specs(catalog: SpecCatalog = Depends(get_counterexamples)) -> list[SpecSummaryResponse]:
    return [SpecSummaryResponse.from_entity(s) for s in catalog.specs.values()]


@router.get("/api/contraexemples/{spec_id}")
async def get_spec(
    spec_id: str,
    catalog: SpecCatalog = Depends(get_counterexamples),
    professor: bool = Depends(is_professor),
) -> SpecResponse:
    with domain_errors():
        return SpecResponse.build(catalog.spec(spec_id_of(spec_id)), with_example=professor)


@router.post("/api/contraexemples/{spec_id}/comprova", dependencies=[Depends(rate_limited)])
async def check_submission(
    spec_id: str,
    body: SubmissionRequest,
    grader: SubmissionGrader = Depends(_get_grader),
    professor: bool = Depends(is_professor),
) -> SubmissionResponse:
    """Rate limited like the model calls: each submission keeps sympy workers busy for up to the pool's deadline."""
    with domain_errors():
        result = await grader.grade(
            SubmissionGraderInput(spec_id=spec_id_of(spec_id), submission=body.to_domain(), reveal_example=professor)
        )
    return SubmissionResponse.from_entity(result)
