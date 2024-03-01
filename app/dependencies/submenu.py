from typing import Annotated

from fastapi import Depends

from app.common.abstract.services.submenu import AbstractSubMenuServices
from app.repositories.submenu import SubMenuRepository
from app.services.cache import cache_service
from app.services.submenu import SubMenuServices


async def get_submenu_services() -> AbstractSubMenuServices:
    return SubMenuServices(repository=SubMenuRepository, cache_service=cache_service)


GetSubMenuServices = Annotated[AbstractSubMenuServices, Depends(get_submenu_services)]
