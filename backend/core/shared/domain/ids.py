import re

from core.shared.domain.checked_value import CheckedStr, HexId


class SessionId(HexId):
    """A tutor, "troba l'error" or quiz session."""


class ExerciseId(CheckedStr):
    """``t<topic>-<problem>[<part>]``, e.g. ``t2-4c``."""

    PATTERN = re.compile(r"t[1-9]-\d+[a-z]?")


class TheoryItemId(CheckedStr):
    """``T<topic>.<num>`` (numbered item of the notes) or ``T<topic>.x<num>`` (unnumbered), e.g. ``T3.12``."""

    PATTERN = re.compile(r"T[1-9]\.x?\d+")


class ProblemSheetId(CheckedStr):
    PATTERN = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
