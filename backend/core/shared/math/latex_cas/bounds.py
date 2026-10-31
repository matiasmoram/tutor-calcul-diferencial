"""Size bounds of the parser. sympy evaluates integer powers and factorials exactly, holding the GIL, so "9^{9^{9}}"
in a message would freeze every thread of the process: anything beyond these bounds is not a usable formula
(unparseable)."""

import sympy as sp


class _ParseError(Exception):
    pass


MAX_INT_BITS = 16384  # ~4900 decimal digits
MAX_EXPONENT = 10_000  # numeric exponent, any base
MAX_FACTORIAL = 1000
MAX_MATRIX_POWER = 64
MAX_MATRIX_ENTRIES = 36
MAX_DET_SIZE = 4


def _bits(x: sp.Rational) -> int:
    return max(abs(int(x.p)).bit_length(), int(x.q).bit_length())


def _sized(e: sp.Basic) -> sp.Basic:
    """`e`, unless its numeric coefficient is too large to keep computing with."""
    c = e if isinstance(e, sp.Rational) else e.as_coeff_Mul()[0] if isinstance(e, sp.Mul) else None
    if isinstance(c, sp.Rational) and _bits(c) > MAX_INT_BITS:
        raise _ParseError("number too large")
    return e


def _pow(base: sp.Basic, exp: sp.Basic) -> sp.Basic:
    """base**exp, refused before sympy starts an exact computation that cannot finish in reasonable time."""
    if base == sp.E:
        return sp.exp(exp)
    if isinstance(exp, sp.Rational):
        if isinstance(base, sp.MatrixBase):
            if abs(exp) > MAX_MATRIX_POWER:
                raise _ParseError("matrix power too large")
        elif abs(exp) > MAX_EXPONENT:
            raise _ParseError("exponent too large")
        elif isinstance(base, sp.Rational) and base not in (0, 1, -1) and _bits(base) * abs(float(exp)) > MAX_INT_BITS:
            raise _ParseError("power too large")
    return _sized(base**exp)


def _factorial(e: sp.Basic) -> sp.Basic:
    if isinstance(e, sp.Integer) and e > MAX_FACTORIAL:
        raise _ParseError("factorial too large")
    return sp.factorial(e)


def _check_magnitude(e: object) -> float | None:
    """Bound of log2|value| of an unevaluated numeric subtree (None if symbolic); raises _ParseError when
    evaluating it would exceed the size bounds. Used on sympy's own parser output, built with evaluate=False."""
    if isinstance(e, sp.Rational):
        return float(_bits(e))
    if not isinstance(e, sp.Basic) or not e.args:
        return None
    sub = [_check_magnitude(a) for a in e.args]
    if isinstance(e, sp.Pow):
        b, x = sub
        if x is None:
            return None
        if x > MAX_EXPONENT.bit_length():
            raise _ParseError("exponent too large")
        if b is None:
            return None
        mag = b * 2.0**x
        if mag > MAX_INT_BITS:
            raise _ParseError("power too large")
        return mag
    if isinstance(e, sp.factorial):
        if sub[0] is not None and sub[0] > MAX_FACTORIAL.bit_length():
            raise _ParseError("factorial too large")
        return None if sub[0] is None else 2.0 ** sub[0] * sub[0]
    if any(m is None for m in sub):
        return None
    if isinstance(e, sp.Mul):
        total = sum(m for m in sub if m is not None)
        if total > MAX_INT_BITS:
            raise _ParseError("number too large")
        return total
    if isinstance(e, sp.Add):
        return max(m for m in sub if m is not None) + len(sub)
    return None
