from pydantic import BaseModel


class ResolutionPart(BaseModel):
    title: str
    step: str  # problems: the sheet step it writes out; "" for theory
    fragments: list[str]


class Resolution(BaseModel):
    """The correct resolution in parts, checked by code and by a blind verifier: what every part's error is put
    into. Theory: part 1 is the statement. Parts are numbered from 1."""

    parts: list[ResolutionPart]
    statement_fragments: int  # 0 for problems

    @property
    def fragments(self) -> list[str]:
        return [f for p in self.parts for f in p.fragments]

    def first_fragment(self, part: int) -> int:
        """The document-wide number of the part's first fragment."""
        return 1 + sum(len(p.fragments) for p in self.parts[: part - 1])
