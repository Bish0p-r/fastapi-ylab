from typing import Sequence
from uuid import UUID

from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy import RowMapping
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.abstract.repository.submenu import AbstractSubMenuRepository
from app.common.abstract.services.cache import AbstractCacheServices
from app.common.abstract.services.submenu import AbstractSubMenuServices
from app.common.exceptions import SubMenuNotFound, SubMenuWithThisTitleExists


class SubMenuServices(AbstractSubMenuServices):
    def __init__(self, repository: type[AbstractSubMenuRepository], cache_service: AbstractCacheServices) -> None:
        self.repository = repository
        self.cache_service = cache_service

    async def list(self, session: AsyncSession, menu_id: UUID) -> Sequence[RowMapping]:
        cached_data = await self.cache_service.get_cache('list:submenu')
        if cached_data is not None:
            return cached_data
        result = await self.repository.get_all_with_counts(session=session, menu_id=menu_id)
        await self.cache_service.set_cache('list:submenu', result)
        return result

    async def retrieve(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID) -> RowMapping:
        cached_data = await self.cache_service.get_cache(f'retrieve:{menu_id}-{submenu_id}')
        if cached_data is not None:
            return cached_data
        result = await self.repository.get_one_or_none_with_counts(
            session=session, menu_id=menu_id, submenu_id=submenu_id
        )
        if result is None:
            raise SubMenuNotFound
        await self.cache_service.set_cache(f'retrieve:{menu_id}-{submenu_id}', result)
        return result

    async def create(
        self, session: AsyncSession, menu_id: UUID, data: dict, background_tasks: BackgroundTasks
    ) -> RowMapping | None:
        try:
            result = await self.repository.create(session=session, menu_id=menu_id, **data)
        except IntegrityError:
            raise SubMenuWithThisTitleExists
        background_tasks.add_task(
            self.cache_service.clear_cache, ('list:tree', 'list:menu', 'list:submenu', f'retrieve:{menu_id}')
        )
        return result

    async def update(
        self, session: AsyncSession, menu_id: UUID, submenu_id: UUID, data: dict, background_tasks: BackgroundTasks
    ) -> RowMapping | None:
        try:
            result = await self.repository.update(session=session, id=submenu_id, menu_id=menu_id, data=data)
        except IntegrityError:
            raise SubMenuWithThisTitleExists
        background_tasks.add_task(
            self.cache_service.clear_cache, ('list:tree', 'list:submenu', f'retrieve:{menu_id}-{submenu_id}')
        )
        return result

    async def delete(
        self, session: AsyncSession, menu_id: UUID, submenu_id: UUID, background_tasks: BackgroundTasks
    ) -> JSONResponse:
        result = await self.repository.delete(session=session, id=submenu_id, menu_id=menu_id)
        if result is None:
            raise SubMenuNotFound
        background_tasks.add_task(
            self.cache_service.clear_cache, ('list:*', f'retrieve:{menu_id}-{submenu_id}*', f'retrieve:{menu_id}')
        )
        return JSONResponse(status_code=200, content={'detail': 'submenu deleted'})
