from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.common.exceptions import DishNotFound, DishWithThisTitleExists
from app.repositories.dish import DishRepository
from app.schemas.dish import DishSchema


class DishServices:
    def __init__(self, repository: type[DishRepository]):
        self.repository = repository

    async def list(self, menu_id: UUID, submenu_id: UUID) -> list[DishSchema]:
        return await self.repository.get_all(menu_id=menu_id, submenu_id=submenu_id)

    async def retrieve(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> DishSchema:
        result = await self.repository.get_one_or_none(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        if result is None:
            raise DishNotFound
        return result

    async def create(self, submenu_id: UUID, data: dict) -> DishSchema:
        try:
            return await self.repository.create(submenu_id=submenu_id, **data)
        except IntegrityError:
            raise DishWithThisTitleExists

    async def update(self, submenu_id: UUID, dish_id: UUID, data: dict) -> DishSchema:
        return await self.repository.update(id=dish_id, submenu_id=submenu_id, data=data)

    async def delete(self, submenu_id: UUID, dish_id: UUID):
        return await self.repository.delete(id=dish_id, submenu_id=submenu_id)
