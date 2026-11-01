"""The limit properties: along paths, along every line through the origin, the iterated limits."""

import sympy as sp

from core.counterexamples.domain.services.deciders.context import Ctx, H, M, Undecided, X, Y, at, describe, tex
from core.counterexamples.domain.services.deciders.directions import path_slopes, special_slopes
from core.counterexamples.domain.services.deciders.one_variable import Limit, compare, limit
from core.counterexamples.domain.services.deciders.sampling import SLOPES
from core.counterexamples.domain.values.properties import PROPERTIES
from core.counterexamples.domain.values.verdict import VerdictStatus


def _missing_paths(ctx: Ctx) -> None:
    if not ctx.cert.paths:
        raise Undecided("Falta el certificat: " + PROPERTIES["limit_no_existeix"].help)


def limit_refuted(ctx: Ctx, against_value: bool) -> tuple[VerdictStatus, str]:
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
        if against_value and compare(lim.value, ctx.c) is False:
            return "ok", f"Pel camí {i} el límit és ${tex(lim.value)} \\ne f(0,0) = {tex(ctx.c)}$."
        found.append((i, lim.value))
    if len(found) == 2 and compare(found[0][1], found[1][1]) is False:
        return "ok", f"Els dos camins donen límits diferents: ${tex(found[0][1])}$ i ${tex(found[1][1])}$."
    if unknown:
        raise Undecided("sympy no ha pogut calcular el límit per algun camí.")
    if against_value:
        return (
            "indeterminat",
            "Pels camins donats el límit és $f(0,0)$: no proven la discontinuïtat. Busca un camí on no ho sigui.",
        )
    if len(found) == 1:
        return "indeterminat", (
            f"Pel camí donat el límit existeix (${tex(found[0][1])}$). Un sol camí només prova que el límit no "
            "existeix si per ell no té límit: afegeix un segon camí amb un límit diferent."
        )
    return "indeterminat", "Els dos camins tenen el mateix límit: no proven que el límit no existeixi."


def lines_at_value(ctx: Ctx) -> tuple[VerdictStatus, str]:
    status, detail = lines_agree(ctx)
    if status not in ("ok", "plausible"):
        return status, detail
    common = limit(at(ctx.g, 0, H), H)
    if common.value is not None and compare(common.value, ctx.c) is False:
        return "falla", f"El límit per les rectes és ${tex(common.value)}$, però $f(0,0) = {tex(ctx.c)}$."
    return status, detail


def lines_agree(ctx: Ctx) -> tuple[VerdictStatus, str]:
    vertical = limit(at(ctx.g, 0, H), H)
    ctx.log(f"\\text{{Recta }} x=0: {describe(vertical)}")
    values: list[tuple[str, sp.Expr]] = []
    for label, lim in [("x=0", vertical)] + [(_line_label(m), limit(at(ctx.g, H, m * H), H)) for m in SLOPES]:
        if lim.exists is False:
            return "falla", f"Per la recta ${label}$ el límit no existeix."
        if lim.exists is None or lim.value is None:
            raise Undecided(f"sympy no ha pogut calcular el límit per la recta ${label}$.")
        values.append((label, lim.value))
    for label, value in values[1:]:
        if compare(value, values[0][1]) is False:
            return "falla", (
                f"Per ${values[0][0]}$ el límit és ${tex(values[0][1])}$ i per ${label}$ és ${tex(value)}$."
            )
    special, complete = special_slopes(at(ctx.g, H, M * H))
    for m in dict.fromkeys([*special, *path_slopes(ctx)]):
        lim = limit(at(ctx.g, H, m * H), H)
        label = f"y={sp.latex(m)}\\,x"
        if lim.exists is False:
            return "falla", f"Per la recta ${label}$ el límit no existeix."
        if lim.exists is None or lim.value is None:
            raise Undecided(f"sympy no ha pogut calcular el límit per la recta ${label}$.")
        if compare(lim.value, values[0][1]) is False:
            return (
                "falla",
                f"Per ${values[0][0]}$ el límit és ${tex(values[0][1])}$ i per ${label}$ és ${tex(lim.value)}$.",
            )
    generic = limit(at(ctx.g, H, M * H), H)
    shown = Limit(generic.exists, generic.value.subs(M, sp.Symbol("m"))) if generic.value is not None else generic
    ctx.log(f"\\text{{Recta }} y=mx: {describe(shown)}")
    if generic.exists is True and generic.value is not None:
        same = compare(generic.value, values[0][1])
        if same is False:
            return "falla", f"Per la recta $y=mx$ el límit és ${tex(generic.value)}$: depèn de $m$."
        # "ok" only when every slope where sympy's generic answer could change has been tried.
        if same is True and complete:
            return "ok", f"Per totes les rectes el límit és ${tex(values[0][1])}$."
    if not complete:
        raise Undecided(_INCOMPLETE_LINES.format(value=tex(values[0][1])))
    return "plausible", (
        f"Per les rectes provades el límit és ${tex(values[0][1])}$; sympy no ha pogut fer el càlcul per a $m$ qualsevol."
    )


def iterated(ctx: Ctx) -> tuple[VerdictStatus, str]:
    results: list[Limit] = []
    for inner_var, outer_var, label in ((Y, X, "\\lim_{x\\to0}\\lim_{y\\to0}"), (X, Y, "\\lim_{y\\to0}\\lim_{x\\to0}")):
        inner = limit(ctx.g, inner_var)  # the other variable is a generic (nonzero) parameter
        outer = limit(inner.value, outer_var) if inner.exists is True and inner.value is not None else inner
        ctx.log(f"{label} f = {describe(outer)}")
        results.append(outer)
    if any(r.exists is False for r in results):
        return "falla", "Algun dels límits iterats no existeix."
    if any(r.exists is None or r.value is None for r in results):
        raise Undecided("sympy no ha pogut calcular els límits iterats.")
    a, b = results[0].value, results[1].value
    assert a is not None and b is not None
    same = compare(a, b)
    if same is None:
        raise Undecided("sympy no pot comparar els dos límits iterats.")
    return (
        ("ok", f"Els dos límits iterats valen ${tex(a)}$.")
        if same
        else (
            "falla",
            f"Els límits iterats són diferents: ${tex(a)}$ i ${tex(b)}$.",
        )
    )


_INCOMPLETE_LINES = (
    "Per les rectes provades el límit és ${value}$, però $f$ sobre $y=mx$ no és d'un tipus on sympy pugui trobar "
    "totes les pendents especials, i no es pot garantir per a tota $m$. Si hi ha una recta sospitosa, dona-la com a "
    "camí en un altre certificat."
)


def _line_label(m: sp.Expr) -> str:
    named: dict[sp.Expr, str] = {sp.Integer(0): "y=0", sp.Integer(1): "y=x", sp.Integer(-1): "y=-x"}
    return named.get(m, f"y={sp.latex(m)}\\,x")
