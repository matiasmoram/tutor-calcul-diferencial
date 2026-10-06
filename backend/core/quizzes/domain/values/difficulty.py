from collections.abc import Mapping
from typing import Literal

# Contract values (HTTP requests, stored quizzes): Catalan.
Difficulty = Literal["facil", "normal", "dificil"]
DIFFICULTIES: tuple[Difficulty, ...] = ("facil", "normal", "dificil")
QUIZ_SIZES: Mapping[Difficulty, int] = {"facil": 6, "normal": 8, "dificil": 10}

_BY_NAME: Mapping[str, Difficulty] = {d: d for d in DIFFICULTIES}


def difficulty_of(name: str) -> Difficulty | None:
    return _BY_NAME.get(name)
