"""A photo of the student's notebook as faithful text + LaTeX (LLM contract: Catalan keys and enum values).

The transcription is never sent straight to the tutor: the student reviews and edits it first, then sends it
like any typed message."""

from typing import Literal, get_args

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

Legibility = Literal["bona", "parcial", "illegible"]
PhotoContent = Literal["treball_matematic", "altre", "buit"]

LEGIBILITIES: tuple[Legibility, ...] = get_args(Legibility)
PHOTO_CONTENTS: tuple[PhotoContent, ...] = get_args(PhotoContent)


def _ca(catalan: str, english: str) -> AliasChoices:
    return AliasChoices(catalan, english)


class Transcription(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True, frozen=True)

    text: str = Field(validation_alias=_ca("transcripcio", "text"), serialization_alias="transcripcio")
    legibility: Legibility = Field(
        validation_alias=_ca("llegibilitat", "legibility"), serialization_alias="llegibilitat"
    )
    content: PhotoContent = Field(validation_alias=_ca("contingut", "content"), serialization_alias="contingut")
    doubts: list[str] = Field(validation_alias=_ca("dubtes", "doubts"), serialization_alias="dubtes")
