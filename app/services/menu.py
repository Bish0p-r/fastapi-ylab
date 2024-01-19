from typing import List
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.repositories.menu import MenuRepository
from app.schemas.menu import MenuSchema, MenuWithCountsSchema
from app.common.exceptions import MenuWithThisTitleExists, MenuNotFound


class MenuServices:
    def __init__(self, repository: type[MenuRepository]):
        self.repository = repository

    async def list(self) -> List[MenuWithCountsSchema]:
        return await self.repository.get_all_with_counts()

    async def retrieve(self, menu_id: UUID) -> MenuWithCountsSchema:
        result = await self.repository.get_one_or_none_with_counts(menu_id=menu_id)
        if result is None:
            raise MenuNotFound
        return result

    async def create(self, data: dict) -> MenuSchema:
        try:
            return await self.repository.create(**data)
        except IntegrityError:
            raise MenuWithThisTitleExists

    async def update(self, menu_id: UUID, data: dict) -> MenuSchema:
        return await self.repository.update(id=menu_id, data=data)

    async def delete(self, menu_id: UUID):
        return await self.repository.delete(id=menu_id)
