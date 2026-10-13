"""The properties a counterexample can be asked to have, all at the origin, and the certificate each one needs.

The checker decides a negative property ("the limit does not exist") from a certificate the student gives (paths
with different limits), never from sympy alone: sympy's two-variable limits are unsound (a polar limit with the angle
left free gives 0 for x^2 y/(x^4+y^2), whose limit does not exist). A positive property ("continuous") needs a radial
bound G(r) -> 0; the inequality itself is only sampled, so it is "plausible", not proved. Properties computed from
one-variable limits (partial derivatives, iterated limits) need no certificate.
"""

from collections.abc import Mapping
from typing import Literal

from pydantic import BaseModel

PropertyKind = Literal[
    "rectes_mateix_limit",
    "iterats_iguals",
    "limit_no_existeix",
    "discontinua",
    "continua",
    "parcials_existeixen",
    "alguna_parcial_no_existeix",
    "direccionals_existeixen",
    "alguna_direccional_no_existeix",
    "diferenciable",
    "no_diferenciable",
    "parcial_discontinua",
    "creuades_diferents",
]

# What the student must add to the function: nothing, 1-2 paths, a radial bound, a direction, or a partial + a path.
# "camins_opcionals": the checker first tries to decide without one (e.g. a directional derivative that is not
# linear in the direction already rules out differentiability).
CertificateKind = Literal["cap", "camins", "camins_opcionals", "fita", "direccio", "parcial_cami"]


class PropertyInfo(BaseModel):
    kind: PropertyKind
    label: str  # LaTeX allowed, shown to the student
    certificate: CertificateKind
    help: str  # how to give the certificate; empty when there is none


PROPERTIES: Mapping[PropertyKind, PropertyInfo] = {
    p.kind: p
    for p in (
        PropertyInfo(
            kind="rectes_mateix_limit",
            label="El límit de $f$ per totes les rectes que passen per l'origen existeix i és el mateix",
            certificate="cap",
            help="",
        ),
        PropertyInfo(
            kind="iterats_iguals",
            label="Els dos límits iterats a l'origen existeixen i coincideixen",
            certificate="cap",
            help="",
        ),
        PropertyInfo(
            kind="limit_no_existeix",
            label="El límit de $f$ a l'origen no existeix",
            certificate="camins",
            help="Dona dos camins $(x(t),y(t))\\to(0,0)$ quan $t\\to0^+$ amb límits diferents, "
            "o un camí on el límit no existeixi.",
        ),
        PropertyInfo(
            kind="discontinua",
            label="$f$ no és contínua a l'origen",
            certificate="camins",
            help="Dona un camí $(x(t),y(t))\\to(0,0)$ on el límit de $f$ no sigui $f(0,0)$ (o no existeixi), "
            "o dos camins amb límits diferents.",
        ),
        PropertyInfo(
            kind="continua",
            label="$f$ és contínua a l'origen",
            certificate="fita",
            help="Dona una fita $G(r)$ amb $|f(r\\cos\\theta, r\\sin\\theta) - f(0,0)| \\le G(r)$ per a tot "
            "$\\theta$ i $0<r\\le 1/2$, i $G(r)\\to0$. $G$ només pot dependre de $r$ (p. ex. $r$, $2r^2$).",
        ),
        PropertyInfo(
            kind="parcials_existeixen",
            label="Les dues derivades parcials a l'origen existeixen",
            certificate="cap",
            help="",
        ),
        PropertyInfo(
            kind="alguna_parcial_no_existeix",
            label="Alguna derivada parcial a l'origen no existeix",
            certificate="cap",
            help="",
        ),
        PropertyInfo(
            kind="direccionals_existeixen",
            label="Totes les derivades direccionals a l'origen existeixen",
            certificate="cap",
            help="",
        ),
        PropertyInfo(
            kind="alguna_direccional_no_existeix",
            label="Alguna derivada direccional a l'origen no existeix",
            certificate="direccio",
            help="Dona una direcció $v=(u,w)$ on la derivada direccional no existeixi.",
        ),
        PropertyInfo(
            kind="diferenciable",
            label="$f$ és diferenciable a l'origen",
            certificate="fita",
            help="Amb $a=\\partial_x f(0,0)$ i $b=\\partial_y f(0,0)$, dona una fita $G(r)$ amb "
            "$\\dfrac{|f(x,y)-f(0,0)-ax-by|}{\\sqrt{x^2+y^2}} \\le G(r)$ per a $0<r\\le1/2$, i $G(r)\\to0$. "
            "$G$ només pot dependre de $r$.",
        ),
        PropertyInfo(
            kind="no_diferenciable",
            label="$f$ no és diferenciable a l'origen",
            certificate="camins_opcionals",
            help="Si cal, dona un camí on $f$ no tendeixi a $f(0,0)$ o on el residu "
            "$\\dfrac{f(x,y)-f(0,0)-ax-by}{\\sqrt{x^2+y^2}}$ no tendeixi a 0.",
        ),
        PropertyInfo(
            kind="parcial_discontinua",
            label="Alguna derivada parcial existeix a l'origen però no hi és contínua",
            certificate="parcial_cami",
            help="Tria la derivada parcial i dona un camí on no tendeixi al seu valor a l'origen.",
        ),
        PropertyInfo(
            kind="creuades_diferents",
            label="$\\dfrac{\\partial^2 f}{\\partial x\\partial y}(0,0) \\ne \\dfrac{\\partial^2 f}{\\partial y\\partial x}(0,0)$"
            " (les dues existeixen)",
            certificate="cap",
            help="",
        ),
    )
}
