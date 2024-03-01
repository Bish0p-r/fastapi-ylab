from decimal import Decimal

from app.common.abstract.services.discount import AbstractDiscountServices
from app.models.dish import Dish
from app.services.cache import CacheService


class DiscountServices(AbstractDiscountServices):
    def __init__(self, cache_service: CacheService) -> None:
        self.cache_service = cache_service

    async def set_discount(self, *dishes: Dish) -> None:
        for dish in dishes:
            discount = await self.cache_service.get_cache(f'discount:{dish.id}')
            if discount is not None:
                discount = int(discount)
                dish.price = Decimal(dish.price * (100 - discount) / 100).quantize(Decimal('1.00'))
