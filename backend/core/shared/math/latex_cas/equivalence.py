"""Numeric fingerprints of parsed formulas, and equivalence by value at shared random points."""

import random
from functools import lru_cache

import mpmath
import sympy as sp
from sympy.core.function import AppliedUndef

from core.shared.math.latex_cas.parser import parse

N_POINTS = 8
MIN_VALID_POINTS = 3
REL_TOL = 1e-8

type _Fingerprint = tuple[str, object, object]  # see `_fingerprint`


@lru_cache(maxsize=4096)
def _value(name: str, k: int) -> complex:
    rng = random.Random(f"cas:{name}:{k}")
    if k < N_POINTS // 2:
        return rng.uniform(0.11, 0.57)  # small positive: inside sqrt(1-x^2-y^2), log(x), ...
    return rng.uniform(-1.9, 1.9)  # signed: separates |x| from x, x^2 from x^4 near 1, ...


def _opaque(e: sp.Basic) -> sp.Basic:
    """Undefined function applications become opaque symbols: f(x,y) is compared by name."""
    if e.has(AppliedUndef):
        e = e.replace(lambda a: isinstance(a, AppliedUndef), lambda a: sp.Symbol(f"__{a}"))
    return e


def _scalar_values(e: sp.Basic) -> tuple[complex | None, ...] | None:
    """Values of a scalar expression at the shared random points (None = point failed)."""
    e = _opaque(e)
    if not isinstance(e, sp.Expr):
        return None
    syms = sorted(e.free_symbols, key=lambda s: s.name)
    vals: list[complex | None] = []
    try:
        f = sp.lambdify(syms, e, modules="mpmath")
    except Exception:
        return None
    for k in range(N_POINTS):
        try:
            v = complex(f(*[mpmath.mpf(_value(s.name, k)) for s in syms]))
            vals.append(v if v == v and abs(v) != float("inf") and abs(v) < 1e300 else None)
        except Exception:
            vals.append(None)
    return tuple(vals)


@lru_cache(maxsize=8192)
def _fingerprint(e: sp.Basic) -> _Fingerprint | None:
    """(kind, shape, per-entry values); kind is 'expr', 'const', 'tuple' or 'matrix'."""
    if isinstance(e, sp.Tuple):
        return ("tuple", len(e), tuple(_fingerprint(x) for x in e))
    if isinstance(e, sp.MatrixBase):
        return ("matrix", e.shape, tuple(_fingerprint(x) for x in e))
    if not isinstance(e, sp.Expr):
        return None
    if not _opaque(e).free_symbols:
        try:
            v = complex(sp.N(e, 30))
        except Exception:
            return ("const", None, None)
        return ("const", None, v if v == v and abs(v) != float("inf") else None)
    return ("expr", None, _scalar_values(e))


def _close(u: complex, v: complex, tol: float = REL_TOL) -> bool:
    return abs(u - v) <= tol * max(1.0, abs(u), abs(v))


def _real(v: complex) -> bool:
    return abs(v.imag) <= 1e-12 * max(1.0, abs(v))


def _decimal_tolerance(e: sp.Basic) -> float | None:
    """A decimal literal with >= 2 decimals may be a rounded value: half a unit in its last place."""
    if isinstance(e, sp.Rational) and not isinstance(e, sp.Integer):
        q = e.q
        d = 0
        while q % 10 == 0:
            q //= 10
            d += 1
        if q == 1 and d >= 2:
            return 0.5 * 10.0**-d * (1 + 1e-9)
    return None


def _compare(a: sp.Basic, b: sp.Basic, fa: _Fingerprint | None, fb: _Fingerprint | None) -> bool | None:
    if fa is None or fb is None:
        return None
    ka, kb = fa[0], fb[0]
    if ka in ("tuple", "matrix") or kb in ("tuple", "matrix"):
        if ka != kb or fa[1] != fb[1]:
            return False
        verdicts = [_compare(x, y, fx, fy) for x, y, fx, fy in zip(a, b, fa[2], fb[2], strict=False)]
        if any(v is False for v in verdicts):
            return False
        return None if any(v is None for v in verdicts) else True
    if ka == "const" and kb == "const":
        if fa[2] is None or fb[2] is None:
            return True if a == b else None  # oo == oo
        if _close(fa[2], fb[2], 1e-12):
            return True
        for x, other in ((a, fb[2]), (b, fa[2])):
            tol = _decimal_tolerance(x)
            if tol is not None and abs(complex(x) - other) <= tol and not isinstance((b if x is a else a), sp.Integer):
                return True
        return False
    va = fa[2] if ka == "expr" else (fa[2],) * N_POINTS if fa[2] is not None else None
    vb = fb[2] if kb == "expr" else (fb[2],) * N_POINTS if fb[2] is not None else None
    if va is None or vb is None:
        return None
    # Points outside the real domain of either side (complex value, pole, log of a negative) are skipped.
    pairs = [(u, v) for u, v in zip(va, vb, strict=False) if u is not None and v is not None and _real(u) and _real(v)]
    if len(pairs) < MIN_VALID_POINTS:
        return None
    return all(_close(u, v) for u, v in pairs)


def _as_expr(x: str | float | sp.Basic) -> sp.Basic | None:
    if isinstance(x, str):
        return parse(x)
    if isinstance(x, (int, float)):
        return sp.nsimplify(x) if isinstance(x, float) else sp.Integer(x)
    return x


def equivalent(a: str | float | sp.Basic, b: str | float | sp.Basic) -> bool | None:
    """Are two formulas (LaTeX strings or sympy objects) mathematically equal? None when undecidable."""
    try:
        ea, eb = _as_expr(a), _as_expr(b)
        if ea is None or eb is None:
            return None
        if ea == eb:
            return True
        if isinstance(ea, sp.core.relational.Relational) or isinstance(eb, sp.core.relational.Relational):
            if type(ea) is not type(eb):
                return (
                    None
                    if not (
                        isinstance(ea, sp.core.relational.Relational) and isinstance(eb, sp.core.relational.Relational)
                    )
                    else False
                )
            direct = [equivalent(ea.lhs, eb.lhs), equivalent(ea.rhs, eb.rhs)]
            if all(direct):
                return True
            if isinstance(ea, (sp.Eq, sp.Ne)):
                swapped = [equivalent(ea.lhs, eb.rhs), equivalent(ea.rhs, eb.lhs)]
                if all(swapped):
                    return True
            return None if None in direct else False
        return _compare(ea, eb, _fingerprint(ea), _fingerprint(eb))
    except Exception:
        return None
