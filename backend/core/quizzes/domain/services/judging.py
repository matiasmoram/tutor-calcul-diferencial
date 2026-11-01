from collections.abc import Sequence

from core.quizzes.domain.entities.statement import Confidence
from core.quizzes.domain.values.drafts import StatementDraft
from core.quizzes.domain.values.verification import AuditReview, SolverAnswer

_UNSURE: Confidence = "baixa"
_AUDIT_FLAGS: tuple[tuple[str, str], ...] = (
    ("solution_correct", "la resolució o el contraexemple no és correcte"),
    ("theory_correct", "la teoria citada no és correcta"),
    ("hint_neutral", "la pista revela la resposta"),
)


def judge(
    drafts: Sequence[StatementDraft], answers: Sequence[SolverAnswer], reviews: Sequence[AuditReview]
) -> list[list[str]]:
    """Code decision on the two verification passes: problems per draft (empty = accepted).

    A draft is kept only if the blind solver reaches the same verdict, with confidence, on a well-posed
    statement, and the audit accepts its solution, citations and hint."""
    solved = {a.num: a for a in answers}
    audited = {r.num: r for r in reviews}
    out: list[list[str]] = []
    for i, d in enumerate(drafts, 1):
        p: list[str] = []
        s = solved.get(i)
        if s is None:
            p.append("el solucionador independent no l'ha resolta")
        else:
            if not s.well_posed:
                p.append(f"el solucionador independent diu que està mal plantejada: {s.justification}")
            if s.verdict != d.verdict:
                p.append(f"el solucionador independent diu que és {s.verdict}, no {d.verdict}: {s.justification}")
            elif s.confidence == _UNSURE:
                p.append(f"el solucionador independent no n'està segur: {s.justification}")
        r = audited.get(i)
        if r is None:
            p.append("l'auditoria no l'ha revisada")
        else:
            for flag, reason in _AUDIT_FLAGS:
                if not getattr(r, flag):
                    p.append(f"auditoria: {reason}: {r.problems}")
        out.append(p)
    return out
