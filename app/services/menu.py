from typing import Sequence
from uuid import UUID

from fastapi.responses import JSONResponse
from sqlalchemy import RowMapping
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import MenuNotFound, MenuWithThisTitleExists
from app.repositories.menu import MenuRepository
from app.services.cache import CacheService


class MenuServices:
    def __init__(self, repository: type[MenuRepository], cache_service: CacheService) -> None:
        self.repository = repository
        self.cache_service = cache_service

    async def list(self, session: AsyncSession) -> Sequence[RowMapping]:
        cached_data = await self.cache_service.get_cache('list:menu')
        if cached_data is not None:
            return cached_data
        result = await self.repository.get_all_with_counts(session=session)
        await self.cache_service.set_cache('list:menu', result)
        return result

    async def retrieve(self, session: AsyncSession, menu_id: UUID) -> RowMapping:
        cached_data = await self.cache_service.get_cache(f'retrieve:{menu_id}')
        if cached_data is not None:
            return cached_data
        result = await self.repository.get_one_or_none_with_counts(session=session, menu_id=menu_id)
        if result is None:
            raise MenuNotFound
        await self.cache_service.set_cache(f'retrieve:{menu_id}', result)
        return result

    async def create(self, session: AsyncSession, data: dict) -> RowMapping | None:
        try:
            result = await self.repository.create(session=session, **data)
        except IntegrityError:
            raise MenuWithThisTitleExists
        await self.cache_service.clear_cache('list:menu')
        return result

    async def update(self, session: AsyncSession, menu_id: UUID, data: dict) -> RowMapping | None:
        try:
            result = await self.repository.update(session=session, id=menu_id, data=data)
        except IntegrityError:
            raise MenuWithThisTitleExists
        await self.cache_service.clear_cache('list:menu', f'retrieve:{menu_id}')
        return result

    async def delete(self, session: AsyncSession, menu_id: UUID) -> JSONResponse:
        result = await self.repository.delete(session=session, id=menu_id)
        if result is None:
            raise MenuNotFound
        await self.cache_service.clear_cache('list:*', f'retrieve:{menu_id}*', f'retrieve:{menu_id}')
        return JSONResponse(status_code=200, content={'detail': 'menu deleted'})
