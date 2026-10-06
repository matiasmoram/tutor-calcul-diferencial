"""Deterministic checks of a draft reply before it reaches the student (the LLM judge comes after them).

The problems are Catalan: they are fed back to the writer as the reason a draft was rejected."""

import re
from collections.abc import Sequence

from core.shared.math.latex_cas import explain
from core.tutoring.domain.values.plan import Plan

_DISPLAY = re.compile(r"\$\$.*?\$\$", re.DOTALL)
_MATH = re.compile(r"\$[^$]*\$")
_NOT_ENDS = re.compile(r"\b(p\. ?ex|etc|vs|cf|pàg|núm)\.|^\s*\d+\.\s", re.IGNORECASE | re.MULTILINE)
_SENTENCE_END = re.compile(r"[.!?…]+(\s|$)")


def _compact(text: str) -> str:
    return re.sub(r"\s+|\\[,;!: ]|\\left|\\right", "", text).replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac")


def count_sentences(text: str) -> int:
    prose = _NOT_ENDS.sub("X", _MATH.sub("X", _DISPLAY.sub("X", text))).strip()
    return max(1, len(_SENTENCE_END.findall(prose))) if prose else 0


def deterministic_check(message: str, plan: Plan, permitted: Sequence[str] = ()) -> list[str]:
    """`permitted`: texts the reply may draw formulas from (allowed content, statement, theory, student's words)."""
    problems: list[str] = []
    if not message.strip():
        return ["missatge buit"]
    for pattern in plan.forbidden_patterns:
        m = re.search(pattern, message, flags=re.IGNORECASE | re.MULTILINE)
        if m:
            problems.append(f"conté contingut prohibit: «{m.group(0)}» (patró {pattern})")
    # Formulas equivalent to forbidden content, whatever the notation ("\\frac14" vs "0.25"): regexes only see spelling.
    literal = [_compact(t) for t in permitted]
    hits = explain(message, plan.forbidden_texts, list(permitted)) if plan.forbidden_texts else []
    for side, forbidden in hits:
        # A formula copied literally from allowed text (e.g. an integrand sympy cannot read) is never a leak.
        if not any(_compact(side) in t for t in literal):
            problems.append(f"fórmula que revela contingut no permès: «{side}» (equival a «{forbidden}»)")
    if plan.requires_question and "?" not in message:
        problems.append("el pla requereix acabar amb una pregunta i no n'hi ha cap")
    n = count_sentences(message)
    if n > plan.max_sentences + 1:
        problems.append(f"massa llarg: {n} frases (màxim {plan.max_sentences})")
    return problems
