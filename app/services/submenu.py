from uuid import UUID
from typing import List

from sqlalchemy.exc import IntegrityError

from app.repositories.submenu import SubMenuRepository
from app.schemas.submenu import SubMenuSchema, SubMenuWithCountSchema
from app.common.exceptions import SubMenuWithThisTitleExists, SubMenuNotFound


class SubMenuServices:
    def __init__(self, repository: type[SubMenuRepository]):
        self.repository = repository

    async def list(self, menu_id: UUID) -> List[SubMenuWithCountSchema]:
        return await self.repository.get_all_with_counts(menu_id=menu_id)

    async def retrieve(self, menu_id: UUID, submenu_id: UUID) -> SubMenuWithCountSchema:
        result = await self.repository.get_one_or_none_with_counts(menu_id=menu_id, submenu_id=submenu_id)
        if result is None:
            raise SubMenuNotFound
        return result

    async def create(self, menu_id: UUID, data: dict) -> SubMenuSchema:
        try:
            return await self.repository.create(menu_id=menu_id, **data)
        except IntegrityError:
            raise SubMenuWithThisTitleExists

    async def update(self, menu_id: UUID, submenu_id: UUID, data: dict) -> SubMenuSchema:
        return await self.repository.update(id=submenu_id, menu_id=menu_id, data=data)

    async def delete(self, menu_id: UUID, submenu_id: UUID):
        return await self.repository.delete(id=submenu_id, menu_id=menu_id)
