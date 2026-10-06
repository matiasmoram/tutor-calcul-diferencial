"""Self-test of the CAS leak checker (backend/tutor/cas.py) over every solution sheet.

    python scripts/check_cas.py            # summary + up to 40 hint hits
    python scripts/check_cas.py --all      # every hint hit
    python scripts/check_cas.py --unparsed # also list a sample of formulas the parser abstains on

1. Recall: for every step, `leaked(detall, prohibides=[detall], permeses=[])` must flag >= 1 formula whenever the
   detail contains a checkable (parsed, non-trivial) formula. Coverage = share of steps with >= 1 checkable formula.
2. Hints must not leak: `leaked(objectiu + idea, prohibides=[own detail + later details + result],
   permeses=[statement])`. Reported twice: as specified (statement only), and as the policy really runs it
   (earlier steps' details are allowed too, since a step is only targeted once the earlier ones are done).

Exit code 1 if recall fails on some step (a checker bug). Hint hits are reported, not fatal: each one is
either a sheet problem or a checker false positive to inspect.
"""

from __future__ import annotations

import argparse
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from tutor import cas  # noqa: E402
from tutor.fitxes import load_exercicis  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="print every hint hit")
    ap.add_argument("--unparsed", action="store_true", help="print a sample of unparsed formula sides")
    args = ap.parse_args()

    exs = load_exercicis()
    n_steps = n_math = n_checkable = n_recall = 0
    n_sides = n_parsed = 0
    recall_fail: list[str] = []
    unparsed: list[str] = []
    hint_hits: list[tuple[str, str, list[str]]] = []
    hint_hits_policy = n_obj_hits = 0
    times: list[float] = []

    for ex in exs.values():
        statement = ex.enunciat_md()
        for i, pas in enumerate(ex.passos):
            n_steps += 1
            segs = cas.formules(pas.detall)
            n_math += bool(segs)
            for seg in segs:
                for side in cas.sides(seg):
                    n_sides += 1
                    if cas._parse_side(side) is not None:
                        n_parsed += 1
                    elif len(unparsed) < 400:
                        unparsed.append(side)
            checkable = cas.checkable(pas.detall)
            if checkable:
                n_checkable += 1
                t0 = time.perf_counter()
                hits = cas.leaked(pas.detall, [pas.detall], [])
                times.append(time.perf_counter() - t0)
                if hits:
                    n_recall += 1
                else:
                    recall_fail.append(f"{ex.id}/{pas.id}")

            draft = f"{pas.objectiu}\n{pas.idea}"
            forbidden = [pas.detall] + [p.detall for p in ex.passos[i + 1:]] + [ex.resultat.valor]
            t0 = time.perf_counter()
            hits = cas.leaked(draft, forbidden, [statement])
            times.append(time.perf_counter() - t0)
            if hits:
                where = {"objectiu": cas.explain(pas.objectiu, forbidden, [statement]),
                         "idea": cas.explain(pas.idea, forbidden, [statement])}
                hint_hits.append((ex.id, pas.id, where))
                n_obj_hits += bool(where["objectiu"])
                earlier = [p.detall for p in ex.passos[:i]]
                if cas.leaked(draft, forbidden, [statement] + earlier):
                    hint_hits_policy += 1

    pct = lambda a, b: f"{a}/{b} ({100 * a / b:.1f}%)" if b else "0/0"  # noqa: E731
    print(f"Exercises: {len(exs)}   steps: {n_steps}")
    print(f"Formula sides parsed: {pct(n_parsed, n_sides)}")
    print(f"Steps whose detail has math: {pct(n_math, n_steps)}")
    print(f"Coverage (steps with >= 1 checkable formula): {pct(n_checkable, n_steps)}"
          f"  = {pct(n_checkable, n_math)} of steps with math")
    print(f"Recall (own detail flagged, over checkable steps): {pct(n_recall, n_checkable)}")
    for r in recall_fail:
        print(f"  RECALL FAIL {r}")
    print(f"Hint self-test, permitted = statement:          hits in {pct(len(hint_hits), n_steps)} steps")
    print(f"Hint self-test, permitted = statement + earlier: hits in {pct(hint_hits_policy, n_steps)} steps")
    print(f"  of which in the objective (level 1): {n_obj_hits}; only in the idea (level 2, where the strategy "
          f"may be named): {len(hint_hits) - n_obj_hits}")
    if times:
        ms = sorted(t * 1000 for t in times)
        print(f"leaked() time: median {statistics.median(ms):.2f} ms, p95 {ms[int(0.95 * len(ms))]:.2f} ms, "
              f"max {ms[-1]:.1f} ms (cold caches included)")
    shown = hint_hits if args.all else hint_hits[:40]
    for ex_id, step, where in shown:
        for field, pairs in where.items():
            for side, match in pairs:
                print(f"  HINT {ex_id}/{step} [{field}]: {side}   ~ forbidden {match}")
    if len(shown) < len(hint_hits):
        print(f"  ... {len(hint_hits) - len(shown)} more (--all)")
    if args.unparsed:
        print("Sample of unparsed sides:")
        for s in unparsed[:120]:
            print(f"  {s}")
    return 1 if recall_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
