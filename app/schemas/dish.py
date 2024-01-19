from decimal import Decimal

from pydantic import Field

from app.common.base.schema import BaseSchema, BaseCreateSchema


class DishSchema(BaseSchema):
    price: Decimal = Field(ge=0.01, decimal_places=2)


class DishCreateSchema(BaseCreateSchema):
    price: Decimal = Field(ge=0.01, decimal_places=2)


class DishUpdateSchema(BaseCreateSchema):
    price: Decimal = Field(ge=0.01, decimal_places=2)
