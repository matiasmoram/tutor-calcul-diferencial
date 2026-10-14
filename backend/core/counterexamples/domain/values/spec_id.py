import re

from core.counterexamples.domain.exceptions import UnknownSpecException
from core.shared.domain.checked_value import CheckedStr


class SpecId(CheckedStr):
    """A challenge, ``<words>`` in kebab case, e.g. ``parcials-sense-continuitat``."""

    PATTERN = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")


def spec_id_of(text: str) -> SpecId:
    """The id from a request: a malformed one is a challenge that does not exist."""
    try:
        return SpecId(text)
    except ValueError:
        raise UnknownSpecException(text) from None
