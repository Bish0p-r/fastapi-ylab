from pydantic import BaseModel, Field, ConfigDict

from app.common.base.schema import BaseSchema, BaseCreateSchema


class MenuSchema(BaseSchema):
    ...


class MenuWithCountsSchema(BaseSchema):
    submenus_count: int
    dishes_count: int


class MenuCreateSchema(BaseCreateSchema):
    ...


class MenuUpdateSchema(BaseCreateSchema):
    ...

