"""Math-provenance leak check with a CAS (architectures.md, sections 2.4 and 6.3).

Regexes miss leaks written in an equivalent form ("\\frac{1}{4}" vs "0.25", "x^2+2x" vs "x(x+2)"). This module
extracts the formulas of a text, parses them into sympy, and compares them by value:

- `formulas(text)`: the math segments of a text ($...$, $$...$$, \\(...\\), \\[...\\]).
- `sides(segment)`: the comparable pieces of a segment: relations (=, <, \\le, \\to, ...) and top-level commas
  split it, so "A = B = C" gives A, B and C; "\\pm" gives both signs.
- `prose_formulas(text)`: equations written in the prose without delimiters ("P_2 = 2 + x + (x^2+y^2)/2").
- `parse(latex)`: LaTeX -> sympy, or None (never raises). A small recursive-descent parser handles the notation
  of the sheets; sympy's lark LaTeX parser is a fallback for what it does not know.
- `equivalent(a, b)`: True / False / None (undecidable). Random-point numeric comparison with shared values per
  free symbol (Schwartz-Zippel style); constants are compared to high precision, and a decimal literal with
  >= 2 decimals matches a constant it rounds (1.73 ~ sqrt(3)).
- `leaked(draft, forbidden, allowed)`: draft formulas equivalent to a forbidden formula and to no permitted one.

Pure functions, no LLM. Only a parsed-and-equivalent comparison gives a verdict: an unparseable formula is never
reported (the regexes and the LLM guard still cover it).
"""

import random
import re
from functools import lru_cache

import sympy as sp
from sympy.core.function import AppliedUndef

__all__ = [
    "checkable",
    "equivalent",
    "explain",
    "formulas",
    "is_trivial",
    "leaked",
    "literal_tokens",
    "parse",
    "prose_formulas",
    "sides",
]

N_POINTS = 8
MIN_VALID_POINTS = 3
REL_TOL = 1e-8
LANDAU = object()  # o(...) / O(...) terms: dropped from sums (Taylor remainders)


class _ParseError(Exception):
    pass


# Size bounds: sympy evaluates integer powers and factorials exactly, holding the GIL, so "9^{9^{9}}" in a message
# would freeze every thread of the process. Anything beyond these bounds is not a usable formula (unparseable).
MAX_INT_BITS = 16384  # ~4900 decimal digits
MAX_EXPONENT = 10_000  # numeric exponent, any base
MAX_FACTORIAL = 1000
MAX_MATRIX_POWER = 64
MAX_MATRIX_ENTRIES = 36
MAX_DET_SIZE = 4


def _bits(x: sp.Rational) -> int:
    return max(abs(int(x.p)).bit_length(), int(x.q).bit_length())


def _sized(e):
    """`e`, unless its numeric coefficient is too large to keep computing with."""
    c = e if isinstance(e, sp.Rational) else e.as_coeff_Mul()[0] if isinstance(e, sp.Mul) else None
    if isinstance(c, sp.Rational) and _bits(c) > MAX_INT_BITS:
        raise _ParseError("number too large")
    return e


def _pow(base, exp):
    """base**exp, refused before sympy starts an exact computation that cannot finish in reasonable time."""
    if base == sp.E:
        return sp.exp(exp)
    if isinstance(exp, sp.Rational):
        if isinstance(base, sp.MatrixBase):
            if abs(exp) > MAX_MATRIX_POWER:
                raise _ParseError("matrix power too large")
        elif abs(exp) > MAX_EXPONENT:
            raise _ParseError("exponent too large")
        elif isinstance(base, sp.Rational) and base not in (0, 1, -1) and _bits(base) * abs(float(exp)) > MAX_INT_BITS:
            raise _ParseError("power too large")
    return _sized(base**exp)


def _factorial(e):
    if isinstance(e, sp.Integer) and e > MAX_FACTORIAL:
        raise _ParseError("factorial too large")
    return sp.factorial(e)


def _check_magnitude(e) -> float | None:
    """Bound of log2|value| of an unevaluated numeric subtree (None if symbolic); raises _ParseError when
    evaluating it would exceed the size bounds. Used on sympy's own parser output, built with evaluate=False."""
    if isinstance(e, sp.Rational):
        return float(_bits(e))
    if not isinstance(e, sp.Basic) or not e.args:
        return None
    sub = [_check_magnitude(a) for a in e.args]
    if isinstance(e, sp.Pow):
        b, x = sub
        if x is None:
            return None
        if x > MAX_EXPONENT.bit_length():
            raise _ParseError("exponent too large")
        if b is None:
            return None
        mag = b * 2.0**x
        if mag > MAX_INT_BITS:
            raise _ParseError("power too large")
        return mag
    if isinstance(e, sp.factorial):
        if sub[0] is not None and sub[0] > MAX_FACTORIAL.bit_length():
            raise _ParseError("factorial too large")
        return None if sub[0] is None else 2.0 ** sub[0] * sub[0]
    if any(m is None for m in sub):
        return None
    if isinstance(e, sp.Mul):
        total = sum(m for m in sub if m is not None)
        if total > MAX_INT_BITS:
            raise _ParseError("number too large")
        return total
    if isinstance(e, sp.Add):
        return max(m for m in sub if m is not None) + len(sub)
    return None


# ---------------------------------------------------------------- extraction

_SEGMENT = re.compile(r"\$\$(.+?)\$\$|(?<!\\)\$(.+?)(?<!\\)\$|\\\[(.+?)\\\]|\\\((.+?)\\\)", re.DOTALL)


@lru_cache(maxsize=4096)
def _formulas(text: str) -> tuple[str, ...]:
    return tuple(next(g for g in m.groups() if g is not None).strip() for m in _SEGMENT.finditer(text or ""))


def formulas(text: str) -> list[str]:
    """Math segments of a text, in order ($$...$$, $...$, \\[...\\], \\(...\\))."""
    return [f for f in _formulas(text) if f]


# Clause ends outside formulas: a sentence end or colon followed by a space (not the point of 2.125), a line
# break, a code fence.
_CLAUSE_END = re.compile(r"[.!?;:](?=\s|$)|\n|`+")
_WORD = re.compile(r"[^\W\d_]+(?:['’·-][^\W\d_]+)*")
_MATH_CHAR = re.compile(r"[\d=+\-*/^_()\[\]{}|\\<>≤≥≈²³½√π·!]|[⁰-₟]")
_PROSE_LETTERS = {"a", "e", "i", "o"}  # Catalan words (to, and, or) when standing alone, not variables
_PROSE_RELATION = re.compile(r"=|≈|\\approx(?![A-Za-z])")


def _mathlike(token: str) -> bool:
    word = token.rstrip(",")
    if not word:
        return False
    if _WORD.fullmatch(word):  # letters only: a variable, a function name, or a prose word
        low = word.lower()
        if len(word) == 1:
            return low not in _PROSE_LETTERS
        return low in _FUNC_ALIASES or low in ("sqrt", "pi") or re.fullmatch(r"[xyzuvw]{2,3}", word) is not None
    return _MATH_CHAR.search(word) is not None


@lru_cache(maxsize=4096)
def _prose_formulas(text: str) -> tuple[str, ...]:
    prose = _SEGMENT.sub("\n", text or "")
    out: list[str] = []
    for clause in _CLAUSE_END.split(prose):
        run: list[str] = []
        for token in [*clause.split(), ""]:
            if token and _mathlike(token):
                run.append(token)
                if not token.endswith(","):  # "x = 2, per tant": the comma closes the formula
                    continue
            candidate = " ".join(run).rstrip(",").strip()
            if _PROSE_RELATION.search(candidate):
                out.append(candidate)
            run = []
    return tuple(out)


def prose_formulas(text: str) -> list[str]:
    """Equations written in plain prose, without $...$ (cheap models skip the delimiters): maximal runs of
    math-looking words that contain "=" or "≈". A word of two or more letters ends a run unless it is a function
    name, so "el valor és x = 3 aproximadament" gives "x = 3"."""
    return list(_prose_formulas(text))


# ---------------------------------------------------------------- normalisation

_UNICODE = {
    "≤": r"\le ",
    "≥": r"\ge ",
    "≠": r"\neq ",
    "·": r"\cdot ",
    "×": r"\times ",
    "−": "-",
    "–": "-",
    "π": r"\pi ",
    "√": r"\sqrt ",
    "∞": r"\infty ",
    "→": r"\to ",
    "±": r"\pm ",
    "∓": r"\mp ",
    "²": "^2",
    "³": "^3",
    "≈": r"\approx ",
    "⇒": r"\Rightarrow ",
    "⇔": r"\iff ",
    "∈": r"\in ",
    "α": r"\alpha ",
    "β": r"\beta ",
    "θ": r"\theta ",
    "λ": r"\lambda ",
    "φ": r"\varphi ",
    "∂": r"\partial ",
    "∇": r"\nabla ",
    "\u00bd": r"\frac{1}{2}",
    "\u00bc": r"\frac{1}{4}",
    "\u00be": r"\frac{3}{4}",
    "\u00a0": " ",
    **{chr(0x2080 + d): f"_{d}" for d in range(10)},  # P\u2082
    **{
        c: f"^{d}"
        for d, c in enumerate("\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079")
        if d not in (2, 3)
    },
}
_FUNC_ALIASES = {
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "tg": "tan",
    "cot": "cot",
    "cotg": "cot",
    "sec": "sec",
    "csc": "csc",
    "cosec": "csc",
    "arcsin": "asin",
    "arccos": "acos",
    "arctan": "atan",
    "arctg": "atan",
    "sinh": "sinh",
    "cosh": "cosh",
    "tanh": "tanh",
    "sh": "sinh",
    "ch": "cosh",
    "th": "tanh",
    "tgh": "tanh",
    "arcsinh": "asinh",
    "arccosh": "acosh",
    "arctanh": "atanh",
    "argsh": "asinh",
    "argch": "acosh",
    "argth": "atanh",
    "ln": "log",
    "log": "log",
    "exp": "exp",
    "sign": "sign",
    "sgn": "sign",
}
_SP_FUNCS = {name: getattr(sp, name) for name in set(_FUNC_ALIASES.values())}
_INVERSE = {"sin": "asin", "cos": "acos", "tan": "atan", "sinh": "asinh", "cosh": "acosh", "tanh": "atanh"}
_GREEK = {
    "alpha",
    "beta",
    "gamma",
    "delta",
    "epsilon",
    "varepsilon",
    "zeta",
    "eta",
    "theta",
    "vartheta",
    "iota",
    "kappa",
    "lambda",
    "mu",
    "nu",
    "xi",
    "rho",
    "varrho",
    "sigma",
    "tau",
    "upsilon",
    "phi",
    "varphi",
    "chi",
    "psi",
    "omega",
    "Gamma",
    "Delta",
    "Theta",
    "Lambda",
    "Xi",
    "Sigma",
    "Upsilon",
    "Phi",
    "Psi",
    "Omega",
}
# Single names that are read as functions when followed by "(": f(x,y), g(t), varphi(x,y), P_2(x), h_1(x)...
_FUNC_LETTERS = set("fghuvwFGHPQTLR") | {"varphi", "phi", "psi", "gamma", "sigma", "Phi", "Psi", "alpha", "beta"}

_DROP = re.compile(
    r"\\(?:left|right)(?:\.|\\[{}|]|\\[lr]?[vV]ert|\\langle|\\rangle|\\lfloor|\\rfloor|\\lceil|\\rceil)?"
    r"|\\[bB]ig{1,2}[lrm]?(?![A-Za-z])|\\[bB]igg[lrm]?(?![A-Za-z])"
    r"|\\(?:displaystyle|textstyle|limits|nolimits)(?![A-Za-z])|(?<!\\)\\[,;:!> ]|~"
)
_WRAPPERS = re.compile(r"\\(?:mathbf|boldsymbol|bm|vec|mathit|mathsf|mathnormal|bar|hat|tilde|overline|underline)\s*")
_NAMED = re.compile(r"\\(?:operatorname\*?|mathrm|text|textrm|textnormal|mbox|textit|textbf)\s*\{([^{}]*)\}")


def _named(m: re.Match) -> str:
    name = m.group(1).strip()
    if name in _FUNC_ALIASES:
        return "\\" + name + " "
    if len(name) == 1 and name.isalpha():  # \mathrm{e}, \mathrm{d}
        return name
    return r" \quad "  # prose inside math ("\text{ si }"): a separator


@lru_cache(maxsize=8192)
def _normalise(latex: str) -> str:
    s = latex
    for k, v in _UNICODE.items():
        s = s.replace(k, v)
    s = s.replace("{,}", ".")
    s = _NAMED.sub(_named, s)
    s = _DROP.sub(" ", s)
    s = re.sub(r"\\[dt]frac(?![A-Za-z])", r"\\frac", s)
    s = re.sub(r"\\(?:cdot|times|ast)(?![A-Za-z])", "*", s)
    s = re.sub(r"\\div(?![A-Za-z])", "/", s)
    s = re.sub(r"\\(?:lvert|rvert|vert)(?![A-Za-z])", "|", s)
    s = re.sub(r"\\(?:leqslant|leq)(?![A-Za-z])", r"\\le", s)
    s = re.sub(r"\\(?:geqslant|geq)(?![A-Za-z])", r"\\ge", s)
    s = re.sub(r"\\ne(?![A-Za-z])", r"\\neq", s)
    s = re.sub(r"\\(?:dfrac|tfrac)", r"\\frac", s)
    s = _WRAPPERS.sub("", s)
    s = re.sub(r"\\(?:qquad|quad)(?![A-Za-z])", r" \\quad ", s)
    return s.strip().rstrip(".,;")


# ---------------------------------------------------------------- splitting into sides

_REL_CMDS = (
    "neq|le|ge|lt|gt|approx|sim|simeq|equiv|cong|to|rightarrow|longrightarrow|Rightarrow|Longrightarrow|implies|"
    "iff|Leftrightarrow|Longleftrightarrow|Leftarrow|impliedby|mapsto|in|notin|ni|subset|subseteq|subsetneq|"
    "supset|supseteq|quad|colon|mid|forall|exists|land|lor|wedge|vee|text|cup|cap|setminus|bigcup|bigcap"
)
# Set braces \{ \} also separate: "\{(x,y) \mid x^2+|y|=5\}" exposes x^2+|y| and 5.
_SPLIT = re.compile(r"\\(?:" + _REL_CMDS + r")(?![A-Za-z])|:=|=|<|>|,|;|&|\\\\|\\\{|\\\}")
_OPEN, _CLOSE = "({[", ")}]"


def _top_level_split(s: str, seps: list[str] | None = None) -> list[str]:
    """Split on relations / separators outside any bracket or environment (those between parts go to `seps`)."""
    parts = _split_parts(s)
    if seps is not None:
        seps += [nxt for _, _, nxt in parts[:-1]]
    return [p for p, _, _ in parts]


def _split_parts(s: str) -> list[tuple[str, str | None, str | None]]:
    """Top-level parts with the separator before and after each one: [(part, previous, next)]."""
    raw: list[tuple[str, str | None]] = []  # (part, separator that ends it)
    start, depth, i = 0, 0, 0
    while i < len(s):
        if s.startswith(r"\begin", i):
            depth += 1
            i += 6
            continue
        if s.startswith(r"\end", i):
            depth = max(0, depth - 1)
            i += 4
            continue
        c = s[i]
        if c == "\\" and i + 1 < len(s) and s[i + 1] in "{}" and depth > 0:
            i += 2  # a set inside brackets: no split, no depth change
            continue
        if c in _OPEN:
            depth += 1
        elif c in _CLOSE:
            depth = max(0, depth - 1)
        elif depth == 0:
            m = _SPLIT.match(s, i)
            if m:
                raw.append((s[start:i].strip(), m.group(0)))
                start = i = m.end()
                continue
        i += 1
    raw.append((s[start:].strip(), None))
    out: list[tuple[str, str | None, str | None]] = []
    prev: str | None = None
    for part, sep in raw:
        if part:
            out.append((part, prev, sep))
            prev = sep
        elif sep is not None:
            prev = sep
    return out


_SOFT = {",", ";", "&", "\\\\", r"\quad", r"\text", r"\{", r"\}"}  # list separators, not relations


def _expand_pm(side: str) -> list[str]:
    if not re.search(r"\\(?:pm|mp)(?![A-Za-z])", side):
        return [side]
    plus = re.sub(r"\\mp(?![A-Za-z])", "-", re.sub(r"\\pm(?![A-Za-z])", "+", side))
    minus = re.sub(r"\\mp(?![A-Za-z])", "+", re.sub(r"\\pm(?![A-Za-z])", "-", side))
    return [plus, minus]


@lru_cache(maxsize=8192)
def _sides(segment: str, values_only: bool = False) -> tuple[str, ...]:
    out: list[str] = []
    for part, prev, nxt in _split_parts(_normalise(segment)):
        # The first side of an equation chain names a quantity ("e^{\sin y} = 1+y+...", "f_x = ..."): it is the
        # right-hand sides that carry the values.
        if values_only and nxt in ("=", ":=") and (prev is None or prev in _SOFT):
            continue
        out += _expand_pm(part)
    return tuple(dict.fromkeys(out))


def sides(segment: str, values_only: bool = False) -> list[str]:
    """Comparable pieces of one math segment ("A = B \\le C" -> [A, B, C]), normalised.

    With `values_only`, the first side of each equation chain ("A" in "A = B = C") is left out."""
    return list(_sides(segment, values_only))


# ---------------------------------------------------------------- tokenizer + parser

_TOKEN = re.compile(r"\\[A-Za-z]+|\\.|\d+\.\d+|\.\d+|\d+|[A-Za-z]|\S")
_ATOM_CMDS = {"pi", "infty", "frac", "sqrt", "begin", "det", "max", "min", "exp", "e"} | _GREEK | set(_FUNC_ALIASES)


class _Parser:
    def __init__(self, text: str):
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

    def parse(self):
        e = self.expr()
        if self.peek() is not None:
            raise _ParseError(f"trailing {self.peek()}")
        if e is LANDAU:
            raise _ParseError("only a remainder term")
        return e

    # -- grammar
    def expr(self):
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

    def term(self):
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

    def unary(self):
        if self.peek() == "-":
            self.take()
            u = self.unary()
            return u if u is LANDAU else -u
        if self.peek() == "+":
            self.take()
            return self.unary()
        return self.power()

    def power(self):
        base = self.postfix(self.atom())
        if self.peek() == "^":
            self.take()
            exp = self.script()
            if base is LANDAU:
                raise _ParseError("power of remainder")
            base = self.postfix(_pow(base, exp))
        return base

    def postfix(self, e):
        while self.peek() == "!":
            self.take()
            e = _factorial(e)
        return e

    def script(self):
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

    def group(self):
        self.expect("{")
        e = self.expr()
        self.expect("}")
        if e is LANDAU:
            raise _ParseError("remainder in group")
        return e

    def arg_group(self):
        """Argument of \\frac / \\sqrt: braced group or a single token (\\frac12)."""
        if self.peek() == "{":
            return self.group()
        t = self.peek()
        if t is not None and t[0].isdigit() and len(t) > 1 and "." not in t:
            self.toks[self.i] = t[1:]
            return sp.Integer(t[0])
        return self.atom()

    def call_args(self) -> list:
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

    def named(self, name: str):
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

    def function(self, name: str):
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

    def matrix(self):
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

    def atom(self):
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


def _det(m):
    if max(m.shape) > MAX_DET_SIZE:
        raise _ParseError("determinant too large")
    return m.det()


_LARK_OK = re.compile(r"^[^{}\\]*$")  # lark is only tried on plain text (never on \lim: notation, not a value)


def _lark(latex: str):
    try:
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


def _degenerate(e) -> bool:
    return isinstance(e, sp.Basic) and (e.has(sp.nan) or e.has(sp.zoo))  # 0/0, 1/0


@lru_cache(maxsize=8192)
def _parse_side(side: str):
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


def parse(latex: str):
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


# ---------------------------------------------------------------- numeric fingerprints and equivalence


@lru_cache(maxsize=4096)
def _value(name: str, k: int) -> complex:
    rng = random.Random(f"cas:{name}:{k}")
    if k < N_POINTS // 2:
        return rng.uniform(0.11, 0.57)  # small positive: inside sqrt(1-x^2-y^2), log(x), ...
    return rng.uniform(-1.9, 1.9)  # signed: separates |x| from x, x^2 from x^4 near 1, ...


def _opaque(e):
    """Undefined function applications become opaque symbols: f(x,y) is compared by name."""
    if e.has(AppliedUndef):
        e = e.replace(lambda a: isinstance(a, AppliedUndef), lambda a: sp.Symbol(f"__{a}"))
    return e


def _scalar_values(e) -> tuple | None:
    """Values of a scalar expression at the shared random points (None = point failed)."""
    e = _opaque(e)
    if not isinstance(e, sp.Expr):
        return None
    syms = sorted(e.free_symbols, key=lambda s: s.name)
    vals = []
    try:
        f = sp.lambdify(syms, e, modules="mpmath")
    except Exception:
        return None
    import mpmath

    for k in range(N_POINTS):
        try:
            v = complex(f(*[mpmath.mpf(_value(s.name, k)) for s in syms]))
            vals.append(v if v == v and abs(v) != float("inf") and abs(v) < 1e300 else None)
        except Exception:
            vals.append(None)
    return tuple(vals)


@lru_cache(maxsize=8192)
def _fingerprint(e):
    """(kind, shape, per-entry values); kind is 'expr', 'const', 'tuple' or 'matrix'."""
    if isinstance(e, sp.Tuple):
        return ("tuple", len(e), tuple(_fingerprint(x) for x in e))
    if isinstance(e, sp.MatrixBase):
        return ("matrix", e.shape, tuple(_fingerprint(x) for x in e))
    if not isinstance(e, sp.Expr):
        return None
    if not _opaque(e).free_symbols:
        try:
            v = complex(sp.N(e, 30))
        except Exception:
            return ("const", None, None)
        return ("const", None, v if v == v and abs(v) != float("inf") else None)
    return ("expr", None, _scalar_values(e))


def _close(u: complex, v: complex, tol: float = REL_TOL) -> bool:
    return abs(u - v) <= tol * max(1.0, abs(u), abs(v))


def _real(v: complex) -> bool:
    return abs(v.imag) <= 1e-12 * max(1.0, abs(v))


def _decimal_tolerance(e) -> float | None:
    """A decimal literal with >= 2 decimals may be a rounded value: half a unit in its last place."""
    if isinstance(e, sp.Rational) and not isinstance(e, sp.Integer):
        q = e.q
        d = 0
        while q % 10 == 0:
            q //= 10
            d += 1
        if q == 1 and d >= 2:
            return 0.5 * 10.0**-d * (1 + 1e-9)
    return None


def _compare(a, b, fa, fb) -> bool | None:
    if fa is None or fb is None:
        return None
    ka, kb = fa[0], fb[0]
    if ka in ("tuple", "matrix") or kb in ("tuple", "matrix"):
        if ka != kb or fa[1] != fb[1]:
            return False
        verdicts = [_compare(x, y, fx, fy) for x, y, fx, fy in zip(a, b, fa[2], fb[2], strict=False)]
        if any(v is False for v in verdicts):
            return False
        return None if any(v is None for v in verdicts) else True
    if ka == "const" and kb == "const":
        if fa[2] is None or fb[2] is None:
            return True if a == b else None  # oo == oo
        if _close(fa[2], fb[2], 1e-12):
            return True
        for x, other in ((a, fb[2]), (b, fa[2])):
            tol = _decimal_tolerance(x)
            if tol is not None and abs(complex(x) - other) <= tol and not isinstance((b if x is a else a), sp.Integer):
                return True
        return False
    va = fa[2] if ka == "expr" else (fa[2],) * N_POINTS if fa[2] is not None else None
    vb = fb[2] if kb == "expr" else (fb[2],) * N_POINTS if fb[2] is not None else None
    if va is None or vb is None:
        return None
    # Points outside the real domain of either side (complex value, pole, log of a negative) are skipped.
    pairs = [(u, v) for u, v in zip(va, vb, strict=False) if u is not None and v is not None and _real(u) and _real(v)]
    if len(pairs) < MIN_VALID_POINTS:
        return None
    return all(_close(u, v) for u, v in pairs)


def _as_expr(x):
    if isinstance(x, str):
        return parse(x)
    if isinstance(x, (int, float)):
        return sp.nsimplify(x) if isinstance(x, float) else sp.Integer(x)
    return x


def equivalent(a, b) -> bool | None:
    """Are two formulas (LaTeX strings or sympy objects) mathematically equal? None when undecidable."""
    try:
        ea, eb = _as_expr(a), _as_expr(b)
        if ea is None or eb is None:
            return None
        if ea == eb:
            return True
        if isinstance(ea, sp.core.relational.Relational) or isinstance(eb, sp.core.relational.Relational):
            if type(ea) is not type(eb):
                return (
                    None
                    if not (
                        isinstance(ea, sp.core.relational.Relational) and isinstance(eb, sp.core.relational.Relational)
                    )
                    else False
                )
            direct = [equivalent(ea.lhs, eb.lhs), equivalent(ea.rhs, eb.rhs)]
            if all(direct):
                return True
            if isinstance(ea, (sp.Eq, sp.Ne)):
                swapped = [equivalent(ea.lhs, eb.rhs), equivalent(ea.rhs, eb.lhs)]
                if all(swapped):
                    return True
            return None if None in direct else False
        return _compare(ea, eb, _fingerprint(ea), _fingerprint(eb))
    except Exception:
        return None


# ---------------------------------------------------------------- leak check


def is_trivial(e) -> bool:
    """Never a leak by itself: single symbols, small integers (|n| <= 2) and their negatives, and notation that
    names a quantity instead of giving it (anything with an undefined function: f(0,0), D_uf(0,0), |f(x,y)|)."""
    if e is None:
        return True
    if isinstance(e, sp.Basic) and e.has(AppliedUndef):
        return True
    if isinstance(e, sp.Mul) and len(e.args) == 2 and e.args[0] == -1:
        e = e.args[1]
    if isinstance(e, sp.Abs):  # |x|, |R_3|
        e = e.args[0]
    if isinstance(e, sp.Symbol) or e in (sp.oo, -sp.oo):  # "x \to \pm\infty": a limit point, not a value
        return True
    if isinstance(e, sp.Integer):
        return abs(int(e)) <= 2
    if isinstance(e, sp.Tuple):  # a tuple with an infinite end is an interval, (0,+\infty): not checked
        return any(x in (sp.oo, -sp.oo) for x in e) or all(is_trivial(x) for x in e)
    return _is_set_notation(e)


def _is_set_notation(e) -> bool:
    """A bare product / power of symbols involving a capital letter: A^c, yA, OZ, D\\varphi, A^TA. In these
    sheets capitals name sets, matrices, axes and operators, so such a product is notation, not a value."""
    if not isinstance(e, (sp.Mul, sp.Pow)) or any(a.is_Number for a in e.atoms(sp.Number) if abs(a) != 1):
        return False
    if e.atoms(sp.Function) or not all(isinstance(a, sp.Symbol) for a in e.atoms() if not a.is_Number):
        return False
    return any(s.name[:1].isupper() and s.name[:1].isascii() for s in e.free_symbols)


def _checkable(e) -> bool:
    return e is not None and isinstance(e, (sp.Expr, sp.Tuple, sp.MatrixBase)) and not is_trivial(e)


@lru_cache(maxsize=4096)
def _candidates(text: str, prose: bool = False, values_only: bool = False) -> tuple[tuple[str, object, object], ...]:
    """Non-trivial parsed sides of every formula in a text: (side text, expr, fingerprint). With `prose`, the
    equations written in the prose without delimiters too."""
    segs = formulas(text) + (prose_formulas(text) if prose else [])
    out = []
    for seg in segs:
        for side in _sides(seg, values_only):
            e = _parse_side(side)
            if not _checkable(e):
                continue
            fp = _fingerprint(e)
            if fp is not None:
                out.append((side, e, fp))
    return tuple(out)


def checkable(text: str, values_only: bool = True) -> list[str]:
    """Sides of a text's formulas that the checker can compare (parsed, non-trivial). With `values_only`
    (how forbidden texts are read), the first side of each equation chain is left out."""
    return [side for side, _, _ in _candidates(text or "", False, values_only)]


MAX_SUBEXPRESSIONS = 300


def _subexpressions(e) -> list:
    """Every subtree of e, plus partial sums / products of small Add / Mul nodes (x+y inside 1+x+y)."""
    from itertools import combinations

    out = []
    for node in sp.preorder_traversal(e):
        if not isinstance(node, sp.Expr) or node is e:
            continue
        out.append(node)
        if isinstance(node, (sp.Add, sp.Mul)) and 3 <= len(node.args) <= 6:
            for k in range(2, len(node.args)):
                out += [node.func(*c) for c in combinations(node.args, k)]
    if isinstance(e, (sp.Add, sp.Mul)) and 3 <= len(e.args) <= 6:
        for k in range(2, len(e.args)):
            out += [e.func(*c) for c in combinations(e.args, k)]
    return out


def _fragments(side: str) -> list[str]:
    """Bracketed pieces of an unparseable side: "(...)" with its parentheses, "{...}" without its braces.
    "\\lim_{(x,y)\\to(0,0)}\\frac{x^4y^4}{\\sqrt{x^2+y^2}}" still permits x^4y^4 and \\sqrt{x^2+y^2}."""
    out, stack = [], []
    for i, c in enumerate(side):
        if c in "({" and not (c == "{" and i and side[i - 1] == "\\"):
            stack.append((c, i))
        elif c in ")}" and stack:
            o, j = stack.pop()
            if (o, c) == ("(", ")"):
                out.append(side[j : i + 1])
            elif (o, c) == ("{", "}"):
                out.append(side[j + 1 : i])
    return out


@lru_cache(maxsize=2048)
def _permitted(text: str) -> tuple[tuple[str, object, object], ...]:
    """Permitted pool of a text: its formulas, their subexpressions (design 6.3 (b)), and the bracketed
    fragments of formulas that do not parse as a whole (limits, notation such as DG^{-1}(4,4,-1))."""
    segs = (formulas(text) or ([text.strip()] if text and text.strip() else [])) + prose_formulas(text)
    roots: list[tuple[str, object]] = []
    for seg in segs:
        for side in _sides(seg):
            e = _parse_side(side)
            if e is not None:
                roots.append((side, e))
                continue
            for frag in _fragments(side):
                for piece in _top_level_split(frag):
                    pe = _parse_side(piece)
                    if pe is not None:
                        roots.append((piece, pe))
    out: list[tuple[str, object, object]] = []
    seen: set = set()

    def add(label: str, e) -> None:
        if e in seen or not _checkable(e) or len(out) >= MAX_SUBEXPRESSIONS:
            return
        seen.add(e)
        fp = _fingerprint(e)
        if fp is not None:
            out.append((label, e, fp))

    for side, e in roots:
        add(side, e)
    for side, e in roots:
        if isinstance(e, (sp.Expr, sp.Tuple)):
            for sub in _subexpressions(e):
                add(f"{side} > {sub}", sub)
    return tuple(out)


_CELL = re.compile(r"&|\\\\|\\quad(?![A-Za-z])")
_ENV = re.compile(r"\\(?:begin|end)\{[A-Za-z]*\*?\}")


def literal_tokens(text: str) -> set[str]:
    """The whole pieces of a text's formulas, normalised: each formula, its sides, the cells of its environments
    (cases, aligned, matrices), and the relation-separated pieces of each bracket or |...| group. A text without
    $...$ counts as one formula. "x-2y" is not a piece of "x-2y-z = 0"; "(x-2)^2+y^2" is one of
    "F(\\{(x,y) \\mid (x-2)^2+y^2 \\le 1\\})"."""
    segs = (formulas(text) or ([text.strip()] if text and text.strip() else [])) + prose_formulas(text)
    out: set[str] = set()
    for seg in segs:
        norm = _normalise(seg)
        out.add(norm)
        pieces = [*_top_level_split(norm), *_CELL.split(_ENV.sub(" ", norm))]
        groups = [g for f in _fragments(norm) for g in ([f, f[1:-1]] if f.startswith("(") else [f])]
        groups += [m.group(0) for m in re.finditer(r"\|[^|]+\|", norm)]
        for group in groups:
            pieces.append(group)
            pieces += _top_level_split(group)
        for piece in pieces:
            out.update(p.strip() for p in [piece, *_CELL.split(piece)] if p.strip())
    return out


def _negated(fp):
    if fp is None or fp[0] in ("tuple", "matrix"):
        return None
    if fp[0] == "const":
        return ("const", None, None if fp[2] is None else -fp[2])
    return ("expr", None, None if fp[2] is None else tuple(None if v is None else -v for v in fp[2]))


def _matches_permitted(e, fp, perm) -> bool:
    """Equal to a permitted formula or subexpression, up to sign (x-y is fine when y-x is permitted)."""
    for _, pe, pfp in perm:
        if e == pe or _compare(e, pe, fp, pfp):
            return True
        nfp = _negated(pfp)
        if nfp is not None and isinstance(pe, sp.Expr) and _compare(e, -pe, fp, nfp):
            return True
    return False


def explain(draft: str, forbidden: list[str], allowed: list[str]) -> list[tuple[str, str]]:
    """Like `leaked`, but each hit comes with the forbidden formula it matches: [(draft side, forbidden side)].

    The draft's equations written without $...$ are checked too. An unexpected error propagates: "no leak" and
    "not checked" must stay distinguishable, so the caller can fail closed."""
    draft_c = _candidates(draft or "", True)
    if not draft_c:
        return []
    forb = [c for t in forbidden for c in _candidates(t or "", False, True)]
    if not forb:
        return []
    perm = [c for t in allowed for c in _permitted(t or "")]
    hits: list[tuple[str, str]] = []
    done: set[str] = set()
    for side, e, fp in draft_c:
        if side in done:
            continue
        done.add(side)
        match = next((fs for fs, fe, ffp in forb if e == fe or _compare(e, fe, fp, ffp)), None)
        if match is None or _matches_permitted(e, fp, perm):
            continue
        hits.append((side, match))
    return hits


def leaked(draft: str, forbidden: list[str], allowed: list[str]) -> list[str]:
    """Draft formulas (or sides of them) equivalent to a forbidden formula and to no permitted one.

    `forbidden` / `allowed` are raw texts (step details, result value, allowed content, student messages);
    their formulas are extracted. A permitted formula also permits its subexpressions, and a permitted text
    without any $...$ is read as one formula (a student message typed without delimiters).
    """
    return [side for side, _ in explain(draft, forbidden, allowed)]
