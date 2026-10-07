from abc import ABC, abstractmethod

from core.quizzes.domain.entities.quiz import Quiz
from core.quizzes.domain.entities.quiz_session import QuizSession
from core.quizzes.domain.values.difficulty import Difficulty

type Availability = dict[str, dict[Difficulty, int]]  # source id -> difficulty -> ready quizzes


class QuizRepository(ABC):
    """Generated and verified quizzes, served again to later students."""

    @abstractmethod
    async def add(self, quiz: Quiz) -> None:
        """Stores the quiz, replacing a stored one with the same id."""

    @abstractmethod
    async def get(self, quiz_id: str) -> Quiz:
        """Raises QuizNotFoundException."""

    @abstractmethod
    async def of_source(self, source_id: str, difficulty: Difficulty) -> list[Quiz]:
        """Oldest first."""

    @abstractmethod
    async def availability(self) -> Availability:
        """Only sources and difficulties with at least one quiz."""


class QuizSessionRepository(ABC):
    @abstractmethod
    async def add(self, quiz_session: QuizSession) -> None: ...

    @abstractmethod
    async def get(self, session_id: str) -> QuizSession:
        """Raises QuizSessionNotFoundException."""

    @abstractmethod
    async def claim_grading(self, session_id: str, now: float, stale_before: float) -> bool:
        """Marks the session as being graded, claimed at `now`, unless it is graded already or another claim newer
        than `stale_before` holds it. True when this caller got the claim (False for an unknown session too)."""

    @abstractmethod
    async def release_grading(self, session_id: str, claimed_at: float) -> None:
        """Drops the claim made at `claimed_at`, only if it is still that one: a claim taken over after it went
        stale belongs to another grading and stays."""

    @abstractmethod
    async def save(self, quiz_session: QuizSession) -> None:
        """Stores the session's hints and submission if nobody saved it since it was read, then bumps its
        ``version``. Raises ConcurrentQuizGradingException otherwise."""
