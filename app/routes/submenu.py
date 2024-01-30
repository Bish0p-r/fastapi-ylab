from uuid import UUID

from fastapi import APIRouter

from app.dependencies.postgresql import GetSession
from app.dependencies.submenu import GetSubMenuServices
from app.schemas.submenu import (SubMenuCreateSchema, SubMenuSchema,
                                 SubMenuUpdateSchema, SubMenuWithCountSchema)

router = APIRouter(prefix="/menus/{menu_id}/submenus", tags=["SubMenus"])


@router.get("/")
async def submenu_list(
    menu_id: UUID, services: GetSubMenuServices, session: GetSession
) -> list[SubMenuWithCountSchema]:
    return await services.list(session=session, menu_id=menu_id)


@router.get("/{submenu_id}")
async def submenu_retrieve(
    menu_id: UUID, submenu_id: UUID, services: GetSubMenuServices, session: GetSession
) -> SubMenuWithCountSchema:
    return await services.retrieve(session=session, menu_id=menu_id, submenu_id=submenu_id)


@router.post("/", status_code=201)
async def submenu_create(
    menu_id: UUID, menu_data: SubMenuCreateSchema, services: GetSubMenuServices, session: GetSession
) -> SubMenuSchema:
    data = menu_data.model_dump()
    return await services.create(session=session, menu_id=menu_id, data=data)


@router.patch("/{submenu_id}")
async def submenu_update(
    menu_id: UUID, submenu_id: UUID, menu_data: SubMenuUpdateSchema, services: GetSubMenuServices, session: GetSession
) -> SubMenuSchema:
    data = menu_data.model_dump()
    return await services.update(session=session, menu_id=menu_id, submenu_id=submenu_id, data=data)


@router.delete("/{submenu_id}")
async def submenu_delete(menu_id: UUID, submenu_id: UUID, services: GetSubMenuServices, session: GetSession):
    return await services.delete(session=session, menu_id=menu_id, submenu_id=submenu_id)
