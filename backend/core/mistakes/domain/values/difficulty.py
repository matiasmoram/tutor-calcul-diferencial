from collections.abc import Mapping
from typing import Literal

# Catalan values: part of the HTTP contract and of the stored documents' paths and JSON.
Difficulty = Literal["facil", "normal", "dificil"]
DIFFICULTIES: tuple[Difficulty, ...] = ("facil", "normal", "dificil")
MISTAKES_PER_DIFFICULTY: Mapping[Difficulty, int] = {"facil": 1, "normal": 2, "dificil": 3}
