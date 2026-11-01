import pytest

from core.mistakes.application import annotations_grader
from core.quizzes.application import answers_grader
from core.shared.domain.claims import claim_timeout
from core.tutoring.application import turn_handler


def test_a_claim_goes_stale_a_margin_after_the_deadline_of_its_work() -> None:
    assert claim_timeout(240.0) == 300.0
    assert claim_timeout(300.0) == 360.0


@pytest.mark.parametrize(
    ("deadline_s", "claim_timeout_s"),
    [
        (turn_handler.TURN_DEADLINE_S, turn_handler.TURN_CLAIM_TIMEOUT_S),
        (annotations_grader.GRADING_DEADLINE_S, annotations_grader.GRADING_CLAIM_TIMEOUT_S),
        (answers_grader.GRADING_DEADLINE_S, answers_grader.GRADING_CLAIM_TIMEOUT_S),
    ],
)
def test_every_claimed_use_case_follows_the_shared_rule(deadline_s: float, claim_timeout_s: float) -> None:
    assert claim_timeout_s == claim_timeout(deadline_s)
