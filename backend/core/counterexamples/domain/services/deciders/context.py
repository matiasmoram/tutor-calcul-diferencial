"""What every decider works on: the parsed f and f(0,0), the certificate, the computations shown to the student,
and the outcomes that end a decision early."""

from collections.abc import Iterator
from dataclasses import dataclass, field

import sympy as sp

from core.counterexamples.domain.services.deciders.numeric import number
from core.counterexamples.domain.services.deciders.one_variable import Limit, compare, limit
from core.counterexamples.domain.values.submission import MAX_CONSTANT, Certificate, Path, extreme_constant
from core.shared.math.sympy_checks import SYMBOLS, InvalidExpression, parse

X, Y, T, R = SYMBOLS["x"], SYMBOLS["y"], SYMBOLS["t"], SYMBOLS["r"]
H = sp.Dummy("h", real=True)
K = sp.Dummy("k", real=True, nonzero=True)
HK = sp.Dummy("h", real=True, nonzero=True)
A, B = sp.Dummy("a", real=True), sp.Dummy("b", real=True)
M = sp.Dummy("m", real=True)
THETA = sp.Dummy("theta", real=True)


class Undecided(Exception):
    pass


class BadCertificate(Exception):
    """The certificate is unusable or proves nothing: the property is not decided ("indeterminat")."""


class BadFunction(Exception):
    """f itself is not a valid answer (undefined off the origin, f(0,0) not a real number): "falla"."""


def at(g: sp.Expr, px: sp.Expr | int, py: sp.Expr | int) -> sp.Expr:
    out = g.subs({X: px, Y: py}, simultaneous=True)
    assert isinstance(out, sp.Expr)
    return out


def tex(e: sp.Expr | None) -> str:
    return "?" if e is None else sp.latex(e)


def describe(lim: Limit) -> str:
    if lim.exists is True:
        return tex(lim.value)
    return "\\text{no existeix}" if lim.exists is False else "\\text{?}"


@dataclass
class Ctx:
    g: sp.Expr
    c: sp.Expr
    cert: Certificate
    lines: list[str]
    context_paths: list[Path] = field(default_factory=list)  # every path of the submission, for cross-checks

    def log(self, line: str) -> None:
        self.lines.append(line)

    def partial(self, var: str) -> Limit:
        quotient = (at(self.g, H, 0) - self.c) / H if var == "x" else (at(self.g, 0, H) - self.c) / H
        lim = limit(quotient, H)
        self.log(f"\\partial_{var} f(0,0) = {describe(lim)}")
        return lim

    def directional(self, u: sp.Expr, w: sp.Expr) -> Limit:
        return limit((at(self.g, H * u, H * w) - self.c) / H, H)

    def paths(self) -> Iterator[tuple[int, sp.Expr, sp.Expr]]:
        for i, p in enumerate(self.cert.paths, 1):
            px, py = parse_path(p, i)
            yield i, px, py

    def along(self, expr: sp.Expr, px: sp.Expr, py: sp.Expr, i: int, what: str = "f") -> Limit:
        on_path = at(expr, px, py)
        # A path through a hole of f (a zero of a denominator, a log of a negative) proves nothing about the limit.
        for k in (2, 3, 4, 5, 7):
            value = on_path.subs(T, sp.Rational(1, 10**k))
            if value.has(sp.zoo, sp.nan, sp.oo, -sp.oo) or number(value) is None:
                raise BadCertificate(f"${what}$ no està definida sobre el camí {i} (per exemple a $t=10^{{-{k}}}$).")
        lim = limit(on_path, T, "+")
        self.log(f"\\text{{Camí {i}: }}\\lim_{{t\\to0^+}} {what}({sp.latex(px)}, {sp.latex(py)}) = {describe(lim)}")
        return lim


def parse_expression(text: str, allowed: set[str], what: str) -> sp.Expr:
    try:
        expr = parse(text)
    except InvalidExpression as e:
        raise BadCertificate(f"{what}: {e}") from e
    if any(str(s) not in allowed for s in expr.free_symbols):
        raise BadCertificate(f"{what}: variable no permesa")
    if (constant := extreme_constant(expr)) is not None:
        raise BadCertificate(
            f"{what}: la constant ${sp.latex(constant)}$ és massa gran o massa petita "
            f"(com a molt {MAX_CONSTANT:g} en valor absolut, i no per sota de {1 / MAX_CONSTANT:g})."
        )
    return expr


def real_roots(expr: sp.Expr) -> sp.Expr:
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


def parse_path(p: Path, i: int) -> tuple[sp.Expr, sp.Expr]:
    px, py = parse_expression(p.x, {"t"}, f"Camí {i}"), parse_expression(p.y, {"t"}, f"Camí {i}")
    for comp in (px, py):
        lim = limit(comp, T, "+")
        if lim.exists is not True or lim.value is None or compare(lim.value, sp.Integer(0)) is not True:
            raise BadCertificate(f"El camí {i} no tendeix a l'origen quan $t\\to0^+$")
    try:
        off_origin = any(float(sp.N((px**2 + py**2).subs(T, s))) > 0 for s in (1e-2, 3e-3, 1e-3))
    except (TypeError, ValueError):
        off_origin = True
    if not off_origin:
        raise BadCertificate(f"El camí {i} es queda a l'origen: ha de ser un camí diferent de $(0,0)$")
    return px, py
