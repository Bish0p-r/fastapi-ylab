from typing import Annotated

from fastapi import Depends

from app.repositories.submenu import SubMenuRepository
from app.services.cache import cache_service
from app.services.submenu import SubMenuServices


async def get_submenu_services() -> SubMenuServices:
    return SubMenuServices(repository=SubMenuRepository, cache_service=cache_service)


GetSubMenuServices = Annotated[SubMenuServices, Depends(get_submenu_services)]
