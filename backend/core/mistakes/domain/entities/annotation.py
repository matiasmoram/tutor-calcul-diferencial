from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class Annotation(BaseModel):
    """A passage the student underlined, with why they think it is wrong. Offsets are characters of the fragment."""

    model_config = ConfigDict(serialize_by_alias=True)

    id: str = Field(max_length=40)
    fragment: int  # 1-based
    start: int = Field(validation_alias=AliasChoices("inici", "start"), serialization_alias="inici")
    end: int = Field(validation_alias=AliasChoices("fi", "end"), serialization_alias="fi")
    comment: str = Field(
        default="",
        max_length=1500,
        validation_alias=AliasChoices("comentari", "comment"),
        serialization_alias="comentari",
    )
