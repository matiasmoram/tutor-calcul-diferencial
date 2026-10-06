"""Output checks before a message reaches the student.

Two layers:
1. Deterministic: forbidden regexes from the sheet, a required closing question, length.
2. LLM judge with the full solution, which checks the plan was respected.
"""

from __future__ import annotations

import re

from . import cas
from .politica import Pla

_DISPLAY = re.compile(r"\$\$.*?\$\$", re.DOTALL)
_MATH = re.compile(r"\$[^$]*\$")
_NOT_ENDS = re.compile(r"\b(p\. ?ex|etc|vs|cf|pàg|núm)\.|^\s*\d+\.\s", re.IGNORECASE | re.MULTILINE)
_SENTENCE_END = re.compile(r"[.!?…]+(\s|$)")


def _compact(text: str) -> str:
    return re.sub(r"\s+|\\[,;!: ]|\\left|\\right", "", text).replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac")


def count_sentences(text: str) -> int:
    prose = _NOT_ENDS.sub("X", _MATH.sub("X", _DISPLAY.sub("X", text))).strip()
    return max(1, len(_SENTENCE_END.findall(prose))) if prose else 0


def deterministic_check(missatge: str, pla: Pla, permeses: list[str] = ()) -> list[str]:
    """`permeses`: texts the reply may draw formulas from (allowed content, statement, theory, student's words)."""
    problems: list[str] = []
    if not missatge.strip():
        return ["missatge buit"]
    for pattern in pla.regex_prohibides:
        m = re.search(pattern, missatge, flags=re.IGNORECASE | re.MULTILINE)
        if m:
            problems.append(f"conté contingut prohibit: «{m.group(0)}» (patró {pattern})")
    # Formulas equivalent to forbidden content, whatever the notation ("\\frac14" vs "0.25"): regexes only see spelling.
    literal = [_compact(t) for t in permeses]
    for side, forbidden in cas.explain(missatge, pla.textos_prohibits, list(permeses)) if pla.textos_prohibits else []:
        # A formula copied literally from allowed text (e.g. an integrand sympy cannot read) is never a leak.
        if not any(_compact(side) in t for t in literal):
            problems.append(f"fórmula que revela contingut no permès: «{side}» (equival a «{forbidden}»)")
    if pla.requereix_pregunta and "?" not in missatge:
        problems.append("el pla requereix acabar amb una pregunta i no n'hi ha cap")
    n = count_sentences(missatge)
    if n > pla.max_frases + 1:
        problems.append(f"massa llarg: {n} frases (màxim {pla.max_frases})")
    return problems
