from uuid import UUID

from cashews import cache
from fastapi import APIRouter

from app.common.base.schema import JsonResponseSchema
from app.dependencies.dish import GetDishServices
from app.dependencies.postgresql import GetSession
from app.schemas.dish import DishCreateSchema, DishSchema, DishUpdateSchema

router = APIRouter(prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dishes'])


@router.get(
    '/',
    description='Get list of dishes',
    responses={200: {'model': list[DishSchema], 'description': 'The list of dishes was found'}},
)
@cache(ttl='3m', key='list:dish')
async def dish_list(
    menu_id: UUID, submenu_id: UUID, services: GetDishServices, session: GetSession
):
    return await services.list(session=session, menu_id=menu_id, submenu_id=submenu_id)


@router.get(
    '/{dish_id}',
    description='Get dish by id',
    responses={
        200: {'model': DishSchema, 'description': 'The dish was found'},
        404: {'model': JsonResponseSchema, 'description': 'The dish was not found'},
    },
)
@cache(ttl='3m', key='retrieve:{dish_id}')
async def dish_retrieve(
    menu_id: UUID, submenu_id: UUID, dish_id: UUID, services: GetDishServices, session: GetSession
):
    return await services.retrieve(session=session, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)


@router.post(
    '/',
    description='Create dish',
    status_code=201,
    response_model=DishSchema,
    responses={
        201: {'model': DishSchema, 'description': 'The dish was created'},
        400: {'model': JsonResponseSchema, 'description': 'The dish with this title already exists'},
    },
)
@cache.invalidate('list:*')
@cache.invalidate('retrieve:{menu_id}')
@cache.invalidate('retrieve:{submenu_id}')
async def dish_create(
    menu_id: UUID, submenu_id: UUID, menu_data: DishCreateSchema, services: GetDishServices, session: GetSession
):
    data = menu_data.model_dump()
    return await services.create(session=session, submenu_id=submenu_id, data=data)


@router.patch(
    '/{dish_id}',
    description='Update dish by id',
    responses={
        200: {'model': DishSchema, 'description': 'The dish was updated'},
        400: {'model': JsonResponseSchema, 'description': 'The dish with this title already exists'},
    },
)
@cache.invalidate('list:dish')
@cache.invalidate('retrieve:{dish_id}')
async def dish_update(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    menu_data: DishUpdateSchema,
    services: GetDishServices,
    session: GetSession,
):
    data = menu_data.model_dump()
    return await services.update(session=session, submenu_id=submenu_id, dish_id=dish_id, data=data)


@router.delete(
    '/{dish_id}',
    description='Delete dish by id',
    responses={
        404: {'model': JsonResponseSchema, 'description': 'The dish was not found'},
        200: {'model': JsonResponseSchema, 'description': 'The dish was deleted'},
    },
)
@cache.invalidate('list:*')
@cache.invalidate('retrieve:{menu_id}')
@cache.invalidate('retrieve:{submenu_id}')
@cache.invalidate('retrieve:{dish_id}')
async def dish_delete(
        menu_id: UUID, submenu_id: UUID, dish_id: UUID, services: GetDishServices, session: GetSession
):
    return await services.delete(session=session, submenu_id=submenu_id, dish_id=dish_id)
