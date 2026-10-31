import pytest

from core.counterexamples.domain.services.deciders import check_property
from core.counterexamples.domain.values.properties import PROPERTIES, PropertyKind
from core.counterexamples.domain.values.submission import Certificate, PropertyCheck, validate_submission
from core.counterexamples.domain.values.verdict import VerdictStatus
from tests.fixtures.counterexamples import authored_challenges

CATALOG = authored_challenges()


def verdict(kind: PropertyKind, function: str, value: str = "0", **certificate: object) -> tuple[VerdictStatus, str]:
    v = check_property(
        PropertyCheck(
            kind=kind, function=function, origin_value=value, certificate=Certificate.model_validate(certificate)
        )
    )
    return v.status, v.detail


@pytest.mark.parametrize("spec_id", sorted(CATALOG.specs))
def test_every_authored_example_passes_its_challenge(spec_id: str) -> None:
    spec = CATALOG.specs[spec_id]
    validate_submission(spec.example, spec.properties)
    for kind in spec.properties:
        cert = spec.example.certificate(kind).model_dump(by_alias=True)
        status, detail = verdict(kind, spec.example.function, spec.example.origin_value, **cert)
        assert status in ("ok", "plausible"), f"{spec_id} / {kind}: {detail}"


def test_the_catalog_uses_every_property() -> None:
    assert {k for s in CATALOG.specs.values() for k in s.properties} == set(PROPERTIES)


TWO_LINES = {"camins": [{"x": "t", "y": "t"}, {"x": "t", "y": "2*t"}]}
DIAGONAL = {"camins": [{"x": "t", "y": "t"}]}


# Wrong submissions never pass. "falla": the property is shown false; "indeterminat": the certificate is missing
# or proves nothing (the property may still be true, as for x**2+y**2 and a path that stays at its limit).
@pytest.mark.parametrize(
    ("kind", "function", "value", "certificate", "expected"),
    [
        # Along the parabola y = x^2 the limit is 1/2: an exact one-variable limit on the curve shows f is not
        # continuous, whatever the bound.
        ("continua", "x**2*y/(x**4+y**2)", "0", {"fita": "r"}, "falla"),
        ("continua", "x**2*y/(x**4+y**2)", "0", {"fita": "2*r**(1/10)"}, "falla"),
        # Off every ray and curve family checked exactly (y = 5x^2): the sampled bound still catches it.
        ("continua", "x*y/sqrt(x**2+y**2)+x**8*y/(x**10+(y-5*x**2)**2)", "0", {"fita": "r"}, "indeterminat"),
        ("continua", "x**2+y**2", "0", {"fita": "1"}, "indeterminat"),
        ("continua", "x**2+y**2", "0", {}, "indeterminat"),
        ("limit_no_existeix", "x**2*y/(x**4+y**2)", "0", TWO_LINES, "indeterminat"),
        ("limit_no_existeix", "x**2+y**2", "0", {"camins": [{"x": "t", "y": "1"}]}, "indeterminat"),
        ("limit_no_existeix", "x**2+y**2", "0", {"camins": [{"x": "0", "y": "0"}]}, "indeterminat"),
        ("limit_no_existeix", "x**2+y**2", "0", {}, "indeterminat"),
        ("discontinua", "x**2+y**2", "0", {"camins": [{"x": "t", "y": "0"}]}, "indeterminat"),
        ("diferenciable", "x*y/sqrt(x**2+y**2)", "0", {"fita": "r"}, "falla"),
        ("diferenciable", "x**2*y/(x**2+y**2)", "0", {"fita": "r"}, "falla"),
        ("creuades_diferents", "x*y", "0", {}, "falla"),
        ("rectes_mateix_limit", "x*y/(x**2+y**2)", "0", {}, "falla"),
        ("iterats_iguals", "(x-y)/(x+y)", "0", {}, "falla"),
        ("no_diferenciable", "x**2+y**2", "0", {}, "indeterminat"),
        ("no_diferenciable", "x**2+y**2", "0", DIAGONAL, "indeterminat"),
        ("no_diferenciable", "Abs(x*y)**(3/4)", "0", DIAGONAL, "indeterminat"),
        ("parcial_discontinua", "x**2+y**2", "0", {"parcial": "x", **DIAGONAL}, "indeterminat"),
        ("direccionals_existeixen", "Abs(x)", "0", {}, "falla"),
        ("alguna_direccional_no_existeix", "x**2", "0", {"direccio": {"u": "0", "w": "0"}}, "indeterminat"),
        ("alguna_parcial_no_existeix", "x**2+y**2", "0", {}, "falla"),
        ("parcials_existeixen", "Abs(x)", "0", {}, "falla"),
        # A slope sympy's generic-m limit hides: along y = 7x the limit is 0, along every other line 1.
        ("rectes_mateix_limit", "(y-7*x)**2/((y-7*x)**2+x**4)", "0", {}, "falla"),
        # f must be defined off the origin: a path through a hole, or a hole on an axis, proves nothing.
        ("limit_no_existeix", "x*y/(x-y)", "0", DIAGONAL, "falla"),
        ("alguna_parcial_no_existeix", "1/x", "0", {}, "falla"),
        ("limit_no_existeix", "x*y/(y-x**2)", "0", {"camins": [{"x": "t", "y": "t**2"}]}, "falla"),
    ],
)
def test_wrong_submissions_never_pass(
    kind: PropertyKind, function: str, value: str, certificate: dict[str, object], expected: VerdictStatus
) -> None:
    assert verdict(kind, function, value, **certificate)[0] == expected


def test_decisions_that_need_no_certificate() -> None:
    # A directional derivative that is not linear in the direction rules out differentiability on its own.
    status, detail = verdict("no_diferenciable", "x**2*y/(x**2+y**2)")
    assert status == "ok" and "lineal" in detail
    assert verdict("discontinua", "x**2+y**2", "1", camins=[{"x": "t", "y": "0"}])[0] == "ok"
    assert verdict("diferenciable", "x**2+y**2", fita="r")[0] == "plausible"


def test_an_unreadable_function_fails_with_the_reason() -> None:
    status, detail = verdict("parcials_existeixen", "import os")
    assert status == "falla" and "La funció" in detail


def test_found_by_simulated_students() -> None:
    # Every concrete direction works; sympy failing on a symbolic (a, b) must not reject it.
    cube = "sign(x**3+y**3)*Abs(x**3+y**3)**(1/3)"
    assert verdict("direccionals_existeixen", cube)[0] == "plausible"
    # sympy loses a sign with atan(y/x) (the crossed derivatives are -1 and 1): undecided, never a wrong "falla".
    assert verdict("creuades_diferents", "x*y*cos(2*atan(y/x))")[0] in ("ok", "indeterminat")
    # One path with a limit proves nothing about non-existence: the message says to add a second one.
    status, detail = verdict("limit_no_existeix", "x**2*y/(x**4+y**2)", camins=[{"x": "t", "y": "t**2"}])
    assert status == "indeterminat" and "segon camí" in detail
    assert verdict("parcials_existeixen", "x*y", "1/0")[0] == "falla"


# Attacks a simulated student found to game the checker: none of them may pass.
LINES_1E15 = (
    "1+x*y*(y-x)*(y+x)*(y-2*x)*(y+3*x)*(2*y-x)*(2*y+x)*(3*y-x)*(y-3*x)*(3*y+x)*(2*y-3*x)*(3*y-2*x)*(7*y+5*x)"
    "/(10**15*(x**2+y**2)**7)"
)
SLOW_DECAY = "x**2*y**2/(x**2+y**2)**2*((sin(1/(x**2+y**2))+(x**2+y**2)**(1/100))**2-sin(1/(x**2+y**2))**2)"
SIN2_COS2 = "sin(x*y/(x**2+y**2)**2)**2+cos(x*y/(x**2+y**2)**2)**2+x**2*y**2*(x**2+y**2)**(1/4)/(x**2+y**2)**2"


@pytest.mark.parametrize(
    ("kind", "function", "value", "certificate"),
    [
        # sympy reads sin^2+cos^2 of a blowing-up argument as AccumBounds(0, 2): "no limit" needs numeric confirmation.
        ("discontinua", SIN2_COS2, "1", DIAGONAL),
        ("limit_no_existeix", SIN2_COS2, "1", DIAGONAL),
        # A bound that is >= 1 exactly at the sampled radii; a change below the smallest radius; a spike on a line.
        ("continua", "1", "0", {"fita": "r*(1+10**9*sin(1/r)**2)"}),
        ("continua", "exp(-10**20*(x**2+y**2))", "0", {"fita": "r"}),
        ("continua", "sign(Abs(x*y))*exp(-(1000*(y-37*x/100))**2/(x**2+y**2))", "0", {"fita": "r"}),
        # Not rational along y = m x, so no special slopes: the student's own line y = x/2 is checked.
        (
            "rectes_mateix_limit",
            "1-sign(Abs(2*y-x))",
            "0",
            {"camins": [{"x": "t", "y": "t/2"}]},
        ),
        # Complex in the thin sector 3/5 < y/x < 2/3.
        ("discontinua", "sqrt((2*x-3*y)*(3*x-5*y))+x**2*y/(x**4+y**2)", "0", {"camins": [{"x": "t", "y": "t**2"}]}),
        # Round 2. Exactly 1 on the 13 fixed slopes, 1 + 1e-15*c(m) elsewhere: no tolerance may call that equal.
        ("rectes_mateix_limit", LINES_1E15, "1", {"camins": [{"x": "t", "y": "5*t+t**2"}]}),
        # (sin A + r^(1/50))^2 - sin(A)^2 -> 0 slowly: sympy says AccumBounds, the expanded form has a limit.
        ("discontinua", SLOW_DECAY, "0", DIAGONAL),
        # D_(1,5) does not exist: the direction of the student's own path is tried.
        ("direccionals_existeixen", "Max(0,1-1000*(y-5*x)**2/(x**2+y**2))", "0", {"camins": [{"x": "t", "y": "5*t"}]}),
        # A discontinuity along y = x^20 and one along y = x^4.
        ("continua", "Abs(x)+x**20*y/(x**40+y**2)", "0", {"fita": "2*r"}),
        ("continua", "Abs(x)+x**20/((y-x**4)**2+x**20)", "0", {"fita": "2*r"}),
        # Undefined on the whole parabola y = x^2.
        ("limit_no_existeix", "x**4/(y-x**2)", "0", TWO_LINES),
    ],
)
def test_attacks_do_not_pass(kind: PropertyKind, function: str, value: str, certificate: dict[str, object]) -> None:
    check = PropertyCheck(
        kind=kind,
        function=function,
        origin_value=value,
        certificate=Certificate.model_validate(certificate),
        context_paths=Certificate.model_validate(certificate).paths,
    )
    assert check_property(check).status not in ("ok", "plausible")


def test_odd_roots_are_the_real_roots() -> None:
    # sympy's own (x**3+y**3)**(1/3) is complex for x**3+y**3 < 0; a student means the real root, as cbrt.
    assert verdict("direccionals_existeixen", "cbrt(x**3+y**3)")[0] == "plausible"
    assert verdict("parcials_existeixen", "(x**3+y**3)**(1/3)")[0] == "ok"
    assert verdict("continua", "(x*y)**(1/3)", fita="r**(2/3)")[0] == "plausible"
    assert verdict("alguna_direccional_no_existeix", "(x*y)**(1/3)", direccio={"u": "1", "w": "1"})[0] == "ok"
    # An even root of a negative is not real, and the message says so (not the advice about holes).
    status, detail = verdict("parcials_existeixen", "sqrt(x)+y")
    assert status == "falla" and "no és real" in detail


# A quotient that blows up (sign or cube root over h) has no limit, although sympy's simplify turns sign(h^2)/h
# into a Piecewise whose sympy limit is 0.
@pytest.mark.parametrize(
    ("kind", "function", "certificate"),
    [
        ("alguna_direccional_no_existeix", "cbrt(x*y)", {"direccio": {"u": "1", "w": "1"}}),
        ("alguna_direccional_no_existeix", "sign(x*y)", {"direccio": {"u": "1", "w": "2"}}),
        ("alguna_parcial_no_existeix", "cbrt(x)", {}),
        ("no_diferenciable", "cbrt(x*y)", {}),
        ("no_diferenciable", "sign(x*y)*Abs(x*y)**(1/3)", {"camins": [{"x": "t", "y": "t"}]}),
    ],
)
def test_a_quotient_that_blows_up_has_no_limit(
    kind: PropertyKind, function: str, certificate: dict[str, object]
) -> None:
    status, detail = verdict(kind, function, "0", **certificate)
    assert status == "ok", detail


# Found by an auditor: none of them may pass.
HIDDEN = "exp(-10**32*(x**2+y**2))"


@pytest.mark.parametrize(
    ("kind", "function", "certificate"),
    [
        ("parcials_existeixen", "cbrt(x)+x*y/(x**2+y**2)", {}),
        ("direccionals_existeixen", "sign(x*y)", {}),
        ("direccionals_existeixen", "x**2*y/(x**4+y**2)+cbrt(x)", {}),
        ("alguna_parcial_no_existeix", "cbrt(x)*Abs(x)", {}),
        # A discontinuity squeezed below every sampled radius by a huge constant.
        ("continua", f"x*y/sqrt(x**2+y**2)+x**2*y/(x**4+y**2)*{HIDDEN}", {"fita": "2*r"}),
        ("continua", f"Abs(x)+x**2*y/(x**4+y**2)*{HIDDEN}", {"fita": "2*r"}),
        # A special line with an irrational slope, where f along y = m x is not a rational function.
        ("rectes_mateix_limit", "x**4*exp(x)/((y-pi*x)**2+x**4)", {}),
        ("rectes_limit_f0", "x**4*exp(x)/((y-pi*x)**2+x**4)", {}),
        ("direccionals_existeixen", "x**2*y/(x**2+y**2)+Abs(x)*x**4/((y-sqrt(2)*x)**2+x**4)", {}),
        # Every directional derivative exists, but D_v is not linear in v.
        ("direccionals_lineals", "x**2*y/(x**2+y**2)", {}),
        ("direccionals_lineals", "x*y/sqrt(x**2+y**2)", {}),
    ],
)
def test_found_by_an_auditor(kind: PropertyKind, function: str, certificate: dict[str, object]) -> None:
    status, detail = verdict(kind, function, "0", **certificate)
    assert status not in ("ok", "plausible"), detail


def test_linear_directional_derivatives() -> None:
    assert verdict("direccionals_lineals", "x**3*y/(x**4+y**2)")[0] == "plausible"
    assert verdict("direccionals_lineals", "x+2*y+x**2*y**2")[0] == "plausible"
    status, detail = verdict("direccionals_lineals", "x**3/(x**2+y**2)")
    assert status == "falla" and "lineal" in detail


def test_a_huge_constant_is_refused_with_the_reason() -> None:
    status, detail = verdict("parcials_existeixen", "x*y*exp(-10**7*x**2)")
    assert status == "falla" and "massa gran" in detail


def test_a_positive_denominator_is_not_a_hole() -> None:
    # (y-x^4)^2 + x^20 > 0 off the origin; expanded, floats lose its sign. Only an exact sign change is a hole.
    assert verdict("alguna_parcial_no_existeix", "Abs(x)+x**20/((y-x**4)**2+x**20)")[0] == "ok"
    assert verdict("parcials_existeixen", "x**2*y/(x**4+y**2)")[0] == "ok"
