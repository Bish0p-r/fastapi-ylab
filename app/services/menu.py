from decimal import Decimal
from typing import Any, Sequence
from uuid import UUID

from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy import RowMapping
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import MenuNotFound, MenuWithThisTitleExists
from app.models.dish import Dish
from app.models.menu import Menu
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

    async def tree(self, session: AsyncSession) -> Sequence[Menu] | Any:
        cached_data = await self.cache_service.get_cache('list:tree')
        if cached_data is not None:
            return cached_data
        result = await self.repository.get_tree_list(session=session)
        dishes = [dish for menu in result for submenu in menu.submenus for dish in submenu.dishes]
        await self.set_discount(*dishes)
        await self.cache_service.set_cache('list:tree', result)
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

    async def create(self, session: AsyncSession, data: dict, background_tasks: BackgroundTasks) -> RowMapping | None:
        try:
            result = await self.repository.create(session=session, **data)
        except IntegrityError:
            raise MenuWithThisTitleExists
        background_tasks.add_task(self.cache_service.clear_cache, ('list:tree', 'list:menu'))
        return result

    async def update(
        self, session: AsyncSession, menu_id: UUID, data: dict, background_tasks: BackgroundTasks
    ) -> RowMapping | None:
        try:
            result = await self.repository.update(session=session, id=menu_id, data=data)
        except IntegrityError:
            raise MenuWithThisTitleExists
        background_tasks.add_task(self.cache_service.clear_cache, ('list:tree', 'list:menu', f'retrieve:{menu_id}'))
        return result

    async def delete(self, session: AsyncSession, menu_id: UUID, background_tasks: BackgroundTasks) -> JSONResponse:
        result = await self.repository.delete(session=session, id=menu_id)
        if result is None:
            raise MenuNotFound
        background_tasks.add_task(self.cache_service.clear_cache, ('list:*', f'retrieve:{menu_id}*'))
        return JSONResponse(status_code=200, content={'detail': 'menu deleted'})

    async def set_discount(self, *data: Dish):
        for dish in data:
            discount = await self.cache_service.get_cache(f'discount:{dish.id}')
            if discount is not None:
                discount = int(discount)
                dish.price = Decimal(dish.price * (100 - discount) / 100).quantize(Decimal('1.00'))
