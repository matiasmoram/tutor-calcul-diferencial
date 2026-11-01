from core.shared.domain.claims import claim_timeout

GRADING_DEADLINE_S = 240.0  # the whole grading, every model call and retry included
GRADING_CLAIM_TIMEOUT_S = claim_timeout(GRADING_DEADLINE_S)
