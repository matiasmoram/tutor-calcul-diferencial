import hashlib
import re
from typing import Self

from core.shared.domain.checked_value import CheckedStr


class MistakeExerciseId(CheckedStr):
    """12 hex characters; also the stored document's file name (``generats/errades/<source>/<difficulty>/<id>.json``)."""

    PATTERN = re.compile(r"[0-9a-f]{12}")

    @classmethod
    def new(cls, fragments: list[str], now: float) -> Self:
        return cls(hashlib.sha1(("".join(fragments) + str(now)).encode()).hexdigest()[:12])
