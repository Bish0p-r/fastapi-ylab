from uuid import UUID

from fastapi import APIRouter, BackgroundTasks

from app.common.base.schema import JsonResponseSchema
from app.dependencies.postgresql import GetSession
from app.dependencies.submenu import GetSubMenuServices
from app.schemas.submenu import (
    SubMenuCreateSchema,
    SubMenuSchema,
    SubMenuUpdateSchema,
    SubMenuWithCountSchema,
)

router = APIRouter(prefix='/menus/{menu_id}/submenus', tags=['SubMenus'])


@router.get(
    path='/',
    description='Get list of submenus',
    response_model=list[SubMenuWithCountSchema],
    responses={200: {'model': list[SubMenuWithCountSchema], 'description': 'The list of submenus was found'}},
)
async def submenu_list(menu_id: UUID, services: GetSubMenuServices, session: GetSession):
    return await services.list(session=session, menu_id=menu_id)


@router.get(
    path='/{submenu_id}',
    description='Get submenu by id',
    response_model=SubMenuWithCountSchema,
    responses={
        200: {'model': SubMenuWithCountSchema, 'description': 'The submenu was found'},
        404: {'model': JsonResponseSchema, 'description': 'The submenu was not found'},
    },
)
async def submenu_retrieve(menu_id: UUID, submenu_id: UUID, services: GetSubMenuServices, session: GetSession):
    return await services.retrieve(session=session, menu_id=menu_id, submenu_id=submenu_id)


@router.post(
    path='/',
    description='Create submenu',
    status_code=201,
    response_model=SubMenuSchema,
    responses={
        201: {'model': SubMenuSchema, 'description': 'The submenu was created'},
        409: {'model': JsonResponseSchema, 'description': 'The submenu with this title already exists'},
    },
)
async def submenu_create(
    menu_id: UUID,
    menu_data: SubMenuCreateSchema,
    services: GetSubMenuServices,
    session: GetSession,
    background_tasks: BackgroundTasks,
):
    data = menu_data.model_dump()
    return await services.create(session=session, menu_id=menu_id, data=data, background_tasks=background_tasks)


@router.patch(
    path='/{submenu_id}',
    description='Update submenu by id',
    responses={
        200: {'model': SubMenuSchema, 'description': 'The submenu was updated'},
        409: {'model': JsonResponseSchema, 'description': 'The submenu with this title already exists'},
    },
)
async def submenu_update(
    menu_id: UUID,
    submenu_id: UUID,
    menu_data: SubMenuUpdateSchema,
    services: GetSubMenuServices,
    session: GetSession,
    background_tasks: BackgroundTasks,
):
    data = menu_data.model_dump()
    return await services.update(
        session=session, menu_id=menu_id, submenu_id=submenu_id, data=data, background_tasks=background_tasks
    )


@router.delete(
    path='/{submenu_id}',
    description='Delete submenu by id',
    responses={
        404: {'model': JsonResponseSchema, 'description': 'The submenu was not found'},
        200: {'model': JsonResponseSchema, 'description': 'The submenu was deleted'},
    },
)
async def submenu_delete(
    menu_id: UUID,
    submenu_id: UUID,
    services: GetSubMenuServices,
    session: GetSession,
    background_tasks: BackgroundTasks,
):
    return await services.delete(
        session=session, menu_id=menu_id, submenu_id=submenu_id, background_tasks=background_tasks
    )
