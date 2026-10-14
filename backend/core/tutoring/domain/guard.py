"""Deterministic checks of a draft reply before it reaches the student (the LLM judge comes after them).

The problems are Catalan: they are fed back to the writer as the reason a draft was rejected."""

import re
from collections.abc import Sequence

from core.course.domain.citations import CITATION
from core.course.domain.entities.theory_item import KIND_NAMES, TheoryItem
from core.shared.math.latex_cas import explain, literal_tokens
from core.shared.math.latex_vocabulary import unknown_commands
from core.tutoring.domain.values.plan import Plan

_DISPLAY = re.compile(r"\$\$.*?\$\$", re.DOTALL)
_MATH = re.compile(r"\$[^$]*\$")
_NOT_ENDS = re.compile(r"\b(p\. ?ex|etc|vs|cf|pàg|núm)\.|^\s*\d+\.\s", re.IGNORECASE | re.MULTILINE)
_SENTENCE_END = re.compile(r"[.!?…]+(\s|$)")
CAS_ERROR_PROBLEM = "comprovació CAS: error intern"


def _compact(text: str) -> str:
    return re.sub(r"\s+|\\[,;!: ]|\\left|\\right", "", text).replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac")


def _literal_sides(texts: Sequence[str]) -> set[str]:
    """The whole formula pieces of the permitted texts, compacted. A draft side is only whitelisted by spelling when
    it is one of them, never a substring of one: "x-2y" must not pass because "x-2y-z" is permitted."""
    return {_compact(token) for text in texts for token in literal_tokens(text)}


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
    if plan.forbidden_texts:
        try:
            hits = explain(message, plan.forbidden_texts, list(permitted))
        except Exception:
            # Fail closed, like a timeout: a draft the CAS could not verify never reaches the student.
            hits = []
            problems.append(CAS_ERROR_PROBLEM)
        literal = _literal_sides(permitted) if hits else set()
        for side, forbidden in hits:
            # A formula copied literally from allowed text (e.g. an integrand sympy cannot read) is never a leak.
            if _compact(side) not in literal:
                problems.append(f"fórmula que revela contingut no permès: «{side}» (equival a «{forbidden}»)")
    unknown = unknown_commands(message)
    if unknown:
        names = ", ".join(f"\\{c}" for c in sorted(unknown))
        problems.append(f"ordres LaTeX que no existeixen (KaTeX les mostraria com a error): {names}")
    if plan.requires_question and "?" not in message:
        problems.append("el pla requereix acabar amb una pregunta i no n'hi ha cap")
    n = count_sentences(message)
    if n > plan.max_sentences + 1:
        problems.append(f"massa llarg: {n} frases (màxim {plan.max_sentences})")
    return problems


def citation_problems(
    message: str, theory: Sequence[TheoryItem], topic: int | None, permitted: Sequence[str] = ()
) -> list[str]:
    """Citations of theory items outside the allowed set (a reserved item can name the whole strategy).

    A citation is fine when it names an allowed item or when a permitted text (allowed content, statement) cites
    the same item. A citation without a topic refers to `topic`, as the web's linker reads it."""

    def keys(text: str) -> list[tuple[tuple[str, int, int], str]]:
        return [
            ((m.group(1), int(m.group(3) or m.group(4) or (topic or 0)), int(m.group(2))), m.group(0))
            for m in CITATION.finditer(text)
        ]

    allowed = {(KIND_NAMES[it.kind], it.topic, it.number) for it in theory if it.number is not None}
    allowed |= {key for text in permitted for key, _ in keys(text)}
    bad = list(dict.fromkeys(cited for key, cited in keys(message) if key not in allowed))
    return [f"cita teoria que no és a la llista permesa: «{c}»" for c in bad]
