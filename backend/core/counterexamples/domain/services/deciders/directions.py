"""The lines and directions where f may behave differently from a generic one: the special slopes of f along
y = m x, and the directions in which the submission's paths leave the origin."""

import sympy as sp

from core.counterexamples.domain.services.deciders.context import BadCertificate, Ctx, H, M, T, at, parse_path
from core.counterexamples.domain.services.deciders.one_variable import Limit, limit
from core.counterexamples.domain.services.deciders.sampling import PROBE_DIRECTIONS


def directions_to_try(ctx: Ctx) -> tuple[list[tuple[sp.Expr, sp.Expr]], bool]:
    """The fixed directions, a direction every 7.5 degrees, the special directions (1, m) of f along y = m x, and the
    direction in which each path of the submission leaves the origin (a feature along a line the student singled out
    is where to look). False when the special directions could not all be found."""
    special, complete = special_slopes(at(ctx.g, H, M * H))
    out: list[tuple[sp.Expr, sp.Expr]] = [(sp.Integer(u), sp.Integer(w)) for u, w in PROBE_DIRECTIONS]
    out += [(sp.Integer(1), m) for m in special]
    out += path_directions(ctx)
    return list(dict.fromkeys(out)), complete


def path_directions(ctx: Ctx) -> list[tuple[sp.Expr, sp.Expr]]:
    """The direction in which each path of the submission leaves the origin."""
    out: list[tuple[sp.Expr, sp.Expr]] = []
    for i, p in enumerate(ctx.context_paths, 1):
        try:
            px, py = parse_path(p, i)
        except BadCertificate:
            continue
        slope = limit(py / px, T, "+") if px != 0 else Limit(None)
        if slope.exists and slope.value is not None and slope.value.is_real:
            x_sign = limit(sp.sign(px), T, "+").value or sp.Integer(1)
            out.append((x_sign, x_sign * slope.value))
        elif px == 0 or (limit(px / py, T, "+").value == 0 if py != 0 else False):
            out.append((sp.Integer(0), limit(sp.sign(py), T, "+").value or sp.Integer(1)))
    return out


def path_slopes(ctx: Ctx) -> list[sp.Expr]:
    """Slopes of the lines tangent to the submission's paths: a line the student singled out is worth checking."""
    return [w / u for u, w in path_directions(ctx) if u != 0]


_MAX_SPECIAL = 12


def special_slopes(on_line: sp.Expr) -> tuple[list[sp.Expr], bool]:
    """The real slopes m where f(h, m h) can behave differently from a generic m: the real roots of the coefficients
    (polynomials in m) of the numerator and denominator of each piece of it that is a rational function of h (the
    whole expression, or the arguments of the powers and functions it is built from). False when some piece that
    depends on m is not of that kind, or there are too many roots: then the generic answer is not trusted for every
    m."""
    roots: set[sp.Expr] = set()
    complete = True

    def visit(e: sp.Basic) -> None:
        nonlocal complete
        if not complete or not e.has(M):
            return
        found = _coefficient_roots(e)
        if found is not None:
            roots.update(found)
        elif isinstance(e, sp.Pow) and not e.exp.has(M):
            visit(e.base)
        elif isinstance(e, sp.Add | sp.Mul | sp.Abs | sp.sign | sp.exp) or (isinstance(e, sp.Function) and e.has(H)):
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
            for coeff in sp.Poly(part, H).coeffs():
                if not coeff.is_polynomial(M):
                    return None
                if coeff.has(M):
                    roots.update(r for r in sp.solve(coeff, M) if isinstance(r, sp.Expr) and r.is_real)
    except (sp.PolynomialError, sp.GeneratorsNeeded, NotImplementedError, TypeError, ValueError):
        return None
    return roots
