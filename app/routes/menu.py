from uuid import UUID

from fastapi import APIRouter

from app.dependencies.menu import GetMenuServices
from app.dependencies.postgresql import GetSession
from app.schemas.menu import MenuCreateSchema, MenuSchema, MenuUpdateSchema, MenuWithCountsSchema

router = APIRouter(prefix="/menus", tags=["Menus"])


@router.get("/")
async def menu_list(services: GetMenuServices, session: GetSession) -> list[MenuWithCountsSchema]:
    return await services.list(session=session)


@router.get("/{menu_id}")
async def menu_retrieve(menu_id: UUID, services: GetMenuServices, session: GetSession) -> MenuWithCountsSchema:
    return await services.retrieve(session=session, menu_id=menu_id)


@router.post("/", status_code=201)
async def menu_create(menu_data: MenuCreateSchema, services: GetMenuServices, session: GetSession) -> MenuSchema:
    data = menu_data.model_dump()
    return await services.create(session=session, data=data)


@router.patch("/{menu_id}")
async def menu_update(
    menu_id: UUID, menu_data: MenuUpdateSchema, services: GetMenuServices, session: GetSession
) -> MenuSchema:
    data = menu_data.model_dump()
    return await services.update(session=session, menu_id=menu_id, data=data)


@router.delete("/{menu_id}")
async def menu_delete(menu_id: UUID, services: GetMenuServices, session: GetSession):
    return await services.delete(session=session, menu_id=menu_id)
