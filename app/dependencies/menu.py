from typing import Annotated

from fastapi import Depends

from app.repositories.menu import MenuRepository
from app.services.cache import cache_service
from app.services.menu import MenuServices


async def get_menu_services() -> MenuServices:
    return MenuServices(repository=MenuRepository, cache_service=cache_service)


GetMenuServices = Annotated[MenuServices, Depends(get_menu_services)]
