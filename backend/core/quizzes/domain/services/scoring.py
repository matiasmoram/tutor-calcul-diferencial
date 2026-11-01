"""Grading decided by code: the verdict is checked here, the LLM's judgement of each justification is capped by
the evidence it quotes and by sympy on the student's own computations, and the score is computed here."""

import re
from collections.abc import Collection, Mapping, Sequence

from core.quizzes.domain.entities.grading import (
    JUSTIFICATIONS,
    Answer,
    Justification,
    QuizGrading,
    StatementGrading,
    StatementSolution,
    StudentCheck,
)
from core.quizzes.domain.entities.quiz import Quiz
from core.quizzes.domain.values.grading_inputs import GraderEvaluation, IdeaCitation
from core.shared.domain.model_usage import ModelUsage
from core.shared.math import latex_cas
from core.shared.math.sympy_checks import InvalidExpression, parse

VERDICT_POINTS = 0.3  # the verdict alone; the justification carries the rest
JUSTIFICATION_POINTS: Mapping[Justification, float] = {
    "correcta": 1.0,
    "parcial": 0.5,
    "incorrecta": 0.0,
    "absent": 0.0,
}
HINT_FACTOR = 0.85
DOWNGRADE: Mapping[Justification, Justification] = {"correcta": "parcial", "parcial": "incorrecta"}
MAX_STUDENT_CHECKS = 3
UNANSWERED_FEEDBACK = "No has contestat aquesta afirmació."
CAS_NOTE = "Algun càlcul de la teva resposta no és correcte (comprovat amb sympy)."

_NUMBER = re.compile(r"(?<![\w$])-?\d+(?:[.,]\d+)?(?:/\d+)?(?![\w$])")


def _squash(text: str) -> str:
    return re.sub(r"[\s$\\{}]+", "", text).lower()


def quote_present(quote: str, text: str) -> bool:
    """The quote must be in the answer, ignoring spacing, `$`, braces and backslashes (LaTeX re-typed by the grader)."""
    quote = _squash(quote)
    return len(quote) >= 3 and quote in _squash(text)


def ideas_with_evidence(ideas: Sequence[IdeaCitation], n: int, text: str) -> set[int]:
    """Key ideas the grader credits with a quote that is really in the answer; one quote credits one idea."""
    out: set[int] = set()
    used: set[str] = set()
    for idea in ideas:
        if not 1 <= idea.num <= n:
            continue
        quote = _squash(idea.quote)
        if quote in used or not quote_present(idea.quote, text):
            continue
        used.add(quote)
        out.add(idea.num)
    return out


def faithful(check: StudentCheck) -> bool:
    """A transcribed value must be stated in the student's quote (as a formula or a number there): otherwise the
    transcriber computed or corrected it, and the check would test something the student never said.
    Parses and evaluates student-written math (`9**9**9` never ends): servers run it through `CheckEvaluator.faithful`,
    in a sympy worker under a deadline."""
    if check.kind == "no_limit" or not check.value.strip():
        return True
    try:
        value = parse(check.value)
    except InvalidExpression:
        return False
    candidates = [side for f in latex_cas.formulas(check.quote) for side in latex_cas.sides(f)]
    candidates += _NUMBER.findall(re.sub(r"\$[^$]*\$", " ", check.quote))
    return any(latex_cas.equivalent(x.replace(",", "."), value) for x in candidates)


def quoted_claims(claims: Sequence[StudentCheck], answer_text: str) -> list[StudentCheck]:
    """The claims whose quote is in the answer (cheap: no math); `faithful` then keeps those worth running."""
    return [c for c in claims if quote_present(c.quote, answer_text)]


def _justification(evaluation: GraderEvaluation | None) -> Justification:
    value = evaluation.justification if evaluation else None
    for j in JUSTIFICATIONS:
        if j == value:
            return j
    return "absent"


def grade_quiz(
    quiz: Quiz,
    answers: Mapping[str, Answer],
    hints: Collection[str],
    evaluations: Mapping[str, GraderEvaluation],
    checked: Mapping[str, list[StudentCheck]],
    summary: str,
    call: ModelUsage | None,
) -> QuizGrading:
    """`answers` by statement id (statements of the quiz only); `checked` holds the evaluated student claims."""
    items: list[StatementGrading] = []
    total = 0.0
    for s in quiz.statements:
        r = answers.get(s.id)
        v = evaluations.get(s.id)
        text = r.justification if r else ""
        just = _justification(v) if text.strip() else "absent"  # nothing written: the model's word is not needed
        correct = bool(r and r.verdict == s.verdict)
        if not correct and just in ("correcta", "parcial"):
            just = "incorrecta"  # a right argument for the wrong verdict cannot exist
        present = ideas_with_evidence(v.ideas if v else [], len(s.key_ideas), text)
        if just == "correcta" and len(present) * 2 < len(s.key_ideas):
            just = "parcial"  # the rubric: a complete argument contains most of the key ideas
        if just == "parcial" and not present:
            just = "incorrecta"  # and a partial one at least one, quoted from the answer
        cs = checked.get(s.id, [])
        cas_note = ""
        if just in DOWNGRADE and any(c.failed for c in cs):
            just = DOWNGRADE[just]
            cas_note = CAS_NOTE
        points = (VERDICT_POINTS + (1 - VERDICT_POINTS) * JUSTIFICATION_POINTS[just]) if correct else 0.0
        if s.id in hints:
            points *= HINT_FACTOR
        total += points
        answered = bool(r and r.verdict)
        items.append(
            StatementGrading(
                id=s.id,
                answer=r.verdict if r else "",
                verdict=s.verdict,
                correct=correct,
                justification=just if answered else "absent",
                feedback=(v.feedback if v else "") if answered else UNANSWERED_FEEDBACK,
                cas_note=cas_note,
                student_checks=cs,
                ideas_present=sorted(present),
                hint_used=s.id in hints,
                points=round(points, 2),
                solution=StatementSolution(
                    counterexample=s.counterexample,
                    solution=s.solution,
                    key_ideas=s.key_ideas,
                    theory=s.theory,
                    checks=s.checks,
                ),
            )
        )
    n = len(quiz.statements)
    return QuizGrading(
        grade=round(100 * total / n) if n else 0,
        correct=sum(i.correct for i in items),
        total=n,
        statements=items,
        summary=summary,
        call=call,
    )
