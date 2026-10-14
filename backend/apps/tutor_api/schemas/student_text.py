"""Text the client sends, checked before anything else runs: a 422 before any model call, never a 500 after it."""

import re
from typing import Annotated

from pydantic import AfterValidator

# NUL cannot be stored in a Postgres text or JSONB column, and a lone surrogate cannot be encoded as UTF-8 at all:
# either one would fail at the database, after the model calls were paid for. The other C0 controls never come from
# a keyboard. Tab, newline and carriage return do (pasted text) and are kept.
_UNUSABLE = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f\ud800-\udfff]")


def check_text(value: str) -> str:
    if m := _UNUSABLE.search(value):
        raise ValueError(f"caràcter no permès (U+{ord(m.group()):04X})")
    return value


StudentText = Annotated[str, AfterValidator(check_text)]
