"""Floats from sympy expressions: exact values to 30 digits, and fast float functions for sampling."""

import math
from collections.abc import Callable

import sympy as sp


def _float_sign(v: float) -> float:
    return float((v > 0) - (v < 0))


# Plain floats wherever the math module has the function (fast); mpmath only for the rest. sign is the usual
# exception to math, and with tens of thousands of sampled points an mpmath fallback costs seconds.
_FLOAT_FUNCTIONS = {"sign": _float_sign}


def float_function(expr: sp.Expr, args: tuple[sp.Symbol, ...]) -> Callable[..., object]:
    return sp.lambdify(args, expr, modules=[_FLOAT_FUNCTIONS, "math", "mpmath"])


def number(e: sp.Basic) -> float | None:
    """A real number to 30 digits (may be +-inf); None if it is not one (complex, nan, still symbolic)."""
    try:
        return real(sp.N(e, 30))
    except Exception:
        return None


def real(value: object) -> float | None:
    try:
        v = complex(value)  # type: ignore[arg-type]
    except (TypeError, ValueError, OverflowError, ZeroDivisionError):
        return None
    if math.isnan(v.real) or math.isnan(v.imag) or abs(v.imag) > 1e-12 * max(1.0, abs(v.real)):
        return None
    return v.real  # may be +-inf: a bound check counts it as a violation


def safe(fn: Callable[..., object], *args: float) -> object:
    try:
        return fn(*args)
    except Exception:
        return None
