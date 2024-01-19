from app.common.base.schema import BaseCreateSchema, BaseSchema


class MenuSchema(BaseSchema):
    ...


class MenuWithCountsSchema(BaseSchema):
    submenus_count: int = 0
    dishes_count: int = 0


class MenuCreateSchema(BaseCreateSchema):
    ...


class MenuUpdateSchema(BaseCreateSchema):
    ...
