"""LaTeX normalisation (Unicode symbols, spacing and notation that carries no value), and the function and Greek
names the parser shares."""

import re
from functools import lru_cache

import sympy as sp

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


def _named(m: re.Match[str]) -> str:
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
