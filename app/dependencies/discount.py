from typing import Annotated

from fastapi import Depends

from app.common.abstract.services.discount import AbstractDiscountServices
from app.services.cache import cache_service
from app.services.discount import DiscountServices


async def get_discount_services() -> AbstractDiscountServices:
    return DiscountServices(cache_service=cache_service)


GetDiscountServices = Annotated[AbstractDiscountServices, Depends(get_discount_services)]
