"""What the student submits: f off the origin, f(0,0), and a certificate for each property that needs one.

Expressions are sympy syntax from untrusted input. They are parsed here with the shared whitelisted parser so that
a typo comes back at once as a 422 with the reason, before any worker process is involved.
"""

import math
import re
from collections.abc import Mapping
from typing import Literal

import sympy as sp
from pydantic import BaseModel, ConfigDict, Field

from core.counterexamples.domain.exceptions import InvalidSubmissionException
from core.counterexamples.domain.values.properties import PROPERTIES, PropertyKind
from core.shared.domain.contract import catalan_alias
from core.shared.math.sympy_checks import InvalidExpression, parse

MAX_PATHS = 2


class Path(BaseModel):
    """(x(t), y(t)) -> (0,0) as t -> 0+."""

    x: str
    y: str


class Direction(BaseModel):
    u: str
    w: str


class Certificate(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    paths: list[Path] = Field(
        default_factory=list, validation_alias=catalan_alias("camins", "paths"), serialization_alias="camins"
    )
    bound: str = Field(default="", validation_alias=catalan_alias("fita", "bound"), serialization_alias="fita")
    direction: Direction | None = Field(
        default=None, validation_alias=catalan_alias("direccio", "direction"), serialization_alias="direccio"
    )
    partial: Literal["x", "y"] | None = Field(
        default=None, validation_alias=catalan_alias("parcial", "partial"), serialization_alias="parcial"
    )


class Submission(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    function: str = Field(validation_alias=catalan_alias("funcio", "function"), serialization_alias="funcio")
    origin_value: str = Field(
        default="0", validation_alias=catalan_alias("valor", "origin_value"), serialization_alias="valor"
    )
    certificates: Mapping[PropertyKind, Certificate] = Field(
        default_factory=dict,
        validation_alias=catalan_alias("certificats", "certificates"),
        serialization_alias="certificats",
    )

    def certificate(self, kind: PropertyKind) -> Certificate:
        return self.certificates.get(kind) or Certificate()


class PropertyCheck(BaseModel):
    """One property to decide for one submission: the unit of work of a sympy worker."""

    kind: PropertyKind
    function: str
    origin_value: str
    certificate: Certificate
    # Every path given anywhere in the submission: a positive property (continuous, differentiable, the same limit
    # on every line) must also hold along them.
    context_paths: list[Path] = Field(default_factory=list)


# exp(exp(exp(1/r^2))) cannot be evaluated near the origin in any reasonable time.
MAX_EXP_DEPTH = 2
_GROWING = (sp.exp, sp.sinh, sp.cosh)


MAX_EXPONENT = 1000


def _has_huge_power(e: sp.Basic) -> bool:
    """A numeric exponent above MAX_EXPONENT, or a power tower of numbers: 10**10**9 is a billion-digit integer."""
    if isinstance(e, sp.Pow) and e.exp.is_number:
        if any(isinstance(a, sp.Integer) and abs(int(a)) > MAX_EXPONENT for a in e.exp.atoms(sp.Integer)):
            return True
        if any(isinstance(q, sp.Pow) and q.exp.is_number and q.exp.is_positive for q in e.exp.atoms(sp.Pow)):
            return True
    return any(_has_huge_power(a) for a in e.args)


# exp(-10**32*(x**2+y**2)) hides a discontinuity below every radius the checker samples: numeric constants are
# kept to a range where every feature of f is on the scale of the sampling.
MAX_CONSTANT = 10**6


def extreme_constant(e: sp.Basic) -> sp.Basic | None:
    """A numeric constant (a number, or a subexpression without variables) with absolute value above MAX_CONSTANT or
    below 1/MAX_CONSTANT (0 aside). Innermost first, so a huge constant is never evaluated inside a bigger one."""
    for a in e.args:
        if (found := extreme_constant(a)) is not None:
            return found
    if e.free_symbols or not isinstance(e, sp.Expr):
        return None
    if isinstance(e, sp.Rational):
        size = abs(e)
        return e if size > MAX_CONSTANT or (size != 0 and size * MAX_CONSTANT < 1) else None
    try:
        value = abs(complex(sp.N(e, 15)))
    except (TypeError, ValueError, OverflowError, ZeroDivisionError):
        return None
    if not math.isfinite(value):
        return None  # 1/0 and the like are refused with their own message
    return e if value > MAX_CONSTANT or 0 < value * MAX_CONSTANT < 1 else None


def _exp_depth(e: sp.Basic) -> int:
    inner = max((_exp_depth(a) for a in e.args), default=0)
    grows = isinstance(e, _GROWING) or (isinstance(e, sp.Pow) and not e.exp.is_number)
    return inner + 1 if grows else inner


# A function of x and y: sympy's own calculus would let the student run limits and derivatives in our workers.
FORBIDDEN_NAMES = frozenset({"diff", "limit"})


def _hint_common_mistakes(text: str, used: set[str], what: str, allowed: set[str]) -> None:
    """The usual ways of writing maths that sympy does not read, with the fix instead of a parser error."""
    if "|" in text:
        raise InvalidSubmissionException(f"{what}: per al valor absolut escriu Abs(...), no |...|")
    if m := re.search(r"(?<![A-Za-z_\d.])(\d+(?:\.\d+)?)\s*([A-Za-z(])", text):
        raise InvalidSubmissionException(
            f"{what}: la multiplicació ha de ser explícita: {m.group(1)}*{m.group(2)}, no {m.group(1)}{m.group(2)}"
        )
    for name in sorted(used):
        if len(name) > 1 and set(name) <= (allowed | {"x", "y"}):
            raise InvalidSubmissionException(f"{what}: «{name}» no és un nom; vols dir {'*'.join(name)}?")
    if "oo" in used or "zoo" in used:
        raise InvalidSubmissionException(f"{what}: ha de ser finit")


def _expression(text: str, what: str, allowed: set[str]) -> None:
    """Reads the expression without evaluating it: this runs on the event loop, outside any worker deadline."""
    used = set(re.findall(r"[A-Za-z_][A-Za-z_0-9]*", text or ""))
    _hint_common_mistakes(text or "", used, what, allowed)
    if used & FORBIDDEN_NAMES:
        raise InvalidSubmissionException(f"{what}: no es pot fer servir {', '.join(sorted(used & FORBIDDEN_NAMES))}")
    try:
        expr = parse(text, evaluate=False)
    except InvalidExpression as e:
        raise InvalidSubmissionException(f"{what}: {e}") from e
    if _has_huge_power(expr):
        raise InvalidSubmissionException(f"{what}: hi ha una potència massa gran (exponent com a molt {MAX_EXPONENT})")
    if _exp_depth(expr) > MAX_EXP_DEPTH:
        raise InvalidSubmissionException(f"{what}: massa exponencials niades (com a molt {MAX_EXP_DEPTH})")
    if (constant := extreme_constant(expr)) is not None:
        raise InvalidSubmissionException(
            f"{what}: la constant {constant} és massa gran o massa petita (com a molt {MAX_CONSTANT:g} en valor "
            f"absolut, i no per sota de {1 / MAX_CONSTANT:g})"
        )
    extra = sorted(str(s) for s in expr.free_symbols if str(s) not in allowed)
    if extra:
        names = ", ".join(sorted(allowed)) or "cap variable"
        raise InvalidSubmissionException(f"{what}: no pot dependre de {', '.join(extra)} (només de {names})")


def validate_submission(submission: Submission, properties: list[PropertyKind]) -> None:
    """Raises `InvalidSubmissionException` on the first expression that cannot be read or uses a wrong variable."""
    _expression(submission.function, "La funció", {"x", "y"})
    _expression(submission.origin_value, "El valor a l'origen", set())
    for kind in properties:
        cert = submission.certificate(kind)
        info = PROPERTIES[kind]
        if len(cert.paths) > MAX_PATHS:
            raise InvalidSubmissionException(f"Com a molt {MAX_PATHS} camins per propietat")
        for i, path in enumerate(cert.paths, 1):
            _expression(path.x, f"Camí {i}, x(t)", {"t"})
            _expression(path.y, f"Camí {i}, y(t)", {"t"})
        if cert.bound.strip():
            _expression(cert.bound, "La fita", {"r"})
        if cert.direction is not None:
            _expression(cert.direction.u, "La direcció (primera component)", set())
            _expression(cert.direction.w, "La direcció (segona component)", set())
        if info.certificate == "parcial_cami" and cert.partial is None and cert.paths:
            raise InvalidSubmissionException("Tria quina derivada parcial no és contínua")
