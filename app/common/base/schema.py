from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class BaseSchema(BaseModel):
    id: UUID
    title: str
    description: str


class BaseCreateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(max_length=128)
    description: str = Field(max_length=1024)
