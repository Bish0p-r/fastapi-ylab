import uuid

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    id: int
    title: str
    description: str
