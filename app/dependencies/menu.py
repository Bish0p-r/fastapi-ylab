from typing import Annotated

from fastapi import Depends

from app.dependencies.discount import get_discount_services
from app.repositories.menu import MenuRepository
from app.services.cache import cache_service
from app.services.menu import MenuServices


async def get_menu_services() -> MenuServices:
    return MenuServices(
        repository=MenuRepository, cache_service=cache_service, discount_service=await get_discount_services()
    )


GetMenuServices = Annotated[MenuServices, Depends(get_menu_services)]
