from pydantic import BaseModel, ConfigDict

from core.course.domain.entities.theory_item import TheoryItem
from core.shared.domain.ids import TheoryItemId


class QuizSource(BaseModel):
    """A whole topic, or one result of the notes as the focus (then most statements turn around it)."""

    model_config = ConfigDict(frozen=True)

    topic: int
    topic_title: str
    notes: tuple[TheoryItem, ...]  # every item of the topic, in the order of the notes
    allowed_refs: tuple[TheoryItemId, ...]  # numbered items the solutions may cite: this topic and earlier ones
    focus: TheoryItem | None = None

    @property
    def id(self) -> str:
        return self.focus.id if self.focus else f"tema-{self.topic}"
