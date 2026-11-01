from pydantic import BaseModel


class LocatedAnnotation(BaseModel):
    """An annotation clipped to its fragment, with the declared errors it can be about."""

    id: str  # the client's id, echoed in the result
    # Our own id for it ("a1", "a2"... by position): what the grader sees and answers with, so a student-chosen id
    # never reaches the prompt and one verdict can only ever score one annotation.
    key: str
    fragment: int
    start: int
    end: int
    text: str  # the underlined passage
    comment: str
    candidates: list[str]  # errors of the same fragment
    overlapping: list[str]  # candidates whose quote the underline touches
    # Candidates hit on their quoted words, not by a highlight of the whole fragment that happens to contain them.
    precise: list[str]
