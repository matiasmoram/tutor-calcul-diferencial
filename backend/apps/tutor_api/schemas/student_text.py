"""Text the client sends, checked before anything else runs: a 422 before any model call, never a 500 after it."""

from typing import Annotated

from pydantic import AfterValidator

from core.shared.domain.text import UNSTORABLE


def check_text(value: str) -> str:
    if m := UNSTORABLE.search(value):
        raise ValueError(f"caràcter no permès (U+{ord(m.group()):04X})")
    return value


StudentText = Annotated[str, AfterValidator(check_text)]
