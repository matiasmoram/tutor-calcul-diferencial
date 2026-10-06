"""CAS math-provenance leak checker (backend/tutor/cas.py): parsing, equivalence, leak detection."""

import sys
import time
from pathlib import Path

import pytest
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from tutor import cas  # noqa: E402
from tutor.cas import equivalent, explain, formules, leaked, parse, sides  # noqa: E402
from tutor.fitxes import load_exercicis  # noqa: E402

x, y, z = sp.symbols("x y z")


# ---------- extraction and splitting


def test_formules_extracts_inline_display_and_bracket_math():
    text = r"Cal $x^2-y^2\neq0$, és a dir $$y\neq\pm x$$, i \(a+b\); costa \$5 i \[c\]."
    assert formules(text) == [r"x^2-y^2\neq0", r"y\neq\pm x", "a+b", "c"]
    assert formules("") == [] and formules("sense fórmules") == []


def test_sides_split_chains_relations_lists_and_sets():
    assert sides(r"\dfrac{\partial u}{\partial x}=\dfrac{2x}{y}=\dfrac{-4xy^2}{(x^2-y^2)^2}") == [
        r"\frac{\partial u}{\partial x}", r"\frac{2x}{y}", r"\frac{-4xy^2}{(x^2-y^2)^2}"]
    assert sides(r"x=1,\ y\le 2") == ["x", "1", "y", "2"]
    assert sides(r"y=\pm x") == ["y", "+ x", "- x"]
    assert sides(r"E=\{(x,y)\mid x^2+|y|=5\}") == ["E", "(x,y)", "x^2+|y|", "5"]
    assert sides(r"f(x,y)\to 0") == ["f(x,y)", "0"]
    # Brackets protect their content: f(x,y) and the limit subscript are not split.
    assert len(sides(r"\lim_{(x,y)\to(0,0)}f(x,y)")) == 1


def test_value_sides_drop_the_name_of_an_equation_chain():
    assert sides(r"e^{\sin y}=1+y+\frac{y^2}{2}+o(y^2)", values_only=True) == [r"1+y+\frac{y^2}{2}+o(y^2)"]
    assert sides(r"a=1,\ b=c=2", values_only=True) == ["1", "c", "2"]
    assert sides(r"|x|\le\sqrt{x^2+y^2}", values_only=True) == ["|x|", r"\sqrt{x^2+y^2}"]


# ---------- parsing


@pytest.mark.parametrize("latex, expected", [
    (r"\dfrac{-4xy^2}{(x^2-y^2)^2}", -4 * x * y**2 / (x**2 - y**2) ** 2),
    (r"\tfrac{\pi}{4}", sp.pi / 4),
    (r"\frac12", sp.Rational(1, 2)),
    ("0{,}25", sp.Rational(1, 4)),
    ("0.25", sp.Rational(1, 4)),
    (r"\left(\dfrac{1}{2}\right)^{2}", sp.Rational(1, 4)),
    (r"x\cdot y", x * y),
    (r"2\,x\;y", 2 * x * y),
    ("x(x+2)", x * (x + 2)),
    (r"e^{x}\sin y", sp.exp(x) * sp.sin(y)),
    (r"\mathrm{e}^{-x^2}", sp.exp(-x**2)),
    (r"\operatorname{tg} x", sp.tan(x)),
    (r"\sin^2 x+\cos^{2}x", sp.sin(x) ** 2 + sp.cos(x) ** 2),
    (r"\sin 2x\cos y", sp.sin(2 * x) * sp.cos(y)),
    (r"\sin^{-1}x", sp.asin(x)),
    (r"\ln(1+x)", sp.log(1 + x)),
    (r"\sqrt[3]{x}", sp.root(x, 3)),
    (r"|x-y|", sp.Abs(x - y)),
    ("x^23", 3 * x**2),  # LaTeX: the exponent is one token
    (r"1+x+\frac{x^2}{2}+o(x^2)", 1 + x + x**2 / 2),  # remainders are dropped
    (r"x-\frac{x^3}{3!}+\cdots", x - x**3 / 6),
    (r"1-s+O_3(s)", 1 - sp.Symbol("s")),
    ("x² − y²", x**2 - y**2),  # unicode
    (r"\det\begin{pmatrix}1&x\\y&2\end{pmatrix}", 2 - x * y),
])
def test_parse_normalises_sheet_notation(latex, expected):
    got = parse(latex)
    assert got is not None, latex
    assert sp.simplify(got - expected) == 0, (latex, got)


def test_parse_structures():
    assert parse("(1,-1,2)") == sp.Tuple(1, -1, 2)
    assert parse(r"\begin{pmatrix}1&x\\y&2\end{pmatrix}") == sp.ImmutableMatrix([[1, x], [y, 2]])
    assert parse("x=1") == sp.Eq(x, 1, evaluate=False)
    assert isinstance(parse(r"x\le 2"), sp.Le)
    f = parse("f(x,y)")
    assert f is not None and f.func.__name__ == "f"
    assert parse("d(A,B)").func.__name__ == "d"  # several arguments: an application, not a product


@pytest.mark.parametrize("bad", [
    "", "}", "{", r"\frac{1}{", r"\frac{\partial f}{\partial x}", r"\mathbb{R}^2", r"\{x\}", "x=1, y=2",
    r"\sum_{i=1}^n x_i", r"\int_0^1 f", "(", ")(", "0/0", r"\begin{cases}1\end{cases}", "^^", "a" * 3000,
    r"\left(" * 50, None, 42,
])
def test_parse_never_raises(bad):
    assert parse(bad) is None or isinstance(parse(bad), sp.Basic)


# ---------- equivalence


@pytest.mark.parametrize("a, b", [
    (r"\frac{1}{4}", "0.25"),
    (r"\frac14", "0{,}25"),
    ("x^2+2x", "x(x+2)"),
    (r"\frac{-4xy^2}{(x^2-y^2)^2}", r"-4xy^2(x^2-y^2)^{-2}"),
    (r"\pi/2", r"\frac{\pi}{2}"),
    (r"\sqrt{12}", r"2\sqrt3"),
    (r"\sqrt{3}", "1.73"),  # a rounded decimal (>= 2 decimals) matches
    (r"\sin^2x+\cos^2x", "1"),
    (r"\ln(xy)", r"\ln x+\ln y"),  # equal on the real domain where both are defined
    (r"\frac{1}{x}", "x^{-1}"),
    ("(1,2)", r"(1,\frac42)"),
    (r"\begin{pmatrix}2x&0\\0&1\end{pmatrix}", r"\begin{pmatrix}x+x&0\\0&1\end{pmatrix}"),
    ("x=1", "1=x"),
    (r"\infty", r"\infty"),
    (r"e^{\ln 2}", "2"),
])
def test_equivalent_true(a, b):
    assert equivalent(a, b) is True


@pytest.mark.parametrize("a, b", [
    ("x^2", "x^3"),
    ("|x|", "x"),
    (r"\sqrt{x^2}", "x"),
    (r"\sqrt3", "1.7"),  # one decimal is too coarse to call it the same value
    (r"\frac13", "0.3"),
    ("x+y", "x+z"),
    ("1", "x"),
    ("(1,2)", "(2,1)"),
    ("(1,2)", "(1,2,3)"),
    (r"\begin{pmatrix}1&0\\0&1\end{pmatrix}", r"\begin{pmatrix}1&0\\0&2\end{pmatrix}"),
])
def test_equivalent_false(a, b):
    assert equivalent(a, b) is False


def test_equivalent_undecidable_is_none():
    assert equivalent(r"\mathbb{R}", "x") is None
    assert equivalent(r"\frac{\partial f}{\partial x}", "2x") is None
    assert equivalent("x=1, y=2", "x") is None


def test_equivalent_accepts_sympy_objects():
    assert equivalent(x * (x + 2), "x^2+2x") is True
    assert equivalent(sp.Rational(1, 4), 0.25) is True


# ---------- leak detection

DETALL = r"$\dfrac{\partial u}{\partial x}=\dfrac{2x(x^2-y^2)-(x^2+y^2)\,2x}{(x^2-y^2)^2}=\dfrac{-4xy^2}{(x^2-y^2)^2}$."
ENUNCIAT = r"$u(x,y)=\dfrac{x^2+y^2}{x^2-y^2}$"


def test_equivalent_form_leak_is_caught():
    draft = r"Fixa't que $u_x = -4xy^2(x^2-y^2)^{-2}$, oi?"
    assert leaked(draft, [DETALL], [ENUNCIAT]) == [r"-4xy^2(x^2-y^2)^{-2}"]
    # Both right-hand sides of the chain have that value; explain() names the first one.
    ((side, match),) = explain(draft, [DETALL], [ENUNCIAT])
    assert side == r"-4xy^2(x^2-y^2)^{-2}" and match == r"\frac{2x(x^2-y^2)-(x^2+y^2) 2x}{(x^2-y^2)^2}"


def test_numeric_value_leak_in_another_notation_is_caught():
    assert leaked(r"El límit val $0{,}25$?", [r"El límit és $\frac{1}{4}$."], []) == ["0.25"]
    assert leaked(r"Potser $\frac{\sqrt2}{2}$?", [r"$\cos\frac{\pi}{4}$ és el màxim, $M=0.7071$"], []) == [
        r"\frac{\sqrt2}{2}"]


def test_factored_form_leak_is_caught():
    forb = [r"$f_x=-6xy^2+3x^2y^3=3xy^2(xy-2)$"]
    assert leaked(r"Has arribat a $-6xy^2+3x^2y^3$?", forb, []) == ["-6xy^2+3x^2y^3"]
    assert leaked(r"Pots treure factor comú: $3xy^2(xy-2)$.", forb, []) == ["3xy^2(xy-2)"]


def test_permitted_formula_is_not_flagged():
    draft = r"Has escrit $\frac{-4xy^2}{(x^2-y^2)^2}$: com hi has arribat?"
    student = r"em surt -4xy^2/(x^2-y^2)^2"  # a student message typed without $...$
    assert leaked(draft, [DETALL], [ENUNCIAT, student]) == []
    assert leaked(draft, [DETALL], [ENUNCIAT, r"crec que és $-\frac{4xy^2}{(x^2-y^2)^2}$"]) == []


def test_subexpression_of_permitted_formula_is_not_flagged():
    # x^2-y^2 is a side of the forbidden detail, but also part of the statement's formula.
    forb = [r"Cal $x^2-y^2\neq0$, és a dir $y\neq\pm x$, i $(x^2-y^2)^2>0$."]
    assert leaked(r"Mira $x^2-y^2$ i $(x^2-y^2)^2$.", forb, []) == ["x^2-y^2", "(x^2-y^2)^2"]
    assert leaked(r"Mira $x^2-y^2$ i $(x^2-y^2)^2$.", forb, [ENUNCIAT]) == ["(x^2-y^2)^2"]
    assert leaked(r"Mira $x^2+y^2$ i $y^2-x^2$ (canvi de signe).", [r"$x^2+y^2=r^2$, $y^2-x^2=1$"],
                  [r"$f=\cos(x^2+y^2)+(x^2-y^2)$"]) == []


def test_name_of_an_equation_is_not_a_leak_but_its_value_is():
    forb = [r"$e^{\sin y}=1+y+\frac{y^2}{2}+o(y^2)$"]
    assert leaked(r"Desenvolupa $e^{\sin y}$ fins a ordre 2.", forb, []) == []
    assert leaked(r"Obtens $1+y+\frac12y^2$?", forb, []) == [r"1+y+\frac12y^2"]


def test_trivial_formulas_are_ignored():
    forb = [r"$x=0$, $y=1$, $k=2$, $f(0,0)=0$, $t\to+\infty$, $(0,+\infty)$, $|x|\le 1$, $-1$"]
    draft = r"Què passa si $x=0$ o $y=1$? Mira $f(0,0)$, $|x|$, $-1$, $k=2$, $t\to\infty$ i l'interval $(0,+\infty)$."
    assert leaked(draft, forb, []) == []


def test_unparseable_formulas_do_not_crash_or_flag():
    forb = [r"$\frac{\partial f}{\partial x}(0,0)=\lim_{h\to0}\frac{f(h,0)-f(0,0)}{h}$", r"$\{x\in\mathbb{R}\}$", "$"]
    draft = r"Pensa en $\frac{\partial f}{\partial x}$, $\mathbb{R}^2$, $\frac{1}{$ i $}}{{$."
    assert leaked(draft, forb, []) == []
    assert leaked("", forb, []) == [] and leaked(draft, [], []) == []
    assert leaked(None, [None], [None]) == []  # type: ignore[list-item]


def test_leaked_on_a_real_sheet():
    ex = load_exercicis()["t3-1a"]
    detall_x = ex.pas("parcial_x").detall
    draft = r"Si simplifiques el numerador, obtens $\frac{-4\,x\,y^{2}}{\left(x^{2}-y^{2}\right)^{2}}$, veritat?"
    assert leaked(draft, [detall_x, ex.resultat.valor], [ex.enunciat_md()])
    # The hint texts of the sheet do not leak the step's detail.
    for i, pas in enumerate(ex.passos):
        forbidden = [p.detall for p in ex.passos[i:]] + [ex.resultat.valor]
        assert leaked(pas.objectiu + pas.idea, forbidden, [ex.enunciat_md()]) == []


def test_leaked_is_fast_once_the_sheet_is_cached():
    ex = load_exercicis()["t3-1a"]
    forbidden = [p.detall for p in ex.passos] + [ex.resultat.valor]
    permitted = [ex.enunciat_md()]
    draft = r"Prova amb $\frac{2x(x^2-y^2)-(x^2+y^2)2x}{(x^2-y^2)^2}$ i compara-ho amb $\frac{4x^2y}{(x^2-y^2)^2}$."
    leaked(draft, forbidden, permitted)  # warm the caches (the sheet is the same every turn)
    t0 = time.perf_counter()
    for i in range(20):
        leaked(draft + " " * i, forbidden, permitted)  # a new draft each time: only the sheet is cached
    assert (time.perf_counter() - t0) / 20 < 0.05


def test_is_trivial():
    assert all(cas.is_trivial(parse(s)) for s in ["x", "-x", "2", "-2", "0", "1", r"\infty", "f(0,0)", "|x|",
                                                  "(0,1)", "A^c", r"D\varphi"])
    assert not any(cas.is_trivial(parse(s)) for s in ["3", r"\frac12", "x+1", "2x", "xy", "(1,3)"])
