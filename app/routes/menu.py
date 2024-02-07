from uuid import UUID

from fastapi import APIRouter, BackgroundTasks

from app.common.base.schema import JsonResponseSchema
from app.dependencies.menu import GetMenuServices
from app.dependencies.postgresql import GetSession
from app.schemas.menu import (
    MenuCreateSchema,
    MenuSchema,
    MenuTreeSchema,
    MenuUpdateSchema,
    MenuWithCountsSchema,
)

router = APIRouter(prefix='/menus', tags=['Menus'])


@router.get(
    path='/',
    description='Get list of menus',
    response_model=list[MenuWithCountsSchema],
    responses={200: {'model': list[MenuWithCountsSchema], 'description': 'The list of menus was found'}},
)
async def menu_list(services: GetMenuServices, session: GetSession):
    return await services.list(session=session)


@router.get(
    path='/tree',
    description='Get tree of menus',
    response_model=list[MenuTreeSchema],
    responses={200: {'model': list[MenuTreeSchema], 'description': 'The tree of menus was found'}},
)
async def menu_tree(services: GetMenuServices, session: GetSession):
    return await services.tree(session=session)


@router.get(
    path='/{menu_id}',
    description='Get menu by id',
    response_model=MenuWithCountsSchema,
    responses={
        200: {'model': MenuWithCountsSchema, 'description': 'The menu was found'},
        404: {'model': JsonResponseSchema, 'description': 'The menu was not found'},
    },
)
async def menu_retrieve(menu_id: UUID, services: GetMenuServices, session: GetSession):
    return await services.retrieve(session=session, menu_id=menu_id)


@router.post(
    path='/',
    description='Create menu',
    status_code=201,
    response_model=MenuSchema,
    responses={
        201: {'model': MenuSchema, 'description': 'The menu was created'},
        409: {'model': JsonResponseSchema, 'description': 'Non-unique menu title'},
    },
)
async def menu_create(
    menu_data: MenuCreateSchema, services: GetMenuServices, session: GetSession, background_tasks: BackgroundTasks
):
    data = menu_data.model_dump()
    return await services.create(session=session, data=data, background_tasks=background_tasks)


@router.patch(
    path='/{menu_id}',
    description='Update menu by id',
    response_model=MenuSchema,
    responses={
        200: {'model': MenuSchema, 'description': 'The menu was updated'},
        409: {'model': JsonResponseSchema, 'description': 'Non-unique menu title'},
    },
)
async def menu_update(
    menu_id: UUID,
    menu_data: MenuUpdateSchema,
    services: GetMenuServices,
    session: GetSession,
    background_tasks: BackgroundTasks,
):
    data = menu_data.model_dump()
    return await services.update(session=session, menu_id=menu_id, data=data, background_tasks=background_tasks)


@router.delete(
    path='/{menu_id}',
    description='Delete menu by id',
    responses={
        404: {'model': JsonResponseSchema, 'description': 'The menu was not found'},
        200: {'model': JsonResponseSchema, 'description': 'The menu was deleted'},
    },
)
async def menu_delete(menu_id: UUID, services: GetMenuServices, session: GetSession, background_tasks: BackgroundTasks):
    return await services.delete(session=session, menu_id=menu_id, background_tasks=background_tasks)
