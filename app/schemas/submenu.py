from app.common.base.schema import BaseCreateSchema, BaseSchema
from app.schemas.dish import DishSchema


class SubMenuSchema(BaseSchema):
    ...


class SubMenuWithCountSchema(BaseSchema):
    dishes_count: int = 0


class SubMenuCreateSchema(BaseCreateSchema):
    ...


class SubMenuUpdateSchema(BaseCreateSchema):
    ...


class SubMenuTreeSchema(SubMenuSchema):
    dishes: list[DishSchema]
