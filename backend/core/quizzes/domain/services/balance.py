"""True/false balance of a quiz. Counterexamples are the point of the activity: at least half of the statements
are false, at least two are true."""

import math
from collections.abc import Sequence

from core.quizzes.domain.values.drafts import StatementDraft

BATCH_SIZE = 5  # statements per generation call: keeps each call well under the client timeout
EXTRA_ROUNDS = 3  # replacement rounds on top of the ones the quiz size needs


def false_range(n: int) -> tuple[int, int]:
    return math.ceil(n / 2), n - 2


def max_rounds(n: int, batch: int = BATCH_SIZE) -> int:
    return math.ceil(n / batch) + EXTRA_ROUNDS


def _falses(kept: Sequence[StatementDraft]) -> int:
    return sum(d.verdict == "fals" for d in kept)


def batch_false_bounds(total: int, kept: Sequence[StatementDraft], count: int) -> tuple[int, int]:
    """How many false statements to ask for in a batch of `count`.

    Hard bounds keep the whole quiz feasible; within them, ask for a mix in every batch."""
    lo, hi = false_range(total)
    falses = _falses(kept)
    trues = len(kept) - falses
    later = total - len(kept) - count  # statements still to come in later batches
    h_lo = max(0, lo - falses - later, count - (total - lo - trues))
    h_hi = max(h_lo, min(count, hi - falses))
    f_lo, f_hi = max(h_lo, count // 2), min(h_hi, count - 1 if count > 2 else count)
    if f_lo > f_hi:
        f_lo, f_hi = h_lo, h_hi
    return f_lo, f_hi


def trim(kept: Sequence[StatementDraft], n: int) -> list[StatementDraft]:
    """Keeps at most what the balance allows: surplus statements of one verdict are dropped (latest first)."""
    lo, hi = false_range(n)
    max_true = n - lo
    out: list[StatementDraft] = []
    falses = trues = 0
    for d in kept:
        if d.verdict == "fals" and falses < hi:
            falses += 1
            out.append(d)
        elif d.verdict == "cert" and trues < max_true:
            trues += 1
            out.append(d)
    return out[:n]


def select_for_verification(
    kept: Sequence[StatementDraft], candidates: Sequence[StatementDraft], n: int, limit: int
) -> tuple[list[StatementDraft], list[StatementDraft]]:
    """Splits the candidates into the ones worth verifying now and the rest, kept as backups for later rounds.

    At most `limit`, never more than the quiz still needs, and never so many of one verdict that `trim` would drop
    them even if all pass: verifying a statement costs two model calls."""
    lo, hi = false_range(n)
    falses = _falses(kept)
    trues = len(kept) - falses
    room = min(limit, n - len(kept))
    chosen: list[StatementDraft] = []
    backups: list[StatementDraft] = []
    for d in candidates:
        if len(chosen) < room and d.verdict == "fals" and falses < hi:
            falses += 1
            chosen.append(d)
        elif len(chosen) < room and d.verdict == "cert" and trues < n - lo:
            trues += 1
            chosen.append(d)
        else:
            backups.append(d)
    return chosen, backups


def is_complete(kept: Sequence[StatementDraft], n: int) -> bool:
    lo, hi = false_range(n)
    return len(kept) == n and lo <= _falses(kept) <= hi
