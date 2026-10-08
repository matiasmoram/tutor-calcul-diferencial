import hashlib
import re
from typing import Self

from core.shared.domain.checked_value import CheckedStr


class QuizId(CheckedStr):
    """12 hex digits; also the file name of a pre-generated quiz (``generats/afirmacions/<source>/<level>/<id>.json``)."""

    PATTERN = re.compile(r"[0-9a-f]{12}")

    @classmethod
    def from_content(cls, text: str, now: float) -> Self:
        return cls(hashlib.sha1((text + str(now)).encode()).hexdigest()[:12])
