import random
from collections.abc import Sequence
from dataclasses import dataclass

from core.mistakes.domain.values.mistake_kind import PROBLEM_MISTAKE_KINDS, THEORY_MISTAKE_KINDS

# Kinds that make sense for a theory statement (part 1): it is changed, not argued.
STATEMENT_KINDS: tuple[str, ...] = ("hipotesi", "conclusio", "quantificador", "implicacio", "desigualtat")


@dataclass(frozen=True)
class CorruptionPlan:
    """What one corrupter is told about the others: the `tipus` it should prefer and the (part, tipus) planned for
    the other flawed parts. The chains run in parallel, so code decides this before they start."""

    kind: str
    others: tuple[tuple[int, str], ...] = ()


def plan_corruptions(rng: random.Random, chosen: Sequence[int], theory: bool) -> dict[int, CorruptionPlan]:
    """A distinct preferred kind for every chosen part (repeating only when the parts outnumber the kinds), drawn
    by `rng`. Theory's statement (part 1) takes one of the statement kinds."""
    valid = THEORY_MISTAKE_KINDS if theory else PROBLEM_MISTAKE_KINDS
    pool: list[str] = []
    kinds: dict[int, str] = {}
    # The statement picks first, from its own kinds; the others take what is left.
    for part in sorted(chosen, key=lambda p: not (theory and p == 1)):
        if not pool:
            pool = list(valid)
            rng.shuffle(pool)
        statement = theory and part == 1
        kind = next((k for k in pool if not statement or k in STATEMENT_KINDS), None)
        if kind is None:  # unreachable while the pool holds a statement kind; kept total
            kind = rng.choice(STATEMENT_KINDS)
        else:
            pool.remove(kind)
        kinds[part] = kind
    return {p: CorruptionPlan(k, tuple((q, kq) for q, kq in sorted(kinds.items()) if q != p)) for p, k in kinds.items()}
