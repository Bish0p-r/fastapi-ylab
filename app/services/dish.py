from typing import Sequence
from uuid import UUID

from fastapi.responses import JSONResponse
from sqlalchemy import RowMapping
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import DishNotFound, DishWithThisTitleExists
from app.repositories.dish import DishRepository
from app.services.cache import CacheService


class DishServices:
    def __init__(self, repository: type[DishRepository]):
        self.repository = repository
        self.cache_service = CacheService()

    async def list(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID) -> Sequence[RowMapping]:
        cached_data = await self.cache_service.get_cache('list:submenu')
        if cached_data is not None:
            return cached_data
        result = await self.repository.get_all_dishes(session=session, menu_id=menu_id, submenu_id=submenu_id)
        await self.cache_service.set_cache('list:dish', result)
        return result

    async def retrieve(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> RowMapping:
        cached_data = await self.cache_service.get_cache(f'retrieve:{menu_id}-{submenu_id}-{dish_id}')
        if cached_data is not None:
            return cached_data
        result = await self.repository.get_one_or_none_dish(
            session=session, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        )
        if result is None:
            raise DishNotFound
        await self.cache_service.set_cache(f'retrieve:{menu_id}-{submenu_id}-{dish_id}', result)
        return result

    async def create(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID, data: dict) -> RowMapping | None:
        try:
            result = await self.repository.create(session=session, submenu_id=submenu_id, **data)
        except IntegrityError:
            raise DishWithThisTitleExists
        await self.cache_service.clear_cache('list:*', f'retrieve:{menu_id}', f'retrieve:{menu_id}-{submenu_id}')
        return result

    async def update(
            self, session: AsyncSession, menu_id: UUID, submenu_id: UUID, dish_id: UUID, data: dict
    ) -> RowMapping | None:
        try:
            result = await self.repository.update(session=session, id=dish_id, submenu_id=submenu_id, data=data)
        except IntegrityError:
            raise DishWithThisTitleExists
        await self.cache_service.clear_cache(
            'list:dish', f'retrieve:{menu_id}', f'retrieve:{menu_id}-{submenu_id}-{dish_id}'
        )
        return result

    async def delete(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> JSONResponse:
        result = await self.repository.delete(session=session, id=dish_id, submenu_id=submenu_id)
        if result is None:
            raise DishNotFound
        await self.cache_service.clear_cache(
            'list:*',
            f'retrieve:{menu_id}',
            f'retrieve:{menu_id}-{submenu_id}',
            f'retrieve:{menu_id}-{submenu_id}-{dish_id}'
        )
        return JSONResponse(status_code=200, content={'detail': 'dish deleted'})
