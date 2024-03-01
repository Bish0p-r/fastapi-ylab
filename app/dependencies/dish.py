from typing import Annotated

from fastapi import Depends

from app.common.abstract.services.dish import AbstractDishServices
from app.dependencies.discount import get_discount_services
from app.repositories.dish import DishRepository
from app.services.cache import cache_service
from app.services.dish import DishServices


async def get_dish_services() -> AbstractDishServices:
    return DishServices(
        repository=DishRepository, cache_service=cache_service, discount_service=await get_discount_services()
    )


GetDishServices = Annotated[AbstractDishServices, Depends(get_dish_services)]
