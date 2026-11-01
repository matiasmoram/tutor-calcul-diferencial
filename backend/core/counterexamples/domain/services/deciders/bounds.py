"""A radial bound G(r): G -> 0 is checked exactly, the inequality on a grid of points ("plausible")."""

import math
import random
import zlib

import sympy as sp

from core.counterexamples.domain.services.deciders.context import (
    THETA,
    BadCertificate,
    Ctx,
    R,
    T,
    Undecided,
    at,
    describe,
    parse_expression,
    parse_path,
    tex,
)
from core.counterexamples.domain.services.deciders.numeric import float_function, real, safe
from core.counterexamples.domain.services.deciders.one_variable import compare, limit
from core.counterexamples.domain.services.deciders.sampling import DIRECTIONS, HUG_POWERS, SWEEP_ANGLES, SWEEP_RADII
from core.counterexamples.domain.values.verdict import VerdictStatus

R_MAX = 0.5
_RADII = tuple(R_MAX * 10 ** (-k / 3) * f for k in range(43) for f in (1.0, 0.977))  # down to ~1e-14
_ANGLES = tuple(2 * math.pi * j / 120 for j in range(120)) + tuple(2 * math.pi * j / 120 + 0.0123 for j in range(120))
_MIN_EVALUATED = 0.5  # of the grid points; fewer (f undefined almost everywhere?) and the bound is not judged


def bound(ctx: Ctx, expr: sp.Expr, target: sp.Expr, what: str) -> tuple[VerdictStatus, str]:
    """|expr - target| <= G(r) near the origin, with G the student's bound: G -> 0 exactly, the inequality sampled."""
    if not ctx.cert.bound.strip():
        raise Undecided(f"Falta la fita $G(r)$ per a {what}.")
    G = parse_expression(ctx.cert.bound, {"r"}, "La fita")
    ctx.log(f"G(r) = {sp.latex(G)}")
    lim = limit(G, R, "+")
    if lim.exists is None:
        raise Undecided("sympy no pot calcular el límit de $G(r)$ quan $r\\to0^+$.")
    if lim.exists is False or lim.value is None or compare(lim.value, sp.Integer(0)) is not True:
        return (
            "indeterminat",
            f"$G(r)$ no tendeix a 0 quan $r\\to0^+$ (tendeix a ${describe(lim)}$): no és una fita útil.",
        )
    # Exact first: along fixed rays and every path of the submission, expr must tend to target. A bound can only be
    # sampled, and a feature thinner than the grid (a spike on a line, a change below the smallest radius) slips by.
    if (refuted := _refuted_on_curves(ctx, expr - target)) is not None:
        return "falla", refuted
    polar = sp.Abs(at(expr - target, R * sp.cos(THETA), R * sp.sin(THETA)))
    try:
        f_num, g_num = float_function(polar, (R, THETA)), float_function(G, (R,))
    except Exception as e:
        raise Undecided(f"No s'ha pogut avaluar numèricament ({type(e).__name__}).") from e
    rng = random.Random(zlib.crc32(f"{expr}|{G}".encode()))  # reproducible per submission
    scattered = [(R_MAX * 10 ** (-12 * rng.random()), 2 * math.pi * rng.random()) for _ in range(600)]
    grid = [
        (r, theta)
        for r in _RADII
        # The angles of the grid, plus angles that hug the axes as r shrinks (curves like y = x^2, y^2 = x^3).
        for theta in (
            *_ANGLES,
            *(b + s * r**p for b in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2) for s in (1, -1) for p in HUG_POWERS),
        )
    ]
    # A fine angular sweep at a few radii: a feature narrow in angle (a spike along a line) is only seen this way.
    sweep = [(r, theta) for r in SWEEP_RADII for theta in SWEEP_ANGLES]
    evaluated = total = 0
    for r, theta in (*grid, *sweep, *scattered):
        total += 1
        g_val = real(safe(g_num, r))
        e_val = real(safe(f_num, r, theta))
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
        raise Undecided("No s'ha pogut avaluar la funció en prou punts per comprovar la fita.")
    return "plausible", (
        f"$G(r)\\to0$ i la fita es compleix en els {evaluated} punts provats amb $0<r\\le{R_MAX}$ "
        "(comprovació numèrica, no una demostració)."
    )


_RAYS: tuple[tuple[int, int], ...] = (*DIRECTIONS, (-1, 0), (0, -1), (-1, -1), (-1, 1), (3, 1), (1, 3), (-3, 2))
_CURVE_FAMILY: tuple[tuple[int, int, int], ...] = tuple((p, c, s) for p in (2, 3) for c in (1, -1, 2) for s in (1, -1))


def _refuted_on_curves(ctx: Ctx, expr: sp.Expr) -> str | None:
    """Why expr does not tend to 0 at the origin, found on a ray or on a path given anywhere in the submission."""
    curves = [(f"raig $({u},{w})t$", sp.Integer(u) * T, sp.Integer(w) * T) for u, w in _RAYS]
    # Both branches of y = c x^p and x = c y^p: the curves tangent to an axis where a discontinuity hides from rays.
    for p, c, s in _CURVE_FAMILY:
        along, across = s * T, c * T**p
        curves.append((f"camí $({sp.latex(along)}, {sp.latex(across)})$", along, across))
        curves.append((f"camí $({sp.latex(across)}, {sp.latex(along)})$", across, along))
    for i, p in enumerate(ctx.context_paths, 1):
        try:
            px, py = parse_path(p, i)
        except BadCertificate:
            continue
        curves.append((f"camí $({sp.latex(px)}, {sp.latex(py)})$", px, py))
    for label, px, py in curves:
        lim = limit(at(expr, px, py), T, "+")
        if lim.exists is False:
            return f"Pel {label} no té límit quan $t\\to0^+$, i hauria de tendir a 0: la fita no pot ser certa."
        if lim.exists and lim.value is not None and compare(lim.value, sp.Integer(0)) is False:
            return f"Pel {label} tendeix a ${tex(lim.value)} \\ne 0$: la fita no pot ser certa."
    return None
