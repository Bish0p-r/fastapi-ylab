from typing import Annotated

from fastapi import Depends

from app.services.menu import MenuServices
from app.repositories.menu import MenuRepository


async def get_menu_services():
    return MenuServices(repository=MenuRepository)


GetMenuServices = Annotated[MenuServices, Depends(get_menu_services)]
