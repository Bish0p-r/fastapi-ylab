from decimal import Decimal

from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from app.common.base.schema import BaseCreateSchema, BaseSchema


class DishSchema(BaseSchema):
    price: Decimal = Field(ge=0.01, decimal_places=2)


class DishCreateSchema(BaseCreateSchema):
    price: Decimal = Field(ge=0.01, decimal_places=2)


class DishUpdateSchema(BaseCreateSchema):
    price: Decimal = Field(ge=0.01, decimal_places=2)


class DishDiscountedPriceSchema(BaseSchema):
    discount: int
    price: Decimal = Field(ge=0.01, decimal_places=2)

    @field_validator('price', mode='before')
    @classmethod
    def validate_price(cls, value: Decimal, values: ValidationInfo) -> Decimal:
        discount = values.data.get('discount')
        if discount:
            value = Decimal(value * (100 - discount) / 100).quantize(Decimal('1.00'))
        return value
