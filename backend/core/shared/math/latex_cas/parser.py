"""LaTeX -> sympy: a recursive-descent parser for the notation of the sheets, with sympy's lark parser as a
fallback."""

import re
from functools import lru_cache

import sympy as sp

from core.shared.math.latex_cas.bounds import (
    MAX_DET_SIZE,
    MAX_MATRIX_ENTRIES,
    _check_magnitude,
    _factorial,
    _ParseError,
    _pow,
    _sized,
)
from core.shared.math.latex_cas.normalise import _FUNC_ALIASES, _FUNC_LETTERS, _GREEK, _INVERSE, _SP_FUNCS, _normalise
from core.shared.math.latex_cas.sides import _top_level_split


class _Remainder:
    """An o(...) / O(...) term: dropped from sums (Taylor remainders)."""


LANDAU = _Remainder()
type _Term = sp.Basic | _Remainder  # what each grammar rule returns

_TOKEN = re.compile(r"\\[A-Za-z]+|\\.|\d+\.\d+|\.\d+|\d+|[A-Za-z]|\S")
_ATOM_CMDS = {"pi", "infty", "frac", "sqrt", "begin", "det", "max", "min", "exp", "e"} | _GREEK | set(_FUNC_ALIASES)


class _Parser:
    def __init__(self, text: str) -> None:
        self.toks = _TOKEN.findall(text)
        self.i = 0
        self.abs_depth = 0

    # -- helpers
    def peek(self, k: int = 0) -> str | None:
        j = self.i + k
        return self.toks[j] if j < len(self.toks) else None

    def take(self) -> str:
        t = self.peek()
        if t is None:
            raise _ParseError("unexpected end")
        self.i += 1
        return t

    def expect(self, t: str) -> None:
        if self.take() != t:
            raise _ParseError(f"expected {t}")

    def parse(self) -> sp.Basic:
        e = self.expr()
        if self.peek() is not None:
            raise _ParseError(f"trailing {self.peek()}")
        if e is LANDAU:
            raise _ParseError("only a remainder term")
        return e

    # -- grammar
    def expr(self) -> _Term:
        terms = []
        sign = 1
        if self.peek() in ("+", "-"):
            sign = -1 if self.take() == "-" else 1
        while True:
            t = self.term()
            if t is not LANDAU:
                terms.append(t if sign == 1 else -t)
            if self.peek() in ("+", "-"):
                sign = -1 if self.take() == "-" else 1
                continue
            break
        if not terms:
            return LANDAU
        if len(terms) == 1:
            return terms[0]
        if any(isinstance(x, sp.Tuple) for x in terms):
            raise _ParseError("sum with a tuple")
        out = terms[0]
        for x in terms[1:]:
            out = out + x  # works for matrices too
        return out

    def _starts_factor(self, t: str | None) -> bool:
        if t is None:
            return False
        if t[0].isdigit() or (t[0] == "." and len(t) > 1) or t.isalpha() or t in ("(", "[", "{"):
            return True
        if t == "|":
            return self.abs_depth == 0
        return t.startswith("\\") and t[1:] in _ATOM_CMDS

    def term(self) -> _Term:
        f = self.unary()
        while True:
            t = self.peek()
            if t == "*":
                self.take()
                g = self.unary()
            elif t == "/":
                self.take()
                g = self.unary()
                if g is LANDAU or f is LANDAU:
                    raise _ParseError("remainder in quotient")
                f = _sized(f / g)
                continue
            elif self._starts_factor(t):
                g = self.power()
            else:
                return f
            if isinstance(f, sp.Tuple) or isinstance(g, sp.Tuple):
                raise _ParseError("product with a tuple (unknown function applied?)")
            if f is LANDAU or g is LANDAU:
                f = LANDAU
            else:
                f = _sized(f * g)

    def unary(self) -> _Term:
        if self.peek() == "-":
            self.take()
            u = self.unary()
            return u if u is LANDAU else -u
        if self.peek() == "+":
            self.take()
            return self.unary()
        return self.power()

    def power(self) -> _Term:
        base = self.postfix(self.atom())
        if self.peek() == "^":
            self.take()
            exp = self.script()
            if base is LANDAU:
                raise _ParseError("power of remainder")
            base = self.postfix(_pow(base, exp))
        return base

    def postfix(self, e: _Term) -> _Term:
        while self.peek() == "!":
            self.take()
            e = _factorial(e)
        return e

    def script(self) -> _Term:
        """Argument of ^ or _: a braced group, or one token (one digit of a number: x^23 is x^2·3)."""
        t = self.peek()
        if t == "{":
            return self.group()
        if t in ("-", "+"):
            self.take()
            s = self.script()
            return -s if t == "-" else s
        if t is not None and t[0].isdigit() and len(t) > 1 and "." not in t:
            self.toks[self.i] = t[1:]
            return sp.Integer(t[0])
        return self.atom()

    def raw_script(self) -> str:
        """Subscript as text (x_0, h_{1}, f_{xy})."""
        t = self.take()
        if t != "{":
            if t[0].isdigit() and len(t) > 1:
                self.toks.insert(self.i, t[1:])
                return t[0]
            return t.lstrip("\\")
        depth, out = 1, []
        while True:
            t = self.take()
            if t == "{":
                depth += 1
            elif t == "}":
                depth -= 1
                if depth == 0:
                    return "".join(out)
            out.append(t.lstrip("\\"))

    def group(self) -> sp.Basic:
        self.expect("{")
        e = self.expr()
        self.expect("}")
        if e is LANDAU:
            raise _ParseError("remainder in group")
        return e

    def arg_group(self) -> _Term:
        """Argument of \\frac / \\sqrt: braced group or a single token (\\frac12)."""
        if self.peek() == "{":
            return self.group()
        t = self.peek()
        if t is not None and t[0].isdigit() and len(t) > 1 and "." not in t:
            self.toks[self.i] = t[1:]
            return sp.Integer(t[0])
        return self.atom()

    def call_args(self) -> list[_Term]:
        self.expect("(")
        args = [self.expr()]
        while self.peek() == ",":
            self.take()
            args.append(self.expr())
        self.expect(")")
        if any(a is LANDAU for a in args):
            raise _ParseError("remainder in arguments")
        return args

    def name_with_scripts(self, name: str) -> str:
        while True:
            if self.peek() == "_":
                self.take()
                name += "_" + self.raw_script()
            elif self.peek() == "'":
                self.take()
                name += "'"
            else:
                return name

    def named(self, name: str) -> _Term:
        """A letter or greek name with optional subscripts / primes, possibly applied as a function."""
        full = self.name_with_scripts(name)
        if name in ("o", "O") and "'" not in full and self.peek() == "(":  # o(x^2), O_3(x,y): a remainder
            self.call_args()
            return LANDAU
        if self.peek() == "(" and (name in _FUNC_LETTERS or "'" in full or "_" in full):
            return sp.Function(full)(*self.call_args())
        if self.peek() == "(":  # d(A,B), B(p,r): several arguments = an application; x(x+2) stays a product
            save = self.i
            try:
                args = self.call_args()
            except _ParseError:
                args = []
            self.i = save
            if len(args) > 1:
                self.call_args()
                return sp.Function(full)(*args)
        if full == "e":
            return sp.E
        return sp.Symbol(full)

    def function(self, name: str) -> sp.Basic:
        fname = _FUNC_ALIASES[name]
        power = None
        if self.peek() == "^":
            self.take()
            power = self.script()
            if power == -1 and fname in _INVERSE:
                fname, power = _INVERSE[fname], None
        if self.peek() == "(":
            self.take()
            arg = self.expr()
            self.expect(")")
        elif self.peek() == "{":
            arg = self.group()
        else:  # \sin x y, \sin 2x: implicit product up to the next operator or function
            arg = self.power()
            while self._starts_factor(self.peek()) and not (
                self.peek().startswith("\\") and self.peek()[1:] in _FUNC_ALIASES
            ):
                arg = arg * self.power()
        if arg is LANDAU:
            raise _ParseError("remainder in function")
        out = _SP_FUNCS[fname](arg)
        return _pow(out, power) if power is not None else out

    def matrix(self) -> sp.Basic:
        env = self.raw_script()
        if env not in ("pmatrix", "bmatrix", "matrix", "vmatrix", "Bmatrix", "smallmatrix"):
            raise _ParseError(f"environment {env}")
        rows, row = [], [self.expr()]
        while True:
            t = self.take()
            if t == "&":
                row.append(self.expr())
            elif t == "\\\\":
                rows.append(row)
                if self.peek() == "\\end":
                    row = None
                else:
                    row = [self.expr()]
            elif t == "\\end":
                if row is not None:
                    rows.append(row)
                if self.raw_script() != env:
                    raise _ParseError("mismatched environment")
                break
            else:
                raise _ParseError(f"unexpected {t} in matrix")
        if len({len(r) for r in rows}) != 1 or any(x is LANDAU for r in rows for x in r):
            raise _ParseError("ragged matrix")
        if len(rows) * len(rows[0]) > MAX_MATRIX_ENTRIES:
            raise _ParseError("matrix too large")
        m = sp.ImmutableMatrix(rows)
        return _det(m) if env == "vmatrix" else m

    def atom(self) -> _Term:
        t = self.take()
        if t[0].isdigit() or (t[0] == "." and len(t) > 1):
            return sp.Rational(t) if "." in t else sp.Integer(t)
        if t.isalpha() and len(t) == 1:
            return self.named(t)
        if t == "(" or t == "[":
            close = ")" if t == "(" else "]"
            items = [self.expr()]
            while self.peek() == ",":
                self.take()
                items.append(self.expr())
            self.expect(close)
            if any(x is LANDAU for x in items):
                raise _ParseError("remainder in brackets")
            return items[0] if len(items) == 1 else sp.Tuple(*items)
        if t == "{":
            self.i -= 1
            return self.group()
        if t == "|" and self.abs_depth == 0:
            self.abs_depth += 1
            e = self.expr()
            self.expect("|")
            self.abs_depth -= 1
            if e is LANDAU:
                raise _ParseError("remainder in abs")
            return sp.Abs(e)
        if t.startswith("\\"):
            cmd = t[1:]
            if cmd in ("cdots", "dots", "ldots"):  # "1 + x + x^2/2 + \cdots": the tail of a series
                return LANDAU
            if cmd == "pi":
                return sp.pi
            if cmd == "infty":
                return sp.oo
            if cmd == "e":
                return sp.E
            if cmd == "frac":
                num = self.arg_group()
                return num / self.arg_group()
            if cmd == "sqrt":
                if self.peek() == "[":
                    self.take()
                    n = self.expr()
                    self.expect("]")
                    return sp.root(self.arg_group(), n)
                return sp.sqrt(self.arg_group())
            if cmd in _FUNC_ALIASES:
                return self.function(cmd)
            if cmd in _GREEK:
                return self.named(cmd)
            if cmd == "begin":
                return self.matrix()
            if cmd == "det":
                m = self.power()
                if not isinstance(m, sp.MatrixBase):
                    raise _ParseError("det of non-matrix")
                return _det(m)
            if cmd in ("max", "min"):
                args = self.call_args()
                return (sp.Max if cmd == "max" else sp.Min)(*args)
        raise _ParseError(f"unsupported token {t}")


def _det(m: sp.MatrixBase) -> sp.Basic:
    if max(m.shape) > MAX_DET_SIZE:
        raise _ParseError("determinant too large")
    return m.det()


_LARK_OK = re.compile(r"^[^{}\\]*$")  # lark is only tried on plain text (never on \lim: notation, not a value)


def _lark(latex: str) -> sp.Expr | None:
    try:
        # Imported on first use: loading the lark grammar is slow, and most formulas never reach this fallback.
        from sympy.parsing.latex import parse_latex

        # Built unevaluated first: sympy would otherwise compute "9^9^9" exactly while parsing it.
        with sp.evaluate(False):
            raw = parse_latex(latex, backend="lark")
        _check_magnitude(raw)
        e = parse_latex(latex, backend="lark")
    except Exception:
        return None
    # A limit is kept unevaluated (opaque): evaluating it would turn notation from the statement into its value.
    return e if isinstance(e, sp.Expr) else None


def _degenerate(e: object) -> bool:
    return isinstance(e, sp.Basic) and (e.has(sp.nan) or e.has(sp.zoo))  # 0/0, 1/0


@lru_cache(maxsize=8192)
def _parse_side(side: str) -> sp.Basic | None:
    try:
        e = _Parser(side).parse()
        return None if _degenerate(e) else e
    except (
        _ParseError,
        TypeError,
        ValueError,
        ZeroDivisionError,
        AttributeError,
        IndexError,
        RecursionError,
        sp.SympifyError,
        sp.ShapeError,
        NotImplementedError,
    ):
        pass
    except Exception:  # never raise to the caller
        return None
    if not (_LARK_OK.search(side) and len(side) < 200):
        return None
    e = _lark(side)
    return None if e is None or _degenerate(e) else e


_RELATIONS = {"=": sp.Eq, r"\neq": sp.Ne, r"\le": sp.Le, r"\ge": sp.Ge, "<": sp.Lt, ">": sp.Gt}


def parse(latex: str) -> sp.Basic | None:
    """LaTeX -> sympy, or None (never raises). "A = B", "A \\le B"... give a sympy relational."""
    try:
        seps: list[str] = []
        parts = _top_level_split(_normalise(latex), seps)
        if len(parts) == 1:
            return _parse_side(parts[0])
        if len(parts) == 2 and len(seps) == 1 and seps[0] in _RELATIONS:
            a, b = _parse_side(parts[0]), _parse_side(parts[1])
            if isinstance(a, sp.Expr) and isinstance(b, sp.Expr):
                return _RELATIONS[seps[0]](a, b, evaluate=False)
        return None
    except Exception:
        return None
