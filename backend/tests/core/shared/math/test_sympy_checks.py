import pytest

from core.shared.math.sympy_checks import MathCheck, evaluate_one
from tests.core.shared.math.builders import ITERATED, check


@pytest.mark.parametrize(
    ("c", "status"),
    [
        (ITERATED, "ok"),
        (check("limit", "x*(m*x)/(x**2+(m*x)**2)", "0"), "falla"),
        (check("no_limit", "sin(1/y)", variable="y"), "ok"),
        (check("no_limit", "y*sin(1/y)", variable="y"), "falla"),
        (check("no_limit", "Abs(x)/x"), "ok"),
        (check("igualtat", "diff(x**2*y, x)", "2*x*y", variable="", point=""), "ok"),
        (check("igualtat", "sqrt(x**2)", "x", variable="", point=""), "falla"),
        (check("limit", "x^2*(x^2)/(x^4+(x^2)^2)", "1/2"), "ok"),
    ],
)
def test_sympy_checks(c: MathCheck, status: str) -> None:
    assert evaluate_one(c).status == status


@pytest.mark.parametrize(
    "expr", ["__import__('os').system('x')", "x.__class__", "open(x)", "lambda: 1", "x; y", "eval(x)"]
)
def test_checks_never_eval_untrusted_python(expr: str) -> None:
    r = evaluate_one(check("limit", expr, "0"))
    assert r.status == "indeterminat" and r.detail


def test_unknown_kind_is_undecided_not_an_error() -> None:
    assert evaluate_one(check("derivada", "x")).status == "indeterminat"


def test_results_serialize_to_the_stored_catalan_keys() -> None:
    assert evaluate_one(ITERATED).model_dump() == {"estat": "ok", "calculat": "m/(m**2 + 1)", "detall": ""}
    assert ITERATED.model_dump()["expressio"] == "x*(m*x)/(x**2+(m*x)**2)"
