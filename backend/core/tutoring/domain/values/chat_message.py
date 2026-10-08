from typing import Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

Role = Literal["alumne", "tutor"]
TurnOrigin = Literal["text", "foto"]  # typed, or transcribed from a photo of the student's notebook


class ChatMessage(BaseModel):
    """One message of the conversation, stored as ``{"rol": ..., "text": ...}``."""

    model_config = ConfigDict(serialize_by_alias=True, frozen=True)

    role: Role = Field(validation_alias=AliasChoices("rol", "role"), serialization_alias="rol")
    text: str

    @classmethod
    def from_student(cls, text: str) -> "ChatMessage":
        return cls(role="alumne", text=text)

    @classmethod
    def from_tutor(cls, text: str) -> "ChatMessage":
        return cls(role="tutor", text=text)
