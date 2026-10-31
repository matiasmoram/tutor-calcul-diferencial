"""Decides one property of a proposed counterexample at the origin, with sympy. Runs inside a worker process.

Only one-variable limits are trusted: a partial or directional derivative is the limit of a difference quotient in h,
a path reduces f to a function of t, an iterated limit is two one-variable limits. sympy's own two-variable limits are
never used (a polar limit with the angle left free is not uniform in the angle). A radial bound G(r) is checked
exactly for G(r) -> 0 and on a grid of points for the inequality, so a property resting on one is "plausible".

`check_property` never raises: anything sympy cannot decide comes back "indeterminat" with the reason.
"""

import math
import random
import zlib
from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass, field

import sympy as sp

from core.counterexamples.domain.values.properties import PROPERTIES, PropertyKind
from core.counterexamples.domain.values.submission import (
    MAX_CONSTANT,
    Certificate,
    Path,
    PropertyCheck,
    extreme_constant,
)
from core.counterexamples.domain.values.verdict import PropertyVerdict, VerdictStatus
from core.shared.math.sympy_checks import SYMBOLS, InvalidExpression, parse

X, Y, T, R = SYMBOLS["x"], SYMBOLS["y"], SYMBOLS["t"], SYMBOLS["r"]
_H = sp.Dummy("h", real=True)
_K = sp.Dummy("k", real=True, nonzero=True)
_HK = sp.Dummy("h", real=True, nonzero=True)
_A, _B = sp.Dummy("a", real=True), sp.Dummy("b", real=True)
_M = sp.Dummy("m", real=True)
_THETA = sp.Dummy("theta", real=True)

# Fixed directions and slopes tried on top of the generic one: sympy solves a limit with a symbolic parameter for a
# "generic" value of it and can miss the special ones (the axes, the diagonals).
DIRECTIONS: tuple[tuple[int, int], ...] = ((1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (1, -3))
SLOPES: tuple[sp.Expr, ...] = tuple(
    sp.Rational(m) for m in ("0", "1", "-1", "2", "-3", "1/2", "-1/2", "1/3", "3", "-1/3", "3/2", "2/3", "-5/7")
)
R_MAX = 0.5
_RADII = tuple(R_MAX * 10 ** (-k / 3) * f for k in range(43) for f in (1.0, 0.977))  # down to ~1e-14
_ANGLES = tuple(2 * math.pi * j / 120 for j in range(120)) + tuple(2 * math.pi * j / 120 + 0.0123 for j in range(120))
_MIN_EVALUATED = 0.5  # of the grid points; fewer (f undefined almost everywhere?) and the bound is not judged


@dataclass(frozen=True)
class _Limit:
    """`exists`: True finite limit, False no finite limit (different side limits, oscillation, infinite), None
    sympy could not tell."""

    exists: bool | None
    value: sp.Expr | None = None


class _Undecided(Exception):
    pass


class _BadCertificate(Exception):
    """The certificate is unusable or proves nothing: the property is not decided ("indeterminat")."""


class _BadFunction(Exception):
    """f itself is not a valid answer (undefined off the origin, f(0,0) not a real number): "falla"."""


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


def _limit(expr: sp.Expr, var: sp.Symbol, side: str = "+-") -> _Limit:
    lim = _sympy_limit(expr, var, side)
    if lim is None:
        return _Limit(None)
    if isinstance(lim, _DoesNotExist):
        return _Limit(False) if _numerically_unsettled(expr, var, side) else _Limit(None)
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
                    return _Limit(True, value)
        # sympy's "no limit" is a proof only if f visibly keeps oscillating (or jumping, or growing) at every scale.
        return _Limit(False, lim) if _numerically_unsettled(expr, var, side) else _Limit(None)
    value = sp.simplify(lim)
    if _numerically_elsewhere(expr, var, side, value):
        return _Limit(None)
    return _Limit(True, value)


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


def _number(e: sp.Basic) -> float | None:
    """A real number to 30 digits (may be +-inf); None if it is not one (complex, nan, still symbolic)."""
    try:
        return _real(sp.N(e, 30))
    except Exception:
        return None


def _near_values(
    expr: sp.Expr, var: sp.Symbol, side: str, params: list[sp.Basic], p_value: sp.Expr
) -> list[tuple[float, float]] | None:
    """Per side asked for, f at the two scales of `_EPSILONS` (parameters fixed to `p_value`); None if f cannot be
    evaluated there."""
    fixed = expr.subs([(p, p_value) for p in params])
    out: list[tuple[float, float]] = []
    for sign in {"+": (1,), "-": (-1,)}.get(side, (1, -1)):
        a, b = (_number(fixed.subs(var, sign * eps)) for eps in _EPSILONS)
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
                    v = _number(fixed.subs(var, sign * sp.Float(scale * w, 30)))
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
        target = _number(value.subs([(p, p_value) for p in params]))
        near = _near_values(expr, var, side, params, p_value)
        if target is None or near is None or not math.isfinite(target):
            continue
        for a, b in near:
            if _settled(a, b) and abs(b - target) > 1e-3 * max(1.0, abs(target)):
                return True
            if abs(b) > 1e3 * max(1.0, abs(target)) and abs(b) > 2 * abs(a):
                return True
    return False


def _compare(a: sp.Expr, b: sp.Expr) -> bool | None:
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


def _at(g: sp.Expr, px: sp.Expr | int, py: sp.Expr | int) -> sp.Expr:
    out = g.subs({X: px, Y: py}, simultaneous=True)
    assert isinstance(out, sp.Expr)
    return out


def _tex(e: sp.Expr | None) -> str:
    return "?" if e is None else sp.latex(e)


def _describe(lim: _Limit) -> str:
    if lim.exists is True:
        return _tex(lim.value)
    return "\\text{no existeix}" if lim.exists is False else "\\text{?}"


@dataclass
class _Ctx:
    g: sp.Expr
    c: sp.Expr
    cert: Certificate
    lines: list[str]
    context_paths: list[Path] = field(default_factory=list)  # every path of the submission, for cross-checks

    def log(self, line: str) -> None:
        self.lines.append(line)

    def partial(self, var: str) -> _Limit:
        quotient = (_at(self.g, _H, 0) - self.c) / _H if var == "x" else (_at(self.g, 0, _H) - self.c) / _H
        lim = _limit(quotient, _H)
        self.log(f"\\partial_{var} f(0,0) = {_describe(lim)}")
        return lim

    def directional(self, u: sp.Expr, w: sp.Expr) -> _Limit:
        return _limit((_at(self.g, _H * u, _H * w) - self.c) / _H, _H)

    def paths(self) -> Iterator[tuple[int, sp.Expr, sp.Expr]]:
        for i, p in enumerate(self.cert.paths, 1):
            px, py = _path(p, i)
            yield i, px, py

    def along(self, expr: sp.Expr, px: sp.Expr, py: sp.Expr, i: int, what: str = "f") -> _Limit:
        on_path = _at(expr, px, py)
        # A path through a hole of f (a zero of a denominator, a log of a negative) proves nothing about the limit.
        for k in (2, 3, 4, 5, 7):
            value = on_path.subs(T, sp.Rational(1, 10**k))
            if value.has(sp.zoo, sp.nan, sp.oo, -sp.oo) or _number(value) is None:
                raise _BadCertificate(f"${what}$ no està definida sobre el camí {i} (per exemple a $t=10^{{-{k}}}$).")
        lim = _limit(on_path, T, "+")
        self.log(f"\\text{{Camí {i}: }}\\lim_{{t\\to0^+}} {what}({sp.latex(px)}, {sp.latex(py)}) = {_describe(lim)}")
        return lim


def _parse(text: str, allowed: set[str], what: str) -> sp.Expr:
    try:
        expr = parse(text)
    except InvalidExpression as e:
        raise _BadCertificate(f"{what}: {e}") from e
    if any(str(s) not in allowed for s in expr.free_symbols):
        raise _BadCertificate(f"{what}: variable no permesa")
    if (constant := extreme_constant(expr)) is not None:
        raise _BadCertificate(
            f"{what}: la constant ${sp.latex(constant)}$ és massa gran o massa petita "
            f"(com a molt {MAX_CONSTANT:g} en valor absolut, i no per sota de {1 / MAX_CONSTANT:g})."
        )
    return expr


def _real_roots(expr: sp.Expr) -> sp.Expr:
    """b**(p/q) with q odd as the real root, which is what a student means by (x*y)**(1/3): sympy's is the complex
    principal root for b < 0. Same form as cbrt."""

    def odd_root(e: sp.Basic) -> bool:
        return (
            isinstance(e, sp.Pow)
            and isinstance(e.exp, sp.Rational)
            and not e.exp.is_Integer
            and e.exp.q % 2 == 1
            and e.base.is_nonnegative is not True
        )

    def real(e: sp.Pow) -> sp.Expr:
        p = e.exp
        assert isinstance(p, sp.Rational)
        magnitude = sp.Pow(sp.Abs(e.base), p)
        return sp.sign(e.base) * magnitude if p.p % 2 else magnitude

    out = expr.replace(odd_root, real)  # type: ignore[arg-type]
    assert isinstance(out, sp.Expr)
    return out


def _path(p: Path, i: int) -> tuple[sp.Expr, sp.Expr]:
    px, py = _parse(p.x, {"t"}, f"Camí {i}"), _parse(p.y, {"t"}, f"Camí {i}")
    for comp in (px, py):
        lim = _limit(comp, T, "+")
        if lim.exists is not True or lim.value is None or _compare(lim.value, sp.Integer(0)) is not True:
            raise _BadCertificate(f"El camí {i} no tendeix a l'origen quan $t\\to0^+$")
    try:
        off_origin = any(float(sp.N((px**2 + py**2).subs(T, s))) > 0 for s in (1e-2, 3e-3, 1e-3))
    except (TypeError, ValueError):
        off_origin = True
    if not off_origin:
        raise _BadCertificate(f"El camí {i} es queda a l'origen: ha de ser un camí diferent de $(0,0)$")
    return px, py


def _float_sign(v: float) -> float:
    return float((v > 0) - (v < 0))


# Plain floats wherever the math module has the function (fast); mpmath only for the rest. sign is the usual
# exception to math, and with tens of thousands of sampled points an mpmath fallback costs seconds.
_FLOAT_FUNCTIONS = {"sign": _float_sign}


def _numeric(expr: sp.Expr, args: tuple[sp.Symbol, ...]) -> Callable[..., object]:
    return sp.lambdify(args, expr, modules=[_FLOAT_FUNCTIONS, "math", "mpmath"])


def _real(value: object) -> float | None:
    try:
        v = complex(value)  # type: ignore[arg-type]
    except (TypeError, ValueError, OverflowError, ZeroDivisionError):
        return None
    if math.isnan(v.real) or math.isnan(v.imag) or abs(v.imag) > 1e-12 * max(1.0, abs(v.real)):
        return None
    return v.real  # may be +-inf: a bound check counts it as a violation


def _bound(ctx: _Ctx, expr: sp.Expr, target: sp.Expr, what: str) -> tuple[VerdictStatus, str]:
    """|expr - target| <= G(r) near the origin, with G the student's bound: G -> 0 exactly, the inequality sampled."""
    if not ctx.cert.bound.strip():
        raise _Undecided(f"Falta la fita $G(r)$ per a {what}.")
    G = _parse(ctx.cert.bound, {"r"}, "La fita")
    ctx.log(f"G(r) = {sp.latex(G)}")
    lim = _limit(G, R, "+")
    if lim.exists is None:
        raise _Undecided("sympy no pot calcular el límit de $G(r)$ quan $r\\to0^+$.")
    if lim.exists is False or lim.value is None or _compare(lim.value, sp.Integer(0)) is not True:
        return (
            "indeterminat",
            f"$G(r)$ no tendeix a 0 quan $r\\to0^+$ (tendeix a ${_describe(lim)}$): no és una fita útil.",
        )
    # Exact first: along fixed rays and every path of the submission, expr must tend to target. A bound can only be
    # sampled, and a feature thinner than the grid (a spike on a line, a change below the smallest radius) slips by.
    if (refuted := _refuted_on_curves(ctx, expr - target)) is not None:
        return "falla", refuted
    polar = sp.Abs(_at(expr - target, R * sp.cos(_THETA), R * sp.sin(_THETA)))
    try:
        f_num, g_num = _numeric(polar, (R, _THETA)), _numeric(G, (R,))
    except Exception as e:
        raise _Undecided(f"No s'ha pogut avaluar numèricament ({type(e).__name__}).") from e
    rng = random.Random(zlib.crc32(f"{expr}|{G}".encode()))  # reproducible per submission
    scattered = [(R_MAX * 10 ** (-12 * rng.random()), 2 * math.pi * rng.random()) for _ in range(600)]
    grid = [
        (r, theta)
        for r in _RADII
        # The angles of the grid, plus angles that hug the axes as r shrinks (curves like y = x^2, y^2 = x^3).
        for theta in (
            *_ANGLES,
            *(b + s * r**p for b in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2) for s in (1, -1) for p in _HUG_POWERS),
        )
    ]
    # A fine angular sweep at a few radii: a feature narrow in angle (a spike along a line) is only seen this way.
    sweep = [(r, theta) for r in _SWEEP_RADII for theta in _SWEEP_ANGLES]
    evaluated = total = 0
    for r, theta in (*grid, *sweep, *scattered):
        total += 1
        g_val = _real(_safe(g_num, r))
        e_val = _real(_safe(f_num, r, theta))
        if e_val is None or g_val is None or not math.isfinite(g_val):
            continue
        evaluated += 1
        if e_val > g_val * (1 + 1e-9) + 1e-12:
            x, y = r * math.cos(theta), r * math.sin(theta)
            return "indeterminat", (
                f"La fita no es compleix: a $(x,y)\\approx({x:.3g}, {y:.3g})$ (r = {r:.3g}) "
                f"el valor és {e_val:.4g} i $G(r)$ = {g_val:.4g}. Busca una fita més gran."
            )
    if evaluated < _MIN_EVALUATED * total:
        raise _Undecided("No s'ha pogut avaluar la funció en prou punts per comprovar la fita.")
    return "plausible", (
        f"$G(r)\\to0$ i la fita es compleix en els {evaluated} punts provats amb $0<r\\le{R_MAX}$ "
        "(comprovació numèrica, no una demostració)."
    )


_RAYS: tuple[tuple[int, int], ...] = (*DIRECTIONS, (-1, 0), (0, -1), (-1, -1), (-1, 1), (3, 1), (1, 3), (-3, 2))
_CURVE_FAMILY: tuple[tuple[int, int, int], ...] = tuple((p, c, s) for p in (2, 3) for c in (1, -1, 2) for s in (1, -1))


def _refuted_on_curves(ctx: _Ctx, expr: sp.Expr) -> str | None:
    """Why expr does not tend to 0 at the origin, found on a ray or on a path given anywhere in the submission."""
    curves = [(f"raig $({u},{w})t$", sp.Integer(u) * T, sp.Integer(w) * T) for u, w in _RAYS]
    # Both branches of y = c x^p and x = c y^p: the curves tangent to an axis where a discontinuity hides from rays.
    for p, c, s in _CURVE_FAMILY:
        along, across = s * T, c * T**p
        curves.append((f"camí $({sp.latex(along)}, {sp.latex(across)})$", along, across))
        curves.append((f"camí $({sp.latex(across)}, {sp.latex(along)})$", across, along))
    for i, p in enumerate(ctx.context_paths, 1):
        try:
            px, py = _path(p, i)
        except _BadCertificate:
            continue
        curves.append((f"camí $({sp.latex(px)}, {sp.latex(py)})$", px, py))
    for label, px, py in curves:
        lim = _limit(_at(expr, px, py), T, "+")
        if lim.exists is False:
            return f"Pel {label} no té límit quan $t\\to0^+$, i hauria de tendir a 0: la fita no pot ser certa."
        if lim.exists and lim.value is not None and _compare(lim.value, sp.Integer(0)) is False:
            return f"Pel {label} tendeix a ${_tex(lim.value)} \\ne 0$: la fita no pot ser certa."
    return None


def _safe(fn: Callable[..., object], *args: float) -> object:
    try:
        return fn(*args)
    except Exception:
        return None


def _missing_paths(ctx: _Ctx) -> None:
    if not ctx.cert.paths:
        raise _Undecided("Falta el certificat: " + PROPERTIES["limit_no_existeix"].help)


def _limit_refuted(ctx: _Ctx, against_value: bool) -> tuple[VerdictStatus, str]:
    """By paths: no limit along one, two different limits, or (for discontinuity) a limit other than f(0,0)."""
    _missing_paths(ctx)
    found: list[tuple[int, sp.Expr]] = []
    unknown = False
    for i, px, py in ctx.paths():
        lim = ctx.along(ctx.g, px, py, i)
        if lim.exists is False:
            return "ok", f"Pel camí {i} el límit no existeix."
        if lim.exists is None or lim.value is None:
            unknown = True
            continue
        if against_value and _compare(lim.value, ctx.c) is False:
            return "ok", f"Pel camí {i} el límit és ${_tex(lim.value)} \\ne f(0,0) = {_tex(ctx.c)}$."
        found.append((i, lim.value))
    if len(found) == 2 and _compare(found[0][1], found[1][1]) is False:
        return "ok", f"Els dos camins donen límits diferents: ${_tex(found[0][1])}$ i ${_tex(found[1][1])}$."
    if unknown:
        raise _Undecided("sympy no ha pogut calcular el límit per algun camí.")
    if against_value:
        return (
            "indeterminat",
            "Pels camins donats el límit és $f(0,0)$: no proven la discontinuïtat. Busca un camí on no ho sigui.",
        )
    if len(found) == 1:
        return "indeterminat", (
            f"Pel camí donat el límit existeix (${_tex(found[0][1])}$). Un sol camí només prova que el límit no "
            "existeix si per ell no té límit: afegeix un segon camí amb un límit diferent."
        )
    return "indeterminat", "Els dos camins tenen el mateix límit: no proven que el límit no existeixi."


def _lines_at_value(ctx: _Ctx) -> tuple[VerdictStatus, str]:
    status, detail = _lines(ctx)
    if status not in ("ok", "plausible"):
        return status, detail
    common = _limit(_at(ctx.g, 0, _H), _H)
    if common.value is not None and _compare(common.value, ctx.c) is False:
        return "falla", f"El límit per les rectes és ${_tex(common.value)}$, però $f(0,0) = {_tex(ctx.c)}$."
    return status, detail


def _lines(ctx: _Ctx) -> tuple[VerdictStatus, str]:
    vertical = _limit(_at(ctx.g, 0, _H), _H)
    ctx.log(f"\\text{{Recta }} x=0: {_describe(vertical)}")
    values: list[tuple[str, sp.Expr]] = []
    for label, lim in [("x=0", vertical)] + [(_line_label(m), _limit(_at(ctx.g, _H, m * _H), _H)) for m in SLOPES]:
        if lim.exists is False:
            return "falla", f"Per la recta ${label}$ el límit no existeix."
        if lim.exists is None or lim.value is None:
            raise _Undecided(f"sympy no ha pogut calcular el límit per la recta ${label}$.")
        values.append((label, lim.value))
    for label, value in values[1:]:
        if _compare(value, values[0][1]) is False:
            return "falla", (
                f"Per ${values[0][0]}$ el límit és ${_tex(values[0][1])}$ i per ${label}$ és ${_tex(value)}$."
            )
    special, complete = _special_slopes(_at(ctx.g, _H, _M * _H))
    for m in dict.fromkeys([*special, *_path_slopes(ctx)]):
        lim = _limit(_at(ctx.g, _H, m * _H), _H)
        label = f"y={sp.latex(m)}\\,x"
        if lim.exists is False:
            return "falla", f"Per la recta ${label}$ el límit no existeix."
        if lim.exists is None or lim.value is None:
            raise _Undecided(f"sympy no ha pogut calcular el límit per la recta ${label}$.")
        if _compare(lim.value, values[0][1]) is False:
            return (
                "falla",
                f"Per ${values[0][0]}$ el límit és ${_tex(values[0][1])}$ i per ${label}$ és ${_tex(lim.value)}$.",
            )
    generic = _limit(_at(ctx.g, _H, _M * _H), _H)
    shown = _Limit(generic.exists, generic.value.subs(_M, sp.Symbol("m"))) if generic.value is not None else generic
    ctx.log(f"\\text{{Recta }} y=mx: {_describe(shown)}")
    if generic.exists is True and generic.value is not None:
        same = _compare(generic.value, values[0][1])
        if same is False:
            return "falla", f"Per la recta $y=mx$ el límit és ${_tex(generic.value)}$: depèn de $m$."
        # "ok" only when every slope where sympy's generic answer could change has been tried.
        if same is True and complete:
            return "ok", f"Per totes les rectes el límit és ${_tex(values[0][1])}$."
    if not complete:
        raise _Undecided(_INCOMPLETE_LINES.format(value=_tex(values[0][1])))
    return "plausible", (
        f"Per les rectes provades el límit és ${_tex(values[0][1])}$; sympy no ha pogut fer el càlcul per a $m$ qualsevol."
    )


def _iterated(ctx: _Ctx) -> tuple[VerdictStatus, str]:
    results: list[_Limit] = []
    for inner_var, outer_var, label in ((Y, X, "\\lim_{x\\to0}\\lim_{y\\to0}"), (X, Y, "\\lim_{y\\to0}\\lim_{x\\to0}")):
        inner = _limit(ctx.g, inner_var)  # the other variable is a generic (nonzero) parameter
        outer = _limit(inner.value, outer_var) if inner.exists is True and inner.value is not None else inner
        ctx.log(f"{label} f = {_describe(outer)}")
        results.append(outer)
    if any(r.exists is False for r in results):
        return "falla", "Algun dels límits iterats no existeix."
    if any(r.exists is None or r.value is None for r in results):
        raise _Undecided("sympy no ha pogut calcular els límits iterats.")
    a, b = results[0].value, results[1].value
    assert a is not None and b is not None
    same = _compare(a, b)
    if same is None:
        raise _Undecided("sympy no pot comparar els dos límits iterats.")
    return (
        ("ok", f"Els dos límits iterats valen ${_tex(a)}$.")
        if same
        else (
            "falla",
            f"Els límits iterats són diferents: ${_tex(a)}$ i ${_tex(b)}$.",
        )
    )


def _partials_exist(ctx: _Ctx) -> tuple[VerdictStatus, str]:
    px, py = ctx.partial("x"), ctx.partial("y")
    for var, lim in (("x", px), ("y", py)):
        if lim.exists is False:
            return "falla", f"$\\partial_{var} f(0,0)$ no existeix."
    if px.exists is None or py.exists is None:
        raise _Undecided("sympy no ha pogut calcular alguna derivada parcial.")
    return "ok", "Les dues derivades parcials existeixen."


def _some_partial_missing(ctx: _Ctx) -> tuple[VerdictStatus, str]:
    px, py = ctx.partial("x"), ctx.partial("y")
    for var, lim in (("x", px), ("y", py)):
        if lim.exists is False:
            return "ok", f"$\\partial_{var} f(0,0)$ no existeix."
    if px.exists is None or py.exists is None:
        raise _Undecided("sympy no ha pogut calcular alguna derivada parcial.")
    return "falla", "Les dues derivades parcials existeixen."


def _directionals_exist(ctx: _Ctx) -> tuple[VerdictStatus, str]:
    directions, complete = _directions_to_try(ctx)
    for u, w in directions:
        lim = ctx.directional(u, w)
        if lim.exists is False:
            ctx.log(f"D_{{({sp.latex(u)},{sp.latex(w)})}} f(0,0) = {_describe(lim)}")
            return "falla", f"La derivada direccional en la direcció $({sp.latex(u)},{sp.latex(w)})$ no existeix."
        if lim.exists is None:
            raise _Undecided(f"sympy no ha pogut calcular la derivada en la direcció $({sp.latex(u)},{sp.latex(w)})$.")
    for u, w in DIRECTIONS:
        ctx.log(f"D_{{({u},{w})}} f(0,0) = {_describe(ctx.directional(sp.Integer(u), sp.Integer(w)))}")
    # The fixed directions decide a failure; a symbolic (a, b) is only evidence, and sympy can fail on it where
    # every concrete direction works (sign(x^3+y^3)*Abs(x^3+y^3)^(1/3)).
    if not complete:
        raise _Undecided(_INCOMPLETE_DIRECTIONS.format(n=len(directions)))
    generic = ctx.directional(_A, _B)
    if generic.exists is True:
        assert generic.value is not None
        shown = generic.value.subs({_A: sp.Symbol("a"), _B: sp.Symbol("b")})
        ctx.log(f"D_{{(a,b)}} f(0,0) = {sp.latex(shown)}")
        return "plausible", (
            "Existeix en una direcció genèrica $(a,b)$ i en totes les direccions provades "
            "(sympy suposa $(a,b)$ genèric: les direccions especials s'han provat a part)."
        )
    return "plausible", (
        f"Existeix en les {len(directions)} direccions provades (una cada 7,5°, les especials i les dels teus camins); "
        "sympy no ha pogut fer el càlcul en una direcció qualsevol $(a,b)$."
    )


def _directions_to_try(ctx: _Ctx) -> tuple[list[tuple[sp.Expr, sp.Expr]], bool]:
    """The fixed directions, a direction every 7.5 degrees, the special directions (1, m) of f along y = m x, and the
    direction in which each path of the submission leaves the origin (a feature along a line the student singled out
    is where to look). False when the special directions could not all be found."""
    special, complete = _special_slopes(_at(ctx.g, _H, _M * _H))
    out: list[tuple[sp.Expr, sp.Expr]] = [(sp.Integer(u), sp.Integer(w)) for u, w in _PROBE_DIRECTIONS]
    out += [(sp.Integer(1), m) for m in special]
    out += _path_directions(ctx)
    return list(dict.fromkeys(out)), complete


def _path_directions(ctx: _Ctx) -> list[tuple[sp.Expr, sp.Expr]]:
    """The direction in which each path of the submission leaves the origin."""
    out: list[tuple[sp.Expr, sp.Expr]] = []
    for i, p in enumerate(ctx.context_paths, 1):
        try:
            px, py = _path(p, i)
        except _BadCertificate:
            continue
        slope = _limit(py / px, T, "+") if px != 0 else _Limit(None)
        if slope.exists and slope.value is not None and slope.value.is_real:
            x_sign = _limit(sp.sign(px), T, "+").value or sp.Integer(1)
            out.append((x_sign, x_sign * slope.value))
        elif px == 0 or (_limit(px / py, T, "+").value == 0 if py != 0 else False):
            out.append((sp.Integer(0), _limit(sp.sign(py), T, "+").value or sp.Integer(1)))
    return out


def _directionals_linear(ctx: _Ctx) -> tuple[VerdictStatus, str]:
    """D_v f(0,0) = grad f(0,0) . v for every v: on every direction tried, then for a symbolic (a, b)."""
    px, py = ctx.partial("x"), ctx.partial("y")
    for var, lim in (("x", px), ("y", py)):
        if lim.exists is False:
            return "falla", f"$\\partial_{var} f(0,0)$ no existeix."
    if px.value is None or py.value is None:
        raise _Undecided("sympy no ha pogut calcular alguna derivada parcial.")
    a, b = px.value, py.value
    directions, complete = _directions_to_try(ctx)
    for u, w in directions:
        lim = ctx.directional(u, w)
        v = f"({sp.latex(u)},{sp.latex(w)})"
        if lim.exists is False:
            return "falla", f"La derivada direccional en la direcció ${v}$ no existeix."
        if lim.exists is None or lim.value is None:
            raise _Undecided(f"sympy no ha pogut calcular la derivada en la direcció ${v}$.")
        linear = sp.simplify(u * a + w * b)
        if _compare(lim.value, linear) is False:
            ctx.log(f"D_{{{v}}} f(0,0) = {_tex(lim.value)} \\ne \\nabla f(0,0)\\cdot v = {_tex(linear)}")
            return "falla", (
                f"$D_v f(0,0) = {_tex(lim.value)}$ però $\\nabla f(0,0)\\cdot v = {_tex(linear)}$ per a $v={v}$: "
                "la derivada direccional no és lineal en $v$."
            )
    ctx.log(f"\\nabla f(0,0) = ({_tex(a)}, {_tex(b)})")
    if not complete:
        raise _Undecided(_INCOMPLETE_DIRECTIONS.format(n=len(directions)))
    generic = ctx.directional(_A, _B)
    if generic.exists is True and generic.value is not None:
        shown = generic.value.subs({_A: sp.Symbol("a"), _B: sp.Symbol("b")})
        ctx.log(f"D_{{(a,b)}} f(0,0) = {sp.latex(shown)}")
        if _compare(generic.value, _A * a + _B * b) is False:
            linear = sp.latex(sp.Symbol("a") * a + sp.Symbol("b") * b)
            return "falla", (
                f"En una direcció genèrica $v=(a,b)$, $D_v f(0,0) = {sp.latex(shown)}$, que no és "
                f"$\\nabla f(0,0)\\cdot v = {linear}$."
            )
    return "plausible", (
        f"$D_v f(0,0) = \\nabla f(0,0)\\cdot v$ en les {len(directions)} direccions provades"
        + (" i en una direcció genèrica $(a,b)$" if generic.exists is True else "")
        + " (comprovació en direccions concretes, no una demostració per a tota $v$)."
    )


_INCOMPLETE_LINES = (
    "Per les rectes provades el límit és ${value}$, però $f$ sobre $y=mx$ no és d'un tipus on sympy pugui trobar "
    "totes les pendents especials, i no es pot garantir per a tota $m$. Si hi ha una recta sospitosa, dona-la com a "
    "camí en un altre certificat."
)
_INCOMPLETE_DIRECTIONS = (
    "Existeix en les {n} direccions provades, però $f$ sobre $y=mx$ no és d'un tipus on sympy pugui trobar totes les "
    "direccions especials, i no es pot garantir per a tota direcció. Si n'hi ha una de sospitosa, dona-la com a camí "
    "en un altre certificat."
)


def _some_directional_missing(ctx: _Ctx) -> tuple[VerdictStatus, str]:
    d = ctx.cert.direction
    if d is None:
        raise _Undecided("Falta el certificat: " + PROPERTIES["alguna_direccional_no_existeix"].help)
    u, w = _parse(d.u, set(), "La direcció"), _parse(d.w, set(), "La direcció")
    if any(_number(c) in (None, math.inf, -math.inf) for c in (u, w)):
        raise _BadCertificate("La direcció ha de ser un vector de nombres reals.")
    if _compare(u, sp.Integer(0)) and _compare(w, sp.Integer(0)):
        raise _BadCertificate("La direcció no pot ser el vector zero.")
    lim = ctx.directional(u, w)
    ctx.log(f"D_{{({sp.latex(u)},{sp.latex(w)})}} f(0,0) = {_describe(lim)}")
    if lim.exists is False:
        return "ok", f"En la direcció $({_tex(u)},{_tex(w)})$ la derivada direccional no existeix."
    if lim.exists is None:
        raise _Undecided("sympy no ha pogut calcular la derivada direccional.")
    return "indeterminat", (
        f"En la direcció donada la derivada direccional existeix i val ${_tex(lim.value)}$: prova una altra direcció."
    )


def _remainder(ctx: _Ctx, a: sp.Expr, b: sp.Expr) -> sp.Expr:
    return (ctx.g - ctx.c - a * X - b * Y) / sp.sqrt(X**2 + Y**2)


def _not_differentiable_automatic(ctx: _Ctx) -> tuple[str | None, tuple[sp.Expr, sp.Expr] | None]:
    """A reason f is not differentiable found without a certificate, and the gradient when both partials exist."""
    px, py = ctx.partial("x"), ctx.partial("y")
    for var, lim in (("x", px), ("y", py)):
        if lim.exists is False:
            return f"$\\partial_{var} f(0,0)$ no existeix.", None
    if px.value is None or py.value is None:
        return None, None
    a, b = px.value, py.value
    for u, w in DIRECTIONS[2:]:
        lim = ctx.directional(sp.Integer(u), sp.Integer(w))
        if lim.exists is False:
            ctx.log(f"D_{{({u},{w})}} f(0,0) = {_describe(lim)}")
            return f"La derivada direccional en la direcció $({u},{w})$ no existeix.", (a, b)
        if lim.exists is True and lim.value is not None:
            linear = sp.simplify(u * a + w * b)
            if _compare(lim.value, linear) is False:
                ctx.log(f"D_{{({u},{w})}} f(0,0) = {_tex(lim.value)} \\ne \\nabla f(0,0)\\cdot v = {_tex(linear)}")
                return (
                    f"$D_v f(0,0) = {_tex(lim.value)}$ però $\\nabla f(0,0)\\cdot v = {_tex(linear)}$ "
                    f"per a $v=({u},{w})$: la derivada direccional no és lineal en $v$."
                ), (a, b)
    return None, (a, b)


def _differentiable(ctx: _Ctx) -> tuple[VerdictStatus, str]:
    reason, gradient = _not_differentiable_automatic(ctx)
    if reason is not None:
        return "falla", reason
    if gradient is None:
        raise _Undecided("sympy no ha pogut calcular les derivades parcials.")
    return _bound(ctx, _remainder(ctx, *gradient), sp.Integer(0), "el residu de la diferencial")


def _not_differentiable(ctx: _Ctx) -> tuple[VerdictStatus, str]:
    reason, gradient = _not_differentiable_automatic(ctx)
    if reason is not None:
        return "ok", reason
    if not ctx.cert.paths:
        raise _Undecided("No s'ha pogut decidir sense certificat. " + PROPERTIES["no_diferenciable"].help)
    unknown = False
    for i, px, py in ctx.paths():
        lim = ctx.along(ctx.g, px, py, i)
        if lim.exists is False or (lim.exists and lim.value is not None and _compare(lim.value, ctx.c) is False):
            return "ok", f"$f$ no és contínua a l'origen (camí {i}), i per tant no és diferenciable."
        if gradient is not None:
            rest = ctx.along(_remainder(ctx, *gradient), px, py, i, what="\\text{residu}")
            if rest.exists is False:
                return "ok", f"Pel camí {i} el residu de la diferencial no té límit."
            if rest.exists and rest.value is not None and _compare(rest.value, sp.Integer(0)) is False:
                return "ok", f"Pel camí {i} el residu de la diferencial tendeix a ${_tex(rest.value)} \\ne 0$."
            unknown = unknown or rest.exists is None
        unknown = unknown or lim.exists is None
    if unknown:
        raise _Undecided("sympy no ha pogut calcular algun límit pels camins donats.")
    return "indeterminat", (
        "Pels camins donats $f\\to f(0,0)$ i el residu tendeix a 0: no proven la no-diferenciabilitat."
    )


def _partial_discontinuous(ctx: _Ctx) -> tuple[VerdictStatus, str]:
    var = ctx.cert.partial
    if var is None or not ctx.cert.paths:
        raise _Undecided("Falta el certificat: " + PROPERTIES["parcial_discontinua"].help)
    at_origin = ctx.partial(var)
    if at_origin.exists is False:
        return "falla", f"$\\partial_{var} f(0,0)$ no existeix (la propietat demana que existeixi)."
    if at_origin.value is None:
        raise _Undecided(f"sympy no ha pogut calcular $\\partial_{var} f(0,0)$.")
    derivative = sp.diff(ctx.g, X if var == "x" else Y)
    ctx.log(f"\\partial_{var} f(x,y) = {sp.latex(sp.simplify(derivative))} \\quad ((x,y)\\ne(0,0))")
    unknown = False
    for i, px, py in ctx.paths():
        lim = ctx.along(derivative, px, py, i, what=f"\\partial_{var} f")
        if lim.exists is False:
            return "ok", f"Pel camí {i}, $\\partial_{var} f$ no té límit a l'origen."
        if lim.value is not None and _compare(lim.value, at_origin.value) is False:
            return "ok", (
                f"Pel camí {i}, $\\partial_{var} f \\to {_tex(lim.value)} \\ne \\partial_{var} f(0,0) = "
                f"{_tex(at_origin.value)}$."
            )
        unknown = unknown or lim.exists is None
    if unknown:
        raise _Undecided("sympy no ha pogut calcular el límit pel camí.")
    return (
        "indeterminat",
        f"Pels camins donats $\\partial_{var} f$ tendeix a $\\partial_{var} f(0,0)$: prova un altre camí.",
    )


def _mixed_partials(ctx: _Ctx) -> tuple[VerdictStatus, str]:
    px, py = ctx.partial("x"), ctx.partial("y")
    if px.exists is False or py.exists is False:
        return "falla", "Calen les dues derivades parcials a l'origen."
    if px.value is None or py.value is None:
        raise _Undecided("sympy no ha pogut calcular alguna derivada parcial.")
    # d/dy (df/dx) at the origin: df/dx on the axis x = 0 (k != 0), then a quotient in k. Symmetrically the other.
    fx_axis = _limit((_at(ctx.g, _H, _K) - _at(ctx.g, 0, _K)) / _H, _H)
    fy_axis = _limit((_at(ctx.g, _HK, _H) - _at(ctx.g, _HK, 0)) / _H, _H)
    if fx_axis.value is None or fy_axis.value is None:
        raise _Undecided("sympy no ha pogut calcular les derivades parcials sobre els eixos.")
    fyx = _limit((fx_axis.value - px.value) / _K, _K)
    fxy = _limit((fy_axis.value - py.value) / _HK, _HK)
    # D_yD_x f = d/dy (df/dx): the order written out, since the notes' d2f/dxdy convention is easy to misread.
    ctx.log(f"D_yD_xf(0,0) = {_describe(fyx)}")
    ctx.log(f"D_xD_yf(0,0) = {_describe(fxy)}")
    if fyx.exists is False or fxy.exists is False:
        return "falla", "Alguna de les derivades creuades no existeix a l'origen."
    if fyx.value is None or fxy.value is None:
        raise _Undecided("sympy no ha pogut calcular les derivades creuades.")
    same = _compare(fyx.value, fxy.value)
    if same is None:
        raise _Undecided("sympy no pot comparar les derivades creuades.")
    if same:
        return "falla", f"Les dues derivades creuades valen ${_tex(fyx.value)}$."
    return "ok", f"$D_yD_xf(0,0) = {_tex(fyx.value)}$ i $D_xD_yf(0,0) = {_tex(fxy.value)}$."


_DECIDERS: Mapping[PropertyKind, Callable[[_Ctx], tuple[VerdictStatus, str]]] = {
    "rectes_mateix_limit": _lines,
    "rectes_limit_f0": _lines_at_value,
    "iterats_iguals": _iterated,
    "limit_no_existeix": lambda ctx: _limit_refuted(ctx, against_value=False),
    "discontinua": lambda ctx: _limit_refuted(ctx, against_value=True),
    "continua": lambda ctx: _bound(ctx, ctx.g, ctx.c, "$|f(x,y)-f(0,0)|$"),
    "parcials_existeixen": _partials_exist,
    "alguna_parcial_no_existeix": _some_partial_missing,
    "direccionals_existeixen": _directionals_exist,
    "direccionals_lineals": _directionals_linear,
    "alguna_direccional_no_existeix": _some_directional_missing,
    "diferenciable": _differentiable,
    "no_diferenciable": _not_differentiable,
    "parcial_discontinua": _partial_discontinuous,
    "creuades_diferents": _mixed_partials,
}


def check_property(check: PropertyCheck) -> PropertyVerdict:
    """Module-level and picklable: the unit of work sent to a sympy worker process."""
    ctx = _Ctx(g=sp.Integer(0), c=sp.Integer(0), cert=check.certificate, lines=[], context_paths=check.context_paths)
    try:
        try:
            ctx.g = _real_roots(_parse(check.function, {"x", "y"}, "La funció"))
            ctx.c = _parse(check.origin_value, set(), "El valor a l'origen")
        except _BadCertificate as e:
            raise _BadFunction(str(e)) from e
        if _number(ctx.c) in (None, math.inf, -math.inf):
            raise _BadFunction("$f(0,0)$ ha de ser un nombre real.")
        _check_defined(ctx.g)
        status, detail = _DECIDERS[check.kind](ctx)
    except _BadFunction as e:
        status, detail = "falla", str(e)
    except (_BadCertificate, _Undecided) as e:
        status, detail = "indeterminat", str(e)
    except Exception as e:  # a sympy bug must not take the request down
        status, detail = "indeterminat", f"error de sympy ({type(e).__name__})"
    return PropertyVerdict(kind=check.kind, status=status, detail=detail, computations=ctx.lines)


def undecided(check: PropertyCheck, reason: str) -> PropertyVerdict:
    return PropertyVerdict(kind=check.kind, status="indeterminat", detail=reason)


def _line_label(m: sp.Expr) -> str:
    named: dict[sp.Expr, str] = {sp.Integer(0): "y=0", sp.Integer(1): "y=x", sp.Integer(-1): "y=-x"}
    return named.get(m, f"y={sp.latex(m)}\\,x")


def _path_slopes(ctx: _Ctx) -> list[sp.Expr]:
    """Slopes of the lines tangent to the submission's paths: a line the student singled out is worth checking."""
    return [w / u for u, w in _path_directions(ctx) if u != 0]


_MAX_SPECIAL = 12


def _special_slopes(on_line: sp.Expr) -> tuple[list[sp.Expr], bool]:
    """The real slopes m where f(h, m h) can behave differently from a generic m: the real roots of the coefficients
    (polynomials in m) of the numerator and denominator of each piece of it that is a rational function of h (the
    whole expression, or the arguments of the powers and functions it is built from). False when some piece that
    depends on m is not of that kind, or there are too many roots: then the generic answer is not trusted for every
    m."""
    roots: set[sp.Expr] = set()
    complete = True

    def visit(e: sp.Basic) -> None:
        nonlocal complete
        if not complete or not e.has(_M):
            return
        found = _coefficient_roots(e)
        if found is not None:
            roots.update(found)
        elif isinstance(e, sp.Pow) and not e.exp.has(_M):
            visit(e.base)
        elif isinstance(e, sp.Add | sp.Mul | sp.Abs | sp.sign | sp.exp) or (isinstance(e, sp.Function) and e.has(_H)):
            for a in e.args:
                visit(a)
        else:  # sin(m), h**m...: zeros or singular values in m that no coefficient shows
            complete = False

    visit(on_line)
    if not complete or len(roots) > _MAX_SPECIAL:
        return [], False
    return sorted(roots, key=lambda r: float(r)), True


def _coefficient_roots(e: sp.Basic) -> set[sp.Expr] | None:
    """The real roots in m of the coefficients of the numerator and denominator of e, when e is a rational function
    of h whose coefficients are polynomials in m; None otherwise."""
    roots: set[sp.Expr] = set()
    try:
        num, den = sp.fraction(sp.cancel(sp.together(e)))
        for part in (num, den):
            for coeff in sp.Poly(part, _H).coeffs():
                if not coeff.is_polynomial(_M):
                    return None
                if coeff.has(_M):
                    roots.update(r for r in sp.solve(coeff, _M) if isinstance(r, sp.Expr) and r.is_real)
    except (sp.PolynomialError, sp.GeneratorsNeeded, NotImplementedError, TypeError, ValueError):
        return None
    return roots


# Integer directions every 7.5 degrees (offset so that no grid line is special), plus the usual ones: a sector where
# f is complex or undefined has to be narrower than that to slip by.
_PROBE_DIRECTIONS = (
    *DIRECTIONS,
    (-1, 0),
    (0, -1),
    (-1, -1),
    (-1, 1),
    *((round(97 * math.cos(a)), round(97 * math.sin(a))) for a in (2 * math.pi * j / 48 + 0.071 for j in range(48))),
)


# theta ~ r^p follows y ~ x^(p+1) near an axis: the curves where a discontinuity hides from every line.
_HUG_POWERS = (0.5, *range(1, 40))
_SWEEP_ANGLES = tuple(2 * math.pi * (j + 0.37) / 4096 for j in range(4096))
_SWEEP_RADII = (0.1, 1e-3, 1e-6)
_HOLE = (
    "ha de ser una funció real a tot $\\mathbb{R}^2\\setminus\\{(0,0)\\}$. Si la fórmula té un forat (p. ex. "
    "$\\sin(1/x)$), canvia-la per una definida a tot arreu (p. ex. $\\sin(1/(x^2+y^2))$)."
)
_NOT_REAL = (
    "ha de ser una funció real a tot $\\mathbb{R}^2\\setminus\\{(0,0)\\}$, i aquí pren un valor complex: una arrel "
    "d'índex parell (sqrt, potència 1/2) o un logaritme d'un nombre negatiu, o una potència amb exponent decimal. "
    "Les arrels d'índex senar ja són reals: cbrt(x*y) o (x*y)**(1/3) valen $-1$ a $(1,-1)$."
)


def _check_defined(g: sp.Expr) -> None:
    """f must be a real function on the whole plane minus the origin: a hole on an axis would otherwise make a
    difference quotient "not exist" (1/x has no partial derivative in y because it is not defined on x = 0)."""
    # Numerically first, on a fine sweep of angles: a thin sector where f is complex (sqrt of a negative) is found.
    try:
        f_num = _numeric(g, (X, Y))
    except Exception:
        f_num = None
    for r in _SWEEP_RADII if f_num is not None else ():
        for theta in _SWEEP_ANGLES:
            x, y = r * math.cos(theta), r * math.sin(theta)
            try:
                value = complex(f_num(x, y))  # type: ignore[misc, arg-type]
            except OverflowError:
                continue
            except (ValueError, ZeroDivisionError, TypeError):
                value = complex(math.nan)
            if math.isnan(value.real) or abs(value.imag) > 1e-9 * max(1.0, abs(value.real)):
                where = f"(x,y)\\approx({x:.3g}, {y:.3g})"
                raise _BadFunction(_undefined_at(g, sp.Rational(x), sp.Rational(y), where))
    _check_denominator(g)
    for u, w in _PROBE_DIRECTIONS:
        for h in (sp.Rational(1, 10), sp.Rational(1, 1000)):
            value = _at(g, h * u, h * w)
            if value.has(sp.zoo, sp.nan) or _number(value) in (
                None,
                math.inf,
                -math.inf,
            ):
                raise _BadFunction(_undefined_at(g, h * u, h * w, f"({sp.latex(h * u)}, {sp.latex(h * w)})"))


def _undefined_at(g: sp.Expr, x: sp.Expr, y: sp.Expr, where: str) -> str:
    """Why f is not a valid answer at (x, y): a value that is not real (sqrt of a negative) or no value (a hole)."""
    try:
        value = complex(sp.N(_at(g, x, y), 30))
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
        d_num = _numeric(den, (X, Y))
    except Exception:
        return
    for r in (0.1, 1e-3, 1e-6):
        thetas = (
            *_SWEEP_ANGLES,
            *(b + s * r**p for b in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2) for s in (1, -1) for p in _HUG_POWERS),
        )
        seen: dict[bool, tuple[float, float]] = {}
        for theta in thetas:
            x, y = r * math.cos(theta), r * math.sin(theta)
            v = _real(_safe(d_num, x, y))
            if v is None or not math.isfinite(v) or v == 0 or (v > 0) in seen:
                continue
            exact = _number(sp.N(den.subs({X: sp.Rational(x), Y: sp.Rational(y)}), 50))
            if exact is not None and exact != 0:
                seen[exact > 0] = (x, y)
            if len(seen) == 2:
                raise _BadFunction(
                    f"El denominador de $f$, ${sp.latex(den)}$, canvia de signe prop de l'origen, així que s'hi anul·la: "
                    f"$f$ no hi està definida. {_HOLE}"
                )
