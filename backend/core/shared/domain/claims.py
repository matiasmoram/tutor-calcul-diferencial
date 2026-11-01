def claim_timeout(deadline_s: float) -> float:
    """Age after which a claim belongs to work (a turn, a grading) that died without releasing it.

    Strictly above the work's deadline: live work is cancelled by its deadline before its claim can go stale, so a
    takeover never runs (and pays) beside the work it replaces. The margin covers the claim and save round trips and
    clock skew between workers."""
    return deadline_s + 60.0
