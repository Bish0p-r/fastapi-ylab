from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import MenuNotFound, MenuWithThisTitleExists
from app.repositories.menu import MenuRepository
from app.schemas.menu import MenuSchema, MenuWithCountsSchema


class MenuServices:
    def __init__(self, repository: type[MenuRepository]):
        self.repository = repository

    async def list(self, session: AsyncSession) -> list[MenuWithCountsSchema]:
        return await self.repository.get_all_with_counts(session=session)

    async def retrieve(self, session: AsyncSession, menu_id: UUID) -> MenuWithCountsSchema:
        result = await self.repository.get_one_or_none_with_counts(session=session, menu_id=menu_id)
        if result is None:
            raise MenuNotFound
        return result

    async def create(self, session: AsyncSession, data: dict) -> MenuSchema:
        try:
            return await self.repository.create(session=session, **data)
        except IntegrityError:
            raise MenuWithThisTitleExists

    async def update(self, session: AsyncSession, menu_id: UUID, data: dict) -> MenuSchema:
        return await self.repository.update(session=session, id=menu_id, data=data)

    async def delete(self, session: AsyncSession, menu_id: UUID):
        return await self.repository.delete(session=session, id=menu_id)
