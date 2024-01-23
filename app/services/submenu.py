from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import SubMenuNotFound, SubMenuWithThisTitleExists
from app.repositories.submenu import SubMenuRepository
from app.schemas.submenu import SubMenuSchema, SubMenuWithCountSchema


class SubMenuServices:
    def __init__(self, repository: type[SubMenuRepository]):
        self.repository = repository

    async def list(self, session: AsyncSession, menu_id: UUID) -> list[SubMenuWithCountSchema]:
        return await self.repository.get_all_with_counts(session=session, menu_id=menu_id)

    async def retrieve(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID) -> SubMenuWithCountSchema:
        result = await self.repository.get_one_or_none_with_counts(
            session=session, menu_id=menu_id, submenu_id=submenu_id
        )
        if result is None:
            raise SubMenuNotFound
        return result

    async def create(self, session: AsyncSession, menu_id: UUID, data: dict) -> SubMenuSchema:
        try:
            return await self.repository.create(session=session, menu_id=menu_id, **data)
        except IntegrityError:
            raise SubMenuWithThisTitleExists

    async def update(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID, data: dict) -> SubMenuSchema:
        return await self.repository.update(session=session, id=submenu_id, menu_id=menu_id, data=data)

    async def delete(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID):
        return await self.repository.delete(session=session, id=submenu_id, menu_id=menu_id)
