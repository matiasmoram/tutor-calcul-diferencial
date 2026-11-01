"""The derivative properties: partial and directional derivatives, differentiability, continuity of a partial,
the mixed partials."""

import math

import sympy as sp

from core.counterexamples.domain.services.deciders.bounds import bound
from core.counterexamples.domain.services.deciders.context import (
    HK,
    A,
    B,
    BadCertificate,
    Ctx,
    H,
    K,
    Undecided,
    X,
    Y,
    at,
    describe,
    parse_expression,
    tex,
)
from core.counterexamples.domain.services.deciders.directions import directions_to_try
from core.counterexamples.domain.services.deciders.numeric import number
from core.counterexamples.domain.services.deciders.one_variable import compare, limit
from core.counterexamples.domain.services.deciders.sampling import DIRECTIONS
from core.counterexamples.domain.values.properties import PROPERTIES
from core.counterexamples.domain.values.verdict import VerdictStatus


def partials_exist(ctx: Ctx) -> tuple[VerdictStatus, str]:
    px, py = ctx.partial("x"), ctx.partial("y")
    for var, lim in (("x", px), ("y", py)):
        if lim.exists is False:
            return "falla", f"$\\partial_{var} f(0,0)$ no existeix."
    if px.exists is None or py.exists is None:
        raise Undecided("sympy no ha pogut calcular alguna derivada parcial.")
    return "ok", "Les dues derivades parcials existeixen."


def some_partial_missing(ctx: Ctx) -> tuple[VerdictStatus, str]:
    px, py = ctx.partial("x"), ctx.partial("y")
    for var, lim in (("x", px), ("y", py)):
        if lim.exists is False:
            return "ok", f"$\\partial_{var} f(0,0)$ no existeix."
    if px.exists is None or py.exists is None:
        raise Undecided("sympy no ha pogut calcular alguna derivada parcial.")
    return "falla", "Les dues derivades parcials existeixen."


def directionals_exist(ctx: Ctx) -> tuple[VerdictStatus, str]:
    directions, complete = directions_to_try(ctx)
    for u, w in directions:
        lim = ctx.directional(u, w)
        if lim.exists is False:
            ctx.log(f"D_{{({sp.latex(u)},{sp.latex(w)})}} f(0,0) = {describe(lim)}")
            return "falla", f"La derivada direccional en la direcció $({sp.latex(u)},{sp.latex(w)})$ no existeix."
        if lim.exists is None:
            raise Undecided(f"sympy no ha pogut calcular la derivada en la direcció $({sp.latex(u)},{sp.latex(w)})$.")
    for u, w in DIRECTIONS:
        ctx.log(f"D_{{({u},{w})}} f(0,0) = {describe(ctx.directional(sp.Integer(u), sp.Integer(w)))}")
    # The fixed directions decide a failure; a symbolic (a, b) is only evidence, and sympy can fail on it where
    # every concrete direction works (sign(x^3+y^3)*Abs(x^3+y^3)^(1/3)).
    if not complete:
        raise Undecided(_INCOMPLETE_DIRECTIONS.format(n=len(directions)))
    generic = ctx.directional(A, B)
    if generic.exists is True:
        assert generic.value is not None
        shown = generic.value.subs({A: sp.Symbol("a"), B: sp.Symbol("b")})
        ctx.log(f"D_{{(a,b)}} f(0,0) = {sp.latex(shown)}")
        return "plausible", (
            "Existeix en una direcció genèrica $(a,b)$ i en totes les direccions provades "
            "(sympy suposa $(a,b)$ genèric: les direccions especials s'han provat a part)."
        )
    return "plausible", (
        f"Existeix en les {len(directions)} direccions provades (una cada 7,5°, les especials i les dels teus camins); "
        "sympy no ha pogut fer el càlcul en una direcció qualsevol $(a,b)$."
    )


def directionals_linear(ctx: Ctx) -> tuple[VerdictStatus, str]:
    """D_v f(0,0) = grad f(0,0) . v for every v: on every direction tried, then for a symbolic (a, b)."""
    px, py = ctx.partial("x"), ctx.partial("y")
    for var, lim in (("x", px), ("y", py)):
        if lim.exists is False:
            return "falla", f"$\\partial_{var} f(0,0)$ no existeix."
    if px.value is None or py.value is None:
        raise Undecided("sympy no ha pogut calcular alguna derivada parcial.")
    a, b = px.value, py.value
    directions, complete = directions_to_try(ctx)
    for u, w in directions:
        lim = ctx.directional(u, w)
        v = f"({sp.latex(u)},{sp.latex(w)})"
        if lim.exists is False:
            return "falla", f"La derivada direccional en la direcció ${v}$ no existeix."
        if lim.exists is None or lim.value is None:
            raise Undecided(f"sympy no ha pogut calcular la derivada en la direcció ${v}$.")
        linear = sp.simplify(u * a + w * b)
        if compare(lim.value, linear) is False:
            ctx.log(f"D_{{{v}}} f(0,0) = {tex(lim.value)} \\ne \\nabla f(0,0)\\cdot v = {tex(linear)}")
            return "falla", (
                f"$D_v f(0,0) = {tex(lim.value)}$ però $\\nabla f(0,0)\\cdot v = {tex(linear)}$ per a $v={v}$: "
                "la derivada direccional no és lineal en $v$."
            )
    ctx.log(f"\\nabla f(0,0) = ({tex(a)}, {tex(b)})")
    if not complete:
        raise Undecided(_INCOMPLETE_DIRECTIONS.format(n=len(directions)))
    generic = ctx.directional(A, B)
    if generic.exists is True and generic.value is not None:
        shown = generic.value.subs({A: sp.Symbol("a"), B: sp.Symbol("b")})
        ctx.log(f"D_{{(a,b)}} f(0,0) = {sp.latex(shown)}")
        if compare(generic.value, A * a + B * b) is False:
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


_INCOMPLETE_DIRECTIONS = (
    "Existeix en les {n} direccions provades, però $f$ sobre $y=mx$ no és d'un tipus on sympy pugui trobar totes les "
    "direccions especials, i no es pot garantir per a tota direcció. Si n'hi ha una de sospitosa, dona-la com a camí "
    "en un altre certificat."
)


def some_directional_missing(ctx: Ctx) -> tuple[VerdictStatus, str]:
    d = ctx.cert.direction
    if d is None:
        raise Undecided("Falta el certificat: " + PROPERTIES["alguna_direccional_no_existeix"].help)
    u, w = parse_expression(d.u, set(), "La direcció"), parse_expression(d.w, set(), "La direcció")
    if any(number(c) in (None, math.inf, -math.inf) for c in (u, w)):
        raise BadCertificate("La direcció ha de ser un vector de nombres reals.")
    if compare(u, sp.Integer(0)) and compare(w, sp.Integer(0)):
        raise BadCertificate("La direcció no pot ser el vector zero.")
    lim = ctx.directional(u, w)
    ctx.log(f"D_{{({sp.latex(u)},{sp.latex(w)})}} f(0,0) = {describe(lim)}")
    if lim.exists is False:
        return "ok", f"En la direcció $({tex(u)},{tex(w)})$ la derivada direccional no existeix."
    if lim.exists is None:
        raise Undecided("sympy no ha pogut calcular la derivada direccional.")
    return "indeterminat", (
        f"En la direcció donada la derivada direccional existeix i val ${tex(lim.value)}$: prova una altra direcció."
    )


def _remainder(ctx: Ctx, a: sp.Expr, b: sp.Expr) -> sp.Expr:
    return (ctx.g - ctx.c - a * X - b * Y) / sp.sqrt(X**2 + Y**2)


def _not_differentiable_automatic(ctx: Ctx) -> tuple[str | None, tuple[sp.Expr, sp.Expr] | None]:
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
            ctx.log(f"D_{{({u},{w})}} f(0,0) = {describe(lim)}")
            return f"La derivada direccional en la direcció $({u},{w})$ no existeix.", (a, b)
        if lim.exists is True and lim.value is not None:
            linear = sp.simplify(u * a + w * b)
            if compare(lim.value, linear) is False:
                ctx.log(f"D_{{({u},{w})}} f(0,0) = {tex(lim.value)} \\ne \\nabla f(0,0)\\cdot v = {tex(linear)}")
                return (
                    f"$D_v f(0,0) = {tex(lim.value)}$ però $\\nabla f(0,0)\\cdot v = {tex(linear)}$ "
                    f"per a $v=({u},{w})$: la derivada direccional no és lineal en $v$."
                ), (a, b)
    return None, (a, b)


def differentiable(ctx: Ctx) -> tuple[VerdictStatus, str]:
    reason, gradient = _not_differentiable_automatic(ctx)
    if reason is not None:
        return "falla", reason
    if gradient is None:
        raise Undecided("sympy no ha pogut calcular les derivades parcials.")
    return bound(ctx, _remainder(ctx, *gradient), sp.Integer(0), "el residu de la diferencial")


def not_differentiable(ctx: Ctx) -> tuple[VerdictStatus, str]:
    reason, gradient = _not_differentiable_automatic(ctx)
    if reason is not None:
        return "ok", reason
    if not ctx.cert.paths:
        raise Undecided("No s'ha pogut decidir sense certificat. " + PROPERTIES["no_diferenciable"].help)
    unknown = False
    for i, px, py in ctx.paths():
        lim = ctx.along(ctx.g, px, py, i)
        if lim.exists is False or (lim.exists and lim.value is not None and compare(lim.value, ctx.c) is False):
            return "ok", f"$f$ no és contínua a l'origen (camí {i}), i per tant no és diferenciable."
        if gradient is not None:
            rest = ctx.along(_remainder(ctx, *gradient), px, py, i, what="\\text{residu}")
            if rest.exists is False:
                return "ok", f"Pel camí {i} el residu de la diferencial no té límit."
            if rest.exists and rest.value is not None and compare(rest.value, sp.Integer(0)) is False:
                return "ok", f"Pel camí {i} el residu de la diferencial tendeix a ${tex(rest.value)} \\ne 0$."
            unknown = unknown or rest.exists is None
        unknown = unknown or lim.exists is None
    if unknown:
        raise Undecided("sympy no ha pogut calcular algun límit pels camins donats.")
    return "indeterminat", (
        "Pels camins donats $f\\to f(0,0)$ i el residu tendeix a 0: no proven la no-diferenciabilitat."
    )


def partial_discontinuous(ctx: Ctx) -> tuple[VerdictStatus, str]:
    var = ctx.cert.partial
    if var is None or not ctx.cert.paths:
        raise Undecided("Falta el certificat: " + PROPERTIES["parcial_discontinua"].help)
    at_origin = ctx.partial(var)
    if at_origin.exists is False:
        return "falla", f"$\\partial_{var} f(0,0)$ no existeix (la propietat demana que existeixi)."
    if at_origin.value is None:
        raise Undecided(f"sympy no ha pogut calcular $\\partial_{var} f(0,0)$.")
    derivative = sp.diff(ctx.g, X if var == "x" else Y)
    ctx.log(f"\\partial_{var} f(x,y) = {sp.latex(sp.simplify(derivative))} \\quad ((x,y)\\ne(0,0))")
    unknown = False
    for i, px, py in ctx.paths():
        lim = ctx.along(derivative, px, py, i, what=f"\\partial_{var} f")
        if lim.exists is False:
            return "ok", f"Pel camí {i}, $\\partial_{var} f$ no té límit a l'origen."
        if lim.value is not None and compare(lim.value, at_origin.value) is False:
            return "ok", (
                f"Pel camí {i}, $\\partial_{var} f \\to {tex(lim.value)} \\ne \\partial_{var} f(0,0) = "
                f"{tex(at_origin.value)}$."
            )
        unknown = unknown or lim.exists is None
    if unknown:
        raise Undecided("sympy no ha pogut calcular el límit pel camí.")
    return (
        "indeterminat",
        f"Pels camins donats $\\partial_{var} f$ tendeix a $\\partial_{var} f(0,0)$: prova un altre camí.",
    )


def mixed_partials(ctx: Ctx) -> tuple[VerdictStatus, str]:
    px, py = ctx.partial("x"), ctx.partial("y")
    if px.exists is False or py.exists is False:
        return "falla", "Calen les dues derivades parcials a l'origen."
    if px.value is None or py.value is None:
        raise Undecided("sympy no ha pogut calcular alguna derivada parcial.")
    # d/dy (df/dx) at the origin: df/dx on the axis x = 0 (k != 0), then a quotient in k. Symmetrically the other.
    fx_axis = limit((at(ctx.g, H, K) - at(ctx.g, 0, K)) / H, H)
    fy_axis = limit((at(ctx.g, HK, H) - at(ctx.g, HK, 0)) / H, H)
    if fx_axis.value is None or fy_axis.value is None:
        raise Undecided("sympy no ha pogut calcular les derivades parcials sobre els eixos.")
    fyx = limit((fx_axis.value - px.value) / K, K)
    fxy = limit((fy_axis.value - py.value) / HK, HK)
    # D_yD_x f = d/dy (df/dx): the order written out, since the notes' d2f/dxdy convention is easy to misread.
    ctx.log(f"D_yD_xf(0,0) = {describe(fyx)}")
    ctx.log(f"D_xD_yf(0,0) = {describe(fxy)}")
    if fyx.exists is False or fxy.exists is False:
        return "falla", "Alguna de les derivades creuades no existeix a l'origen."
    if fyx.value is None or fxy.value is None:
        raise Undecided("sympy no ha pogut calcular les derivades creuades.")
    same = compare(fyx.value, fxy.value)
    if same is None:
        raise Undecided("sympy no pot comparar les derivades creuades.")
    if same:
        return "falla", f"Les dues derivades creuades valen ${tex(fyx.value)}$."
    return "ok", f"$D_yD_xf(0,0) = {tex(fyx.value)}$ i $D_xD_yf(0,0) = {tex(fxy.value)}$."
