from typing import Annotated

from fastapi import Depends

from app.repositories.dish import DishRepository
from app.services.cache import CacheService
from app.services.dish import DishServices


async def get_dish_services() -> DishServices:
    return DishServices(repository=DishRepository, cache_service=CacheService())


GetDishServices = Annotated[DishServices, Depends(get_dish_services)]
