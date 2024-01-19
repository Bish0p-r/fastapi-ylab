from app.common.base.schema import BaseSchema, BaseCreateSchema


class MenuSchema(BaseSchema):
    ...


class MenuWithCountsSchema(BaseSchema):
    submenus_count: int = 0
    dishes_count: int = 0


class MenuCreateSchema(BaseCreateSchema):
    ...


class MenuUpdateSchema(BaseCreateSchema):
    ...
