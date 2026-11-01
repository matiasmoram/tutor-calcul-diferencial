"""f must be a real function defined on the whole plane minus the origin."""

import math

import sympy as sp

from core.counterexamples.domain.services.deciders.context import BadFunction, X, Y, at
from core.counterexamples.domain.services.deciders.numeric import float_function, number, real, safe
from core.counterexamples.domain.services.deciders.sampling import (
    HUG_POWERS,
    PROBE_DIRECTIONS,
    SWEEP_ANGLES,
    SWEEP_RADII,
)

_HOLE = (
    "ha de ser una funció real a tot $\\mathbb{R}^2\\setminus\\{(0,0)\\}$. Si la fórmula té un forat (p. ex. "
    "$\\sin(1/x)$), canvia-la per una definida a tot arreu (p. ex. $\\sin(1/(x^2+y^2))$)."
)
_NOT_REAL = (
    "ha de ser una funció real a tot $\\mathbb{R}^2\\setminus\\{(0,0)\\}$, i aquí pren un valor complex: una arrel "
    "d'índex parell (sqrt, potència 1/2) o un logaritme d'un nombre negatiu, o una potència amb exponent decimal. "
    "Les arrels d'índex senar ja són reals: cbrt(x*y) o (x*y)**(1/3) valen $-1$ a $(1,-1)$."
)


def check_defined(g: sp.Expr) -> None:
    """f must be a real function on the whole plane minus the origin: a hole on an axis would otherwise make a
    difference quotient "not exist" (1/x has no partial derivative in y because it is not defined on x = 0)."""
    # Numerically first, on a fine sweep of angles: a thin sector where f is complex (sqrt of a negative) is found.
    try:
        f_num = float_function(g, (X, Y))
    except Exception:
        f_num = None
    for r in SWEEP_RADII if f_num is not None else ():
        for theta in SWEEP_ANGLES:
            x, y = r * math.cos(theta), r * math.sin(theta)
            try:
                value = complex(f_num(x, y))  # type: ignore[misc, arg-type]
            except OverflowError:
                continue
            except (ValueError, ZeroDivisionError, TypeError):
                value = complex(math.nan)
            if math.isnan(value.real) or abs(value.imag) > 1e-9 * max(1.0, abs(value.real)):
                where = f"(x,y)\\approx({x:.3g}, {y:.3g})"
                raise BadFunction(_undefined_at(g, sp.Rational(x), sp.Rational(y), where))
    _check_denominator(g)
    for u, w in PROBE_DIRECTIONS:
        for h in (sp.Rational(1, 10), sp.Rational(1, 1000)):
            value = at(g, h * u, h * w)
            if value.has(sp.zoo, sp.nan) or number(value) in (
                None,
                math.inf,
                -math.inf,
            ):
                raise BadFunction(_undefined_at(g, h * u, h * w, f"({sp.latex(h * u)}, {sp.latex(h * w)})"))


def _undefined_at(g: sp.Expr, x: sp.Expr, y: sp.Expr, where: str) -> str:
    """Why f is not a valid answer at (x, y): a value that is not real (sqrt of a negative) or no value (a hole)."""
    try:
        value = complex(sp.N(at(g, x, y), 30))
    except (TypeError, ValueError, OverflowError, ZeroDivisionError):
        value = complex(math.nan)
    if math.isfinite(abs(value)) and abs(value.imag) > 1e-12 * max(1.0, abs(value.real)):
        return f"$f$ no és real a ${where}$: {_NOT_REAL}"
    return f"$f$ no està definida a ${where}$: {_HOLE}"


def _check_denominator(g: sp.Expr) -> None:
    """A denominator that changes sign on a circle around the origin vanishes there: f has a hole along a curve
    (x^4/(y-x^2) is undefined on the whole parabola), which no fixed set of probe points can be relied on to hit.

    The denominator is kept as written (no expansion: (y-x^4)^2+x^20 expanded loses its sign to rounding), floats
    only find candidates, and a sign change counts only once confirmed at exact points to 50 digits."""
    try:
        den = sp.fraction(sp.together(g))[1]
    except Exception:
        return
    if not den.free_symbols:
        return
    try:
        d_num = float_function(den, (X, Y))
    except Exception:
        return
    for r in (0.1, 1e-3, 1e-6):
        thetas = (
            *SWEEP_ANGLES,
            *(b + s * r**p for b in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2) for s in (1, -1) for p in HUG_POWERS),
        )
        seen: dict[bool, tuple[float, float]] = {}
        for theta in thetas:
            x, y = r * math.cos(theta), r * math.sin(theta)
            v = real(safe(d_num, x, y))
            if v is None or not math.isfinite(v) or v == 0 or (v > 0) in seen:
                continue
            exact = number(sp.N(den.subs({X: sp.Rational(x), Y: sp.Rational(y)}), 50))
            if exact is not None and exact != 0:
                seen[exact > 0] = (x, y)
            if len(seen) == 2:
                raise BadFunction(
                    f"El denominador de $f$, ${sp.latex(den)}$, canvia de signe prop de l'origen, així que s'hi anul·la: "
                    f"$f$ no hi està definida. {_HOLE}"
                )
