from core.shared.domain.claims import claim_timeout

GRADING_DEADLINE_S = 240.0  # the whole grading, every model call and retry included
# Hints are recorded under the grading claim too: both take a stale claim over at the same age.
GRADING_CLAIM_TIMEOUT_S = claim_timeout(GRADING_DEADLINE_S)
