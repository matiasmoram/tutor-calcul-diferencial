"""One-variable limits with sympy, cross-checked numerically, and exact comparison of their values."""

import math
from dataclasses import dataclass

import sympy as sp

from core.counterexamples.domain.services.deciders.numeric import number


@dataclass(frozen=True)
class Limit:
    """`exists`: True finite limit, False no finite limit (different side limits, oscillation, infinite), None
    sympy could not tell."""

    exists: bool | None
    value: sp.Expr | None = None


class _DoesNotExist:
    """sympy proved different side limits (still to be confirmed numerically)."""


def _sympy_limit(expr: sp.Expr, var: sp.Symbol, side: str) -> sp.Expr | _DoesNotExist | None:
    """sympy's own answer: an expression, "does not exist", or None when sympy fails."""
    try:
        lim = sp.limit(expr, var, 0, side)
    except ValueError as e:
        # sympy: "The limit does not exist since left hand limit = a and right hand limit = b". Any other
        # ValueError is sympy failing, not a proof.
        return _DoesNotExist() if "does not exist" in str(e) else None
    except Exception:  # NotImplementedError, PoleError, recursion... : sympy cannot tell
        return None
    if not isinstance(lim, sp.Expr) or lim.has(sp.Limit) or lim.has(sp.nan):
        return None
    return lim


def _unbounded_or_oscillating(lim: sp.Expr) -> bool:
    return isinstance(lim, sp.AccumBounds) or lim.has(sp.AccumBounds) or lim.has(sp.oo, -sp.oo, sp.zoo)


def limit(expr: sp.Expr, var: sp.Symbol, side: str = "+-") -> Limit:
    lim = _sympy_limit(expr, var, side)
    if lim is None:
        return Limit(None)
    if isinstance(lim, _DoesNotExist):
        return Limit(False) if _numerically_unsettled(expr, var, side) else Limit(None)
    if _unbounded_or_oscillating(lim):
        # sympy reads sin(A)^2 + cos(A)^2 with A blowing up as AccumBounds(0, 2): an equivalent form may show the
        # limit. One level of rewrites, each handed straight to sympy (rewriting a rewrite ping-pongs between
        # expand and simplify), and a finite answer only if the numbers do not contradict it: simplify turns
        # sign(h^2)/h into a Piecewise whose sympy limit is 0.
        for form in _rewritten(expr):
            retry = _sympy_limit(form, var, side)
            if isinstance(retry, sp.Expr) and not _unbounded_or_oscillating(retry):
                value = sp.simplify(retry)
                if not _numerically_elsewhere(expr, var, side, value):
                    return Limit(True, value)
        # sympy's "no limit" is a proof only if f visibly keeps oscillating (or jumping, or growing) at every scale.
        return Limit(False, lim) if _numerically_unsettled(expr, var, side) else Limit(None)
    value = sp.simplify(lim)
    if _numerically_elsewhere(expr, var, side, value):
        return Limit(None)
    return Limit(True, value)


_PARAMETER_VALUES = (sp.Rational(3, 7), sp.Rational(-5, 11))


def _rewritten(expr: sp.Expr) -> list[sp.Expr]:
    """Equivalent forms on which sympy's limit may succeed where it reported AccumBounds on the original. A form with
    a Piecewise is dropped: sympy takes the limit of one branch and may pick the one valid only at 0."""
    out: list[sp.Expr] = []
    for rewrite in (sp.expand, sp.trigsimp, sp.simplify):
        try:
            form = rewrite(expr)
        except Exception:
            continue
        if isinstance(form, sp.Expr) and form != expr and form not in out and not form.has(sp.Piecewise):
            out.append(form)
    return out


_EPSILONS = (sp.Rational(1, 10**9), sp.Rational(1, 10**12))


def _near_values(
    expr: sp.Expr, var: sp.Symbol, side: str, params: list[sp.Basic], p_value: sp.Expr
) -> list[tuple[float, float]] | None:
    """Per side asked for, f at the two scales of `_EPSILONS` (parameters fixed to `p_value`); None if f cannot be
    evaluated there."""
    fixed = expr.subs([(p, p_value) for p in params])
    out: list[tuple[float, float]] = []
    for sign in {"+": (1,), "-": (-1,)}.get(side, (1, -1)):
        a, b = (number(fixed.subs(var, sign * eps)) for eps in _EPSILONS)
        if a is None or b is None or not (math.isfinite(a) and math.isfinite(b)):
            return None
        out.append((a, b))
    return out


def _settled(a: float, b: float) -> bool:
    return abs(a - b) <= 1e-6 * max(1.0, abs(b))


_SCALES = (1e-3, 1e-6, 1e-9, 1e-12)
_WINDOW = (1.0, 1.21, 1.43, 1.67, 1.94)


def _numerically_unsettled(expr: sp.Expr, var: sp.Symbol, side: str) -> bool:
    """f near 0 keeps a spread that does not shrink: across the window [s, 2s] (both sides when two-sided) the values
    differ at every scale s, and as much at the smallest scale as at the largest. A jump, an oscillation like
    sin(1/t) and a blow-up all qualify; a slow convergence, or an identity sympy did not see, does not."""
    params = sorted(expr.free_symbols - {var}, key=str)
    signs = {"+": (1,), "-": (-1,)}.get(side, (1, -1))
    for p_value in _PARAMETER_VALUES:
        fixed = expr.subs([(p, p_value) for p in params])
        spreads: list[float] = []
        for scale in _SCALES:
            values: list[float] = []
            for sign in signs:
                for w in _WINDOW:
                    v = number(fixed.subs(var, sign * sp.Float(scale * w, 30)))
                    if v is None:
                        return False
                    values.append(v)
            spread = max(values) - min(values)
            if not spread > 1e-6 * max(1.0, min(abs(v) for v in values)):
                return False
            spreads.append(spread)
        if not spreads[-1] >= 0.1 * spreads[0]:
            return False
    return True


def _numerically_elsewhere(expr: sp.Expr, var: sp.Symbol, side: str, value: sp.Expr) -> bool:
    """sympy can return a wrong finite limit (with atan(y/x) it loses a sign). Cross-check: with the parameters fixed
    to sample values, f near 0 settles (two scales agree) on a number other than sympy's. Only a clear, converged
    disagreement counts, so slow convergence (1/log) is not flagged. So does a clear blow-up (|f| large and growing
    between the two scales, as h^(-1/3) does): no finite value can be the limit."""
    params = sorted((expr.free_symbols | value.free_symbols) - {var}, key=str)
    for p_value in _PARAMETER_VALUES:
        target = number(value.subs([(p, p_value) for p in params]))
        near = _near_values(expr, var, side, params, p_value)
        if target is None or near is None or not math.isfinite(target):
            continue
        for a, b in near:
            if _settled(a, b) and abs(b - target) > 1e-3 * max(1.0, abs(target)):
                return True
            if abs(b) > 1e3 * max(1.0, abs(target)) and abs(b) > 2 * abs(a):
                return True
    return False


def compare(a: sp.Expr, b: sp.Expr) -> bool | None:
    """True only when sympy simplifies a - b to 0; False when a - b is clearly nonzero at an exact sample point
    (60 digits, so a perturbation of 1e-15 is seen); None otherwise. No numeric tolerance can make "equal" true."""
    try:
        d = sp.simplify(a - b)
    except Exception:
        return None
    if d == 0:
        return True
    params = sorted(d.free_symbols, key=str)
    for values in _COMPARE_POINTS:
        try:
            v = complex(sp.N(d.subs(dict(zip(params, values, strict=False))), 60))
        except (TypeError, ValueError, ZeroDivisionError):
            continue
        if math.isfinite(abs(v)) and abs(v) > 1e-40:
            return False
    return None


_COMPARE_POINTS = tuple(
    tuple(sp.Rational(n, d) for n, d in row)
    for row in (((3, 7), (-5, 11), (2, 13)), ((-17, 19), (7, 3), (-1, 5)), ((11, 2), (1, 9), (13, 6)))
)
