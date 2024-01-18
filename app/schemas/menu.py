from app.common.base.schema import BaseSchema

from pydantic import BaseModel, Field, ConfigDict


class MenuSchema(BaseSchema):
    ...


class MenuCreateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(max_length=128)
    description: str = Field(max_length=1024)


class MenuUpdateSchema(MenuCreateSchema):
    ...

