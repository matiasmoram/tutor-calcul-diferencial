import re

import pytest

from core.counterexamples.application.submission_grader import SubmissionGrader, SubmissionGraderInput
from core.counterexamples.domain.exceptions import InvalidSubmissionException, UnknownSpecException
from core.counterexamples.domain.values.spec_id import SpecId
from core.counterexamples.domain.values.submission import Submission
from core.counterexamples.domain.values.verdict import SubmissionResult
from core.counterexamples.infra.pool_property_checker import PoolPropertyChecker
from core.shared.math.infra.sympy_pool import SympyCheckPool
from tests.fixtures.counterexamples import authored_challenges


@pytest.fixture
def grader() -> SubmissionGrader:
    return SubmissionGrader(authored_challenges(), PoolPropertyChecker(SympyCheckPool(in_process=True)))


def submission(function: str, value: str = "0", **certificates: object) -> Submission:
    return Submission.model_validate({"funcio": function, "valor": value, "certificats": certificates})


async def grade(grader: SubmissionGrader, spec_id: str, body: Submission, reveal: bool = False) -> SubmissionResult:
    return await grader.grade(SubmissionGraderInput(spec_id=SpecId(spec_id), submission=body, reveal_example=reveal))


async def test_a_counterexample_with_its_certificates_passes(grader: SubmissionGrader) -> None:
    body = submission("x*y/(x**2+y**2)", discontinua={"camins": [{"x": "t", "y": "t"}]})
    result = await grade(grader, "parcials-sense-continuitat", body)
    assert [v.status for v in result.verdicts] == ["ok", "ok"] and result.passed and result.rigorous
    assert result.example is not None and result.example.explanation


async def test_a_function_without_the_property_fails_and_says_why(grader: SubmissionGrader) -> None:
    body = submission("x**2+y**2", discontinua={"camins": [{"x": "t", "y": "t"}]})
    result = await grade(grader, "parcials-sense-continuitat", body)
    assert not result.passed and result.verdicts[1].status == "indeterminat" and result.verdicts[1].detail
    assert result.example is None
    assert (await grade(grader, "parcials-sense-continuitat", body, reveal=True)).example is not None


async def test_a_bound_makes_it_plausible_not_rigorous(grader: SubmissionGrader) -> None:
    body = submission("x**2*y/(x**2+y**2)", continua={"fita": "r"})
    result = await grade(grader, "direccionals-no-diferenciable", body)
    assert result.passed and not result.rigorous


@pytest.mark.parametrize(
    ("body", "message"),
    [
        (submission("x*y*z"), "només de x, y"),
        (submission("x**"), "La funció"),
        (submission("x*y", discontinua={"camins": [{"x": "s", "y": "t"}]}), "Camí 1"),
        (submission("x", value="x"), "valor a l'origen"),
        (submission("limit(x, x, 0)"), "no es pot fer servir limit"),
        # Read without evaluating: a power tower must not freeze the event loop before reaching a worker.
        (submission("9**9**9**9*z"), "potència massa gran"),
    ],
)
async def test_unreadable_input_is_rejected_before_any_check(
    grader: SubmissionGrader, body: Submission, message: str
) -> None:
    with pytest.raises(InvalidSubmissionException, match=message) as e:
        await grade(grader, "parcials-sense-continuitat", body)
    assert e.value.error_code == 422


async def test_unknown_challenge(grader: SubmissionGrader) -> None:
    with pytest.raises(UnknownSpecException):
        await grade(grader, "nope", submission("x"))


@pytest.mark.parametrize(
    ("function", "message"),
    [("2x*y", "2*x"), ("|x|", "Abs(...)"), ("xy/(x**2+y**2)", "vols dir x*y?")],
)
async def test_common_typing_mistakes_get_the_fix(grader: SubmissionGrader, function: str, message: str) -> None:
    with pytest.raises(InvalidSubmissionException, match=re.escape(message)):
        await grade(grader, "parcials-sense-continuitat", submission(function))


async def test_an_exponential_tower_is_rejected_before_any_worker(grader: SubmissionGrader) -> None:
    with pytest.raises(InvalidSubmissionException, match="exponencials niades"):
        await grade(grader, "parcials-sense-continuitat", submission("exp(-exp(exp(1/(x**2+y**2))))"))


@pytest.mark.parametrize("value", ["10**10**9", "2**5000"])
async def test_huge_powers_are_rejected_before_any_worker(grader: SubmissionGrader, value: str) -> None:
    with pytest.raises(InvalidSubmissionException, match="potència massa gran"):
        await grade(grader, "parcials-sense-continuitat", submission("x*y", value=value))
