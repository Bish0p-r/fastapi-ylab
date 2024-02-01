from typing import Annotated

from fastapi import Depends

from app.repositories.menu import MenuRepository
from app.services.menu import MenuServices


async def get_menu_services() -> MenuServices:
    return MenuServices(repository=MenuRepository)


GetMenuServices = Annotated[MenuServices, Depends(get_menu_services)]
