from pydantic import BaseModel, ConfigDict, Field

from core.shared.domain.contract import catalan_alias


class Annotation(BaseModel):
    """A passage the student underlined, with why they think it is wrong. Offsets are characters of the fragment."""

    model_config = ConfigDict(serialize_by_alias=True)

    id: str = Field(max_length=40)
    fragment: int  # 1-based
    start: int = Field(validation_alias=catalan_alias("inici", "start"), serialization_alias="inici")
    end: int = Field(validation_alias=catalan_alias("fi", "end"), serialization_alias="fi")
    comment: str = Field(
        default="",
        max_length=1500,
        validation_alias=catalan_alias("comentari", "comment"),
        serialization_alias="comentari",
    )
