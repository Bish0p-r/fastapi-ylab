from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.dependencies.dish import GetDishServices
from app.schemas.dish import DishCreateSchema, DishSchema, DishUpdateSchema

router = APIRouter(prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes", tags=["Dishes"])


@router.get("/")
async def dish_list(menu_id: UUID, submenu_id: UUID, services: GetDishServices) -> List[DishSchema]:
    return await services.list(menu_id=menu_id, submenu_id=submenu_id)


@router.get("/{dish_id}")
async def dish_retrieve(menu_id: UUID, submenu_id: UUID, dish_id: UUID, services: GetDishServices) -> DishSchema:
    return await services.retrieve(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)


@router.post("/", status_code=201)
async def dish_create(menu_id: UUID, submenu_id: UUID, menu_data: DishCreateSchema, services: GetDishServices) -> DishSchema:
    data = menu_data.model_dump()
    return await services.create(submenu_id=submenu_id, data=data)


@router.patch("/{dish_id}")
async def dish_update(
    menu_id: UUID, submenu_id: UUID, dish_id: UUID, menu_data: DishUpdateSchema, services: GetDishServices
) -> DishSchema:
    data = menu_data.model_dump()
    return await services.update(submenu_id=submenu_id, dish_id=dish_id, data=data)


@router.delete("/{dish_id}")
async def dish_delete(menu_id: UUID, submenu_id: UUID, dish_id: UUID, services: GetDishServices):
    return await services.delete(submenu_id=submenu_id, dish_id=dish_id)
