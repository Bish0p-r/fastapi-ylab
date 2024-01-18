from uuid import UUID
from typing import List

from sqlalchemy.exc import IntegrityError

from app.repositories.menu import MenuRepository
from app.schemas.menu import MenuSchema
from app.common.exceptions import MenuWithThisTitleExists


class MenuServices:
    def __init__(self, repository: type[MenuRepository]):
        self.repository = repository

    async def list(self) -> List[MenuSchema]:
        return await self.repository.get_all()

    async def retrieve(self, menu_id: int) -> MenuSchema:
        return await self.repository.get_by_id(model_id=menu_id)

    async def create(self, data: dict) -> MenuSchema:
        try:
            return await self.repository.create(**data)
        except IntegrityError:
            raise MenuWithThisTitleExists

    async def update(self, menu_id: int, data: dict) -> MenuSchema:
        return await self.repository.update(model_id=menu_id, **data)

    async def delete(self, menu_id: int):
        return await self.repository.delete(id=menu_id)
