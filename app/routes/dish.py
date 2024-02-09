from uuid import UUID

from fastapi import APIRouter, BackgroundTasks

from app.common.base.schema import JsonResponseSchema
from app.dependencies.dish import GetDishServices
from app.dependencies.postgresql import GetSession
from app.schemas.dish import (
    DishCreateSchema,
    DishDiscountedPriceSchema,
    DishSchema,
    DishUpdateSchema,
)

router = APIRouter(prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dishes'])


@router.get(
    path='/',
    description='Get list of dishes',
    response_model=list[DishDiscountedPriceSchema],
    responses={200: {'model': list[DishDiscountedPriceSchema], 'description': 'The list of dishes was found'}},
)
async def dish_list(menu_id: UUID, submenu_id: UUID, services: GetDishServices, session: GetSession):
    return await services.list(session=session, menu_id=menu_id, submenu_id=submenu_id)


@router.get(
    path='/{dish_id}',
    description='Get dish by id',
    response_model=DishDiscountedPriceSchema,
    responses={
        200: {'model': DishDiscountedPriceSchema, 'description': 'The dish was found'},
        404: {'model': JsonResponseSchema, 'description': 'The dish was not found'},
    },
)
async def dish_retrieve(menu_id: UUID, submenu_id: UUID, dish_id: UUID, services: GetDishServices, session: GetSession):
    return await services.retrieve(session=session, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)


@router.post(
    path='/',
    description='Create dish',
    status_code=201,
    response_model=DishSchema,
    responses={
        201: {'model': DishSchema, 'description': 'The dish was created'},
        409: {'model': JsonResponseSchema, 'description': 'The dish with this title already exists'},
    },
)
async def dish_create(
    menu_id: UUID,
    submenu_id: UUID,
    menu_data: DishCreateSchema,
    services: GetDishServices,
    session: GetSession,
    background_tasks: BackgroundTasks,
):
    data = menu_data.model_dump()
    return await services.create(
        session=session, menu_id=menu_id, submenu_id=submenu_id, data=data, background_tasks=background_tasks
    )


@router.patch(
    path='/{dish_id}',
    description='Update dish by id',
    response_model=DishSchema,
    responses={
        200: {'model': DishSchema, 'description': 'The dish was updated'},
        409: {'model': JsonResponseSchema, 'description': 'The dish with this title already exists'},
    },
)
async def dish_update(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    menu_data: DishUpdateSchema,
    services: GetDishServices,
    session: GetSession,
    background_tasks: BackgroundTasks,
):
    data = menu_data.model_dump()
    return await services.update(
        session=session,
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        data=data,
        background_tasks=background_tasks,
    )


@router.delete(
    path='/{dish_id}',
    description='Delete dish by id',
    responses={
        404: {'model': JsonResponseSchema, 'description': 'The dish was not found'},
        200: {'model': JsonResponseSchema, 'description': 'The dish was deleted'},
    },
)
async def dish_delete(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    services: GetDishServices,
    session: GetSession,
    background_tasks: BackgroundTasks,
):
    return await services.delete(
        session=session, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, background_tasks=background_tasks
    )
