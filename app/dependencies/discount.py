from typing import Annotated

from fastapi import Depends

from app.services.cache import cache_service
from app.services.discount import DiscountServices


async def get_discount_services() -> DiscountServices:
    return DiscountServices(cache_service=cache_service)


GetDiscountServices = Annotated[DiscountServices, Depends(get_discount_services)]
