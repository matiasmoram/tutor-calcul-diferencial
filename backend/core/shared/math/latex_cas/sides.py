"""Splitting a math segment into its comparable sides at top-level relations and separators."""

import re
from functools import lru_cache

from core.shared.math.latex_cas.normalise import _normalise

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
