from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.abstract.repository.base import AbstractCRUDRepository
from app.common.abstract.repository.dish import AbstractDishRepository
from app.common.abstract.repository.menu import AbstractMenuRepository
from app.common.abstract.repository.submenu import AbstractSubMenuRepository
from app.common.abstract.services.cache import AbstractCacheServices


class AdminServices:
    def __init__(
        self,
        menu_repo: type[AbstractMenuRepository],
        submenu_repo: type[AbstractSubMenuRepository],
        dish_repo: type[AbstractDishRepository],
        cache_service: AbstractCacheServices,
    ) -> None:
        self.menu_repo = menu_repo
        self.submenu_repo = submenu_repo
        self.dish_repo = dish_repo
        self.cache_service = cache_service

    @staticmethod
    async def is_fields_equal(data1: Any, data2: dict, fields: tuple) -> bool:
        for field in fields:
            if str(getattr(data1, field)) != str(data2[field]):
                return False
        return True

    async def delete_not_in(self, session: AsyncSession, ids_data: dict) -> None:
        await self.menu_repo.delete_not_in_list(session, ids_data['menus'])
        await self.submenu_repo.delete_not_in_list(session, ids_data['submenus'])
        await self.dish_repo.delete_not_in_list(session, ids_data['dishes'])

    async def create_or_update(
        self, repo: type[AbstractCRUDRepository], data: list, fields: tuple, session: AsyncSession
    ) -> None:
        for item in data:
            existed_item = await repo.get_one_or_none(session, id=item['id'])

            if existed_item and not await self.is_fields_equal(existed_item, item, fields):
                await repo.update(session, item, id=item['id'])
            elif existed_item is None:
                await repo.create(session, **item)

    async def set_discount(self, data: list) -> None:
        for d in data:
            await self.cache_service.set_cache(f'discount:{d["id"]}', d['discount'], ex=None)

    async def start_sync(self, session: AsyncSession, parsed_data: dict) -> None:
        ids_data = {
            'menus': [i['id'] for i in parsed_data['menus']],
            'submenus': [i['id'] for i in parsed_data['submenus']],
            'dishes': [i['id'] for i in parsed_data['dishes']],
        }
        await self.cache_service.clear_all_cache()
        await self.delete_not_in(session, ids_data)
        await self.create_or_update(self.menu_repo, parsed_data['menus'], ('title', 'description'), session)
        await self.create_or_update(self.submenu_repo, parsed_data['submenus'], ('title', 'description'), session)
        await self.create_or_update(self.dish_repo, parsed_data['dishes'], ('title', 'description', 'price'), session)
        await self.set_discount(parsed_data['discounts'])
