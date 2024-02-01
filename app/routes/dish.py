from uuid import UUID

from cashews import cache
from fastapi import APIRouter

from app.dependencies.dish import GetDishServices
from app.dependencies.postgresql import GetSession
from app.schemas.dish import DishCreateSchema, DishSchema, DishUpdateSchema

router = APIRouter(prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dishes'])


@router.get('/')
@cache(ttl='3m', key='list:dish')
async def dish_list(
    menu_id: UUID, submenu_id: UUID, services: GetDishServices, session: GetSession
) -> list[DishSchema]:
    return await services.list(session=session, menu_id=menu_id, submenu_id=submenu_id)


@router.get('/{dish_id}')
@cache(ttl='3m', key='retrieve:{dish_id}')
async def dish_retrieve(
    menu_id: UUID, submenu_id: UUID, dish_id: UUID, services: GetDishServices, session: GetSession
) -> DishSchema:
    return await services.retrieve(session=session, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)


@router.post('/', status_code=201)
@cache.invalidate('list:*')
@cache.invalidate('retrieve:{menu_id}')
@cache.invalidate('retrieve:{submenu_id}')
async def dish_create(
    menu_id: UUID, submenu_id: UUID, menu_data: DishCreateSchema, services: GetDishServices, session: GetSession
) -> DishSchema:
    data = menu_data.model_dump()
    return await services.create(session=session, submenu_id=submenu_id, data=data)


@router.patch('/{dish_id}')
@cache.invalidate('list:dish')
@cache.invalidate('retrieve:{dish_id}')
async def dish_update(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    menu_data: DishUpdateSchema,
    services: GetDishServices,
    session: GetSession,
) -> DishSchema:
    data = menu_data.model_dump()
    return await services.update(session=session, submenu_id=submenu_id, dish_id=dish_id, data=data)


@router.delete('/{dish_id}')
@cache.invalidate('list:*')
@cache.invalidate('retrieve:{menu_id}')
@cache.invalidate('retrieve:{submenu_id}')
@cache.invalidate('retrieve:{dish_id}')
async def dish_delete(menu_id: UUID, submenu_id: UUID, dish_id: UUID, services: GetDishServices, session: GetSession):
    return await services.delete(session=session, submenu_id=submenu_id, dish_id=dish_id)
