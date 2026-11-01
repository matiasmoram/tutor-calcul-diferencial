"""Code gates on a generated document (Catalan messages: they go back to the generator as rejection reasons).

1. VALIDATION   error count, one error per fragment, quotes located in their fragment, balanced $...$ so KaTeX
                renders, no LaTeX command outside the known vocabulary; for theory, statement/proof split and at least one error in the statement.
2. VERIFICATION an independent pass that never sees the declared errors lists every error it finds; code then
                requires that every declared error is found as an error (not as the consequence of an earlier one),
                nothing else is wrong and, with 2 or more errors, that no error inherits the consequence of an
                earlier one."""

from pydantic import BaseModel

from core.mistakes.domain.entities.mistake_exercise import DeclaredMistake
from core.mistakes.domain.services.locate import locate, overlap
from core.mistakes.domain.values.llm_outputs import (
    SEVERITY_CONSEQUENCE,
    SEVERITY_ERROR,
    GenerationDraft,
    VerifierFinding,
)
from core.mistakes.domain.values.mistake_kind import PROBLEM_MISTAKE_KINDS, THEORY_MISTAKE_KINDS
from core.shared.math.latex_vocabulary import dollars_balanced, unknown_commands


class GenerationCheck(BaseModel):
    fragments: list[str]
    mistakes: list[DeclaredMistake]
    statement_fragments: int
    problems: list[str]  # empty: valid

    @property
    def valid(self) -> bool:
        return not self.problems


def unknown_message(commands: set[str]) -> str:
    listed = ", ".join(sorted(f"\\{c}" for c in commands))
    return f"fa servir ordres LaTeX que no existeixen ({listed}); fes servir només ordres estàndard de LaTeX/KaTeX"


def fragment_problems(fragments: list[str], where: str = "") -> list[str]:
    """Each fragment not empty, with balanced $...$ so KaTeX renders, no $$, and no LaTeX command outside the known
    vocabulary. `where` follows the fragment's number in the messages (" de la part 2")."""
    problems: list[str] = []
    for i, f in enumerate(fragments, 1):
        if not f:
            problems.append(f"el fragment {i}{where} és buit")
        if not dollars_balanced(f):
            problems.append(f"el fragment {i}{where} té un nombre senar de '$' (LaTeX mal tancat)")
        if "$$" in f:
            problems.append(f"el fragment {i}{where} fa servir $$...$$; cal $...$")
        if unknown := unknown_commands(f):
            problems.append(f"el fragment {i}{where} {unknown_message(unknown)}")
    return problems


def validate_generation(draft: GenerationDraft, n: int, theory: bool = False) -> GenerationCheck:
    # Never drop an empty fragment: the declared errors are numbered by the fragments as sent.
    fragments = [f.strip() for f in draft.fragments]
    problems: list[str] = []
    if not 4 <= len(fragments) <= 14:
        problems.append(f"el nombre de fragments ha de ser entre 4 i 14 (n'hi ha {len(fragments)})")
    problems += fragment_problems(fragments)
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
        for field, value in (
            ("cita", e.quote),
            ("explicacio", e.explanation),
            ("correccio", e.correction),
            ("pista", e.hint),
        ):
            if unknown := unknown_commands(value):
                problems.append(f"el camp '{field}' de l'error {k} {unknown_message(unknown)}")
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


def same_problem(mistake: DeclaredMistake, finding: VerifierFinding, fragments: list[str] | None = None) -> bool:
    """Whether a verifier's finding is the declared error. A different problem in the same fragment does not confirm
    it: the quotes must overlap (fragment-only matching when the verifier gives no locatable quote)."""
    if finding.fragment != mistake.fragment:
        return False
    quote = (finding.quote or "").strip()
    if not quote:
        return True
    span = locate(fragments[mistake.fragment - 1], quote) if fragments else None
    return span is None or overlap(span[0], span[1], mistake.start, mistake.end)


def located_before(finding: VerifierFinding, mistake: DeclaredMistake, fragments: list[str] | None = None) -> bool:
    """Whether the finding sits before the declared error: in an earlier fragment, or in the same one with its quote
    located before the error's. A finding that cannot be placed is not before."""
    fragment = finding.fragment
    if not isinstance(fragment, int) or isinstance(fragment, bool):
        return False
    if fragment != mistake.fragment:
        return fragment < mistake.fragment
    span = locate(fragments[fragment - 1], finding.quote) if fragments else None
    return span is not None and span[0] < mistake.start


def compare_verification(
    mistakes: list[DeclaredMistake], findings: list[VerifierFinding], fragments: list[str] | None = None
) -> list[str]:
    """The independent check must find every declared error, as an error, and nothing else that is wrong. A declared
    error the verifier only sees as a consequence inherits an earlier error; with 2 or more errors, a consequence
    before the last one means an earlier error's wrong values reach a later error: errors must not compound."""
    issues: list[str] = []
    errors = [p for p in findings if p.severity == SEVERITY_ERROR]
    consequences = [p for p in findings if p.severity == SEVERITY_CONSEQUENCE]
    for e in mistakes:
        if any(same_problem(e, p, fragments) for p in errors):
            continue
        if any(same_problem(e, p, fragments) for p in consequences):
            issues.append(
                f"l'error declarat al fragment {e.fragment} («{e.quote}») només hereta un error anterior (el "
                "verificador el veu com una conseqüència): els errors no es poden encadenar"
            )
        else:
            issues.append(
                f"l'error declarat al fragment {e.fragment} («{e.quote}») no l'ha detectat el verificador: "
                "potser no és un error real o és ambigu"
            )
    for p in errors:
        # Inside a declared fragment too: a second, different error there is just as unintended.
        if not any(same_problem(e, p, fragments) for e in mistakes):
            issues.append(f"hi ha un error NO intencionat al fragment {p.fragment}: «{p.quote}» — {p.explanation}")
    if len(mistakes) >= 2:
        last = max(mistakes, key=lambda e: (e.fragment, e.start))
        for p in consequences:
            if located_before(p, last, fragments):
                issues.append(
                    f"un error es propaga fins a un altre error: la conseqüència del fragment {p.fragment} "
                    f"(«{p.quote}») és anterior a l'últim error declarat (fragment {last.fragment}); només l'últim "
                    "error pot canviar valors que es fan servir després"
                )
    return issues
