from pydantic import BaseModel, Field


class TopicSection(BaseModel):
    id: str  # "2.1"
    title: str


class Topic(BaseModel):
    number: int
    title: str
    sections: list[TopicSection] = Field(default_factory=list)
