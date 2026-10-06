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


def overlap(a0: int, a1: int, b0: int, b1: int) -> bool:
    return max(a0, b0) < min(a1, b1)
