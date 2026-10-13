"""What the student submits: f off the origin, f(0,0), and a certificate for each property that needs one.

Expressions are sympy syntax from untrusted input. They are parsed here with the shared whitelisted parser so that
a typo comes back at once as a 422 with the reason, before any worker process is involved.
"""

import re
from collections.abc import Mapping
from typing import Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from core.counterexamples.domain.exceptions import InvalidSubmissionException
from core.counterexamples.domain.properties import PROPERTIES, PropertyKind
from core.shared.math.sympy_checks import InvalidExpression, parse

MAX_PATHS = 2


def _ca(catalan: str, english: str) -> AliasChoices:
    return AliasChoices(catalan, english)


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
        default_factory=list, validation_alias=_ca("camins", "paths"), serialization_alias="camins"
    )
    bound: str = Field(default="", validation_alias=_ca("fita", "bound"), serialization_alias="fita")
    direction: Direction | None = Field(
        default=None, validation_alias=_ca("direccio", "direction"), serialization_alias="direccio"
    )
    partial: Literal["x", "y"] | None = Field(
        default=None, validation_alias=_ca("parcial", "partial"), serialization_alias="parcial"
    )


class Submission(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    function: str = Field(validation_alias=_ca("funcio", "function"), serialization_alias="funcio")
    origin_value: str = Field(default="0", validation_alias=_ca("valor", "origin_value"), serialization_alias="valor")
    certificates: Mapping[PropertyKind, Certificate] = Field(
        default_factory=dict, validation_alias=_ca("certificats", "certificates"), serialization_alias="certificats"
    )

    def certificate(self, kind: PropertyKind) -> Certificate:
        return self.certificates.get(kind) or Certificate()


class PropertyCheck(BaseModel):
    """One property to decide for one submission: the unit of work of a sympy worker."""

    kind: PropertyKind
    function: str
    origin_value: str
    certificate: Certificate


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
