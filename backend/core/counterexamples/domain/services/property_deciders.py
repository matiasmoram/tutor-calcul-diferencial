"""Decides one property of a proposed counterexample at the origin, with sympy. Runs inside a worker process.

Only one-variable limits are trusted: a partial or directional derivative is the limit of a difference quotient in h,
a path reduces f to a function of t, an iterated limit is two one-variable limits. sympy's own two-variable limits are
never used (a polar limit with the angle left free is not uniform in the angle). A radial bound G(r) is checked
exactly for G(r) -> 0 and on a grid of points for the inequality, so a property resting on one is "plausible".

`check_property` never raises: anything sympy cannot decide comes back "indeterminat" with the reason.
"""

import math
from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass

import sympy as sp

from core.counterexamples.domain.properties import PROPERTIES, PropertyKind
from core.counterexamples.domain.values.submission import Certificate, Path, PropertyCheck
from core.counterexamples.domain.values.verdict import PropertyVerdict, VerdictStatus
from core.shared.math.sympy_checks import SYMBOLS, InvalidExpression, equal, parse

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
SLOPES: tuple[int, ...] = (0, 1, -1, 2, -3)
R_MAX = 0.5
_RADII = tuple(R_MAX * 10 ** (-k / 3) * f for k in range(19) for f in (1.0, 0.977))
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
    pass


def _limit(expr: sp.Expr, var: sp.Symbol, side: str = "+-") -> _Limit:
    try:
        lim = sp.limit(expr, var, 0, side)
    except ValueError as e:
        # sympy: "The limit does not exist since left hand limit = a and right hand limit = b". Any other
        # ValueError is sympy failing, not a proof.
        if "does not exist" not in str(e) or _numerically_settles(expr, var, side):
            return _Limit(None)
        return _Limit(False)
    except Exception:  # NotImplementedError, PoleError, recursion... : sympy cannot tell
        return _Limit(None)
    if lim.has(sp.Limit) or lim.has(sp.nan):
        return _Limit(None)
    if isinstance(lim, sp.AccumBounds) or lim.has(sp.AccumBounds) or lim.has(sp.oo, -sp.oo, sp.zoo):
        # "No limit" from sympy is a proof only if f does not visibly settle on one number near 0.
        return _Limit(None) if _numerically_settles(expr, var, side) else _Limit(False, lim)
    value = sp.simplify(lim)
    if _numerically_elsewhere(expr, var, side, value):
        return _Limit(None)
    return _Limit(True, value)


_PARAMETER_VALUES = (sp.Rational(3, 7), sp.Rational(-5, 11))
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


def _numerically_settles(expr: sp.Expr, var: sp.Symbol, side: str) -> bool:
    """Every side, at both scales, gives the same number: f clearly has a limit, whatever sympy said."""
    params = sorted(expr.free_symbols - {var}, key=str)
    for p_value in _PARAMETER_VALUES:
        near = _near_values(expr, var, side, params, p_value)
        if near is None:
            return False
        values = [v for pair in near for v in pair]
        if not _settled(min(values), max(values)):
            return False
    return True


def _numerically_elsewhere(expr: sp.Expr, var: sp.Symbol, side: str, value: sp.Expr) -> bool:
    """sympy can return a wrong finite limit (with atan(y/x) it loses a sign). Cross-check: with the parameters fixed
    to sample values, f near 0 settles (two scales agree) on a number other than sympy's. Only a clear, converged
    disagreement counts, so slow convergence (1/log) is not flagged."""
    params = sorted((expr.free_symbols | value.free_symbols) - {var}, key=str)
    for p_value in _PARAMETER_VALUES:
        target = _number(value.subs([(p, p_value) for p in params]))
        near = _near_values(expr, var, side, params, p_value)
        if target is None or near is None or not math.isfinite(target):
            continue
        for a, b in near:
            if _settled(a, b) and abs(b - target) > 1e-3 * max(1.0, abs(target)):
                return True
    return False


def _compare(a: sp.Expr, b: sp.Expr) -> bool | None:
    """True/False only when decided: two numbers are compared to 30 digits, anything else through `equal`."""
    if a.free_symbols or b.free_symbols:
        return equal(a, b)
    try:
        d = sp.simplify(a - b)
        if d == 0:
            return True
        value = complex(sp.N(d, 30))
    except (TypeError, ValueError, ZeroDivisionError):
        return None
    return False if abs(value) > 1e-20 else None


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
    return expr


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


def _numeric(expr: sp.Expr, args: tuple[sp.Symbol, ...]) -> Callable[..., object]:
    return sp.lambdify(args, expr, modules=["math", "mpmath"])


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
        return "falla", f"$G(r)$ no tendeix a 0 quan $r\\to0^+$ (tendeix a ${_describe(lim)}$)."
    polar = sp.Abs(_at(expr - target, R * sp.cos(_THETA), R * sp.sin(_THETA)))
    try:
        f_num, g_num = _numeric(polar, (R, _THETA)), _numeric(G, (R,))
    except Exception as e:
        raise _Undecided(f"No s'ha pogut avaluar numèricament ({type(e).__name__}).") from e
    evaluated = total = 0
    for r in _RADII:
        g_val = _real(_safe(g_num, r))
        # The angles of the grid, plus angles that hug the axes as r shrinks (curved paths like y = x^2).
        near_axes = [
            base + s * r**p for base in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2) for s in (1, -1) for p in (1, 2)
        ]
        for theta in (*_ANGLES, *near_axes):
            total += 1
            e_val = _real(_safe(f_num, r, theta))
            if e_val is None or g_val is None or not math.isfinite(g_val):
                continue
            evaluated += 1
            if e_val > g_val * (1 + 1e-9) + 1e-12:
                x, y = r * math.cos(theta), r * math.sin(theta)
                return "falla", (
                    f"La fita no es compleix: a $(x,y)\\approx({x:.3g}, {y:.3g})$ (r = {r:.3g}) "
                    f"el valor és {e_val:.4g} i $G(r)$ = {g_val:.4g}."
                )
    if evaluated < _MIN_EVALUATED * total:
        raise _Undecided("No s'ha pogut avaluar la funció en prou punts per comprovar la fita.")
    return "plausible", (
        f"$G(r)\\to0$ i la fita es compleix en els {evaluated} punts provats amb $0<r\\le{R_MAX}$ "
        "(comprovació numèrica, no una demostració)."
    )


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
            "falla",
            "Pels camins donats el límit és $f(0,0)$: no proven la discontinuïtat. Busca un camí on no ho sigui.",
        )
    if len(found) == 1:
        return "falla", (
            f"Pel camí donat el límit existeix (${_tex(found[0][1])}$). Un sol camí només prova que el límit no "
            "existeix si per ell no té límit: afegeix un segon camí amb un límit diferent."
        )
    return "falla", "Els dos camins tenen el mateix límit: no proven que el límit no existeixi."


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
    special = _special_slopes(_at(ctx.g, _H, _M * _H))
    for m in special or []:
        lim = _limit(_at(ctx.g, _H, m * _H), _H)
        label = f"y={sp.latex(m)}x"
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
        if same is True and special is not None:
            return "ok", f"Per totes les rectes el límit és ${_tex(values[0][1])}$."
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
    for u, w in DIRECTIONS:
        lim = ctx.directional(sp.Integer(u), sp.Integer(w))
        ctx.log(f"D_{{({u},{w})}} f(0,0) = {_describe(lim)}")
        if lim.exists is False:
            return "falla", f"La derivada direccional en la direcció $({u},{w})$ no existeix."
        if lim.exists is None:
            raise _Undecided(f"sympy no ha pogut calcular la derivada en la direcció $({u},{w})$.")
    # The fixed directions decide a failure; a symbolic (a, b) is only evidence, and sympy can fail on it where
    # every concrete direction works (sign(x^3+y^3)*Abs(x^3+y^3)^(1/3)).
    generic = ctx.directional(_A, _B)
    if generic.exists is True:
        assert generic.value is not None
        shown = generic.value.subs({_A: sp.Symbol("a"), _B: sp.Symbol("b")})
        ctx.log(f"D_{{(a,b)}} f(0,0) = {sp.latex(shown)}")
        return "plausible", (
            "Existeix en una direcció genèrica $(a,b)$ i en totes les direccions provades "
            "(sympy suposa $(a,b)$ genèric: les direccions especials s'han provat a part)."
        )
    return (
        "plausible",
        "Existeix en totes les direccions provades; sympy no ha pogut fer el càlcul en una direcció qualsevol.",
    )


def _some_directional_missing(ctx: _Ctx) -> tuple[VerdictStatus, str]:
    d = ctx.cert.direction
    if d is None:
        raise _Undecided("Falta el certificat: " + PROPERTIES["alguna_direccional_no_existeix"].help)
    u, w = _parse(d.u, set(), "La direcció"), _parse(d.w, set(), "La direcció")
    if _compare(u, sp.Integer(0)) and _compare(w, sp.Integer(0)):
        raise _BadCertificate("La direcció no pot ser el vector zero.")
    lim = ctx.directional(u, w)
    ctx.log(f"D_{{({sp.latex(u)},{sp.latex(w)})}} f(0,0) = {_describe(lim)}")
    if lim.exists is False:
        return "ok", f"En la direcció $({_tex(u)},{_tex(w)})$ la derivada direccional no existeix."
    if lim.exists is None:
        raise _Undecided("sympy no ha pogut calcular la derivada direccional.")
    return "falla", f"En la direcció donada la derivada direccional existeix i val ${_tex(lim.value)}$."


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
    return "falla", "Pels camins donats $f\\to f(0,0)$ i el residu tendeix a 0: no proven la no-diferenciabilitat."


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
    return "falla", f"Pels camins donats $\\partial_{var} f$ tendeix a $\\partial_{var} f(0,0)$."


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
    ctx.log(f"\\frac{{\\partial^2 f}}{{\\partial y\\partial x}}(0,0) = {_describe(fyx)}")
    ctx.log(f"\\frac{{\\partial^2 f}}{{\\partial x\\partial y}}(0,0) = {_describe(fxy)}")
    if fyx.exists is False or fxy.exists is False:
        return "falla", "Alguna de les derivades creuades no existeix a l'origen."
    if fyx.value is None or fxy.value is None:
        raise _Undecided("sympy no ha pogut calcular les derivades creuades.")
    same = _compare(fyx.value, fxy.value)
    if same is None:
        raise _Undecided("sympy no pot comparar les derivades creuades.")
    if same:
        return "falla", f"Les dues derivades creuades valen ${_tex(fyx.value)}$."
    return "ok", f"Les derivades creuades són ${_tex(fyx.value)}$ i ${_tex(fxy.value)}$."


_DECIDERS: Mapping[PropertyKind, Callable[[_Ctx], tuple[VerdictStatus, str]]] = {
    "rectes_mateix_limit": _lines,
    "iterats_iguals": _iterated,
    "limit_no_existeix": lambda ctx: _limit_refuted(ctx, against_value=False),
    "discontinua": lambda ctx: _limit_refuted(ctx, against_value=True),
    "continua": lambda ctx: _bound(ctx, ctx.g, ctx.c, "$|f(x,y)-f(0,0)|$"),
    "parcials_existeixen": _partials_exist,
    "alguna_parcial_no_existeix": _some_partial_missing,
    "direccionals_existeixen": _directionals_exist,
    "alguna_direccional_no_existeix": _some_directional_missing,
    "diferenciable": _differentiable,
    "no_diferenciable": _not_differentiable,
    "parcial_discontinua": _partial_discontinuous,
    "creuades_diferents": _mixed_partials,
}


def check_property(check: PropertyCheck) -> PropertyVerdict:
    """Module-level and picklable: the unit of work sent to a sympy worker process."""
    ctx = _Ctx(g=sp.Integer(0), c=sp.Integer(0), cert=check.certificate, lines=[])
    try:
        ctx.g = _parse(check.function, {"x", "y"}, "La funció")
        ctx.c = _parse(check.origin_value, set(), "El valor a l'origen")
        if _number(ctx.c) in (None, math.inf, -math.inf):
            raise _BadCertificate("$f(0,0)$ ha de ser un nombre real.")
        _check_defined(ctx.g)
        status, detail = _DECIDERS[check.kind](ctx)
    except _BadCertificate as e:
        status, detail = "falla", str(e)
    except _Undecided as e:
        status, detail = "indeterminat", str(e)
    except Exception as e:  # a sympy bug must not take the request down
        status, detail = "indeterminat", f"error de sympy ({type(e).__name__})"
    return PropertyVerdict(kind=check.kind, status=status, detail=detail, computations=ctx.lines)


def undecided(check: PropertyCheck, reason: str) -> PropertyVerdict:
    return PropertyVerdict(kind=check.kind, status="indeterminat", detail=reason)


def _line_label(m: int) -> str:
    return {0: "y=0", 1: "y=x", -1: "y=-x"}.get(m, f"y={m}x")


_MAX_SPECIAL = 12


def _special_slopes(on_line: sp.Expr) -> list[sp.Expr] | None:
    """The real slopes m where f(h, m h), a rational function of h, can behave differently from a generic m: the
    roots of the coefficients (polynomials in m) of its numerator and denominator. None when f along the line is not
    a rational function, or there are too many: then the generic answer cannot be trusted for every m."""
    try:
        num, den = sp.fraction(sp.cancel(sp.together(on_line)))
        roots: set[sp.Expr] = set()
        for part in (num, den):
            poly = sp.Poly(part, _H)
            for coeff in poly.coeffs():
                if not coeff.is_polynomial(_M):
                    return None
                if coeff.has(_M):
                    roots.update(r for r in sp.real_roots(sp.Poly(coeff, _M)) if isinstance(r, sp.Expr))
    except (sp.PolynomialError, sp.GeneratorsNeeded, NotImplementedError, TypeError, ValueError):
        return None
    if len(roots) > _MAX_SPECIAL:
        return None
    return sorted(roots, key=lambda r: float(r))


_PROBE_DIRECTIONS = (*DIRECTIONS, (-1, 0), (0, -1), (-1, -1), (-1, 1))


def _check_defined(g: sp.Expr) -> None:
    """f must be a real function on the whole plane minus the origin: a hole on an axis would otherwise make a
    difference quotient "not exist" (1/x has no partial derivative in y because it is not defined on x = 0)."""
    for u, w in _PROBE_DIRECTIONS:
        for h in (sp.Rational(1, 10), sp.Rational(1, 1000)):
            value = _at(g, h * u, h * w)
            if value.has(sp.zoo, sp.nan, sp.oo, -sp.oo) or _number(value) in (
                None,
                math.inf,
                -math.inf,
            ):
                raise _BadCertificate(
                    f"$f$ no està definida a $({sp.latex(h * u)}, {sp.latex(h * w)})$: "
                    "ha de ser una funció real a tot $\\mathbb{R}^2\\setminus\\{(0,0)\\}$."
                )
