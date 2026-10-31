"""Decides one property of a proposed counterexample at the origin, with sympy. Runs inside a worker process.

Only one-variable limits are trusted: a partial or directional derivative is the limit of a difference quotient in h,
a path reduces f to a function of t, an iterated limit is two one-variable limits. sympy's own two-variable limits are
never used (a polar limit with the angle left free is not uniform in the angle). A radial bound G(r) is checked
exactly for G(r) -> 0 and on a grid of points for the inequality, so a property resting on one is "plausible".

`check_property` never raises: anything sympy cannot decide comes back "indeterminat" with the reason.
"""

import math
from collections.abc import Callable, Mapping

import sympy as sp

from core.counterexamples.domain.services.deciders.bounds import bound
from core.counterexamples.domain.services.deciders.context import (
    BadCertificate,
    BadFunction,
    Ctx,
    Undecided,
    parse_expression,
    real_roots,
)
from core.counterexamples.domain.services.deciders.definedness import check_defined
from core.counterexamples.domain.services.deciders.derivatives import (
    differentiable,
    directionals_exist,
    directionals_linear,
    mixed_partials,
    not_differentiable,
    partial_discontinuous,
    partials_exist,
    some_directional_missing,
    some_partial_missing,
)
from core.counterexamples.domain.services.deciders.limits import iterated, limit_refuted, lines_agree, lines_at_value
from core.counterexamples.domain.services.deciders.numeric import number
from core.counterexamples.domain.values.properties import PropertyKind
from core.counterexamples.domain.values.submission import PropertyCheck
from core.counterexamples.domain.values.verdict import PropertyVerdict, VerdictStatus

__all__ = ["check_property", "undecided"]

_DECIDERS: Mapping[PropertyKind, Callable[[Ctx], tuple[VerdictStatus, str]]] = {
    "rectes_mateix_limit": lines_agree,
    "rectes_limit_f0": lines_at_value,
    "iterats_iguals": iterated,
    "limit_no_existeix": lambda ctx: limit_refuted(ctx, against_value=False),
    "discontinua": lambda ctx: limit_refuted(ctx, against_value=True),
    "continua": lambda ctx: bound(ctx, ctx.g, ctx.c, "$|f(x,y)-f(0,0)|$"),
    "parcials_existeixen": partials_exist,
    "alguna_parcial_no_existeix": some_partial_missing,
    "direccionals_existeixen": directionals_exist,
    "direccionals_lineals": directionals_linear,
    "alguna_direccional_no_existeix": some_directional_missing,
    "diferenciable": differentiable,
    "no_diferenciable": not_differentiable,
    "parcial_discontinua": partial_discontinuous,
    "creuades_diferents": mixed_partials,
}


def check_property(check: PropertyCheck) -> PropertyVerdict:
    """Module-level and picklable: the unit of work sent to a sympy worker process."""
    ctx = Ctx(g=sp.Integer(0), c=sp.Integer(0), cert=check.certificate, lines=[], context_paths=check.context_paths)
    try:
        try:
            ctx.g = real_roots(parse_expression(check.function, {"x", "y"}, "La funció"))
            ctx.c = parse_expression(check.origin_value, set(), "El valor a l'origen")
        except BadCertificate as e:
            raise BadFunction(str(e)) from e
        if number(ctx.c) in (None, math.inf, -math.inf):
            raise BadFunction("$f(0,0)$ ha de ser un nombre real.")
        check_defined(ctx.g)
        status, detail = _DECIDERS[check.kind](ctx)
    except BadFunction as e:
        status, detail = "falla", str(e)
    except (BadCertificate, Undecided) as e:
        status, detail = "indeterminat", str(e)
    except Exception as e:  # a sympy bug must not take the request down
        status, detail = "indeterminat", f"error de sympy ({type(e).__name__})"
    return PropertyVerdict(kind=check.kind, status=status, detail=detail, computations=ctx.lines)


def undecided(check: PropertyCheck, reason: str) -> PropertyVerdict:
    return PropertyVerdict(kind=check.kind, status="indeterminat", detail=reason)
