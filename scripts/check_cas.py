"""Self-test of the CAS leak checker (backend/core/shared/math/latex_cas/) over every solution sheet.

    python scripts/check_cas.py            # summary + up to 40 hint hits
    python scripts/check_cas.py --all      # every hint hit
    python scripts/check_cas.py --unparsed # also list a sample of formulas the parser abstains on

1. Recall: for every step, `leaked(detail, forbidden=[detail], allowed=[])` must flag >= 1 formula whenever the
   detail contains a checkable (parsed, non-trivial) formula. Coverage = share of steps with >= 1 checkable formula.
2. Hints must not leak: `leaked(objective + idea, forbidden=[own detail + later details + result],
   allowed=[statement])`. Reported twice: as specified (statement only), and as the policy really runs it
   (earlier steps' details are allowed too, since a step is only targeted once the earlier ones are done).

Exit code 1 if recall fails on some step (a checker bug). Hint hits are reported, not fatal: each one is
either a sheet problem or a checker false positive to inspect.
"""

import argparse
import statistics
import time

from core.course.infra.yaml_course_source import YamlCourseSource
from core.shared.math import latex_cas as cas
from settings import BACKEND_DIR


def _pct(a: int, b: int) -> str:
    return f"{a}/{b} ({100 * a / b:.1f}%)" if b else "0/0"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="print every hint hit")
    ap.add_argument("--unparsed", action="store_true", help="print a sample of unparsed formula sides")
    args = ap.parse_args()

    exs = YamlCourseSource(BACKEND_DIR / "exercicis", BACKEND_DIR / "teoria").load().exercises
    n_steps = n_math = n_checkable = n_recall = 0
    n_sides = n_parsed = 0
    recall_fail: list[str] = []
    unparsed: list[str] = []
    hint_hits: list[tuple[str, str, dict[str, list[tuple[str, str]]]]] = []
    hint_hits_policy = n_obj_hits = 0
    times: list[float] = []

    for ex in exs.values():
        statement = ex.statement_md()
        for i, step in enumerate(ex.steps):
            n_steps += 1
            segs = cas.formulas(step.detail)
            n_math += bool(segs)
            for seg in segs:
                for side in cas.sides(seg):
                    n_sides += 1
                    if cas._parse_side(side) is not None:
                        n_parsed += 1
                    elif len(unparsed) < 400:
                        unparsed.append(side)
            if cas.checkable(step.detail):
                n_checkable += 1
                t0 = time.perf_counter()
                hits = cas.leaked(step.detail, [step.detail], [])
                times.append(time.perf_counter() - t0)
                if hits:
                    n_recall += 1
                else:
                    recall_fail.append(f"{ex.id}/{step.id}")

            draft = f"{step.objective}\n{step.idea}"
            forbidden = [step.detail] + [s.detail for s in ex.steps[i + 1 :]] + [ex.result.value]
            t0 = time.perf_counter()
            hits = cas.leaked(draft, forbidden, [statement])
            times.append(time.perf_counter() - t0)
            if hits:
                where = {
                    "objectiu": cas.explain(step.objective, forbidden, [statement]),
                    "idea": cas.explain(step.idea, forbidden, [statement]),
                }
                hint_hits.append((ex.id, step.id, where))
                n_obj_hits += bool(where["objectiu"])
                earlier = [s.detail for s in ex.steps[:i]]
                if cas.leaked(draft, forbidden, [statement, *earlier]):
                    hint_hits_policy += 1

    print(f"Exercises: {len(exs)}   steps: {n_steps}")
    print(f"Formula sides parsed: {_pct(n_parsed, n_sides)}")
    print(f"Steps whose detail has math: {_pct(n_math, n_steps)}")
    print(
        f"Coverage (steps with >= 1 checkable formula): {_pct(n_checkable, n_steps)}"
        f"  = {_pct(n_checkable, n_math)} of steps with math"
    )
    print(f"Recall (own detail flagged, over checkable steps): {_pct(n_recall, n_checkable)}")
    for r in recall_fail:
        print(f"  RECALL FAIL {r}")
    print(f"Hint self-test, permitted = statement:          hits in {_pct(len(hint_hits), n_steps)} steps")
    print(f"Hint self-test, permitted = statement + earlier: hits in {_pct(hint_hits_policy, n_steps)} steps")
    print(
        f"  of which in the objective (level 1): {n_obj_hits}; only in the idea (level 2, where the strategy "
        f"may be named): {len(hint_hits) - n_obj_hits}"
    )
    if times:
        ms = sorted(t * 1000 for t in times)
        print(
            f"leaked() time: median {statistics.median(ms):.2f} ms, p95 {ms[int(0.95 * len(ms))]:.2f} ms, "
            f"max {ms[-1]:.1f} ms (cold caches included)"
        )
    shown = hint_hits if args.all else hint_hits[:40]
    for ex_id, step_id, where in shown:
        for field, pairs in where.items():
            for side, match in pairs:
                print(f"  HINT {ex_id}/{step_id} [{field}]: {side}   ~ forbidden {match}")
    if len(shown) < len(hint_hits):
        print(f"  ... {len(hint_hits) - len(shown)} more (--all)")
    if args.unparsed:
        print("Sample of unparsed sides:")
        for s in unparsed[:120]:
            print(f"  {s}")
    return 1 if recall_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
