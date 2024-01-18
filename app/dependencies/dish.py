from typing import Annotated

from fastapi import Depends

from app.services.dish import DishServices
from app.repositories.dish import DishRepository


async def get_dish_services():
    return DishServices(repository=DishRepository)

GetDishServices = Annotated[DishServices, Depends(get_dish_services)]
