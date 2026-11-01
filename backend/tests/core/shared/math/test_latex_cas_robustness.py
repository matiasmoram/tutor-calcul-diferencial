"""The CAS leak check on hostile or careless input: bounded time, unparseable instead of hanging, prose formulas."""

import time

import pytest

from core.shared.math import latex_cas as cas
from core.shared.math.latex_cas import leaks

HUGE = [
    r"$9^{9^{9}}$",
    "9^9^9",
    "9**9**9",
    r"$10!!!!$",
    "10!!!!",
    r"$2^{2^{100}}$",
    r"$(2x)^{10^{9}}$",
    r"$\sin^{99999999}(x)$",
    r"$((10^{900})^{9})^{9}$",
    r"$\begin{vmatrix} a&b&c&d&e \\ a&b&c&d&e \\ a&b&c&d&e \\ a&b&c&d&e \\ a&b&c&d&e \end{vmatrix}$",
]


@pytest.mark.parametrize("text", HUGE)
def test_huge_numbers_are_unparseable_not_a_hang(text: str) -> None:
    t0 = time.perf_counter()
    for side in [s for f in cas.formulas(text) or [text] for s in cas.sides(f)]:
        cas.parse(side)
    # A student message in the permitted pool, and as a draft, as the guard reads them.
    cas.explain(r"La idea és $x^2+1$ i $\frac{3}{7}$.", [r"$\frac{3}{7}$"], [text])
    cas.explain(text, [r"$\frac{3}{7}$"], [])
    assert time.perf_counter() - t0 < 1.0


def test_large_but_reasonable_numbers_still_parse() -> None:
    assert cas.equivalent("2^{100}", str(2**100)) is True
    assert cas.equivalent("10!", "3628800") is True
    assert cas.parse("x^{12}") is not None


def test_undelimited_equations_in_prose_are_checked() -> None:
    forbidden = [r"$P_2(x,y)=2+x+y+\frac{x^2+y^2}{2}$"]
    for draft in (
        "Prova: P_2 = x + y + 2 + (x^2+y^2)/2. Ho veus?",
        "Prova: P2 = 1 + 1 + x + y + (x^2+y^2)/2. Ho veus?",
        "Fixa't: P₂ = 2 + x + y + ½(x² + y²). Ho veus?",
        "```\nP_2 = x+y+2+(x^2+y^2)/2\n```\nHo veus?",
    ):
        assert cas.explain(draft, forbidden, []), draft


def test_prose_formulas_stop_at_words() -> None:
    assert cas.prose_formulas("el valor és x = 3 aproximadament, i y = 4") == ["x = 3", "y = 4"]
    assert cas.prose_formulas("Si $x=1$ llavors y = 2x + 3 és la recta.") == ["y = 2x + 3"]
    assert cas.prose_formulas("Mira el denominador. Què passa si fixes una recta?") == []


def test_prose_formulas_of_the_permitted_texts_are_permitted() -> None:
    forbidden = [r"$x+y+2$"]
    assert cas.explain("Tens x + y + 2 = 0. Ho veus?", forbidden, ["he trobat que P = x + y + 2, oi?"]) == []


def test_an_unexpected_error_propagates_instead_of_meaning_no_leak(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*_: object) -> object:
        raise MemoryError

    monkeypatch.setattr(leaks, "_compare", boom)
    with pytest.raises(MemoryError):
        cas.explain(r"Mira $(x+1)^2$.", [r"$x^2+2x+1$"], [])
