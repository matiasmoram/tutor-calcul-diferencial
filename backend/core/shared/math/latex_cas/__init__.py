"""Math-provenance leak check with a CAS.

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

from core.shared.math.latex_cas.equivalence import equivalent
from core.shared.math.latex_cas.extraction import formulas, prose_formulas
from core.shared.math.latex_cas.leaks import checkable, explain, is_trivial, leaked, literal_tokens
from core.shared.math.latex_cas.parser import _parse_side as _parse_side  # scripts/check_cas.py parses one side
from core.shared.math.latex_cas.parser import parse
from core.shared.math.latex_cas.sides import sides

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
