"""Fixed sample sets: directions, slopes, and the angles and radii of the numeric sweeps."""

import math

import sympy as sp

# Fixed directions and slopes tried on top of the generic one: sympy solves a limit with a symbolic parameter for a
# "generic" value of it and can miss the special ones (the axes, the diagonals).
DIRECTIONS: tuple[tuple[int, int], ...] = ((1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (1, -3))
SLOPES: tuple[sp.Expr, ...] = tuple(
    sp.Rational(m) for m in ("0", "1", "-1", "2", "-3", "1/2", "-1/2", "1/3", "3", "-1/3", "3/2", "2/3", "-5/7")
)


# Integer directions every 7.5 degrees (offset so that no grid line is special), plus the usual ones: a sector where
# f is complex or undefined has to be narrower than that to slip by.
PROBE_DIRECTIONS = (
    *DIRECTIONS,
    (-1, 0),
    (0, -1),
    (-1, -1),
    (-1, 1),
    *((round(97 * math.cos(a)), round(97 * math.sin(a))) for a in (2 * math.pi * j / 48 + 0.071 for j in range(48))),
)


# theta ~ r^p follows y ~ x^(p+1) near an axis: the curves where a discontinuity hides from every line.
HUG_POWERS = (0.5, *range(1, 40))
SWEEP_ANGLES = tuple(2 * math.pi * (j + 0.37) / 4096 for j in range(4096))
SWEEP_RADII = (0.1, 1e-3, 1e-6)
