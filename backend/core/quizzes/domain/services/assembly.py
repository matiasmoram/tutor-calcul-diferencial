from collections.abc import Sequence
from random import Random

from core.quizzes.domain.entities.quiz import GenerationRound, Quiz, QuizVerification
from core.quizzes.domain.entities.statement import Statement
from core.quizzes.domain.values.difficulty import Difficulty
from core.quizzes.domain.values.drafts import StatementDraft
from core.quizzes.domain.values.quiz_id import QuizId
from core.shared.domain.ids import TheoryItemId


def build_quiz(
    source_id: str,
    topic: int,
    difficulty: Difficulty,
    kept: Sequence[StatementDraft],
    rounds: list[GenerationRound],
    rng: Random,
    now: float,
) -> Quiz:
    """The quiz from its accepted drafts, shuffled: verdicts must not follow the generation order."""
    drafts = list(kept)
    rng.shuffle(drafts)
    statements = [
        Statement(
            id=f"a{i}",
            statement=d.statement.strip(),
            verdict="fals" if d.verdict == "fals" else "cert",
            concept=d.concept.strip(),
            trap=d.trap,
            counterexample=d.counterexample.strip() if d.verdict == "fals" else "",
            solution=d.solution.strip(),
            key_ideas=[i.strip() for i in d.key_ideas if i.strip()],
            hint=d.hint.strip(),
            theory=[TheoryItemId(r) for r in dict.fromkeys(d.theory)],
            checks=d.checks,
            verification=d.verification,
        )
        for i, d in enumerate(drafts, 1)
    ]
    return Quiz(
        id=QuizId.from_content("".join(s.statement for s in statements), now),
        source_id=source_id,
        topic=topic,
        difficulty=difficulty,
        statements=statements,
        verification=QuizVerification(rounds=rounds),
        created_at=now,
    )
