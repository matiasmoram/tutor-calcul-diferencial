import pytest

from core.counterexamples.domain.properties import PROPERTIES, PropertyKind
from core.counterexamples.domain.services.property_deciders import check_property
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


# Wrong submissions: each must fail, or stay undecided when a certificate is missing; never pass.
@pytest.mark.parametrize(
    ("kind", "function", "value", "certificate", "expected"),
    [
        # The parabola y = x^2 breaks every bound G(r) -> 0, also close to the origin (angles hugging the axis).
        ("continua", "x**2*y/(x**4+y**2)", "0", {"fita": "r"}, "falla"),
        ("continua", "x**2*y/(x**4+y**2)", "0", {"fita": "2*r**(1/10)"}, "falla"),
        ("continua", "x**2+y**2", "0", {"fita": "1"}, "falla"),
        ("continua", "x**2+y**2", "0", {}, "indeterminat"),
        ("limit_no_existeix", "x**2*y/(x**4+y**2)", "0", TWO_LINES, "falla"),
        ("limit_no_existeix", "x**2+y**2", "0", {"camins": [{"x": "t", "y": "1"}]}, "falla"),
        ("limit_no_existeix", "x**2+y**2", "0", {"camins": [{"x": "0", "y": "0"}]}, "falla"),
        ("limit_no_existeix", "x**2+y**2", "0", {}, "indeterminat"),
        ("discontinua", "x**2+y**2", "0", {"camins": [{"x": "t", "y": "0"}]}, "falla"),
        ("diferenciable", "x*y/sqrt(x**2+y**2)", "0", {"fita": "r"}, "falla"),
        ("diferenciable", "x**2*y/(x**2+y**2)", "0", {"fita": "r"}, "falla"),
        ("creuades_diferents", "x*y", "0", {}, "falla"),
        ("rectes_mateix_limit", "x*y/(x**2+y**2)", "0", {}, "falla"),
        ("iterats_iguals", "(x-y)/(x+y)", "0", {}, "falla"),
        ("no_diferenciable", "x**2+y**2", "0", {}, "indeterminat"),
        ("no_diferenciable", "x**2+y**2", "0", DIAGONAL, "falla"),
        ("no_diferenciable", "Abs(x*y)**(3/4)", "0", DIAGONAL, "falla"),
        ("parcial_discontinua", "x**2+y**2", "0", {"parcial": "x", **DIAGONAL}, "falla"),
        ("direccionals_existeixen", "Abs(x)", "0", {}, "falla"),
        ("alguna_direccional_no_existeix", "x**2", "0", {"direccio": {"u": "0", "w": "0"}}, "falla"),
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
    assert status == "falla" and "segon camí" in detail
    assert verdict("parcials_existeixen", "x*y", "1/0")[0] == "falla"
