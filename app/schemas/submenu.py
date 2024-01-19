from app.common.base.schema import BaseSchema, BaseCreateSchema


class SubMenuSchema(BaseSchema):
    ...


class SubMenuWithCountSchema(BaseSchema):
    dishes_count: int


class SubMenuCreateSchema(BaseCreateSchema):
    ...


class SubMenuUpdateSchema(BaseCreateSchema):
    ...
