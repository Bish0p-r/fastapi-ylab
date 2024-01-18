from typing import Annotated

from fastapi import Depends

from app.services.submenu import SubMenuServices
from app.repositories.submenu import SubMenuRepository


async def get_submenu_services():
    return SubMenuServices(repository=SubMenuRepository)

GetSubMenuServices = Annotated[SubMenuServices, Depends(get_submenu_services)]
