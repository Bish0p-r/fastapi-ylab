from uuid import UUID

from cashews import cache
from fastapi import APIRouter

from app.common.base.schema import JsonResponseSchema
from app.dependencies.menu import GetMenuServices
from app.dependencies.postgresql import GetSession
from app.schemas.menu import (
    MenuCreateSchema,
    MenuSchema,
    MenuUpdateSchema,
    MenuWithCountsSchema,
)

router = APIRouter(prefix='/menus', tags=['Menus'])


@router.get(
    '/',
    description='Get list of menus',
    responses={200: {'model': list[MenuWithCountsSchema], 'description': 'The list of menus was found'}}
)
@cache(ttl='3m', key='list:menu')
async def menu_list(services: GetMenuServices, session: GetSession):
    return await services.list(session=session)


@router.get(
    '/{menu_id}',
    description='Get menu by id',
    responses={
        200: {'model': MenuSchema, 'description': 'The menu was found'},
        404: {'model': JsonResponseSchema, 'description': 'The menu was not found'}}
)
@cache(ttl='3m', key='retrieve:{menu_id}')
async def menu_retrieve(menu_id: UUID, services: GetMenuServices, session: GetSession):
    return await services.retrieve(session=session, menu_id=menu_id)


@router.post(
    '/',
    description='Create menu',
    status_code=201,
    response_model=MenuSchema,
    responses={
        201: {'model': MenuSchema, 'description': 'The menu was created'},
        400: {'model': JsonResponseSchema, 'description': 'Non-unique menu title'}}
)
@cache.invalidate('list:menu')
async def menu_create(menu_data: MenuCreateSchema, services: GetMenuServices, session: GetSession):
    data = menu_data.model_dump()
    return await services.create(session=session, data=data)


@router.patch(
    '/{menu_id}',
    description='Update menu by id',
    responses={
        200: {'model': MenuSchema, 'description': 'The menu was updated'},
        400: {'model': JsonResponseSchema, 'description': 'Non-unique menu title'}}
)
@cache.invalidate('list:menu')
@cache.invalidate('retrieve:{menu_id}')
async def menu_update(
    menu_id: UUID, menu_data: MenuUpdateSchema, services: GetMenuServices, session: GetSession
):
    data = menu_data.model_dump()
    return await services.update(session=session, menu_id=menu_id, data=data)


@router.delete(
    '/{menu_id}',
    description='Delete menu by id',
    responses={
        404: {'model': JsonResponseSchema, 'description': 'The menu was not found'},
        200: {'model': JsonResponseSchema, 'description': 'The menu was deleted'}}
)
@cache.invalidate('list:*')
@cache.invalidate('retrieve:{menu_id}')
async def menu_delete(menu_id: UUID, services: GetMenuServices, session: GetSession):
    return await services.delete(session=session, menu_id=menu_id)
