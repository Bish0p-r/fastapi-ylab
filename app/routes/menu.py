from uuid import UUID

from fastapi import APIRouter

from app.dependencies.menu import GetMenuServices
from app.schemas.menu import (MenuCreateSchema, MenuSchema, MenuUpdateSchema,
                              MenuWithCountsSchema)

router = APIRouter(prefix="/menus", tags=["Menus"])


@router.get("/")
async def menu_list(services: GetMenuServices) -> list[MenuWithCountsSchema]:
    return await services.list()


@router.get("/{menu_id}")
async def menu_retrieve(menu_id: UUID, services: GetMenuServices) -> MenuWithCountsSchema:
    return await services.retrieve(menu_id=menu_id)


@router.post("/", status_code=201)
async def menu_create(menu_data: MenuCreateSchema, services: GetMenuServices) -> MenuSchema:
    data = menu_data.model_dump()
    return await services.create(data=data)


@router.patch("/{menu_id}")
async def menu_update(menu_id: UUID, menu_data: MenuUpdateSchema, services: GetMenuServices) -> MenuSchema:
    data = menu_data.model_dump()
    return await services.update(menu_id=menu_id, data=data)


@router.delete("/{menu_id}")
async def menu_delete(menu_id: UUID, services: GetMenuServices):
    return await services.delete(menu_id=menu_id)
