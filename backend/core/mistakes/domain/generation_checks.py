"""Code gates on a generated document (Catalan messages: they go back to the generator as rejection reasons).

1. VALIDATION   error count, one error per fragment, quotes located in their fragment, balanced $...$ so KaTeX
                renders; for theory, statement/proof split and at least one error in the statement.
2. VERIFICATION an independent pass that never sees the declared errors lists every error it finds; code then
                requires that every declared error is found and nothing else is wrong."""

import re

from pydantic import BaseModel

from core.mistakes.domain.entities.mistake_exercise import DeclaredMistake
from core.mistakes.domain.locate import locate, overlap
from core.mistakes.domain.values.llm_outputs import GenerationDraft, VerifierFinding
from core.mistakes.domain.values.mistake_kind import PROBLEM_MISTAKE_KINDS, THEORY_MISTAKE_KINDS


class GenerationCheck(BaseModel):
    fragments: list[str]
    mistakes: list[DeclaredMistake]
    statement_fragments: int
    problems: list[str]  # empty: valid

    @property
    def valid(self) -> bool:
        return not self.problems


def validate_generation(draft: GenerationDraft, n: int, theory: bool = False) -> GenerationCheck:
    fragments = [f.strip() for f in draft.fragments if f.strip()]
    problems: list[str] = []
    if not 4 <= len(fragments) <= 14:
        problems.append(f"el nombre de fragments ha de ser entre 5 i 10 (n'hi ha {len(fragments)})")
    for i, f in enumerate(fragments, 1):
        if len(re.findall(r"(?<!\\)\$", f)) % 2:
            problems.append(f"el fragment {i} té un nombre senar de '$' (LaTeX mal tancat)")
        if "$$" in f:
            problems.append(f"el fragment {i} fa servir $$...$$; cal $...$")
    n_statement = draft.statement_fragments if theory else 0
    if theory and (not isinstance(n_statement, int) or not 1 <= n_statement <= 3 or n_statement > len(fragments) - 3):
        problems.append(
            f"n_enunciat ha de ser entre 1 i 3 i deixar com a mínim 3 fragments de demostració (n_enunciat={n_statement})"
        )
    raw = draft.mistakes
    if len(raw) != n:
        problems.append(f"calen exactament {n} errors (n'hi ha {len(raw)})")
    valid_kinds = THEORY_MISTAKE_KINDS if theory else PROBLEM_MISTAKE_KINDS
    mistakes: list[DeclaredMistake] = []
    used: set[int] = set()
    for k, e in enumerate(raw, 1):
        fi = e.fragment
        if not isinstance(fi, int) or not 1 <= fi <= len(fragments):
            problems.append(f"l'error {k} apunta a un fragment inexistent ({fi})")
            continue
        if fi in used:
            problems.append(f"hi ha dos errors al fragment {fi}; han de ser en fragments diferents")
        used.add(fi)
        if e.kind not in valid_kinds:
            problems.append(f"l'error {k} té un tipus no vàlid ({e.kind}); tipus vàlids: {', '.join(valid_kinds)}")
        for field, value in (("explicacio", e.explanation), ("correccio", e.correction), ("pista", e.hint)):
            if not value.strip():
                problems.append(f"l'error {k} no té '{field}'")
        pos = locate(fragments[fi - 1], e.quote)
        if pos is None:
            problems.append(f"la cita de l'error {k} no apareix literalment al fragment {fi}: «{e.quote}»")
            continue
        mistakes.append(
            DeclaredMistake(
                id=f"e{k}",
                fragment=fi,
                quote=fragments[fi - 1][pos[0] : pos[1]],
                start=pos[0],
                end=pos[1],
                kind=e.kind if e.kind is not None else "logica",
                explanation=e.explanation,
                correction=e.correction,
                hint=e.hint,
            )
        )
    if theory and isinstance(n_statement, int) and n_statement >= 1 and raw:
        frags = [e.fragment for e in raw if isinstance(e.fragment, int)]
        if not any(f <= n_statement for f in frags):
            problems.append("cal com a mínim un error a l'enunciat (els primers n_enunciat fragments)")
        if n >= 2 and not any(f > n_statement for f in frags):
            problems.append("amb 2 o més errors, com a mínim un ha de ser a la demostració")
    return GenerationCheck(
        fragments=fragments,
        mistakes=mistakes,
        statement_fragments=n_statement if isinstance(n_statement, int) else 0,
        problems=problems,
    )


def compare_verification(
    mistakes: list[DeclaredMistake], findings: list[VerifierFinding], fragments: list[str] | None = None
) -> list[str]:
    """The independent check must find every declared error and nothing else that is wrong."""
    issues: list[str] = []
    real = [p for p in findings if p.severity in ("error", "consequencia")]
    declared = {e.fragment for e in mistakes}

    def same_problem(e: DeclaredMistake, p: VerifierFinding) -> bool:
        # A different problem in the same fragment does not confirm the declared one: the quotes must overlap
        # (fragment-only matching when the verifier gives no locatable quote).
        if p.fragment != e.fragment:
            return False
        quote = (p.quote or "").strip()
        if not quote:
            return True
        span = locate(fragments[e.fragment - 1], quote) if fragments else None
        return span is None or overlap(span[0], span[1], e.start, e.end)

    for e in mistakes:
        if not any(same_problem(e, p) for p in real):
            issues.append(
                f"l'error declarat al fragment {e.fragment} («{e.quote}») no l'ha detectat el verificador: "
                "potser no és un error real o és ambigu"
            )
    for p in findings:
        if p.severity == "error" and p.fragment not in declared:
            issues.append(f"hi ha un error NO intencionat al fragment {p.fragment}: «{p.quote}» — {p.explanation}")
    return issues
