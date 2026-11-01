"""Finding the formulas of a text: delimited math segments, and equations written in the prose."""

import re
from functools import lru_cache

from core.shared.math.latex_cas.normalise import _FUNC_ALIASES

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
