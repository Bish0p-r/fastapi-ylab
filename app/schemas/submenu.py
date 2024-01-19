from app.common.base.schema import BaseCreateSchema, BaseSchema


class SubMenuSchema(BaseSchema):
    ...


class SubMenuWithCountSchema(BaseSchema):
    dishes_count: int = 0


class SubMenuCreateSchema(BaseCreateSchema):
    ...


class SubMenuUpdateSchema(BaseCreateSchema):
    ...
