"""Code checks of the generated statements: structure, LaTeX, neutral hints, existing citations, sympy results."""

import re
import unicodedata
from collections.abc import Collection, Sequence

from core.quizzes.domain.values.drafts import StatementDraft
from core.shared.math.latex_vocabulary import unknown_commands
from core.shared.math.sympy_checks import CheckResult, MathCheck

# A hint that names the verdict or the tool gives the answer away.
_REVEALS_VERDICT = re.compile(r"\b(cert[ae]?|fals[ae]?|contraexemples?|falsedat|veritat)\b", re.IGNORECASE)
MAX_CHECKS = 6


def normal_key(text: str) -> str:
    """Duplicate detection key: accents, case, spacing and punctuation ignored."""
    text = unicodedata.normalize("NFKD", text.lower())
    return re.sub(r"[^a-z0-9]+", "", text)


def dollars_balanced(text: str) -> bool:
    return len(re.findall(r"(?<!\\)\$", text)) % 2 == 0 and "$$" not in text


def validate_draft(d: StatementDraft, refs: Collection[str]) -> list[str]:
    """Problems of one generated statement (structure only; the sympy checks run separately)."""
    problems: list[str] = []
    if d.verdict not in ("cert", "fals"):
        problems.append("veredicte no vàlid")
    for name, value in (
        ("enunciat", d.statement),
        ("resolucio", d.solution),
        ("pista", d.hint),
        ("concepte", d.concept),
    ):
        if not value.strip():
            problems.append(f"falta '{name}'")
    if d.verdict == "fals" and not d.counterexample.strip():
        problems.append("és falsa però no dona el contraexemple")
    ideas = [i for i in d.key_ideas if i.strip()]
    if not 1 <= len(ideas) <= 4:
        problems.append("cal entre 1 i 4 idees clau")
    for name, value in (
        ("enunciat", d.statement),
        ("contraexemple", d.counterexample),
        ("resolucio", d.solution),
        ("pista", d.hint),
        ("concepte", d.concept),
    ):
        if not dollars_balanced(value):
            problems.append(f"'{name}' té el LaTeX mal tancat o fa servir $$")
        if unknown := unknown_commands(value):
            problems.append(f"'{name}' fa servir ordres LaTeX que no existeixen: {', '.join(sorted(unknown))}")
    if _REVEALS_VERDICT.search(d.hint):
        problems.append("la pista revela el veredicte (no pot dir cert/fals/contraexemple)")
    if _REVEALS_VERDICT.search(d.concept):
        problems.append("el concepte revela el veredicte")
    bad = [r for r in d.theory if r not in refs]
    if bad:
        problems.append(f"cita ítems inexistents: {', '.join(bad)}")
    if len(d.checks) > MAX_CHECKS:
        problems.append("massa comprovacions (màxim 4)")
    return problems


def all_checks(drafts: Sequence[StatementDraft]) -> list[MathCheck]:
    """Every draft's checks in one flat batch, for a single sympy evaluation."""
    return [c for d in drafts for c in d.checks]


def with_results(drafts: Sequence[StatementDraft], results: Sequence[CheckResult]) -> list[StatementDraft]:
    """The drafts with the results of `all_checks(drafts)` attached, in the same order."""
    pending = iter(results)
    return [d.model_copy(update={"checks": [c.with_result(next(pending)) for c in d.checks]}) for d in drafts]


def check_problems(d: StatementDraft) -> list[str]:
    return [
        f"la comprovació «{c.description}» ({c.kind}: {c.expression}"
        f"{' → ' + c.value if c.value else ''}) és FALSA segons sympy"
        f"{': dona ' + c.computed if c.computed else ''}{' (' + c.detail + ')' if c.detail else ''}"
        for c in d.checks
        if c.failed
    ]
