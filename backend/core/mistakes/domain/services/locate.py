import re


def locate(fragment: str, quote: str) -> tuple[int, int] | None:
    """Exact position of the quote, tolerating only whitespace differences."""
    quote = quote.strip()
    if not quote:
        return None
    i = fragment.find(quote)
    if i >= 0:
        return i, i + len(quote)
    pattern = r"\s+".join(re.escape(tok) for tok in quote.split())
    m = re.search(pattern, fragment)
    return (m.start(), m.end()) if m else None


def locate_all(fragment: str, quote: str) -> list[tuple[int, int]]:
    """Every position of the quote, overlapping ones included; whitespace-tolerant only when it is nowhere exact."""
    quote = quote.strip()
    if not quote:
        return []
    exact = [(i, i + len(quote)) for i in occurrences(fragment, quote)]
    if exact:
        return exact
    pattern = r"\s+".join(re.escape(tok) for tok in quote.split())
    return [(m.start(), m.end()) for m in re.finditer(pattern, fragment)]


def occurrences(text: str, part: str) -> list[int]:
    """The start of every occurrence of `part` in `text`, overlapping ones included."""
    if not part:
        return []
    return [m.start() for m in re.finditer(f"(?={re.escape(part)})", text)]


# The units the frontend lets a student select (frontend/errades.js tokenize): a $...$ formula is one token.
_SELECTABLE = re.compile(r"\$[^$]+\$|[^\s$]+")


def selectable_span(fragment: str, start: int, end: int) -> tuple[int, int]:
    """The shortest highlight the frontend allows that covers [start, end): widened to whole tokens, so a quote
    inside a long formula spans the whole formula."""
    for m in _SELECTABLE.finditer(fragment):
        if overlap(m.start(), m.end(), start, end):
            start, end = min(start, m.start()), max(end, m.end())
    return start, end


def overlap(a0: int, a1: int, b0: int, b1: int) -> bool:
    return max(a0, b0) < min(a1, b1)
