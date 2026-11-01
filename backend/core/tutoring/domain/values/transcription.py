"""A photo of the student's notebook as faithful text + LaTeX (LLM contract: Catalan keys and enum values).

The transcription is never sent straight to the tutor: the student reviews and edits it first, then sends it
like any typed message."""

from typing import Literal, get_args

from pydantic import BaseModel, ConfigDict, Field

from core.shared.domain.contract import catalan_alias

Legibility = Literal["bona", "parcial", "illegible"]
PhotoContent = Literal["treball_matematic", "altre", "buit"]

LEGIBILITIES: tuple[Legibility, ...] = get_args(Legibility)
PHOTO_CONTENTS: tuple[PhotoContent, ...] = get_args(PhotoContent)


class Transcription(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True, frozen=True)

    text: str = Field(validation_alias=catalan_alias("transcripcio", "text"), serialization_alias="transcripcio")
    legibility: Legibility = Field(
        validation_alias=catalan_alias("llegibilitat", "legibility"), serialization_alias="llegibilitat"
    )
    content: PhotoContent = Field(
        validation_alias=catalan_alias("contingut", "content"), serialization_alias="contingut"
    )
    doubts: list[str] = Field(validation_alias=catalan_alias("dubtes", "doubts"), serialization_alias="dubtes")
