from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import DishNotFound, DishWithThisTitleExists
from app.repositories.dish import DishRepository
from app.schemas.dish import DishSchema


class DishServices:
    def __init__(self, repository: type[DishRepository]):
        self.repository = repository

    async def list(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID) -> list[DishSchema]:
        return await self.repository.get_all(session=session, menu_id=menu_id, submenu_id=submenu_id)

    async def retrieve(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> DishSchema:
        result = await self.repository.get_one_or_none(
            session=session, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        )
        if result is None:
            raise DishNotFound
        return result

    async def create(self, session: AsyncSession, submenu_id: UUID, data: dict) -> DishSchema:
        try:
            return await self.repository.create(session=session, submenu_id=submenu_id, **data)
        except IntegrityError:
            raise DishWithThisTitleExists

    async def update(self, session: AsyncSession, submenu_id: UUID, dish_id: UUID, data: dict) -> DishSchema:
        try:
            return await self.repository.update(session=session, id=dish_id, submenu_id=submenu_id, data=data)
        except IntegrityError:
            raise DishWithThisTitleExists

    async def delete(self, session: AsyncSession, submenu_id: UUID, dish_id: UUID):
        return await self.repository.delete(session=session, id=dish_id, submenu_id=submenu_id)
