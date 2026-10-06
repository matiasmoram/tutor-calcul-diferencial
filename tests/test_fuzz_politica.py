"""Policy invariants fuzzed over a sample of real sheets (see scripts/fuzz_politica.py for the full run)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from fuzz_politica import check  # noqa: E402
from test_harness import EX, TEORIA  # noqa: E402

SAMPLE = sorted(EX)[::11]  # ~30 exercises across all temes


@pytest.mark.parametrize("ex_id", SAMPLE)
def test_policy_invariants_hold_under_random_sessions(ex_id):
    viol = []
    for profile, seeds in (("random", 6), ("stuck_trying", 2), ("beggar", 2)):
        for seed in range(seeds):
            viol += check(EX[ex_id], TEORIA, seed, 16, profile)
    assert not viol, viol[:3]
